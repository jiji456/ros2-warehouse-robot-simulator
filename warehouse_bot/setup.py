from setuptools import find_packages, setup

package_name = 'warehouse_bot'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=('test',)),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/simulation.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jiji456',
    maintainer_email='maintainer@example.com',
    description='ROS 2 warehouse robot simulator with path planning and telemetry',
    license='MIT',
    tests_require=['setuptools'],
    entry_points={
        'console_scripts': [
            'warehouse-sim = warehouse_bot.cli:main',
            'warehouse-ros = warehouse_bot.ros_node:main',
        ],
    },
)
