import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import random

class DToFLidarSimulator(Node):
    def __init__(self):
        super().__init__('dtof_lidar_simulator')
        
        self.left_pub = self.create_publisher(Range, '/dtof/left', 10)
        self.right_pub = self.create_publisher(Range, '/dtof/right', 10)
        
        self.timer = self.create_timer(0.01, self.timer_callback)
        
        self.min_range = 0.05
        self.max_range = 10.0

    def timer_callback(self):
        now = self.get_clock().now().to_msg()
        
        left_msg = self.create_range_msg(now, 'left_front_link')
        right_msg = self.create_range_msg(now, 'right_front_link')
        
        self.left_pub.publish(left_msg)
        self.right_pub.publish(right_msg)

    def create_range_msg(self, stamp, frame_id):
        msg = Range()
        msg.header.stamp = stamp
        msg.header.frame_id = frame_id
        msg.radiation_type = Range.INFRARED
        msg.field_of_view = 0.03
        msg.min_range = self.min_range
        msg.max_range = self.max_range
        msg.range = random.uniform(self.min_range, self.max_range)
        return msg

def main(args=None):
    rclpy.init(args=args)
    node = DToFLidarSimulator()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

