import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Импортируем тип сообщения


class Trafic(Node):
    def __init__(self):
        super().__init__('trafic_light')
        self.publisher_ = self.create_publisher(
            String,
            'traffic_light',
            10
        )
        self.timer = self.create_timer(3.0, self.trafic_light)
        self.count = 0
    
    def trafic_light(self):
        msg = String()
        if self.count == 0:
            msg.data = "RED"
            self.count += 1
        elif self.count == 1:
            msg.data = "YELLOW"
            self.count += 1
        elif self.count == 2:
            msg.data = "GREEN"
            self.count = 0
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Trafic()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
