import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool

class TemperatureSensor(Node):
    def __init__(self):
        super().__init__('temperature_sensor')
        self.current_temp = 25.0
        self.is_moving = False

        self.temp_pub = self.create_publisher(Float32, '/temperature', 10)
        self.motor_sub = self.create_subscription(Bool, '/motor_state', self.motor_callback, 10)
        self.timer = self.create_timer(2.0, self.update_temperature)

    def motor_callback(self, msg):
        self.is_moving = msg.data

    def update_temperature(self):
        if self.is_moving:
            self.current_temp += 2.0
        else:
            self.current_temp -= 1.0

        self.current_temp = max(25.0, min(80.0, self.current_temp))

        msg = Float32()
        msg.data = self.current_temp
        self.temp_pub.publish(msg)

        if self.current_temp > 70.0:
            self.get_logger().warning(f'ВНИМАНИЕ: Перегрев! Температура: {self.current_temp}°C')
        else:
            self.get_logger().info(f'Температура: {self.current_temp}°C')

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSensor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
