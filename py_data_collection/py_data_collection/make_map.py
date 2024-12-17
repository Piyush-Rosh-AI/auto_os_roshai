import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import h5py
import numpy as np
from geometry_msgs.msg import TransformStamped
import tf2_ros
from tf2_ros import TransformBroadcaster
from tf2_ros import Buffer, TransformListener
class HDF5ToOdomNode(Node):
    def __init__(self):
        super().__init__('hdf5_to_odom_node')

        # Open the HDF5 file for reading
        self.hdf5_file = h5py.File('/home/roshai/nav_ws/src/py_data_collection/py_data_collection/sensor_data.h5', 'r')
        # Initialize the TransformBroadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        # Initialize ROS 2 publisher for Odometry data
        self.odom_publisher = self.create_publisher(Odometry, '/odom', 10)

        # Variables to keep track of the current index for the dataset
        self.odom_index = 0

        self.get_logger().info("HDF5 to Odometry Node started and publishing odometry data.")

        # Set a timer to periodically read data and publish it
        self.create_timer(0.1, self.timer_callback)  # Publish every 1 second

    def timer_callback(self):
        """
        This function will be called periodically to read data from the HDF5 file and publish it.
        """
        # Check if there is more Odometry data to publish
        if self.odom_index < self.hdf5_file['position'].shape[0]:
            # Read Odometry data from HDF5
            odom_data = Odometry()
            odom_data.header.stamp.sec= int(self.hdf5_file['odom_sec_timestamps'][self.odom_index])
            odom_data.header.stamp.nanosec= int(self.hdf5_file['odom_nanosec_timestamps'][self.odom_index])
            odom_data.header.frame_id = 'map'
            odom_data.child_frame_id = 'odom'

            # Set position and orientation
            odom_data.pose.pose.position.x = float(self.hdf5_file['position'][self.odom_index][0])
            odom_data.pose.pose.position.y = float(self.hdf5_file['position'][self.odom_index][1])
            odom_data.pose.pose.position.z = float(self.hdf5_file['position'][self.odom_index][2])

            odom_data.pose.pose.orientation.x = float(self.hdf5_file['orientation'][self.odom_index][0])
            odom_data.pose.pose.orientation.y = float(self.hdf5_file['orientation'][self.odom_index][1])
            odom_data.pose.pose.orientation.z = float(self.hdf5_file['orientation'][self.odom_index][2])
            odom_data.pose.pose.orientation.w = float(self.hdf5_file['orientation'][self.odom_index][3])

            
            transform = TransformStamped()

            # Set the timestamp
            transform.header.stamp.sec=odom_data.header.stamp.sec
            transform.header.stamp.nanosec=odom_data.header.stamp.nanosec

            # Set the frame IDs
            transform.header.frame_id = 'map'  # Parent frame (fixed)
            transform.child_frame_id = 'odom'  # Child frame (moving)

            # Set the translation (x, y, z) in the transform
            transform.transform.translation.x = odom_data.pose.pose.position.x
            transform.transform.translation.y = odom_data.pose.pose.position.y
            transform.transform.translation.z = 0.0  # 2D transform, so z is 0

            # Set the rotation (using quaternion) for the transform
            transform.transform.rotation.x = float(self.hdf5_file['orientation'][self.odom_index][0])
            transform.transform.rotation.y = float(self.hdf5_file['orientation'][self.odom_index][1])
            transform.transform.rotation.z = float(self.hdf5_file['orientation'][self.odom_index][2])
            transform.transform.rotation.w = float(self.hdf5_file['orientation'][self.odom_index][3])

            # Publish the transform
            self.tf_broadcaster.sendTransform(transform)
            # Publish Odometry data
            self.odom_publisher.publish(odom_data)
            self.odom_index += 1
            self.get_logger().info(f"Published Odometry data #{self.odom_index}")

        # If all data has been published, log that the process is complete
        if self.odom_index >= self.hdf5_file['position'].shape[0]:
            self.get_logger().info("All Odometry data has been published.")
            rclpy.shutdown()

    def __del__(self):
        # Ensure the HDF5 file is closed when the node is destroyed
        self.hdf5_file.close()
        self.get_logger().info('HDF5 file closed.')

def main(args=None):
    rclpy.init(args=args)

    # Create the node
    node = HDF5ToOdomNode()

    # Spin the node to keep reading and publishing data
    rclpy.spin(node)

    # Clean up before shutdown
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()