import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan, Image
from tf2_ros import TransformListener, Buffer
import h5py
import numpy as np
from sensor_msgs_py import point_cloud2  # For image handling (if needed)

class HDF5_Write(Node):
    def __init__(self):
        super().__init__('sensor_data_subscriber')

        # Subscription to the /odom, /imu/data, /scan, /camera/image_raw, and tf topics
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

        # Camera Subscription (Raw image topic)
        self.camera_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # Change to your actual camera topic
            self.camera_callback,
            10
        )

        # Initialize the TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Create or open an HDF5 file
        self.h5_file = h5py.File('sensor_datas.h5', 'w')

        # Create groups for storing data
        self.odom_group = self.h5_file.create_group('odom_data')
        self.odom_header_group = self.odom_group.create_group('header')
        self.odom_header_stamp_group = self.odom_header_group.create_group('stamp')
        self.odom_pose_group = self.odom_group.create_group('pose')
        self.odom_pose_pose_group = self.odom_pose_group.create_group('pose')

        self.imu_group = self.h5_file.create_group('imu_data')
        self.imu_header_group = self.imu_group.create_group('header')
        self.imu_header_stamp_group = self.imu_header_group.create_group('stamp')


        self.lidar_group = self.h5_file.create_group('lidar_data')
        self.lidar_header_group = self.lidar_group.create_group('header')
        self.lidar_header_stamp_group = self.lidar_header_group.create_group('stamp')

        self.tf_group = self.h5_file.create_group('tf_data')  # New group for storing TF data
        self.tf_header_group = self.tf_group.create_group('header')
        self.tf_header_stamp_group = self.tf_header_group.create_group('stamp')
        
        self.camera_group = self.h5_file.create_group('camera_data')  # New group for storing Camera data
        self.camera_header_group = self.camera_group.create_group('header')
        self.camera_header_stamp_group = self.camera_header_group.create_group('stamp')
        
        # Create a timer to call tf_callback every 100ms (0.1 seconds)
        self.create_timer(0.1, self.tf_callback)  # Call tf_callback every 100ms

    def odom_callback(self, msg: Odometry):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        if 'position' not in self.odom_pose_pose_group:
            self.odom_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=msg.header.frame_id)      
            self.odom_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([msg.header.stamp.sec], dtype=np.float64))
            self.odom_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([msg.header.stamp.nanosec / 1e9], dtype=np.float64))
            self.odom_pose_pose_group.create_dataset('position',shape=(1,3),maxshape=(None, 3),chunks=(1, 3),data=[position.x, position.y, position.z])
            self.odom_pose_pose_group.create_dataset('orientation', shape=(1,4),maxshape=(None, 4),chunks=(1, 4),  data=[orientation.x, orientation.y, orientation.z, orientation.w])
          
        else:
            self.odom_header_group['frame_id'].resize(self.odom_header_group['frame_id'].shape[0] + 1, axis=0)
            self.odom_header_group['frame_id'][-1] = msg.header.frame_id
            self.odom_header_stamp_group['sec'].resize(self.odom_header_stamp_group['sec'].shape[0] + 1, axis=0)
            self.odom_header_stamp_group['sec'][-1] = msg.header.stamp.sec
            self.odom_header_stamp_group['nanosec'].resize(self.odom_header_stamp_group['nanosec'].shape[0] + 1, axis=0)
            self.odom_header_stamp_group['nanosec'][-1] = msg.header.stamp.nanosec
            self.odom_pose_pose_group['position'].resize(self.odom_pose_pose_group['position'].shape[0] + 1, axis=0)
            self.odom_pose_pose_group['position'][-1] = np.array([position.x, position.y, position.z])
            self.odom_pose_pose_group['orientation'].resize(self.odom_pose_pose_group['orientation'].shape[0] + 1, axis=0)
            self.odom_pose_pose_group['orientation'][-1] = np.array([orientation.x, orientation.y, orientation.z,orientation.w], dtype=np.float64)


        self.get_logger().info(f"Odometry data received at {msg.header.stamp.sec:.2f}")


    def imu_callback(self, msg: Imu):
        # Extract data from IMU message
        acceleration = [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z]
        angular_velocity = [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z]
        orientation = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9

        acceleration_data = np.array(acceleration, dtype=np.float64)
        angular_velocity_data = np.array(angular_velocity, dtype=np.float64)
        orientation_data = np.array(orientation, dtype=np.float64)

        if 'linear_acceleration' not in self.imu_group:
            self.imu_group.create_dataset(
                'linear_acceleration',
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
            self.imu_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=msg.header.frame_id)      
            self.imu_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([msg.header.stamp.sec], dtype=np.float64))
            self.imu_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([msg.header.stamp.nanosec / 1e9], dtype=np.float64))
        else:
            self.imu_header_group['frame_id'].resize(self.imu_header_group['frame_id'].shape[0] + 1, axis=0)
            self.imu_header_group['frame_id'][-1] = msg.header.frame_id
            self.imu_header_stamp_group['sec'].resize(self.imu_header_stamp_group['sec'].shape[0] + 1, axis=0)
            self.imu_header_stamp_group['sec'][-1] = msg.header.stamp.sec
            self.imu_header_stamp_group['nanosec'].resize(self.imu_header_stamp_group['nanosec'].shape[0] + 1, axis=0)
            self.imu_header_stamp_group['nanosec'][-1] = msg.header.stamp.nanosec
            self.imu_group['linear_acceleration'].resize(self.imu_group['linear_acceleration'].shape[0] + 1, axis=0)
            self.imu_group['linear_acceleration'][-1] = acceleration_data
            self.imu_group['angular_velocity'].resize(self.imu_group['angular_velocity'].shape[0] + 1, axis=0)
            self.imu_group['angular_velocity'][-1] = angular_velocity_data
            self.imu_group['orientation'].resize(self.imu_group['orientation'].shape[0] + 1, axis=0)
            self.imu_group['orientation'][-1] = orientation_data

        self.get_logger().info(f"IMU data received at {timestamp:.2f}")

    def lidar_callback(self, msg: LaserScan):
        # Extract ranges and timestamp from the LaserScan message
        ranges = msg.ranges
 

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
            self.lidar_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=msg.header.frame_id)      
            self.lidar_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([msg.header.stamp.sec], dtype=np.float64))
            self.lidar_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([msg.header.stamp.nanosec / 1e9], dtype=np.float64))
          
        else:
            self.lidar_header_group['frame_id'].resize(self.lidar_header_group['frame_id'].shape[0] + 1, axis=0)
            self.lidar_header_group['frame_id'][-1] = msg.header.frame_id
            self.lidar_header_stamp_group['sec'].resize(self.lidar_header_stamp_group['sec'].shape[0] + 1, axis=0)
            self.lidar_header_stamp_group['sec'][-1] = msg.header.stamp.sec
            self.lidar_header_stamp_group['nanosec'].resize(self.lidar_header_stamp_group['nanosec'].shape[0] + 1, axis=0)
            self.lidar_header_stamp_group['nanosec'][-1] = msg.header.stamp.nanosec
           
            self.lidar_group['ranges'].resize(self.lidar_group['ranges'].shape[0] + 1, axis=0)
            self.lidar_group['ranges'][-1] = ranges_data

        self.get_logger().info(f"LiDAR scan data received at {msg.header.stamp.sec:.2f}")

    def camera_callback(self, msg: Image):
        # Extract image data and timestamp from the camera image message
        image_data = np.array(msg.data, dtype=np.uint8)


        if 'image' not in self.camera_group:
            self.camera_group.create_dataset(
                'image',
                shape=(1, len(image_data)),
                data=image_data,
                maxshape=(None, len(image_data)),
                chunks=(1, len(image_data)),
                compression="gzip"
            )
            self.camera_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=msg.header.frame_id)      
            self.camera_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([msg.header.stamp.sec], dtype=np.float64))
            self.camera_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([msg.header.stamp.nanosec / 1e9], dtype=np.float64))
 
        else:
            self.camera_header_group['frame_id'].resize(self.camera_header_group['frame_id'].shape[0] + 1, axis=0)
            self.camera_header_group['frame_id'][-1] = msg.header.frame_id
            self.camera_header_stamp_group['sec'].resize(self.camera_header_stamp_group['sec'].shape[0] + 1, axis=0)
            self.camera_header_stamp_group['sec'][-1] = msg.header.stamp.sec
            self.camera_header_stamp_group['nanosec'].resize(self.camera_header_stamp_group['nanosec'].shape[0] + 1, axis=0)
            self.camera_header_stamp_group['nanosec'][-1] = msg.header.stamp.nanosec
            
            self.camera_group['image'].resize(self.camera_group['image'].shape[0] + 1, axis=0)
            self.camera_group['image'][-1] = image_data


        self.get_logger().info(f"Camera image received at {msg.header.stamp.sec:.2f}")
    
    def tf_callback(self):
        try:
            # Get the latest transform from base_link to map (or any other frames of interest)
            transform = self.tf_buffer.lookup_transform('odom', 'base_link', rclpy.time.Time())
            # Convert the transform to a numpy array or other suitable format
            position = transform.transform.translation
            orientation = transform.transform.rotation

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
                self.tf_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=transform.header.frame_id)      
                self.tf_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([transform.header.stamp.sec], dtype=np.float64))
                self.tf_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([transform.header.stamp.nanosec / 1e9], dtype=np.float64))
    
            else:
                self.tf_header_group['frame_id'].resize(self.tf_header_group['frame_id'].shape[0] + 1, axis=0)
                self.tf_header_group['frame_id'][-1] = transform.header.frame_id
                self.tf_header_stamp_group['sec'].resize(self.tf_header_stamp_group['sec'].shape[0] + 1, axis=0)
                self.tf_header_stamp_group['sec'][-1] = transform.header.stamp.sec
                self.tf_header_stamp_group['nanosec'].resize(self.tf_header_stamp_group['nanosec'].shape[0] + 1, axis=0)
                self.tf_header_stamp_group['nanosec'][-1] = transform.header.stamp.nanosec
                self.tf_group['transform'].resize(self.tf_group['transform'].shape[0] + 1, axis=0)
                self.tf_group['transform'][-1] = transform_data

            self.get_logger().info(f"TF data received at {transform.header.stamp.sec:.2f}")
        
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
