import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Imu, LaserScan, Image,PointCloud2,NavSatFix,MagneticField,FluidPressure,Temperature
import h5py
import json

class HDF5_Read(Node):
    
    def __init__(self):
        super().__init__('hdf5_data_publisher')
        try:
            # Open the HDF5 file
            self.h5_file = h5py.File('/home/roshai/sim_ws/15_40|January 20, 2025_file.h5', 'r')
        except Exception as e:
            self.get_logger().error(f"Error opening HDF5 file: {e}")
            self.h5_file = None  # Set to None if the file can't be opened
            
        # Create publishers for each topic
        self.gps_filtered_publisher = self.create_publisher(NavSatFix, '/gps/filtered', 10)
        self.gps_filtered_index = 1
        self.gps_2_pose_publisher = self.create_publisher(PoseWithCovarianceStamped, '/gps_2/pose', 10)
        self.gps_2_pose_index = 1
        self.vectornav_odom_data_publisher = self.create_publisher(Odometry, '/vectornav_odom_data', 10)
        self.vectornav_odom_data_index = 1
        self.odometry_gps_publisher = self.create_publisher(Odometry, '/odometry/gps', 10)
        self.odometry_gps_index = 1
        self.odometry_navsat_publisher = self.create_publisher(Odometry, '/odometry/navsat', 10)
        self.odometry_navsat_index = 1
        self.ouster_imu_publisher = self.create_publisher(Imu, '/ouster/imu', 10)
        self.ouster_imu_index = 1        
        self.vectornav_IMU_publisher = self.create_publisher(Imu, '/vectornav/IMU', 10)
        self.vectornav_IMU_index = 1
        self.ouster_points_publisher = self.create_publisher(PointCloud2, '/ouster/points', 10)
        self.ouster_points_index = 1
        self.ouster_nearir_image_publisher = self.create_publisher(Image, '/ouster/nearir_image', 10)
        self.ouster_nearir_image_index = 1
        self.ouster_range_image_publisher = self.create_publisher(Image, '/ouster/range_image', 10)
        self.ouster_range_image_index = 1
        self.ouster_reflec_image_publisher = self.create_publisher(Image, '/ouster/reflec_image', 10)
        self.ouster_reflec_image_index = 1
        self.ouster_signal_image_publisher = self.create_publisher(Image, '/ouster/signal_image', 10)
        self.ouster_signal_image_index = 1
        self.vectornav_MAG_publisher = self.create_publisher(MagneticField, '/vectornav/MAG', 10)
        self.vectornav_MAG_index = 1
        self.vectornav_Temp_publisher = self.create_publisher(Temperature, '/vectornav/Temp', 10)
        self.vectornav_Temp_index = 1
        self.vectornav_Pres_publisher = self.create_publisher(FluidPressure, '/vectornav/Pres', 10)
        self.vectornav_Pres_index = 1
        self.vectornav_GPS_publisher = self.create_publisher(NavSatFix, '/vectornav/GPS', 10)
        self.vectornav_GPS_index = 1
        
        

        #timer for each topic
        self.create_timer(self.gps_filtered_timer(True), self.gps_filtered_timer)
        self.create_timer(self.gps_2_pose_timer(True), self.gps_2_pose_timer)    
        self.create_timer(self.vectornav_odom_data_timer(True), self.vectornav_odom_data_timer)
        self.create_timer(self.odometry_gps_timer(True), self.odometry_gps_timer)
        self.create_timer(self.odometry_navsat_timer(True), self.odometry_navsat_timer)
        self.create_timer(self.ouster_imu_timer(True), self.ouster_imu_timer)    
        self.create_timer(self.vectornav_IMU_timer(True), self.vectornav_IMU_timer)
        self.create_timer(self.ouster_points_timer(True), self.ouster_points_timer)
        self.create_timer(self.ouster_nearir_image_timer(True), self.ouster_nearir_image_timer)
        self.create_timer(self.ouster_range_image_timer(True), self.ouster_range_image_timer)
        self.create_timer(self.ouster_reflec_image_timer(True), self.ouster_reflec_image_timer)
        self.create_timer(self.ouster_signal_image_timer(True), self.ouster_signal_image_timer)    
        self.create_timer(self.vectornav_MAG_timer(True), self.vectornav_MAG_timer)
        self.create_timer(self.vectornav_Temp_timer(True), self.vectornav_Temp_timer)
        self.create_timer(self.vectornav_Pres_timer(True), self.vectornav_Pres_timer)
        self.create_timer(self.vectornav_GPS_timer(True), self.vectornav_GPS_timer)
        
    def navsatfix_unload_JSON(self, gps_dict):
        """
        Converts a dictionary into a NavSatFix message.
        """
        # Create a new NavSatFix message
        gps_msg = NavSatFix()

        # Populate the header
        gps_msg.header.frame_id = gps_dict['header']['frame_id']
        gps_msg.header.stamp.sec = gps_dict['header']['stamp']['sec']
        gps_msg.header.stamp.nanosec = gps_dict['header']['stamp']['nanosec']

        # Populate the latitude, longitude, altitude, and other GPS-related data
        gps_msg.latitude = gps_dict['latitude']
        gps_msg.longitude = gps_dict['longitude']
        gps_msg.altitude = gps_dict['altitude']

        # Populate additional fields such as status and covariance if available
        gps_msg.status.status = gps_dict['status']['status']
        gps_msg.status.service = gps_dict['status']['service']
        gps_msg.position_covariance = gps_dict.get('position_covariance', [0.0]*9)  # Default covariance

        # Return the NavSatFix message to be published
        return gps_msg
    def posewithcovariance_unload_JSON(self, pose_dict):
        """
        Converts a dictionary into a PoseWithCovariance message.
        """
        # Create a new PoseWithCovariance message
        pose_msg = PoseWithCovarianceStamped()

        # Populate the header
        pose_msg.header.frame_id = pose_dict['header']['frame_id']
        pose_msg.header.stamp.sec = pose_dict['header']['stamp']['sec']
        pose_msg.header.stamp.nanosec = pose_dict['header']['stamp']['nanosec']

        # Populate the pose data (position and orientation)
        pose_msg.pose.position.x = pose_dict['pose']['position']['x']
        pose_msg.pose.position.y = pose_dict['pose']['position']['y']
        pose_msg.pose.position.z = pose_dict['pose']['position']['z']

        pose_msg.pose.orientation.x = pose_dict['pose']['orientation']['x']
        pose_msg.pose.orientation.y = pose_dict['pose']['orientation']['y']
        pose_msg.pose.orientation.z = pose_dict['pose']['orientation']['z']
        pose_msg.pose.orientation.w = pose_dict['pose']['orientation']['w']

        # Populate the covariance matrix
        pose_msg.covariance = pose_dict.get('covariance', [0.0] * 36)  # Default covariance if not available

        # Return the PoseWithCovariance message to be published
        return pose_msg            
    def odom_unload_JSON(self, odom_dict):
        """
        Converts a dictionary into an Odometry message and publishes it.
        """
        # Create a new Odometry message
        avgTime=odom_dict['avgTime']
        odom_msg = Odometry()
        
        # Populate the header
        odom_msg.header.frame_id = odom_dict['header']['frame_id']
        odom_msg.header.stamp.sec = odom_dict['header']['stamp']['sec']
        odom_msg.header.stamp.nanosec = odom_dict['header']['stamp']['nanosec']
        
        # Populate the pose data (position and orientation)
        odom_msg.pose.pose.position.x = odom_dict['pose']['position']['x']
        odom_msg.pose.pose.position.y = odom_dict['pose']['position']['y']
        odom_msg.pose.pose.position.z = odom_dict['pose']['position']['z']
        
        odom_msg.pose.pose.orientation.x = odom_dict['pose']['orientation']['x']
        odom_msg.pose.pose.orientation.y = odom_dict['pose']['orientation']['y']
        odom_msg.pose.pose.orientation.z = odom_dict['pose']['orientation']['z']
        odom_msg.pose.pose.orientation.w = odom_dict['pose']['orientation']['w']
        
        # Populate the twist data (linear and angular velocities)
        odom_msg.twist.twist.linear.x = odom_dict['twist']['linear']['x']
        odom_msg.twist.twist.linear.y = odom_dict['twist']['linear']['y']
        odom_msg.twist.twist.linear.z = odom_dict['twist']['linear']['z']
        
        odom_msg.twist.twist.angular.x = odom_dict['twist']['angular']['x']
        odom_msg.twist.twist.angular.y = odom_dict['twist']['angular']['y']
        odom_msg.twist.twist.angular.z = odom_dict['twist']['angular']['z']
        
        # Publish the odometry message
        return odom_msg,avgTime
    def imu_unload_JSON(self, imu_dict):
        """
        Converts a dictionary into an IMU message.
        """
        # Create a new IMU message
        imu_msg = Imu()

        # Populate the header
        imu_msg.header.frame_id = imu_dict['header']['frame_id']
        imu_msg.header.stamp.sec = imu_dict['header']['stamp']['sec']
        imu_msg.header.stamp.nanosec = imu_dict['header']['stamp']['nanosec']

        # Populate the orientation data (quaternion)
        imu_msg.orientation.x = imu_dict['orientation']['x']
        imu_msg.orientation.y = imu_dict['orientation']['y']
        imu_msg.orientation.z = imu_dict['orientation']['z']
        imu_msg.orientation.w = imu_dict['orientation']['w']

        # Populate the angular velocity data (radians per second)
        imu_msg.angular_velocity.x = imu_dict['angular_velocity']['x']
        imu_msg.angular_velocity.y = imu_dict['angular_velocity']['y']
        imu_msg.angular_velocity.z = imu_dict['angular_velocity']['z']

        # Populate the linear acceleration data (meters per second squared)
        imu_msg.linear_acceleration.x = imu_dict['linear_acceleration']['x']
        imu_msg.linear_acceleration.y = imu_dict['linear_acceleration']['y']
        imu_msg.linear_acceleration.z = imu_dict['linear_acceleration']['z']

        # Return the IMU message to be published
        return imu_msg   
    def pointcloud_unload_JSON(self, pointcloud_dict):
        """
        Converts a dictionary into a PointCloud2 message.
        """
        # Create a new PointCloud2 message
        pointcloud_msg = PointCloud2()

        # Populate the header
        pointcloud_msg.header.frame_id = pointcloud_dict['header']['frame_id']
        pointcloud_msg.header.stamp.sec = pointcloud_dict['header']['stamp']['sec']
        pointcloud_msg.header.stamp.nanosec = pointcloud_dict['header']['stamp']['nanosec']

        # Example fields in the pointcloud data (x, y, z, intensity, etc.)
        # Ensure the fields match your data structure
        points = pointcloud_dict['points']  # Assume this is a list of [x, y, z, intensity, ...]
        pointcloud_msg.height = 1  # Assuming the data represents a 2D point cloud
        pointcloud_msg.width = len(points)
        pointcloud_msg.is_dense = True

        # Populate pointcloud data (just an example: x, y, z, intensity, etc.)
        pointcloud_msg.data = b''.join([struct.pack('fff', *point[:3]) for point in points])  # packing as floats for x, y, z

        # Return the PointCloud2 message to be published
        return pointcloud_msg
    def image_unload_JSON(self, image_dict):
        """
        Converts a dictionary into an Image message.
        """
        # Create a new Image message
        image_msg = Image()

        # Populate the header
        image_msg.header.frame_id = image_dict['header']['frame_id']
        image_msg.header.stamp.sec = image_dict['header']['stamp']['sec']
        image_msg.header.stamp.nanosec = image_dict['header']['stamp']['nanosec']

        # Populate the image data
        image_msg.height = image_dict['height']
        image_msg.width = image_dict['width']
        image_msg.encoding = image_dict['encoding']
        image_msg.step = image_dict['step']
        image_msg.data = np.frombuffer(image_dict['data'], dtype=np.uint8).tobytes()

        # Return the Image message to be published
        return image_msg
    def magneticfield_unload_JSON(self, magnetic_dict):
        """
        Converts a dictionary into a MagneticField message.
        """
        # Create a new MagneticField message
        magnetic_msg = MagneticField()

        # Populate the header
        magnetic_msg.header.frame_id = magnetic_dict['header']['frame_id']
        magnetic_msg.header.stamp.sec = magnetic_dict['header']['stamp']['sec']
        magnetic_msg.header.stamp.nanosec = magnetic_dict['header']['stamp']['nanosec']

        # Populate the magnetic field data (x, y, z components)
        magnetic_msg.magnetic_field.x = magnetic_dict['magnetic_field']['x']
        magnetic_msg.magnetic_field.y = magnetic_dict['magnetic_field']['y']
        magnetic_msg.magnetic_field.z = magnetic_dict['magnetic_field']['z']

        # Return the MagneticField message to be published
        return magnetic_msg       
    def temperature_unload_JSON(self, temp_dict):
        """
        Converts a dictionary into a Temperature message.
        """
        # Create a new Temperature message
        temp_msg = Temperature()

        # Populate the header
        temp_msg.header.frame_id = temp_dict['header']['frame_id']
        temp_msg.header.stamp.sec = temp_dict['header']['stamp']['sec']
        temp_msg.header.stamp.nanosec = temp_dict['header']['stamp']['nanosec']

        # Populate the temperature data
        temp_msg.temperature = temp_dict['temperature']

        # Return the Temperature message to be published
        return temp_msg
    def fluidpressure_unload_JSON(self, pressure_dict):
        """
        Converts a dictionary into a FluidPressure message.
        """
        # Create a new FluidPressure message
        pressure_msg = FluidPressure()

        # Populate the header
        pressure_msg.header.frame_id = pressure_dict['header']['frame_id']
        pressure_msg.header.stamp.sec = pressure_dict['header']['stamp']['sec']
        pressure_msg.header.stamp.nanosec = pressure_dict['header']['stamp']['nanosec']

        # Populate the fluid pressure data
        pressure_msg.fluid_pressure = pressure_dict['fluid_pressure']

        # Return the FluidPressure message to be published
        return pressure_msg
    
    def gps_filtered_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'gps_filtered_data' in self.h5_file:
                gps_filtered_data = self.h5_file['gps_filtered_data']
                if self.gps_filtered_index < len(gps_filtered_data):
                    # Read one entry from the gps_filtered_data dataset
                    gps_filtered_entry = gps_filtered_data[self.gps_filtered_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.gps_filtered_index}: {gps_filtered_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(gps_filtered_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        gps_filtered_entry = gps_filtered_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            gps_filtered_dict = json.loads(gps_filtered_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.gps_filtered_unload_JSON(gps_filtered_dict)
                           
                            if(sendAvgTime==True):
                                return avgTime
                            self.gps_filtered_publisher.publish(unload_JSON)
                            self.gps_filtered_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.gps_filtered_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.gps_filtered_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.gps_filtered_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'gps_filtered_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def gps_2_pose_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'gps_2_pose_data' in self.h5_file:
                gps_2_pose_data = self.h5_file['gps_2_pose_data']
                if self.gps_2_pose_index < len(gps_2_pose_data):
                    # Read one entry from the gps_2_pose_data dataset
                    gps_2_pose_entry = gps_2_pose_data[self.gps_2_pose_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.gps_2_pose_index}: {gps_2_pose_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(gps_2_pose_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        gps_2_pose_entry = gps_2_pose_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            gps_2_pose_dict = json.loads(gps_2_pose_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.navsatfix_unload_JSON(gps_2_pose_dict)
                           
                            if(sendAvgTime==True):
                                return avgTime
                            self.gps_2_pose_publisher.publish(unload_JSON)
                            self.gps_2_pose_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.gps_2_pose_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.gps_2_pose_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.gps_2_pose_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def vectornav_odom_data_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_odom_data' in self.h5_file:
                odometry_data = self.h5_file['vectornav_odom_data']
                if self.odom_index < len(odometry_data):
                    # Read one entry from the vectornav_odom_data dataset
                    odometry_entry = odometry_data[self.odom_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.odom_index}: {odometry_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(odometry_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        odometry_entry = odometry_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            odom_dict = json.loads(odometry_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(odom_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odom_publisher.publish(unload_JSON)
                            self.odom_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.odom_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.odom_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.odom_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def odometry_gps_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'odometry_gps_data' in self.h5_file:
                odometry_gps_data = self.h5_file['odometry_gps_data']
                if self.odometry_gps_index < len(odometry_gps_data):
                    # Read one entry from the odometry_gps_data dataset
                    odometry_gps_entry = odometry_gps_data[self.odometry_gps_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.odometry_gps_index}: {odometry_gps_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(odometry_gps_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        odometry_gps_entry = odometry_gps_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            odometry_gps_dic = json.loads(odometry_gps_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(odometry_gps_dic)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odometry_gps_publisher.publish(unload_JSON)
                            self.odometry_gps_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.odometry_gps_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.odometry_gps_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.odometry_gps_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'odometry_gps_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def odometry_navsat_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'navsat_odom_data' in self.h5_file:
                navsat_odom_data = self.h5_file['navsat_odom_data']
                if self.navsat_odom_index < len(navsat_odom_data):
                    # Read one entry from the navsat_odom_data dataset
                    navsat_odom_entry = navsat_odom_data[self.navsat_odom_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.navsat_odom_index}: {navsat_odom_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(navsat_odom_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        navsat_odom_entry = navsat_odom_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            navsat_odom_dict = json.loads(navsat_odom_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.navsatfix_unload_JSON(navsat_odom_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odometry_navsat_publisher.publish(unload_JSON)
                            self.navsat_odom_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.navsat_odom_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.navsat_odom_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.navsat_odom_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'navsat_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def ouster_imu_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'ouster_imu_data' in self.h5_file:
                ouster_imu_data = self.h5_file['ouster_imu_data']
                if self.ouster_imu_index < len(ouster_imu_data):
                    # Read one entry from the ouster_imu_data dataset
                    ouster_imu_entry = ouster_imu_data[self.ouster_imu_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.ouster_imu_index}: {ouster_imu_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(ouster_imu_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        ouster_imu_entry = ouster_imu_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            odom_dict = json.loads(ouster_imu_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.imu_unload_JSON(odom_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.ouster_imu_publisher.publish(unload_JSON)
                            self.ouster_imu_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.ouster_imu_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.ouster_imu_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.ouster_imu_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'ouster_imu_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def vectornav_IMU_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_IMU_data' in self.h5_file:
                vectornav_IMU_data = self.h5_file['vectornav_IMU_data']
                if self.vectornav_IMU_index < len(vectornav_IMU_data):
                    # Read one entry from the vectornav_IMU_data dataset
                    vectornav_IMU_entry = vectornav_IMU_data[self.vectornav_IMU_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_IMU_index}: {vectornav_IMU_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_IMU_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_IMU_entry = vectornav_IMU_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_IMU_dict = json.loads(vectornav_IMU_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(vectornav_IMU_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odom_publisher.publish(unload_JSON)
                            self.vectornav_IMU_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_IMU_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_IMU_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_IMU_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_IMU_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def ouster_points_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_odom_data' in self.h5_file:
                odometry_data = self.h5_file['vectornav_odom_data']
                if self.odom_index < len(odometry_data):
                    # Read one entry from the vectornav_odom_data dataset
                    odometry_entry = odometry_data[self.odom_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.odom_index}: {odometry_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(odometry_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        odometry_entry = odometry_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            odom_dict = json.loads(odometry_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(odom_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_IMU_publisher.publish(unload_JSON)
                            self.odom_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.odom_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.odom_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.odom_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def ouster_nearir_image_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'ouster_nearir_image_data' in self.h5_file:
                ouster_nearir_image_data = self.h5_file['ouster_nearir_image_data']
                if self.ouster_nearir_image_index < len(ouster_nearir_image_data):
                    # Read one entry from the ouster_nearir_image_data dataset
                    ouster_nearir_image_entry = ouster_nearir_image_data[self.ouster_nearir_image_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.ouster_nearir_image_index}: {ouster_nearir_image_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(ouster_nearir_image_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        ouster_nearir_image_entry = ouster_nearir_image_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            ouster_nearir_image_dict = json.loads(ouster_nearir_image_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(ouster_nearir_image_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.ouster_nearir_image_publisher.publish(unload_JSON)
                            self.ouster_nearir_image_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.ouster_nearir_image_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.ouster_nearir_image_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.ouster_nearir_image_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'ouster_nearir_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def ouster_range_image_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'ouster_range_image_data' in self.h5_file:
                ouster_range_image_data = self.h5_file['ouster_range_image_data']
                if self.ouster_range_image_index < len(ouster_range_image_data):
                    # Read one entry from the ouster_range_image_data dataset
                    ouster_range_image_entry = ouster_range_image_data[self.ouster_range_image_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.ouster_range_image_index}: {ouster_range_image_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(ouster_range_image_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        ouster_range_image_entry = ouster_range_image_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            ouster_range_image_dict = json.loads(ouster_range_image_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(ouster_range_image_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odom_publisher.publish(unload_JSON)
                            self.ouster_range_image_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.ouster_range_image_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.ouster_range_image_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.ouster_range_image_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'ouster_range_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def ouster_reflec_image_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_odom_data' in self.h5_file:
                odometry_data = self.h5_file['vectornav_odom_data']
                if self.odom_index < len(odometry_data):
                    # Read one entry from the vectornav_odom_data dataset
                    odometry_entry = odometry_data[self.odom_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.odom_index}: {odometry_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(odometry_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        odometry_entry = odometry_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            odom_dict = json.loads(odometry_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.image_unload_JSON(odom_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.ouster_range_image_publisher.publish(unload_JSON)
                            self.odom_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.odom_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.odom_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.odom_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def ouster_signal_image_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'ouster_signal_image_data' in self.h5_file:
                ouster_signal_image_data = self.h5_file['ouster_signal_image_data']
                if self.ouster_signal_image_index < len(ouster_signal_image_data):
                    # Read one entry from the ouster_signal_image_data dataset
                    ouster_signal_image_entry = ouster_signal_image_data[self.ouster_signal_image_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.ouster_signal_image_index}: {ouster_signal_image_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(ouster_signal_image_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        ouster_signal_image_entry = ouster_signal_image_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            ouster_signal_image_dict = json.loads(ouster_signal_image_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.image_unload_JSON(ouster_signal_image_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.ouster_signal_image_publisher.publish(unload_JSON)
                            self.ouster_signal_image_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.ouster_signal_image_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.ouster_signal_image_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.ouster_signal_image_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'ouster_signal_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def vectornav_MAG_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_MAG_data' in self.h5_file:
                vectornav_MAG_data = self.h5_file['vectornav_MAG_data']
                if self.vectornav_MAG_index < len(vectornav_MAG_data):
                    # Read one entry from the vectornav_MAG_data dataset
                    vectornav_MAG_entry = vectornav_MAG_data[self.vectornav_MAG_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_MAG_index}: {vectornav_MAG_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_MAG_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_MAG_entry = vectornav_MAG_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_MAG_dict = json.loads(vectornav_MAG_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.magneticfield_unload_JSON(vectornav_MAG_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_MAG_publisher.publish(unload_JSON)
                            self.vectornav_MAG_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_MAG_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_MAG_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_MAG_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_MAG_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def vectornav_Temp_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_Temp_data' in self.h5_file:
                vectornav_Temp_timer = self.h5_file['vectornav_Temp_data']
                if self.vectornav_Temp_index < len(vectornav_Temp_timer):
                    # Read one entry from the vectornav_Temp_data dataset
                    vectornav_Temp_entry = vectornav_Temp_timer[self.vectornav_Temp_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_Temp_index}: {vectornav_Temp_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_Temp_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_Temp_entry = vectornav_Temp_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_Temp_dict = json.loads(vectornav_Temp_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.temperature_unload_JSON(vectornav_Temp_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_Temp_publisher.publish(unload_JSON)
                            self.vectornav_Temp_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_Temp_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_Temp_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_Temp_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_Temp_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def vectornav_Pres_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_Pres_data' in self.h5_file:
                vectornav_Temp_timer = self.h5_file['vectornav_Pres_data']
                if self.vectornav_Pres_index < len(vectornav_Temp_timer):
                    # Read one entry from the vectornav_Pres_data dataset
                    vectornav_Pres_entry = vectornav_Temp_timer[self.vectornav_Pres_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_Pres_index}: {vectornav_Pres_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_Pres_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_Pres_entry = vectornav_Pres_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_Pres_dict = json.loads(vectornav_Pres_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.fluidpressure_unload_JSON(vectornav_Pres_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_Pres_publisher.publish(unload_JSON)
                            self.vectornav_Pres_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_Pres_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_Pres_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_Pres_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_Pres_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def vectornav_GPS_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_Temp_data' in self.h5_file:
                vectornav_GPS_data = self.h5_file['vectornav_Temp_data']
                if self.vectornav_GPS_index < len(vectornav_GPS_data):
                    # Read one entry from the vectornav_Temp_data dataset
                    vectornav_GPS_entry = vectornav_GPS_data[self.vectornav_GPS_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_GPS_index}: {vectornav_GPS_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_GPS_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_GPS_entry = vectornav_GPS_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_GPS_dict = json.loads(vectornav_GPS_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.navsatfix_unload_JSON(vectornav_GPS_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_GPS_publisher.publish(unload_JSON)
                            self.vectornav_GPS_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_GPS_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_GPS_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_GPS_index}. Skipping.")
                else:
                    self.get_logger().info("All odometry data has been published.")
            else:
                self.get_logger().warn("No 'vectornav_Temp_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
    def __del__(self):
        # Close the HDF5 file when done
        self.h5_file.close()

def main(args=None):
    rclpy.init(args=args)

    # Create an instance of the HDF5_Read node
    hdf5_data_publisher = HDF5_Read()

    # Spin the node so it can keep publishing data
    rclpy.spin(hdf5_data_publisher)

    # Cleanly shut down the node
    hdf5_data_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
