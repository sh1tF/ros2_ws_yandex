import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from nav_msgs.msg import Odometry
import math

class WheelOdometry(Node):
    def __init__(self):
        super().__init__('wheel_odometry')
        
        self.counts_per_rev = 16384
        self.wheel_diameter = 0.065
        self.wheel_base = 0.25
        self.wheel_circumference = math.pi * self.wheel_diameter
        
        self.prev_counts = [0, 0, 0, 0]
        self.prev_time = self.get_clock().now()
        self.first_reading = True
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.total_path = 0.0
        
        self.encoder_sub = self.create_subscription(
            Int32MultiArray, '/encoders/raw', self.encoder_callback, 10)
        
        self.odom_pub = self.create_publisher(
            Odometry, '/odom/wheel', 10)
        
        self.get_logger().info('Wheel Odometry started')
    
    def encoder_callback(self, msg):
        counts = list(msg.data)
        current_time = self.get_clock().now()
        
        if self.first_reading:
            self.prev_counts = counts
            self.prev_time = current_time
            self.first_reading = False
            return
        
        delta_left = ((counts[0] - self.prev_counts[0]) + (counts[1] - self.prev_counts[1])) / 2.0
        delta_right = ((counts[2] - self.prev_counts[2]) + (counts[3] - self.prev_counts[3])) / 2.0
        
        dist_left = (delta_left / self.counts_per_rev) * self.wheel_circumference
        dist_right = (delta_right / self.counts_per_rev) * self.wheel_circumference
        
        avg_dist_abs = (abs(dist_left) + abs(dist_right)) / 2.0
        if avg_dist_abs > 0:
            slip_ratio = abs(dist_left - dist_right) / avg_dist_abs
            if slip_ratio > 0.20:
                self.get_logger().warning(f'WARNING: Slip detected! Diff ratio: {slip_ratio:.2%}')

        dist_center = (dist_left + dist_right) / 2.0
        delta_theta = (dist_right - dist_left) / self.wheel_base
        
        dt = (current_time - self.prev_time).nanoseconds / 1e9
        if dt > 0:
            vx = dist_center / dt
            if abs(vx) > 2.0:
                self.get_logger().error(f'ERROR: Unrealistic speed vx={vx:.2f} m/s!')

        self.total_path += abs(dist_center)
        
        self.x += dist_center * math.cos(self.theta + delta_theta / 2.0)
        self.y += dist_center * math.sin(self.theta + delta_theta / 2.0)
        self.theta += delta_theta
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
        
        self.publish_odometry()
        
        self.prev_counts = counts
        self.prev_time = current_time
        
        self.get_logger().info(
            f'Odom: x={self.x:.2f}, y={self.y:.2f}, Path: {self.total_path:.2f}m'
        )
    
    def publish_odometry(self):
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.w = math.cos(self.theta / 2.0)
        odom.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        self.odom_pub.publish(odom)

def main(args=None):
    rclpy.init(args=args)
    node = WheelOdometry()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
