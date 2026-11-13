"""Breadth-first shortest-path planner for a four-connected grid."""

from collections import deque
from typing import Dict, List, Optional

from warehouse_bot.models import Point
from warehouse_bot.world import GridWorld


DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def shortest_path(world: GridWorld, start: Point, goal: Point) -> Optional[List[Point]]:
    """Return a path including start and goal, or None when no route exists."""
    if world.is_blocked(start) or world.is_blocked(goal):
        return None
    if start == goal:
        return [start]

    queue = deque([start])
    previous: Dict[Point, Optional[Point]] = {start: None}
    while queue:
        current = queue.popleft()
        for dx, dy in DIRECTIONS:
            neighbor = Point(current.x + dx, current.y + dy)
            if world.is_blocked(neighbor) or neighbor in previous:
                continue
            previous[neighbor] = current
            if neighbor == goal:
                path = [goal]
                cursor = current
                while cursor is not None:
                    path.append(cursor)
                    cursor = previous[cursor]
                path.reverse()
                return path
            queue.append(neighbor)
    return None
