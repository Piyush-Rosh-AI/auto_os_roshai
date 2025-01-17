import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan, Image
import h5py
import json

class HDF5_Read(Node):
    
    def __init__(self):
        super().__init__('hdf5_data_publisher')

        # Create publishers for each topic
        self.odom_publisher = self.create_publisher(Odometry, '/odom', 10)

        try:
            # Open the HDF5 file
            self.h5_file = h5py.File('/home/roshai/sim_ws/2025_1_17_13_7_file', 'r')
        except Exception as e:
            self.get_logger().error(f"Error opening HDF5 file: {e}")
            self.h5_file = None  # Set to None if the file can't be opened

        self.odom_index = 1

        # Create a timer to call the publish_data every 1 second
        self.create_timer(0.1, self.publish_odom)  # Timer callback every 0.1 seconds (10Hz)

    def publish_odom_from_dict(self, odom_dict):
        """
        Converts a dictionary into an Odometry message and publishes it.
        """
        # Create a new Odometry message
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
        self.odom_publisher.publish(odom_msg)

    def publish_odom(self):
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
                            print("now decoding")
                            odom_dict = json.loads(odometry_entry.decode('utf-8'))
                           
                            self.publish_odom_from_dict(odom_dict)
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
