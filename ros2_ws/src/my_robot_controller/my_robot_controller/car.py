import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Car(Node): 
    def __init__(self):
        super().__init__('car')
        
        # Создаём Subscriber
        self.subscriber_ = self.create_subscription(
            String,                    # тип сообщения
            'traffic_light',              # имя топика
            self.callback,        # функция обработки
            10                         # размер очереди
        )
    def callback(self, msg):
        if msg.data == "RED":
            self.get_logger().info("Остановка!")
        elif msg.data == "YELLOW":
            self.get_logger().info("Замедляюсь...")
        elif msg.data == "GREEN":
            self.get_logger().info("Еду!")

def main(args=None):
    rclpy.init(args=args)
    node = Car()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
