import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu
import h5py
import numpy as np
from nav_msgs.msg import Odometry  # Import Odometry message
class LiDARAndIMUToHDF5Node(Node):
    def __init__(self):
        super().__init__('lidar_imu_to_hdf5_node')

        # Create an HDF5 file where the data will be stored
        self.hdf5_file = h5py.File('sensor_data.h5', 'w')

        # Create datasets for LiDAR and IMU data
        # LiDAR dataset for range data (360 points per scan)
        self.lidar_dataset = self.hdf5_file.create_dataset(
            'ranges', (0, 360), maxshape=(None, 360), chunks=True)
        self.lidar_sec_timestamps = self.hdf5_file.create_dataset(
            'lidar_sec_timestamps', (0,), maxshape=(None,), dtype='float64', chunks=True)
        self.lidar_nanosec_timestamps = self.hdf5_file.create_dataset(
            'lidar_nanosec_timestamps', (0,), maxshape=(None,), dtype='float64', chunks=True)

        # IMU dataset for angular velocity and linear acceleration (each as 3D vectors)
        # Angular velocity (x, y, z) and linear acceleration (x, y, z) per IMU message
        self.imu_angular_velocity_dataset = self.hdf5_file.create_dataset(
            'angular_velocity', (0, 3), maxshape=(None, 3), chunks=True)
        self.imu_linear_acceleration_dataset = self.hdf5_file.create_dataset(
            'linear_acceleration', (0, 3), maxshape=(None, 3), chunks=True)
        self.imu_sec_timestamps = self.hdf5_file.create_dataset(
            'imu_sec_timestamps', (0,), maxshape=(None,), dtype='float64', chunks=True)
        self.imu_nanosec_timestamps = self.hdf5_file.create_dataset(
            'imu_nanosec_timestamps', (0,), maxshape=(None,), dtype='float64', chunks=True)
        
        # Odometry dataset for position (x, y, z) and orientation (quaternion x, y, z, w)
        self.odom_sec_timestamps = self.hdf5_file.create_dataset(
            'odom_sec_timestamps', (0,), maxshape=(None,), dtype='float64', chunks=True)
        self.odom_nanosec_timestamps = self.hdf5_file.create_dataset(
            'odom_nanosec_timestamps', (0,), maxshape=(None,), dtype='float64', chunks=True)
        self.odometry_position_dataset = self.hdf5_file.create_dataset(
            'position', (0, 3), maxshape=(None, 3), chunks=True)
        self.odometry_orientation_dataset = self.hdf5_file.create_dataset(
            'orientation', (0, 4), maxshape=(None, 4), chunks=True)
        # Subscribe to the /scan topic for LiDAR data
        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',  # Topic name for LiDAR
            self.lidar_callback,
            10  # QoS (Quality of Service)
        )

        # Subscribe to the /imu topic for IMU data
        self.imu_subscription = self.create_subscription(
            Imu,
            '/imu',  # Topic name for IMU
            self.imu_callback,
            10  # QoS (Quality of Service)
        )
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',  # Topic name for Odometry
            self.odom_callback,
            10  # QoS (Quality of Service)
        )

    def lidar_callback(self, msg: LaserScan):
        """
        Callback function for LiDAR data. Saves the range values to the HDF5 file.
        """
        ranges = np.array(msg.ranges)  # Convert LiDAR ranges to NumPy array
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        # Resize the LiDAR dataset to accommodate the new data and append it
        current_size = self.lidar_dataset.shape[0]
        self.lidar_dataset.resize((current_size + 1, 360))
        self.lidar_dataset[current_size] = ranges



        current_size_timestamps = self.lidar_sec_timestamps.shape[0]
        self.lidar_sec_timestamps.resize((current_size_timestamps + 1,))
        self.lidar_sec_timestamps[current_size_timestamps] = msg.header.stamp.sec
        
        current_size_timestamps = self.lidar_nanosec_timestamps.shape[0]
        self.lidar_nanosec_timestamps.resize((current_size_timestamps + 1,))
        self.lidar_nanosec_timestamps[current_size_timestamps] = msg.header.stamp.nanosec
        self.get_logger().info(f"Saved LiDAR scan data to HDF5: {ranges[:5]}...")  # Log first 5 range values

    def imu_callback(self, msg: Imu):
        """
        Callback function for IMU data. Saves the angular velocity and linear acceleration to the HDF5 file.
        """
        angular_velocity = np.array([msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z])
        linear_acceleration = np.array([msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z])

        # Resize the IMU datasets to accommodate the new data and append it
        current_size_angular_velocity = self.imu_angular_velocity_dataset.shape[0]
        self.imu_angular_velocity_dataset.resize((current_size_angular_velocity + 1, 3))
        self.imu_angular_velocity_dataset[current_size_angular_velocity] = angular_velocity

        current_size_linear_acceleration = self.imu_linear_acceleration_dataset.shape[0]
        self.imu_linear_acceleration_dataset.resize((current_size_linear_acceleration + 1, 3))
        self.imu_linear_acceleration_dataset[current_size_linear_acceleration] = linear_acceleration

        current_size_timestamps = self.imu_sec_timestamps.shape[0]
        self.imu_sec_timestamps.resize((current_size_timestamps + 1,))
        self.imu_sec_timestamps[current_size_timestamps] = msg.header.stamp.sec
        
        current_size_timestamps = self.imu_nanosec_timestamps.shape[0]
        self.imu_nanosec_timestamps.resize((current_size_timestamps + 1,))
        self.imu_nanosec_timestamps[current_size_timestamps] = msg.header.stamp.nanosec

        self.get_logger().info(f"Saved IMU data to HDF5: Angular Velocity: {angular_velocity}, Linear Acceleration: {linear_acceleration}")
    def odom_callback(self, msg: Odometry):
        """
        Callback function for Odometry data. Saves the position and orientation to the HDF5 file.
        """
        position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
        orientation = np.array([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                                msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])

        # Resize the Odometry datasets to accommodate the new data and append it
        current_size_position = self.odometry_position_dataset.shape[0]
        self.odometry_position_dataset.resize((current_size_position + 1, 3))
        self.odometry_position_dataset[current_size_position] = position

        current_size_orientation = self.odometry_orientation_dataset.shape[0]
        self.odometry_orientation_dataset.resize((current_size_orientation + 1, 4))
        self.odometry_orientation_dataset[current_size_orientation] = orientation
        
        # timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        current_size_timestamps = self.odom_sec_timestamps.shape[0]
        self.odom_sec_timestamps.resize((current_size_timestamps + 1,))
        self.odom_sec_timestamps[current_size_timestamps] = msg.header.stamp.sec
        
        current_size_timestamps = self.odom_nanosec_timestamps.shape[0]
        self.odom_nanosec_timestamps.resize((current_size_timestamps + 1,))
        self.odom_nanosec_timestamps[current_size_timestamps] = msg.header.stamp.nanosec
        self.get_logger().info(f"Saved Odometry data to HDF5: Position: {position}, Orientation: {orientation}")

    def __del__(self):
        """
        Ensure the HDF5 file is closed when the node is destroyed.
        """
        self.hdf5_file.close()
        self.get_logger().info('HDF5 file closed.')

def main(args=None):
    rclpy.init(args=args)

    # Create the node
    node = LiDARAndIMUToHDF5Node()

    # Spin the node to keep listening for messages
    rclpy.spin(node)

    # Clean up before shutdown
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
