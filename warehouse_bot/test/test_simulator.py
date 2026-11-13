import unittest

from warehouse_bot.models import Point, Task
from warehouse_bot.planner import shortest_path
from warehouse_bot.simulator import WarehouseSimulator
from warehouse_bot.world import GridWorld


class PlannerTests(unittest.TestCase):
    def test_path_avoids_obstacles(self):
        world = GridWorld(5, 5, [Point(2, 1), Point(2, 2), Point(2, 3)])
        path = shortest_path(world, Point(0, 2), Point(4, 2))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], Point(0, 2))
        self.assertEqual(path[-1], Point(4, 2))
        self.assertTrue(all(not world.is_blocked(point) for point in path))

    def test_no_path_when_goal_is_blocked(self):
        world = GridWorld(3, 3, [Point(2, 2)])
        self.assertIsNone(shortest_path(world, Point(0, 0), Point(2, 2)))


class SimulatorTests(unittest.TestCase):
    def test_default_mission_completes(self):
        simulator = WarehouseSimulator()
        statuses = []
        for _ in range(200):
            event = simulator.step()
            statuses.append(event['status'])
            if simulator.finished:
                break
        self.assertTrue(simulator.finished)
        self.assertIn('task_completed', statuses)
        self.assertEqual(simulator.position, Point(9, 6))

    def test_replans_around_new_obstacle(self):
        world = GridWorld(5, 3)
        task = Task('dynamic', pickup=Point(3, 1), dropoff=Point(4, 1))
        simulator = WarehouseSimulator(world, Point(0, 1), [task])
        simulator.step()
        world.add_obstacle(Point(2, 1))
        event = simulator.step()
        self.assertNotEqual(simulator.position, Point(2, 1))
        self.assertEqual(event['status'], 'moving')

    def test_sensor_reports_wall_and_boundary(self):
        world = GridWorld(3, 3, [Point(1, 2)])
        readings = world.sensor_readings(Point(1, 1), max_range=3)
        self.assertEqual(readings.north, 0)
        self.assertEqual(readings.east, 1)

    def test_rejects_blocked_start(self):
        world = GridWorld(3, 3, [Point(0, 0)])
        with self.assertRaises(ValueError):
            WarehouseSimulator(world, Point(0, 0), [])


if __name__ == '__main__':
    unittest.main()
