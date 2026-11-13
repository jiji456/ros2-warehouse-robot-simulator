"""Shared, ROS-independent data models for the simulator."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def as_list(self) -> list[int]:
        return [self.x, self.y]


@dataclass(frozen=True)
class Task:
    task_id: str
    pickup: Point
    dropoff: Point

    @property
    def waypoints(self) -> Tuple[Point, Point]:
        return (self.pickup, self.dropoff)


@dataclass(frozen=True)
class SensorReadings:
    north: Optional[int]
    east: Optional[int]
    south: Optional[int]
    west: Optional[int]

    def as_dict(self) -> dict[str, Optional[int]]:
        return {
            'north': self.north,
            'east': self.east,
            'south': self.south,
            'west': self.west,
        }
