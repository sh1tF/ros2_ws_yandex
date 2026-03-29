import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

class ToFSimulator(Node):
    def __init__(self):
        super().__init__('tof_simulator')
        self.dist_left = 1.5
        self.dist_right = 1.5
        
        self.left_pub = self.create_publisher(Range, '/tof/left', 10)
        self.right_pub = self.create_publisher(Range, '/tof/right', 10)
        
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.timer = self.create_timer(0.02, self.publish_ranges)

    def cmd_vel_callback(self, msg):
        self.dist_left -= (msg.linear.x + msg.angular.z) * 0.02
        self.dist_right -= (msg.linear.x - msg.angular.z) * 0.02
        
        self.dist_left = max(0.03, min(2.0, self.dist_left))
        self.dist_right = max(0.03, min(2.0, self.dist_right))

    def publish_ranges(self):
        t = self.get_clock().now().to_msg()
        self.left_pub.publish(self.make_msg(t, 'tof_left', self.dist_left))
        self.right_pub.publish(self.make_msg(t, 'tof_right', self.dist_right))

    def make_msg(self, t, frame, val):
        m = Range()
        m.header.stamp = t
        m.header.frame_id = frame
        m.radiation_type = 1
        m.field_of_view = 0.44
        m.min_range = 0.03
        m.max_range = 2.0
        m.range = float(val)
        return m

def main(args=None):
    rclpy.init(args=args)
    n = ToFSimulator()
    rclpy.spin(n)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

