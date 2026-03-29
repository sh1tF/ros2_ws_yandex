import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        self.subscription = self.create_subscription(String, 'robot_status', self.status_callback, 10)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.current_status = "UNKNOWN"
        self.timer = self.create_timer(0.1, self.timer_callback)

    def status_callback(self, msg):
        if msg.data != self.current_status:
            self.get_logger().info(f'Switching mode to: {msg.data}')
            self.current_status = msg.data

    def timer_callback(self):
        cmd = Twist()
        
        if self.current_status == "ALL OK":
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
        elif self.current_status == "WARNING: Low battery":
            cmd.linear.x = 0.1
            cmd.angular.z = 0.0
        elif self.current_status == "WARNING: Obstacle close":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        elif self.current_status == "CRITICAL":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

