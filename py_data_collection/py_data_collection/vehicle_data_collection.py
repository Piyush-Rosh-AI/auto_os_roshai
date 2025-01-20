import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Imu, LaserScan, Image,PointCloud2,NavSatFix,MagneticField,FluidPressure,Temperature
from tf2_ros import TransformListener, Buffer
import h5py
import numpy as np
import time
import json
import datetime
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
import os
#@todo @piyush-
# -header in alphabetical format
# -check for the variables names
# -make the file into chunks if memory increases at certain extend


class HDF5_Write(Node):
    def __init__(self):
        super().__init__('sensor_data_subscriber')
        #frequency
        self.messageCounter=0
        self.startTime=0
        
        
        
        #Get current date and time for the file name
        current_time = datetime.datetime.now()
        strdate = datetime.datetime(current_time.year, current_time.month, current_time.day)
        formatted_date = strdate.strftime("%B %d, %Y")
        self.hdf_name=str(current_time.hour)+ '_'  + str(current_time.minute)+"|"+formatted_date+ '_file.h5'
        
        self.h5_file = h5py.File(self.hdf_name, 'w')
        
        qos_profile = QoSProfile(
            depth=10,  # Set the queue size for the subscriber (buffer size)
            reliability=ReliabilityPolicy.BEST_EFFORT,  # Reliable message delivery
            durability=DurabilityPolicy.VOLATILE,  # Volatile messages (do not persist)
        )
        
        # Subscription to the odometry message types
        self.gps_filtered_subscription = self.create_subscription(
            NavSatFix,
            '/gps/filtered',  # Change this to your actual odom topic if needed
            self.gps_filtered_callback,
            qos_profile
        )
        self.gps_filtered_data=self.h5_file.create_dataset('gps_filtered_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
       
        # Subscription to the odometry message types
        self.gps_2_pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/gps_2/pose',  # Change this to your actual odom topic if needed
            self.gps_2_pose_callback,
            qos_profile
        )
        self.gps_2_pose_data=self.h5_file.create_dataset('gps_2_pose_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
       
        # Subscription to the odometry message types
        self.vectornav_odom_subscription = self.create_subscription(
            Odometry,
            '/vectornav_odom_data',  # Change this to your actual odom topic if needed
            self.vectornav_odom_callback,
            qos_profile
        )
        self.vectornav_odom_data=self.h5_file.create_dataset('vectornav_odom_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
        self.gps_odom_subscription = self.create_subscription(
            Odometry,
            '/odometry/gps',  # Change this to your actual odom topic if needed
            self.gps_odom_callback,
            qos_profile
        )
        self.odometry_gps_data=self.h5_file.create_dataset('odometry_gps_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
      
        self.navsat_odom_subscription = self.create_subscription(
            Odometry,
            '/odometry/navsat',  # Change this to your actual odom topic if needed
            self.navsat_odom_callback,
            qos_profile
        )
        self.odometry_navsat_data=self.h5_file.create_dataset('odometry_navsat_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
      
        # Subscription to the imu message types
        self.ouster_imu_subscription = self.create_subscription(
            Imu,
            '/ouster/imu',  # Change this to your actual imu topic if needed
            self.ouster_imu_callback,
            qos_profile
        )
        self.ouster_imu_data=self.h5_file.create_dataset('ouster_imu_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
       
        self.vectornav_imu_subscription = self.create_subscription(
            Imu,
            '/vectornav/IMU',  # Change this to your actual imu topic if needed
            self.vectornav_imu_callback,
            qos_profile
        )
        self.vectornav_IMU_data=self.h5_file.create_dataset('vectornav_IMU_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
       
        # Subscription to the pointclouddata2 message types

        self.ousterpoints_lidar_subscription = self.create_subscription(
            PointCloud2,
            '/ouster/points',  # Change this to your actual scan topic if needed
            self.ousterpoints_lidar_callback,
            qos_profile
        )
        self.ouster_points_data=self.h5_file.create_dataset('ouster_points_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
  
        # Subscription to the Image message types
        self.ouster_nearir_image_camera_subscription = self.create_subscription(
            Image,
            '/ouster/nearir_image',  # Change to your actual camera topic
            self.ouster_nearir_image_camera_callback,
            qos_profile
        )
        self.ouster_nearir_image_data=self.h5_file.create_dataset('ouster_nearir_image_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
  
        self.ouster_range_image_camera_subscription = self.create_subscription(
            Image,
            '/ouster/range_image',  # Change to your actual camera topic
            self.ouster_range_image_camera_callback,
            qos_profile
        )
        self.ouster_range_image_data=self.h5_file.create_dataset('ouster_range_image_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
  
        self.ouster_reflec_image_camera_subscription = self.create_subscription(
            Image,
            '/ouster/reflec_image',  # Change to your actual camera topic
            self.ouster_reflec_image_camera_callback,
            qos_profile
        )
        self.ouster_reflec_image_data=self.h5_file.create_dataset('ouster_reflec_image_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
  
        self.ouster_signal_image_camera_subscription = self.create_subscription(
            Image,
            '/ouster/signal_image',  # Change to your actual camera topic
            self.ouster_signal_image_camera_callback,
            qos_profile
        )
        self.ouster_signal_image_data=self.h5_file.create_dataset('ouster_signal_image_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
        
        self.vectornav_mag_subscription = self.create_subscription(
            MagneticField,
            '/vectornav/MAG',  # Change to your actual camera topic
            self.vectornav_mag_callback,
            qos_profile
        )
        self.vectornav_mag_data=self.h5_file.create_dataset('vectornav_MAG_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
   
        self.vectornav_temp_subscription = self.create_subscription(
            Temperature,
            '/vectornav/Temp',  # Change to your actual camera topic
            self.vectornav_temp_callback,
            qos_profile
        )
        self.vectornav_Temp_data=self.h5_file.create_dataset('vectornav_Temp_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
        
        self.vectornav_pres_subscription = self.create_subscription(
            FluidPressure,
            '/vectornav/Pres',  # Change to your actual camera topic
            self.vectornav_pres_callback,
            qos_profile
        )
        self.vectornav_Pres_data=self.h5_file.create_dataset('vectornav_Pres_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
     
        self.vectornav_gps_subscription = self.create_subscription(
            NavSatFix,
            '/vectornav/GPS',  # Change to your actual camera topic
            self.vectornav_gps_callback,
            qos_profile
        )
        self.vectornav_gps_data=self.h5_file.create_dataset('vectornav_GPS_data', shape=(1,),maxshape=(None, ),chunks=(1, ),  data='S512',compression="gzip")
       
                 
    def odom_JSON(self,msg:Odometry,avgTime):      
        return  {'avgTime':avgTime,
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
    def pointcloud2_JSON(self,msg:PointCloud2):    
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
    def navsatfix_JSON(self, msg: NavSatFix):  
        return {
            'header': {
                'frame_id': msg.header.frame_id,
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                }
            },
            'status': {
                'status': msg.status.status,
                'service': msg.status.service
            },
            'latitude': msg.latitude,
            'longitude': msg.longitude,
            'altitude': msg.altitude,
            'position_covariance': [
                msg.position_covariance[0], msg.position_covariance[1], msg.position_covariance[2],
                msg.position_covariance[3], msg.position_covariance[4], msg.position_covariance[5],
                msg.position_covariance[6], msg.position_covariance[7], msg.position_covariance[8]
            ],
            'position_covariance_type': msg.position_covariance_type
        }
    def posewithcovariancestamped_JSON(self, msg: PoseWithCovarianceStamped):  
        return {
            'header': {
                'frame_id': msg.header.frame_id,
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                }
            },
            'pose': {
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
                'covariance': [
                    msg.pose.covariance[0], msg.pose.covariance[1], msg.pose.covariance[2], msg.pose.covariance[3], msg.pose.covariance[4], msg.pose.covariance[5],
                    msg.pose.covariance[6], msg.pose.covariance[7], msg.pose.covariance[8], msg.pose.covariance[9], msg.pose.covariance[10], msg.pose.covariance[11],
                    msg.pose.covariance[12], msg.pose.covariance[13], msg.pose.covariance[14], msg.pose.covariance[15], msg.pose.covariance[16], msg.pose.covariance[17],
                    msg.pose.covariance[18], msg.pose.covariance[19], msg.pose.covariance[20], msg.pose.covariance[21], msg.pose.covariance[22], msg.pose.covariance[23],
                    msg.pose.covariance[24], msg.pose.covariance[25]
                ]
            }
        }
    def magneticfield_JSON(self, msg: MagneticField):
        return {
            'header': {
                'frame_id': msg.header.frame_id,
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                }
            },
            'magnetic_field': {
                'x': msg.magnetic_field.x,
                'y': msg.magnetic_field.y,
                'z': msg.magnetic_field.z
            }
        }
    def temperature_JSON(self, msg: Temperature):
        return {
            'header': {
                'frame_id': msg.header.frame_id,
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                }
            },
            'temperature': msg.temperature
        }
    def fluid_pressure_JSON(self, msg:FluidPressure):
        return {
            'header': {
                'frame_id': msg.header.frame_id,
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                }
            },
            'fluid_pressure': msg.fluid_pressure,
            'variance': msg.variance
        }
    def image_JSON(self, msg: Image):  
        return {
            'header': {
                'frame_id': msg.header.frame_id,
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                }
            },
            'height': msg.height,
            'width': msg.width,
            'encoding': msg.encoding,
            'is_bigendian': msg.is_bigendian,
            'step': msg.step,
            'data': list(msg.data)  # Image data is typically in raw byte format, so convert to a list
        }

    def gps_filtered_callback(self, msg: Odometry):
        print("getting the data for gps filtered data")
        self.gps_filtered_data.resize(self.gps_filtered_data.shape[0] + 1, axis=0)
        self.gps_filtered_data[-1] = np.string_(json.dumps(self.navsatfix_JSON(msg)))
    def gps_2_pose_callback(self, msg: Odometry):
   
        self.gps_2_pose_data.resize(self.gps_2_pose_data.shape[0] + 1, axis=0)
        self.gps_2_pose_data[-1] = np.string_(json.dumps(self.posewithcovariancestamped_JSON(msg)))
  
    def vectornav_odom_callback(self, msg: Odometry):
        avgTime=0
        if(self.messageCounter>0):
            lastRecordedTime=time.time()
            elapsedTime=lastRecordedTime-self.startTime
            avgTime=elapsedTime/self.messageCounter
            # print(avgTime)
        else:
            self.startTime=time.time()
            
        self.vectornav_odom_data.resize(self.vectornav_odom_data.shape[0] + 1, axis=0)
        self.vectornav_odom_data[-1] = np.string_(json.dumps(self.odom_JSON(msg,avgTime)))
        self.messageCounter=self.messageCounter+1     
    def gps_odom_callback(self, msg: Odometry):
        self.odometry_gps_data.resize(self.odometry_gps_data.shape[0] + 1, axis=0)
        self.odometry_gps_data[-1] = np.string_(json.dumps(self.odom_JSON(msg)))
    def navsat_odom_callback(self, msg: Odometry):
        self.odometry_navsat_data.resize(self.odometry_navsat_data.shape[0] + 1, axis=0)
        self.odometry_navsat_data[-1] = np.string_(json.dumps(self.odom_JSON(msg)))

    def ouster_imu_callback(self, msg: Imu):
        self.ouster_imu_data.resize(self.ouster_imu_data.shape[0] + 1, axis=0)
        self.ouster_imu_data[-1] = np.string_(json.dumps(self.imu_JSON(msg)))
    def vectornav_imu_callback(self, msg: Imu):
        self.vectornav_IMU_data.resize(self.vectornav_IMU_data.shape[0] + 1, axis=0)
        self.vectornav_IMU_data[-1] = np.string_(json.dumps(self.imu_JSON(msg)))

    def ousterpoints_lidar_callback(self, msg: PointCloud2):
        self.ouster_points_data.resize(self.ouster_points_data.shape[0] + 1, axis=0)
        self.ouster_points_data[-1] = np.string_(json.dumps(self.pointcloud2_JSON(msg)))

    def ouster_nearir_image_camera_callback(self, msg: Image):
        self.ouster_nearir_image_data.resize(self.ouster_nearir_image_data.shape[0] + 1, axis=0)
        self.ouster_nearir_image_data[-1] = np.string_(json.dumps(self.image_JSON(msg)))
    def ouster_range_image_camera_callback(self, msg: Image):
        self.ouster_range_image_data.resize(self.ouster_range_image_data.shape[0] + 1, axis=0)
        self.ouster_range_image_data[-1] = np.string_(json.dumps(self.image_JSON(msg)))
    def ouster_reflec_image_camera_callback(self, msg: Image):
        self.ouster_reflec_image_data.resize(self.ouster_reflec_image_data.shape[0] + 1, axis=0)
        self.ouster_reflec_image_data[-1] = np.string_(json.dumps(self.image_JSON(msg)))
    def ouster_signal_image_camera_callback(self, msg: Image):
        self.ouster_signal_image_data.resize(self.ouster_signal_image_data.shape[0] + 1, axis=0)
        self.ouster_signal_image_data[-1] = np.string_(json.dumps(self.image_JSON(msg)))
    
    def vectornav_mag_callback(self,msg:MagneticField):
        self.vectornav_MAG_data.resize(self.vectornav_MAG_data.shape[0] + 1, axis=0)
        self.vectornav_MAG_data[-1] = np.string_(json.dumps(self.magneticfield_JSON(msg)))

    def vectornav_temp_callback(self,msg:Temperature):
        self.vectornav_Temp_data.resize(self.vectornav_Temp_data.shape[0] + 1, axis=0)
        self.vectornav_Temp_data[-1] = np.string_(json.dumps(self.temperature_JSON(msg)))
    
    def vectornav_pres_callback(self,msg:FluidPressure):
        self.vectornav_Pres_data.resize(self.vectornav_Pres_data.shape[0] + 1, axis=0)
        self.vectornav_Pres_data[-1] = np.string_(json.dumps(self.fluid_pressure_JSON(msg)))
   
    def vectornav_gps_callback(self,msg:NavSatFix):
        self.vectornav_GPS_data.resize(self.vectornav_GPS_data.shape[0] + 1, axis=0)
        self.vectornav_GPS_data[-1] = np.string_(json.dumps(self.navsatfix_JSON(msg)))

    def __del__(self):
        # Close the HDF5 file when done
        file_size = os.path.getsize(self.hdf_name)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024

        print(f"Size of the file: {file_size_mb:.2f} MB")
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
