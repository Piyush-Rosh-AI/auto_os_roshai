import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan, Image,PointCloud2
from tf2_ros import TransformListener, Buffer
import h5py
import numpy as np
import time
import json

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




        self.lidar_group = self.h5_file.create_group('lidar_data')
        self.lidar_header_group = self.lidar_group.create_group('header')
        self.lidar_header_stamp_group = self.lidar_header_group.create_group('stamp')

        self.tf_group = self.h5_file.create_group('tf_data')  # New group for storing TF data
        self.tf_header_group = self.tf_group.create_group('header')
        self.tf_header_stamp_group = self.tf_header_group.create_group('stamp')
        
        self.camera_group = self.h5_file.create_group('camera_data')  # New group for storing Camera data
        self.camera_header_group = self.camera_group.create_group('header')
        self.camera_header_stamp_group = self.camera_header_group.create_group('stamp')


        self.odom_data=self.h5_file.create_dataset('odom_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
        self.imu_data=self.h5_file.create_dataset('imu_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
        self.laserscan_data=self.h5_file.create_dataset('laserscan_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
          
        
        # Create a timer to call tf_callback every 100ms (0.1 seconds)
        self.create_timer(0.1, self.tf_callback)  # Call tf_callback every 100ms
    def odom_JSON(self,msg:Odometry):
        return  {
                'header': {
                    'frame_id': msg.header.frame_id,
                    'stamp': {
                        'sec': msg.header.stamp.sec,
                        'nanosec': msg.header.stamp.nanosec
                    }
                },
                'pose': {
                    'position': {
                        'x': msg.pose.pose.position.x,
                        'y': msg.pose.pose.position.y,
                        'z': msg.pose.pose.position.z
                    },
                    'orientation': {
                        'x': msg.pose.pose.orientation.x,
                        'y': msg.pose.pose.orientation.y,
                        'z': msg.pose.pose.orientation.z,
                        'w': msg.pose.pose.orientation.w
                    }
                },
                'twist': {
                    'linear': {
                        'x': msg.twist.twist.linear.x,
                        'y': msg.twist.twist.linear.y,
                        'z': msg.twist.twist.linear.z
                    },
                    'angular': {
                        'x': msg.twist.twist.angular.x,
                        'y': msg.twist.twist.angular.y,
                        'z': msg.twist.twist.angular.z
                    }
                }
            }

    def imu_JSON(self,msg:Imu):
        return {
                    'header': {
                        'frame_id': msg.header.frame_id,
                        'stamp': {
                            'sec': msg.header.stamp.sec,
                            'nanosec': msg.header.stamp.nanosec
                        }
                    },
                    'orientation': {
                        'x': msg.orientation.x,
                        'y': msg.orientation.y,
                        'z': msg.orientation.z,
                        'w': msg.orientation.w
                    },
                    'angular_velocity': {
                        'x': msg.angular_velocity.x,
                        'y': msg.angular_velocity.y,
                        'z': msg.angular_velocity.z
                    },
                    'linear_acceleration': {
                        'x': msg.linear_acceleration.x,
                        'y': msg.linear_acceleration.y,
                        'z': msg.linear_acceleration.z
                    }
                }

    def laserscan_JSON(self,msg:LaserScan):
        return {
        'header': {
            'frame_id': msg.header.frame_id,
            'stamp': {
                'sec': msg.header.stamp.sec,
                'nanosec': msg.header.stamp.nanosec
            }
        },
        'angle_min': msg.angle_min,
        'angle_max': msg.angle_max,
        'angle_increment': msg.angle_increment,
        'time_increment': msg.time_increment,
        'scan_time': msg.scan_time,
        'range_min': msg.range_min,
        'range_max': msg.range_max,
        # 'ranges': msg.ranges,  # List of range values (distance measurements)
        # 'intensities': msg.intensities  # List of intensity values (optional)
        }

    def PointCloud2_JSON(self,msg:PointCloud2):
        return  {
                'header': {
                    'frame_id': msg.header.frame_id,
                    'stamp': {
                        'sec': msg.header.stamp.sec,
                        'nanosec': msg.header.stamp.nanosec
                    }
                },
                'height': msg.height,
                'width': msg.width,
                'fields': [{'name': field.name,
                            'offset': field.offset,
                            'datatype': field.datatype,
                            'count': field.count} for field in msg.fields],
                'is_bigendian': msg.is_bigendian,
                'point_step': msg.point_step,
                'row_step': msg.row_step,
                'is_dense': msg.is_dense,
                'data': []  # This will store the actual point data
            }

    
    def odom_callback(self, msg: Odometry):

        odometry_data=self.odom_JSON(msg)   
        # Serialize the dictionary to a JSON string
        odometry_json = json.dumps(odometry_data)
  
        self.odom_data.resize(self.odom_data.shape[0] + 1, axis=0)
        self.odom_data[-1] = np.string_(odometry_json)


        self.get_logger().info(f"Odometry data received at {msg.header.stamp.sec:.2f}")


    def imu_callback(self, msg: Imu):
        imu_data=self.imu_JSON(msg)   
        # Serialize the dictionary to a JSON string
        imu_json = json.dumps(imu_data)
  
        self.imu_data.resize(self.imu_data.shape[0] + 1, axis=0)
        self.imu_data[-1] = np.string_(imu_json)


        self.get_logger().info(f"Odometry data received at {msg.header.stamp.sec:.2f}")

    def lidar_callback(self, msg: LaserScan):
        laserscan_data=self.laserscan_JSON(msg)   
        # Serialize the dictionary to a JSON string
        laserscan_json = json.dumps(laserscan_data)
  
        self.laserscan_data.resize(self.laserscan_data.shape[0] + 1, axis=0)
        self.laserscan_data[-1] = np.string_(laserscan_json)


        self.get_logger().info(f"Odometry data received at {msg.header.stamp.sec:.2f}")


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
            self.camera_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=msg.header.frame_id,compression="gzip")      
            self.camera_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([msg.header.stamp.sec], dtype=np.float64),compression="gzip")
            self.camera_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([msg.header.stamp.nanosec / 1e9], dtype=np.float64),compression="gzip")
 
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
                self.tf_header_group.create_dataset('frame_id',shape=(1,1),maxshape=(None, 1),chunks=(1, 1), data=transform.header.frame_id,compression="gzip")      
                self.tf_header_stamp_group.create_dataset('sec',shape=(1,),maxshape=(None, ),chunks=(1, ), data=np.array([transform.header.stamp.sec], dtype=np.float64),compression="gzip")
                self.tf_header_stamp_group.create_dataset('nanosec', shape=(1,),maxshape=(None, ),chunks=(1, ),data=np.array([transform.header.stamp.nanosec / 1e9], dtype=np.float64),compression="gzip")
    
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
