from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='warehouse_bot',
            executable='warehouse-ros',
            name='warehouse_simulator',
            output='screen',
            parameters=[{'step_period_sec': 0.5}],
        ),
    ])
