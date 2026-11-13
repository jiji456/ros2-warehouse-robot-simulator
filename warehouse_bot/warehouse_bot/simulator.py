"""Task execution loop and JSON-friendly simulation telemetry."""

from datetime import datetime, timezone
from typing import Iterable, Optional

from warehouse_bot.models import Point, Task
from warehouse_bot.planner import shortest_path
from warehouse_bot.world import GridWorld


class WarehouseSimulator:
    def __init__(
        self,
        world: Optional[GridWorld] = None,
        start: Point = Point(1, 1),
        tasks: Optional[Iterable[Task]] = None,
    ) -> None:
        self.world = world or default_world()
        if self.world.is_blocked(start):
            raise ValueError('Robot start must be a free cell')
        self.position = start
        self.tasks = list(tasks) if tasks is not None else default_tasks()
        self.task_index = 0
        self.waypoint_index = 0
        self.sequence = 0
        for task in self.tasks:
            for waypoint in task.waypoints:
                if self.world.is_blocked(waypoint):
                    raise ValueError(f'Task waypoint is not traversable: {waypoint}')

    @property
    def finished(self) -> bool:
        return self.task_index >= len(self.tasks)

    def step(self) -> dict:
        """Advance one grid cell and return one telemetry event."""
        task = self._current_task()
        if task is None:
            return self._event('idle', None, 'No pending tasks')

        target = task.waypoints[self.waypoint_index]
        if self.position == target:
            self.waypoint_index += 1
            if self.waypoint_index == len(task.waypoints):
                self.task_index += 1
                self.waypoint_index = 0
                return self._event('task_completed', None, f'Task {task.task_id} completed')
            return self._event(
                'waypoint_reached',
                task.waypoints[self.waypoint_index],
                'Pickup reached; continuing to drop-off',
            )

        path = shortest_path(self.world, self.position, target)
        if path is None:
            return self._event('blocked', target, 'No safe path to target')
        next_position = path[1]

        # This simulation check is not a safety-rated collision-prevention system.
        if self.world.is_blocked(next_position):
            return self._event('blocked', target, 'Obstacle detected; replanning on next step')
        self.position = next_position
        return self._event('moving', target, f'Moved to {self.position.x},{self.position.y}')

    def _current_task(self) -> Optional[Task]:
        return None if self.finished else self.tasks[self.task_index]

    def _event(self, status: str, target: Optional[Point], detail: str) -> dict:
        self.sequence += 1
        task = self._current_task()
        return {
            'sequence': self.sequence,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'position': self.position.as_list(),
            'task_id': task.task_id if task else None,
            'status': status,
            'target': target.as_list() if target else None,
            'sensors': self.world.sensor_readings(self.position).as_dict(),
            'detail': detail,
        }


def default_world() -> GridWorld:
    obstacles = [Point(5, y) for y in range(8) if y != 3]
    obstacles += [Point(3, 4), Point(4, 4), Point(8, 2), Point(8, 3)]
    return GridWorld(width=12, height=8, obstacles=obstacles)


def default_tasks() -> list[Task]:
    return [Task('order-001', pickup=Point(9, 1), dropoff=Point(9, 6))]
