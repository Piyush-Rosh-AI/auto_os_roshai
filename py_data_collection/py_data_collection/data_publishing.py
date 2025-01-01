import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
import h5py

class OdomImuPublisher(Node):
    def __init__(self):
        super().__init__('odom_imu_hdf5_publisher')

        # ROS 2 Publishers for Odometry and IMU
        self.odom_pub = self.create_publisher(Odometry, 'odom_hdf5', 10)
        self.imu_pub = self.create_publisher(Imu, 'imu_hdf5', 10)

        # HDF5 file path
        self.file_path = '/home/roshai/sim_ws/sensor_data.h5'  # Replace with your HDF5 file path

        # Timer to periodically publish data
        self.timer = self.create_timer(0.1, self.publish_data)  # 10 Hz

    def read_hdf5_data(self):
        """
        Reads odometry and IMU data from an HDF5 file.
        Returns:
            tuple: (position, orientation, linear_accel, angular_velocity)
        """
        with h5py.File(self.file_path, 'r') as f:
            odom_timestamp = f['odom_data/timestamps'][:]
            position = f['odom_data/position'][:]
            orientation = f['odom_data/orientation'][:]
            linear_accel = f['imu_data/acceleration'][:]
            angular_velocity = f['imu_data/angular_velocity'][:]
        return position, orientation, linear_accel, angular_velocity

    def create_odometry_msg(self, position, orientation):
        """
        Create a ROS 2 Odometry message from position and orientation.
        """
        odom_msg = Odometry()

        # Set header
        odom_msg.header = Header()
        odom_msg.header.stamp = 1.0
        odom_msg.header.frame_id = "odom"

        # Set position
        odom_msg.pose.pose.position.x = position[0]
        odom_msg.pose.pose.position.y = position[1]
        odom_msg.pose.pose.position.z = position[2]

        # Set orientation (quaternion)
        odom_msg.pose.pose.orientation.x = orientation[0]
        odom_msg.pose.pose.orientation.y = orientation[1]
        odom_msg.pose.pose.orientation.z = orientation[2]
        odom_msg.pose.pose.orientation.w = orientation[3]

        return odom_msg

    def create_imu_msg(self, linear_accel, angular_velocity):
        """
        Create a ROS 2 IMU message from linear acceleration and angular velocity.
        """
        imu_msg = Imu()

        # Set header
        imu_msg.header = Header()
        imu_msg.header.stamp = 2.0
        imu_msg.header.frame_id = "imu_link"

        # Set linear acceleration
        imu_msg.linear_acceleration.x = linear_accel[0]
        imu_msg.linear_acceleration.y = linear_accel[1]
        imu_msg.linear_acceleration.z = linear_accel[2]

        # Set angular velocity
        imu_msg.angular_velocity.x = angular_velocity[0]
        imu_msg.angular_velocity.y = angular_velocity[1]
        imu_msg.angular_velocity.z = angular_velocity[2]

        return imu_msg

    def publish_data(self):
        """
        Reads data from HDF5 and publishes it to ROS 2 topics.
        """
        # Read data from HDF5 file
        position, orientation, linear_accel, angular_velocity = self.read_hdf5_data()

        # Create Odometry and IMU messages
        odom_msg = self.create_odometry_msg(position, orientation)
        imu_msg = self.create_imu_msg(linear_accel, angular_velocity)

        # Publish the messages
        self.odom_pub.publish(odom_msg)
        self.imu_pub.publish(imu_msg)

        self.get_logger().info('Published Odometry and IMU data')

def main(args=None):
    rclpy.init(args=args)

    # Create and run the node
    node = OdomImuPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
