import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan, Image
from std_msgs.msg import Header
import h5py
import numpy as np

class HDF5_Read(Node):
    
    def __init__(self):
        super().__init__('hdf5_data_publisher')

        # Create publishers for each topic
        self.odom_publisher = self.create_publisher(Odometry, '/odom', 10)
        self.imu_publisher = self.create_publisher(Imu, '/imu', 10)
        self.lidar_publisher = self.create_publisher(LaserScan, '/scan', 10)
        self.camera_publisher = self.create_publisher(Image, '/camera/image_raw', 10)

        # Open the HDF5 file
        self.h5_file = h5py.File('sensor_datas.h5', 'r')
        self.index =0
        # Create a timer to call the publish_data every 1 second
        
        self.create_timer(0.1, self.publish_data)  # Timer callback every 1 second

    def publish_data(self):
        # Publish Odometry Data
        if 'odom_data' in self.h5_file:
            odom_group = self.h5_file['odom_data']
            if(self.index<len(odom_group['header/stamp/sec'])):
                header = Header()
                header.stamp.sec = int(odom_group['header/stamp/sec'][self.index])
                header.stamp.nanosec = int(odom_group['header/stamp/nanosec'][self.index]*1e9)

                odom_msg = Odometry()
                odom_msg.header = header
                odom_msg.header.frame_id = str(odom_group['header/frame_id'][self.index])

                position = odom_group['pose/pose/position'][self.index]
                orientation = odom_group['pose/pose/orientation'][self.index]
                odom_msg.pose.pose.position.x = position[0]
                odom_msg.pose.pose.position.y = position[1]
                odom_msg.pose.pose.position.z = position[2]
                odom_msg.pose.pose.orientation.x = orientation[0]
                odom_msg.pose.pose.orientation.y = orientation[1]
                odom_msg.pose.pose.orientation.z = orientation[2]
                odom_msg.pose.pose.orientation.w = orientation[3]

                self.odom_publisher.publish(odom_msg)
            else:
                print("The odometry data was out of range")

        # Publish IMU Data
        if 'imu_data' in self.h5_file:
            imu_group = self.h5_file['imu_data']
            if(self.index<len(imu_group['header/stamp/sec'])):
                header = Header()
                header.stamp.sec = int(imu_group['header/stamp/sec'][self.index])
                header.stamp.nanosec = int(imu_group['header/stamp/nanosec'][self.index]*1e9)

                imu_msg = Imu()
                imu_msg.header = header
                imu_msg.header.frame_id = str(imu_group['header/frame_id'][self.index])

                # Acceleration
                imu_msg.linear_acceleration.x = imu_group['linear_acceleration'][self.index][0]
                imu_msg.linear_acceleration.y = imu_group['linear_acceleration'][self.index][1]
                imu_msg.linear_acceleration.z = imu_group['linear_acceleration'][self.index][2]

                # Angular Velocity
                imu_msg.angular_velocity.x = imu_group['angular_velocity'][self.index][0]
                imu_msg.angular_velocity.y = imu_group['angular_velocity'][self.index][1]
                imu_msg.angular_velocity.z = imu_group['angular_velocity'][self.index][2]

                # Orientation
                imu_msg.orientation.x = imu_group['orientation'][self.index][0]
                imu_msg.orientation.y = imu_group['orientation'][self.index][1]
                imu_msg.orientation.z = imu_group['orientation'][self.index][2]
                imu_msg.orientation.w = imu_group['orientation'][self.index][3]

                self.imu_publisher.publish(imu_msg)
            else:
                print("The imu_group data was out of range")
        # Publish LiDAR Data
        if 'lidar_data' in self.h5_file:
            lidar_group = self.h5_file['lidar_data']
            if(self.index<len(lidar_group['header/stamp/sec'])):

                header = Header()
                header.stamp.sec = int(lidar_group['header/stamp/sec'][self.index])
                header.stamp.nanosec = int(lidar_group['header/stamp/nanosec'][self.index]*1e9)

                lidar_msg = LaserScan()
                lidar_msg.header = header
                lidar_msg.header.frame_id = str(lidar_group['header/frame_id'][self.index])
                lidar_msg.ranges = lidar_group['ranges'][self.index]

                self.lidar_publisher.publish(lidar_msg)
            else:
                print("The lidar_group data was out of range")

            

        # Publish Camera Image Data
        if 'camera_data' in self.h5_file:
            camera_group = self.h5_file['camera_data']
            if(self.index<len(camera_group['header/stamp/sec'])):
                header = Header()
                header.stamp.sec = int(camera_group['header/stamp/sec'][self.index])
                header.stamp.nanosec = int(camera_group['header/stamp/nanosec'][self.index]*1e9)

                camera_msg = Image()
                camera_msg.header = header
                camera_msg.header.frame_id = str(camera_group['header/frame_id'][self.index])
                camera_msg.data = camera_group['image'][self.index].tolist()  # Convert numpy array to list for Image message


                self.camera_publisher.publish(camera_msg)
            else:
                print("The camera_group data was out of range")
        self.index=self.index+1
        self.get_logger().info("Published data to topics.")

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
