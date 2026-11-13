"""Grid map and idealized simulated range sensors."""

from typing import Iterable, Optional

from warehouse_bot.models import Point, SensorReadings


class GridWorld:
    def __init__(self, width: int, height: int, obstacles: Iterable[Point] = ()) -> None:
        if width <= 0 or height <= 0:
            raise ValueError('World dimensions must be positive')
        self.width = width
        self.height = height
        self.obstacles = set(obstacles)
        for obstacle in self.obstacles:
            if not self.in_bounds(obstacle):
                raise ValueError(f'Obstacle outside world: {obstacle}')

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def is_blocked(self, point: Point) -> bool:
        return not self.in_bounds(point) or point in self.obstacles

    def add_obstacle(self, point: Point) -> None:
        if not self.in_bounds(point):
            raise ValueError(f'Obstacle outside world: {point}')
        self.obstacles.add(point)

    def sensor_readings(self, origin: Point, max_range: int = 5) -> SensorReadings:
        """Return free cells to the nearest obstacle or boundary per direction.

        Zero means the adjacent cell is blocked. None means nothing was detected
        within range. Distances are measured in grid cells.
        """
        if max_range < 0:
            raise ValueError('Sensor range cannot be negative')
        directions = {
            'north': (0, 1),
            'east': (1, 0),
            'south': (0, -1),
            'west': (-1, 0),
        }
        readings = {}
        for name, (dx, dy) in directions.items():
            distance: Optional[int] = None
            for offset in range(1, max_range + 1):
                point = Point(origin.x + dx * offset, origin.y + dy * offset)
                if self.is_blocked(point):
                    distance = offset - 1
                    break
            readings[name] = distance
        return SensorReadings(**readings)
