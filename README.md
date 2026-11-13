# ROS 2 Warehouse Robot Simulator

A portfolio project demonstrating a small autonomous warehouse-robot workflow: navigate a grid-based warehouse, reach a pickup point, deliver an item to a drop-off point, and publish structured telemetry. The simulation core is written in Python and can run without ROS 2; an optional ROS 2 node publishes simulator events for inspection.

> **Scope and safety:** This is an educational software simulation, not a production robotics stack. It does not control motors or physical equipment, and its simulated sensors and obstacle checks are not safety-rated. See [Safety and limitations](docs/safety.md).

## What it demonstrates

- **Robot behavior:** step-based navigation through a configurable warehouse grid.
- **Path planning:** breadth-first search (BFS) for shortest paths on a four-connected grid; replanning on each step allows the simulation to respond to map changes.
- **Task execution:** pickup and drop-off waypoints with task status transitions.
- **Sensor simulation:** idealized cardinal range readings for nearby obstacles and boundaries.
- **Telemetry:** timestamped JSON events written to the terminal or a JSON Lines file.
- **ROS 2 integration:** optional `rclpy` node publishing telemetry on `/warehouse/telemetry` as `std_msgs/msg/String`.
- **Quality practices:** ROS-independent core logic and Python unit tests.

## Architecture

```text
GridWorld + simulated range sensors
              ↓
WarehouseSimulator ──→ BFS path planner
        │
        ├── CLI → stdout / JSONL file
        └── ROS 2 adapter → /warehouse/telemetry
```

The simulator and planner do not depend on ROS 2, which makes the core logic easier to run and test. Read the [architecture notes](docs/architecture.md) for the runtime flow and telemetry fields.

## Quick start (Python only)

Python 3.9 or later is recommended. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ./warehouse_bot
warehouse-sim
```

Save telemetry to a JSON Lines file:

```bash
warehouse-sim --jsonl telemetry.jsonl
```

Limit the simulation run:

```bash
warehouse-sim --max-steps 100
```

Each telemetry record includes `sequence`, `timestamp`, `position`, `task_id`, `status`, `target`, `sensors`, and `detail`.

## Run with ROS 2

Install a ROS 2 distribution supported by your operating system, including `rclpy`, `std_msgs`, `ament_python`, `colcon`, and the ROS 2 launch packages. Then run from the repository root:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch warehouse_bot simulation.launch.py
```

In another terminal, source the ROS 2 and workspace setup files, then inspect the topic:

```bash
ros2 topic echo /warehouse/telemetry
```

The ROS 2 adapter publishes simulation state only. It does not subscribe to motion commands or control hardware.

## Run tests

```bash
python -m unittest discover -s warehouse_bot/test -v
```

The tests cover path planning around obstacles, blocked destinations, dynamic obstacle replanning, simulated sensor readings, mission completion, and invalid start positions.

## Repository structure

```text
warehouse_bot/
├── launch/                 # ROS 2 launch entry point
├── resource/               # ament package marker
├── test/                   # standard-library unit tests
├── warehouse_bot/
│   ├── cli.py               # standalone command-line runner
│   ├── models.py            # points, tasks, and sensor readings
│   ├── planner.py           # BFS shortest-path planner
│   ├── ros_node.py          # ROS 2 telemetry publisher
│   ├── simulator.py         # task execution and event generation
│   └── world.py             # grid and simulated sensors
├── package.xml
└── setup.py

docs/
├── architecture.md
├── portfolio-copy.md        # LinkedIn and résumé-ready project description
└── safety.md
```

## Possible next steps

- Add a visualizer for the grid, robot pose, route, and task state.
- Add configurable maps and task lists rather than fixed example data.
- Add ROS 2 integration tests and continuous integration.
- Extend the simulation with noisy sensors, localization uncertainty, and more realistic robot motion—while keeping safety-critical behavior outside this educational prototype.

## Skills shown

Python · ROS 2 (`rclpy`) · BFS path planning · robotics simulation · sensor modeling · task-state logic · JSON telemetry · unit testing · technical documentation
