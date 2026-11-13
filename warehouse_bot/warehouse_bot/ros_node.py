"""ROS 2 adapter that publishes simulator telemetry; it does not control hardware."""

import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from warehouse_bot.simulator import WarehouseSimulator


class WarehouseSimulatorNode(Node):
    def __init__(self) -> None:
        super().__init__('warehouse_simulator')
        self.declare_parameter('step_period_sec', 0.5)
        period = float(self.get_parameter('step_period_sec').value)
        if period <= 0:
            raise ValueError('step_period_sec must be positive')
        self.simulator = WarehouseSimulator()
        self.publisher = self.create_publisher(String, '/warehouse/telemetry', 10)
        self.timer = self.create_timer(period, self.publish_step)
        self.get_logger().info('Simulation started; publishing /warehouse/telemetry')

    def publish_step(self) -> None:
        event = self.simulator.step()
        message = String()
        message.data = json.dumps(event, sort_keys=True)
        self.publisher.publish(message)
        if event['status'] == 'task_completed':
            self.get_logger().info(event['detail'])
        if self.simulator.finished:
            self.timer.cancel()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = WarehouseSimulatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
