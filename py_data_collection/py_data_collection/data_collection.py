import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan
from tf2_ros import TransformListener, Buffer
import h5py
import numpy as np

class HDF5_Write(Node):
    def __init__(self):
        super().__init__('sensor_data_subscriber')
        
        # Subscription to the /odom, /imu/data, /scan, and tf topics
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',  # Change this to your actual odom topic if needed
            self.odom_callback,
            10
        )
        
        self.imu_subscription = self.create_subscription(
            Imu,
            '/imu',  # Change this to your actual imu topic if needed
            self.imu_callback,
            10
        )

        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',  # Change this to your actual scan topic if needed
            self.lidar_callback,
            10
        )
        
        # Initialize the TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Create or open an HDF5 file
        self.h5_file = h5py.File('sensor_data.h5', 'w')
        
        # Create groups for storing data
        self.odom_group = self.h5_file.create_group('odom_data')
        self.imu_group = self.h5_file.create_group('imu_data')
        self.lidar_group = self.h5_file.create_group('lidar_data')
        self.tf_group = self.h5_file.create_group('tf_data')  # New group for storing TF data
        self.message_group = self.h5_file.create_group('message_types')
        
        # Store the message type in the 'message_types' group
        self.message_group.create_dataset('odom_message_type', data='nav_msgs/msg/Odometry')
        self.message_group.create_dataset('imu_message_type', data='sensor_msgs/msg/Imu')
        self.message_group.create_dataset('lidar_message_type', data='sensor_msgs/msg/LaserScan')

        self.create_timer(0.1, self.tf_callback)  # 

    def odom_callback(self, msg: Odometry):
        # Extract position, orientation, and timestamp from the Odometry message
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        position_data = np.array([position.x, position.y, position.z], dtype=np.float64)
        orientation_data = np.array([orientation.x, orientation.y, orientation.z, orientation.w], dtype=np.float64)

        # Check if the datasets exist, and create them if not
        if 'position' not in self.odom_group:
            self.odom_group.create_dataset(
                'position', 
                shape=(1,3),
                data=position_data, 
                maxshape=(None, 3)  
            )
            self.odom_group.create_dataset(
                'orientation', 
                shape=(1,4),
                data=orientation_data, 
                maxshape=(None, 4),  
                chunks=(1, 4),  
                compression="gzip"
            )
            self.odom_group.create_dataset(
                'timestamps', 
                shape=(1,),
                data=np.array([timestamp], dtype=np.float64), 
                maxshape=(None,),  
                chunks=(1,),  
                compression="gzip"
            )
        else:
            self.odom_group['position'].resize(self.odom_group['position'].shape[0] + 1, axis=0)
            self.odom_group['position'][-1] = position_data
            self.odom_group['orientation'].resize(self.odom_group['orientation'].shape[0] + 1, axis=0)
            self.odom_group['orientation'][-1] = orientation_data
            self.odom_group['timestamps'].resize(self.odom_group['timestamps'].shape[0] + 1, axis=0)
            self.odom_group['timestamps'][-1] = timestamp

        self.get_logger().info(f"Odometry data received at {timestamp:.2f}")

    def imu_callback(self, msg: Imu):
        # Extract data from IMU message
        acceleration = [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z]
        angular_velocity = [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z]
        orientation = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        
        acceleration_data = np.array(acceleration, dtype=np.float64)
        angular_velocity_data = np.array(angular_velocity, dtype=np.float64)
        orientation_data = np.array(orientation, dtype=np.float64)

        if 'acceleration' not in self.imu_group:
            self.imu_group.create_dataset(
                'acceleration',
                shape=(1, 3),
                data=acceleration_data,
                maxshape=(None, 3),
                chunks=(1, 3),
                compression="gzip"
            )
            self.imu_group.create_dataset(
                'angular_velocity',
                shape=(1, 3),
                data=angular_velocity_data,
                maxshape=(None, 3),
                chunks=(1, 3),
                compression="gzip"
            )
            self.imu_group.create_dataset(
                'orientation',
                shape=(1, 4),
                data=orientation_data,
                maxshape=(None, 4),
                chunks=(1, 4),
                compression="gzip"
            )
            self.imu_group.create_dataset(
                'timestamps',
                shape=(1,),
                data=np.array([timestamp], dtype=np.float64),
                maxshape=(None,),
                chunks=(1,),
                compression="gzip"
            )
        else:
            self.imu_group['acceleration'].resize(self.imu_group['acceleration'].shape[0] + 1, axis=0)
            self.imu_group['acceleration'][-1] = acceleration_data
            self.imu_group['angular_velocity'].resize(self.imu_group['angular_velocity'].shape[0] + 1, axis=0)
            self.imu_group['angular_velocity'][-1] = angular_velocity_data
            self.imu_group['orientation'].resize(self.imu_group['orientation'].shape[0] + 1, axis=0)
            self.imu_group['orientation'][-1] = orientation_data
            self.imu_group['timestamps'].resize(self.imu_group['timestamps'].shape[0] + 1, axis=0)
            self.imu_group['timestamps'][-1] = timestamp

        self.get_logger().info(f"IMU data received at {timestamp:.2f}")

    def lidar_callback(self, msg: LaserScan):
        # Extract ranges and timestamp from the LaserScan message
        ranges = msg.ranges
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        
        ranges_data = np.array(ranges, dtype=np.float64)

        if 'ranges' not in self.lidar_group:
            self.lidar_group.create_dataset(
                'ranges',
                shape=(1, len(ranges)),
                data=ranges_data,
                maxshape=(None, len(ranges)),
                chunks=(1, len(ranges)),
                compression="gzip"
            )
            self.lidar_group.create_dataset(
                'timestamps',
                shape=(1,),
                data=np.array([timestamp], dtype=np.float64),
                maxshape=(None,),
                chunks=(1,),
                compression="gzip"
            )
        else:
            self.lidar_group['ranges'].resize(self.lidar_group['ranges'].shape[0] + 1, axis=0)
            self.lidar_group['ranges'][-1] = ranges_data
            self.lidar_group['timestamps'].resize(self.lidar_group['timestamps'].shape[0] + 1, axis=0)
            self.lidar_group['timestamps'][-1] = timestamp

        self.get_logger().info(f"LiDAR scan data received at {timestamp:.2f}")

    def tf_callback(self):
        try:
            # Get the latest transform from base_link to map (or any other frames of interest)
            transform = self.tf_buffer.lookup_transform('odom', 'base_link', rclpy.time.Time())
            # Convert the transform to a numpy array or other suitable format
            position = transform.transform.translation
            orientation = transform.transform.rotation
            timestamp = transform.header.stamp.sec + transform.header.stamp.nanosec / 1e9

            transform_data = np.array([position.x, position.y, position.z, orientation.x, orientation.y, orientation.z, orientation.w], dtype=np.float64)

            if 'transform' not in self.tf_group:
                self.tf_group.create_dataset(
                    'transform',
                    shape=(1, 7),  # 7 values (position + orientation)
                    data=transform_data,
                    maxshape=(None, 7),
                    chunks=(1, 7),
                    compression="gzip"
                )
                self.tf_group.create_dataset(
                    'timestamps',
                    shape=(1,),
                    data=np.array([timestamp], dtype=np.float64),
                    maxshape=(None,),
                    chunks=(1,),
                    compression="gzip"
                )
            else:
                self.tf_group['transform'].resize(self.tf_group['transform'].shape[0] + 1, axis=0)
                self.tf_group['transform'][-1] = transform_data
                self.tf_group['timestamps'].resize(self.tf_group['timestamps'].shape[0] + 1, axis=0)
                self.tf_group['timestamps'][-1] = timestamp

            self.get_logger().info(f"TF data received at {timestamp:.2f}")
        
        except Exception as e:
            self.get_logger().warn(f"Failed to get transform: {e}")

    def __del__(self):
        # Close the HDF5 file when done
        self.h5_file.close()


def main(args=None):
    rclpy.init(args=args)

    # Create an instance of the HDF5_Write node
    sensor_data_subscriber = HDF5_Write()

    # Spin the node so it can keep receiving messages
    rclpy.spin(sensor_data_subscriber)

    # Cleanly shut down the node
    sensor_data_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
