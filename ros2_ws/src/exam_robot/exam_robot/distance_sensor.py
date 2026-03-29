import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class DistanceSensor(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        self.publisher_ = self.create_publisher(Float32, 'distance', 10)
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 10)
        
        self.distance = 3.0
        self.current_linear_x = 0.0
        
        self.timer = self.create_timer(0.2, self.timer_callback)

    def cmd_callback(self, msg):
        self.current_linear_x = msg.linear.x

    def timer_callback(self):
        if self.current_linear_x == 0.0:
            self.distance = 3.0
        elif self.current_linear_x > 0.0:
            self.distance = max(0.5, self.distance - 0.2)
        elif self.current_linear_x < 0.0:
            self.distance = min(3.0, self.distance + 0.2)

        msg = Float32()
        msg.data = float(self.distance)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

