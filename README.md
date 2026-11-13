# ROS 2 Warehouse Robot Simulator

A safety-conscious portfolio project that simulates a warehouse robot using a grid map, simulated range sensors, breadth-first path planning, pickup/drop-off tasks, and JSON telemetry. Its core runs with ordinary Python; an optional ROS 2 node publishes telemetry.

> **Simulation only.** This software does not control physical robots or safety-rated equipment. Do not connect it to hardware without qualified engineering review and validated, hardware-specific safeguards.

## Features

- Configurable grid world with obstacles and simulated cardinal range sensors.
- Shortest-path planning with replanning on each step.
- Pickup and drop-off task execution.
- JSON Lines telemetry to stdout or a file.
- Optional ROS 2 telemetry publisher on `/warehouse/telemetry` (`std_msgs/msg/String`).
- Unit tests using Python's standard library.

## Run with Python (no ROS 2 required)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ./warehouse_bot
warehouse-sim
```

Save telemetry to a file:

```bash
warehouse-sim --jsonl telemetry.jsonl
```

Limit the run with `warehouse-sim --max-steps 100`. Each JSON event includes a sequence number, timestamp, robot position, task status, target waypoint, sensor readings, and detail.

## Run with ROS 2

Install a ROS 2 distribution supported by your operating system, including `rclpy`, `std_msgs`, `ament_python`, `colcon`, and the ROS 2 launch packages. Then, from the repository root:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch warehouse_bot simulation.launch.py
```

In another terminal, source the ROS 2 and workspace setup files, then inspect telemetry:

```bash
ros2 topic echo /warehouse/telemetry
```

The ROS node publishes simulation state only. It does not subscribe to motion commands or drive hardware.

## Tests

```bash
python -m unittest discover -s warehouse_bot/test -v
```

## Project layout

- `warehouse_bot/warehouse_bot/`: simulator, map, planner, CLI, and ROS 2 adapter.
- `warehouse_bot/launch/`: ROS 2 launch file.
- `warehouse_bot/test/`: unit tests.
- `docs/architecture.md`: architecture and telemetry format.
- `docs/safety.md`: scope and safety limitations.
