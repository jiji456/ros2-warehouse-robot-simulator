# Architecture

## Runtime flow

1. `GridWorld` stores traversable cells and obstacles and produces idealized four-direction sensor readings.
2. `WarehouseSimulator` selects the active task waypoint (pickup, then drop-off) and requests a route at each step.
3. `shortest_path` uses breadth-first search over four-connected cells. Replanning each step lets the simulator react to map changes between steps.
4. The simulator checks that the next cell is still traversable, moves one cell, and emits a telemetry event.
5. The CLI writes JSON Lines to stdout or a file. The optional ROS 2 node publishes the same event shape to `/warehouse/telemetry`.

## Telemetry fields

`sequence`, `timestamp`, `position`, `task_id`, `status`, `target`, `sensors`, and `detail`.

The core is ROS-independent, so task and planning logic can be tested using standard Python. ROS 2 is an adapter for publishing state, not a hardware-control layer.
