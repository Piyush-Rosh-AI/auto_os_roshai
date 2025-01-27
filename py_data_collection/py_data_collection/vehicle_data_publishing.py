import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped,TransformStamped
from sensor_msgs.msg import Imu, LaserScan, Image,PointCloud2,NavSatFix,MagneticField,FluidPressure,Temperature
import h5py
import json
import tf2_ros
time_void=0.0
class HDF5_Read(Node):
    
    def __init__(self):
        super().__init__('hdf5_data_publisher')
        try:
            # Open the HDF5 file
            self.h5_file = h5py.File('/home/roshai/sim_ws/18_15|January 27, 2025_file.h5', 'r')
        except Exception as e:
            self.get_logger().error(f"Error opening HDF5 file: {e}")
            self.h5_file = None  # Set to None if the file can't be opened
            
        # Create publishers for each topic
        self.gps_filtered_publisher = self.create_publisher(NavSatFix, '/gps/filtered', 10)
        self.gps_filtered_index = 1
        self.gps_2_pose_publisher = self.create_publisher(PoseWithCovarianceStamped, '/gps_2/pose', 10)
        self.gps_2_pose_index = 1
        self.vectornav_odom_data_publisher = self.create_publisher(Odometry, '/vectornav/odom', 10)#
        self.vectornav_odom_index = 1
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
        self.vectornav_magentic_publisher = self.create_publisher(MagneticField, '/vectornav/magnetic', 10)
        self.vectornav_magentic_index = 1
        self.vectornav_temperature_publisher = self.create_publisher(Temperature, '/vectornav/temperature', 10)
        self.vectornav_temperature_index = 1
        self.vectornav_pressure_publisher = self.create_publisher(FluidPressure, '/vectornav/pressure', 10)
        self.vectornav_pressure_index = 1
        self.vectornav_gnss_publisher = self.create_publisher(NavSatFix, '/vectornav/gnss', 10)
        self.vectornav_gnss_index = 1
        self.broadcaster = tf2_ros.TransformBroadcaster(self)
        self.transforms_data = self.h5_file['tf_transforms'][:]
        self.timer = self.create_timer(1.0, self.publish_transforms)
        self.transform_index = 1
        

        #timer for each topic
        self.create_timer(self.gps_filtered_timer(True), self.gps_filtered_timer)
        self.create_timer(self.gps_2_pose_timer(True), self.gps_2_pose_timer)    
        self.create_timer(self.vectornav_odom_timer(True), self.vectornav_odom_timer)
        self.create_timer(self.odometry_gps_timer(True), self.odometry_gps_timer)
        self.create_timer(self.odometry_navsat_timer(True), self.odometry_navsat_timer)
        self.create_timer(self.ouster_imu_timer(True), self.ouster_imu_timer)    
        self.create_timer(self.vectornav_IMU_timer(True), self.vectornav_IMU_timer)
        self.create_timer(self.ouster_points_timer(True), self.ouster_points_timer)
        self.create_timer(self.ouster_nearir_image_timer(True), self.ouster_nearir_image_timer)
        self.create_timer(self.ouster_range_image_timer(True), self.ouster_range_image_timer)
        self.create_timer(self.ouster_reflec_image_timer(True), self.ouster_reflec_image_timer)
        self.create_timer(self.ouster_signal_image_timer(True), self.ouster_signal_image_timer)    
        self.create_timer(self.vectornav_magnetic_timer(True), self.vectornav_magnetic_timer)
        self.create_timer(self.vectornav_temperature_timer(True), self.vectornav_temperature_timer)
        self.create_timer(self.vectornav_pressure_timer(True), self.vectornav_pressure_timer)
        self.create_timer(self.vectornav_gnss_timer(True), self.vectornav_gnss_timer)
        
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
    def transform_unload_JSON(self, transform_dict):
        """
        Converts a dictionary into a TransformStamped message.
        """
        # Create a new TransformStamped message
        transform_msg = TransformStamped()

        # Populate the header
        transform_msg.header.frame_id = transform_dict['header']['frame_id']
        transform_msg.header.stamp.sec = transform_dict['header']['stamp']['sec']
        transform_msg.header.stamp.nanosec = transform_dict['header']['stamp']['nanosec']
        transform_msg.child_frame_id = transform_dict['child_frame_id']

        # Populate the translation data
        transform_msg.transform.translation.x = transform_dict['translation']['x']
        transform_msg.transform.translation.y = transform_dict['translation']['y']
        transform_msg.transform.translation.z = transform_dict['translation']['z']

        # Populate the rotation data (quaternion)
        transform_msg.transform.rotation.x = transform_dict['rotation']['x']
        transform_msg.transform.rotation.y = transform_dict['rotation']['y']
        transform_msg.transform.rotation.z = transform_dict['rotation']['z']
        transform_msg.transform.rotation.w = transform_dict['rotation']['w']

        # Return the TransformStamped message to be published
        return transform_msg    
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
                            unload_JSON,avgTime=self.navsatfix_unload_JSON(gps_filtered_dict)
                           
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
                    self.get_logger().info("All gps_filtered_data has been published.")
            # else:
            #     self.get_logger().warn("No 'gps_filtered_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                    self.get_logger().info("All gps_2_pose_data has been published.")
            # else:
            #     self.get_logger().warn("No 'gps_2_pose_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
            
    def vectornav_odom_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_odom_data' in self.h5_file:
                vectornav_odom_data = self.h5_file['vectornav_odom_data']
                if self.vectornav_odom_index < len(vectornav_odom_data):
                    # Read one entry from the vectornav_odom_data dataset
                    vectornav_odom_entry = vectornav_odom_data[self.vectornav_odom_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_odom_index}: {vectornav_odom_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_odom_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_odom_entry = vectornav_odom_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_odom_dict = json.loads(vectornav_odom_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.odom_unload_JSON(vectornav_odom_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odom_publisher.publish(unload_JSON)
                            self.vectornav_odom_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_odom_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_odom_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_odom_index}. Skipping.")
                else:
                    self.get_logger().info("All vectornav_odom_data has been published.")
            # else:
            #     self.get_logger().warn("No 'vectornav_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                    self.get_logger().info("All odometry_gps_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'odometry_gps_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def odometry_navsat_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'odometry_navsat_data' in self.h5_file:
                odometry_navsat_data = self.h5_file['odometry_navsat_data']
                if self.odometry_navsat_index < len(odometry_navsat_data):
                    # Read one entry from the navsat_odom_data dataset
                    odometry_navsat_entry = odometry_navsat_data[self.odometry_navsat_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.odometry_navsat_index}: {odometry_navsat_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(odometry_navsat_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        odometry_navsat_entry = odometry_navsat_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            odometry_navsat_dict = json.loads(odometry_navsat_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.navsatfix_unload_JSON(odometry_navsat_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.odometry_navsat_publisher.publish(unload_JSON)
                            self.odometry_navsat_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.odometry_navsat_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.odometry_navsat_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.odometry_navsat_index}. Skipping.")
                else:
                    self.get_logger().info("All navsat_odom data has been published.")
            # else:
            #     self.get_logger().warn("No 'navsat_odom_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                            
                            ouster_imu_dict = json.loads(ouster_imu_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.imu_unload_JSON(ouster_imu_dict)
                           
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
                    self.get_logger().info("All ouster_imu_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'ouster_imu_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                    self.get_logger().info("All vectornav_IMU_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'vectornav_IMU_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def ouster_points_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'ouster_points_data' in self.h5_file:
                ouster_points_data = self.h5_file['ouster_points_data']
                if self.ouster_points_index < len(ouster_points_data):
                    # Read one entry from the ouster_points_data dataset
                    ouster_points_entry = ouster_points_data[self.ouster_points_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.ouster_points_index}: {ouster_points_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(ouster_points_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        ouster_points_entry = ouster_points_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            ouster_points_dict = json.loads(ouster_points_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.pointcloud_unload_JSON(ouster_points_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.ouster_points_publisher.publish(unload_JSON)
                            self.ouster_points_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.ouster_points_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.ouster_points_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.ouster_points_index}. Skipping.")
                else:
                    self.get_logger().info("All ouster_points_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'ouster_points_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                    self.get_logger().info("All ouster_nearir_image_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'ouster_nearir_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                    self.get_logger().info("All ouster_range_image_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'ouster_range_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def ouster_reflec_image_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'ouster_reflec_image_data' in self.h5_file:
                ouster_reflec_image_data = self.h5_file['vectorouster_reflec_image_datanav_odom_data']
                if self.ouster_reflec_image_index < len(ouster_reflec_image_data):
                    # Read one entry from the ouster_reflec_image_data dataset
                    ouster_reflec_image_entry = ouster_reflec_image_data[self.ouster_reflec_image_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.ouster_reflec_image_index}: {ouster_reflec_image_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(ouster_reflec_image_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        ouster_reflec_image_entry = ouster_reflec_image_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            ouster_reflec_image_dict = json.loads(ouster_reflec_image_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.image_unload_JSON(ouster_reflec_image_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.ouster_range_image_publisher.publish(unload_JSON)
                            self.ouster_reflec_image_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.ouster_reflec_image_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.ouster_reflec_image_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.ouster_reflec_image_index}. Skipping.")
                else:
                    self.get_logger().info("All ouster_reflec_image_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'ouster_reflec_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
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
                    self.get_logger().info("All ouster_signal_image_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'ouster_signal_image_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def vectornav_magnetic_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_magnetic_data' in self.h5_file:
                vectornav_magnetic_data = self.h5_file['vectornav_magnetic_data']
                if self.vectornav_magnetic_index < len(vectornav_magnetic_data):
                    # Read one entry from the vectornav_magnetic_data dataset
                    vectornav_magnetic_entry = vectornav_magnetic_data[self.vectornav_magnetic_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_magnetic_index}: {vectornav_magnetic_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_magnetic_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_magnetic_entry = vectornav_magnetic_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_magnetic_dict = json.loads(vectornav_magnetic_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.magneticneticfield_unload_JSON(vectornav_magnetic_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_magnetic_publisher.publish(unload_JSON)
                            self.vectornav_magnetic_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_magnetic_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_magnetic_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_magnetic_index}. Skipping.")
                else:
                    self.get_logger().info("All vectornav_magnetic_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'vectornav_magnetic_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def vectornav_temperature_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_temperature_data' in self.h5_file:
                vectornav_temperature_data = self.h5_file['vectornav_temperature_data']
                if self.vectornav_temperature_index < len(vectornav_temperature_data):
                    # Read one entry from the vectornav_temperature_data dataset
                    vectornav_temperature_entry = vectornav_temperature_data[self.vectornav_temperature_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_temperature_index}: {vectornav_temperature_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_temperature_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_temperature_entry = vectornav_temperature_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_temperature_dict = json.loads(vectornav_temperature_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.temperatureerature_unload_JSON(vectornav_temperature_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_temperature_publisher.publish(unload_JSON)
                            self.vectornav_temperature_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_temperature_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_temperature_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_temperature_index}. Skipping.")
                else:
                    self.get_logger().info("All vectornav_temperature_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'vectornav_temperature_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def vectornav_pressure_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_pressure_data' in self.h5_file:
                vectornav_pressure_data = self.h5_file['vectornav_pressure_data']
                if self.vectornav_pressure_index < len(vectornav_pressure_data):
                    # Read one entry from the vectornav_pressure_data dataset
                    vectornav_pressure_entry = vectornav_pressure_data[self.vectornav_pressure_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_pressure_index}: {vectornav_pressure_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_pressure_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_pressure_entry = vectornav_pressure_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_pressure_dict = json.loads(vectornav_pressure_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.fluidpressuresure_unload_JSON(vectornav_pressure_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_pressure_publisher.publish(unload_JSON)
                            self.vectornav_pressure_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_pressure_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_pressure_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_pressure_index}. Skipping.")
                else:
                    self.get_logger().info("All vectornav_pressure_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'vectornav_pressure_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def vectornav_gnss_timer(self,sendAvgTime=False):
        try:
            # Check if the dataset exists and has data
            if 'vectornav_gnss_data' in self.h5_file:
                vectornav_gnss_data = self.h5_file['vectornav_gnss_data']
                if self.vectornav_gnss_index < len(vectornav_gnss_data):
                    # Read one entry from the vectornav_Temp_data dataset
                    vectornav_gnss_entry = vectornav_gnss_data[self.vectornav_gnss_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.vectornav_gnss_index}: {vectornav_gnss_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(vectornav_gnss_entry) > 0:
                        # Strip any null bytes or padding that may be at the end of the byte string
                        vectornav_gnss_entry = vectornav_gnss_entry.rstrip(b'\x00')  # Remove null bytes
                        try:
                            # Decode the byte string to UTF-8 and deserialize it
                            
                            vectornav_gnss_dict = json.loads(vectornav_gnss_entry.decode('utf-8'))
                            unload_JSON,avgTime=self.navsatfix_unload_JSON(vectornav_gnss_dict)
                           
                            if(sendAvgTime==True):
                                print("returned avg time")
                                return avgTime
                            self.vectornav_gnss_publisher.publish(unload_JSON)
                            self.vectornav_gnss_index += 1
                            self.get_logger().info(f"Published odometry data at index {self.vectornav_gnss_index}.")
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_gnss_index}: {str(e)}")
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.vectornav_gnss_index}. Skipping.")
                else:
                    self.get_logger().info("All vectornav_gnss_data data has been published.")
            # else:
            #     self.get_logger().warn("No 'vectornav_gnss_data' found in HDF5 file.")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {str(e)}")
        return time_void
    def publish_transforms(self):
        print("in transform")
        try:
            print("in try")
            # Check if the dataset exists and has data
            if 'tf_transforms' in self.h5_file:
                print("in try tf_tranform")
                if self.transform_index < len(self.transforms_data):
                    print("in index check")
                    # Read one entry from the tf_transforms dataset
                    transforms_data_entry = self.transforms_data[self.transform_index]

                    # Log the raw data before decoding
                    self.get_logger().info(f"Raw data at index {self.transform_index}: {transforms_data_entry}")

                    # Ensure the data is not empty and remove padding or null bytes
                    if len(transforms_data_entry) > 0:
                        # Decode the byte string and deserialize it
                        try:
                            transforms_data_entry = transforms_data_entry.rstrip(b'\x00')
                            
                            transforms_data_dict = json.loads(transforms_data_entry.decode('utf-8'))
                            
                            # Publish the transform
                            self.broadcaster.sendTransform(self.transform_unload_JSON(transforms_data_dict))
                            self.get_logger().info(f"Published transform from 'base_link' to 'rear_left_wheel'.")

                            # Increment the index for the next transformation
                            self.transform_index += 1
                        except json.JSONDecodeError as e:
                            self.get_logger().error(f"JSON Decode error at index {self.vectornav_gnss_index}: {str(e)}")
                   
                    else:
                        self.get_logger().warn(f"Empty entry at index {self.transform_index}. Skipping.")
                else:
                    self.get_logger().info("All transformations have been published.")
            # else:
            #     self.get_logger().warn("No 'tf_transforms' found in HDF5 file.")
        
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
