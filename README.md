# ROS 2 Warehouse Robot Simulator

A portfolio project demonstrating a small autonomous warehouse-robot workflow: navigate a grid-based warehouse, reach a pickup point, deliver an item to a drop-off point, and publish structured telemetry.

> **Scope and safety:** This is an educational software simulation, not a production robotics stack. It does not control motors or physical equipment, and its simulated sensors and obstacle checks are not safety-rated.

## What it demonstrates

- **Robot behavior:** step-based navigation through a configurable warehouse grid.
- **Path planning:** breadth-first search (BFS) for shortest paths on a four-connected grid; replanning on each step allows the simulation to respond to map changes.
- **Task execution:** pickup and drop-off waypoints with task status transitions.
- **Sensor simulation:** idealized cardinal range readings for nearby obstacles and boundaries.
- **Telemetry:** timestamped JSON events written to the terminal or a JSON Lines file.
- **Web dashboard:** interactive floor map, robot route, mission progress, sensor readings, and controls to run, single-step, pause, or reset the simulation.
- **ROS 2 integration:** optional `rclpy` node publishing telemetry on `/warehouse/telemetry` as `std_msgs/msg/String`.
- **Quality practices:** ROS-independent core logic and Python unit tests.

## Architecture

```text
GridWorld + simulated range sensors
              ↓
WarehouseSimulator ──→ BFS path planner
        │                        │
        ├── CLI → stdout / JSONL │
        ├── FastAPI → browser dashboard
        └── ROS 2 adapter → /warehouse/telemetry
```

The simulator and planner do not depend on ROS 2, which makes the core logic easier to run and test. Read the [architecture notes](docs/architecture.md) for the runtime flow and telemetry fields.

## Quick start (Python CLI)

Python 3.9 or later is recommended. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ./warehouse_bot
warehouse-sim
```

## Interactive web dashboard

Install the web API dependencies and launch the local dashboard:

```bash
python -m pip install -e ./warehouse_bot
python -m pip install -r web_dashboard/requirements.txt
uvicorn app:app --app-dir web_dashboard --reload
```

Open <http://127.0.0.1:8000>. Use **Start mission** to animate the robot, **Step** to advance one simulation tick, **Pause mission** to pause, or the reset icon to restart. The dashboard API docs are available at <http://127.0.0.1:8000/docs>.

The dashboard is a local demo interface; do not expose its API to untrusted networks or connect it to physical robot controls. See [dashboard setup and limitations](web_dashboard/README.md).

### Run the dashboard on Replit

The web dashboard can run on Replit without ROS 2. Import this GitHub repository into Replit, then configure the Replit workflow or deployment to use the repository root as the working directory.

Install the simulator package and dashboard dependencies as the build/install command:

```bash
python -m pip install -e ./warehouse_bot
python -m pip install -r web_dashboard/requirements.txt
```

Use this as the run command. Replit provides the `PORT` environment variable; bind Uvicorn to `0.0.0.0` so the web preview/deployment can reach the app:

```bash
uvicorn app:app --app-dir web_dashboard --host 0.0.0.0 --port ${PORT:-8000}
```

If configuring a `.replit` file, the run command can be set like this:

```toml
run = "uvicorn app:app --app-dir web_dashboard --host 0.0.0.0 --port ${PORT:-8000}"
```

Open the web preview or published app URL after the server starts. ROS 2 is not required for the dashboard; the ROS 2 node is a separate optional runtime. The dashboard API is intended for demos—do not expose it to untrusted users or connect it to physical robot controls.

Save CLI telemetry to a JSON Lines file with `warehouse-sim --jsonl telemetry.jsonl`, or limit the run with `warehouse-sim --max-steps 100`. Each telemetry record includes `sequence`, `timestamp`, `position`, `task_id`, `status`, `target`, `sensors`, and `detail`.

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
warehouse_bot/              # ROS 2 package and simulator core
web_dashboard/               # FastAPI API and browser dashboard
├── app.py
├── requirements.txt
└── static/                   # HTML, CSS, JavaScript UI

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

Python · ROS 2 (`rclpy`) · FastAPI · JavaScript · HTML/CSS · BFS path planning · robotics simulation · sensor modeling · task-state logic · JSON telemetry · unit testing · technical documentation
