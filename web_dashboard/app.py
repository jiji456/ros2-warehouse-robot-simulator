"""Local web API and dashboard for the warehouse robot simulator."""

from pathlib import Path
import sys
import threading
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Support running from a source checkout without requiring an editable install.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / 'warehouse_bot'))

from warehouse_bot.models import Point  # noqa: E402
from warehouse_bot.planner import shortest_path  # noqa: E402
from warehouse_bot.simulator import WarehouseSimulator  # noqa: E402

WEB_DIR = Path(__file__).resolve().parent
app = FastAPI(title='Warehouse Robot Simulator API', version='1.0.0')
app.mount('/static', StaticFiles(directory=WEB_DIR / 'static'), name='static')
_simulator = WarehouseSimulator()
_last_event: dict[str, Any] = {
    'sequence': 0,
    'status': 'ready',
    'detail': 'Ready to start simulation',
}
_lock = threading.Lock()


@app.get('/', include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(WEB_DIR / 'static' / 'index.html')


def _state() -> dict[str, Any]:
    task = _simulator._current_task()
    target = task.waypoints[_simulator.waypoint_index] if task else None
    path = shortest_path(_simulator.world, _simulator.position, target) if target else None
    return {
        'width': _simulator.world.width,
        'height': _simulator.world.height,
        'position': _simulator.position.as_list(),
        'obstacles': [point.as_list() for point in sorted(_simulator.world.obstacles)],
        'target': target.as_list() if target else None,
        'path': [point.as_list() for point in path] if path else [],
        'task_id': task.task_id if task else None,
        'task_index': _simulator.task_index,
        'task_count': len(_simulator.tasks),
        'waypoint_index': _simulator.waypoint_index,
        'finished': _simulator.finished,
        'sensors': _simulator.world.sensor_readings(_simulator.position).as_dict(),
        'event': dict(_last_event),
    }


@app.get('/api/state')
def get_state() -> dict[str, Any]:
    with _lock:
        return _state()


@app.post('/api/step')
def step_simulation() -> dict[str, Any]:
    global _last_event
    with _lock:
        if _simulator.finished:
            raise HTTPException(status_code=409, detail='Mission is complete. Reset to run it again.')
        _last_event = _simulator.step()
        return _state()


@app.post('/api/reset')
def reset_simulation() -> dict[str, Any]:
    global _simulator, _last_event
    with _lock:
        _simulator = WarehouseSimulator()
        _last_event = {
            'sequence': 0,
            'status': 'ready',
            'detail': 'Simulation reset and ready',
        }
        return _state()
