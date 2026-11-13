# Web dashboard

The dashboard is a local browser UI for the simulator. It shows the warehouse map, robot position and route, mission waypoint progress, simulated range sensors, and the latest event. Start/pause, single-step, and reset controls call a small FastAPI backend, which advances the same Python `WarehouseSimulator` used by the CLI.

## Run locally

From the repository root, install the simulator package and dashboard dependencies:

```bash
python -m pip install -e ./warehouse_bot
python -m pip install -r web_dashboard/requirements.txt
uvicorn app:app --app-dir web_dashboard --reload
```

Open <http://127.0.0.1:8000>. The API documentation is available at <http://127.0.0.1:8000/docs>.

The API is intended for local demos. Do not expose it to an untrusted network or connect it to physical robot controls. See [safety notes](../docs/safety.md).
