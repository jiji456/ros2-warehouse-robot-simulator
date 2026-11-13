const $ = (id) => document.getElementById(id);
const mapElement = $('warehouseMap');
let running = false;
let timer = null;
let state = null;

async function request(path, method = 'GET') {
  const response = await fetch(path, { method, headers: { 'Accept': 'application/json' } });
  const body = await response.json();
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`);
  return body;
}

function pointKey(point) { return `${point[0]},${point[1]}`; }

function renderMap(data) {
  const obstacleSet = new Set(data.obstacles.map(pointKey));
  const routeSet = new Set(data.path.map(pointKey));
  const robotKey = pointKey(data.position);
  const targetKey = data.target ? pointKey(data.target) : null;
  mapElement.style.setProperty('--columns', data.width);
  mapElement.replaceChildren();

  for (let y = data.height - 1; y >= 0; y -= 1) {
    for (let x = 0; x < data.width; x += 1) {
      const key = `${x},${y}`;
      const cell = document.createElement('div');
      cell.className = 'map-cell';
      cell.setAttribute('aria-label', `Cell ${x}, ${y}`);
      if (obstacleSet.has(key)) {
        cell.classList.add('obstacle-cell');
        cell.innerHTML = '<span class="rack-lines" aria-hidden="true"></span>';
      } else if (key === robotKey) {
        cell.classList.add('robot-cell');
        cell.innerHTML = '<span class="robot-icon" aria-hidden="true">↗</span>';
        cell.setAttribute('aria-label', `Robot at ${x}, ${y}`);
      } else if (key === targetKey) {
        cell.classList.add('target-cell');
        cell.innerHTML = `<span>${data.waypoint_index === 0 ? 'A' : 'B'}</span>`;
        cell.setAttribute('aria-label', `Current target at ${x}, ${y}`);
      } else if (routeSet.has(key)) {
        cell.classList.add('route-cell');
        cell.innerHTML = '<span aria-hidden="true"></span>';
      }
      mapElement.appendChild(cell);
    }
  }
  $('mapDimensions').innerHTML = `${data.width} × ${data.height} <span>GRID</span>`;
}

function render(data) {
  state = data;
  renderMap(data);
  const [x, y] = data.position;
  $('positionMetric').textContent = `${String(x).padStart(2, '0')}, ${String(y).padStart(2, '0')}`;
  $('coordinates').textContent = `X ${String(x).padStart(2, '0')}   Y ${String(y).padStart(2, '0')}`;
  $('taskId').textContent = data.task_id || 'MISSION COMPLETE';
  $('taskMetric').textContent = data.task_id || 'DONE';
  $('taskSubmetric').textContent = data.task_id ? 'PICKUP → DROP-OFF' : 'ALL TASKS COMPLETE';
  const sensors = data.sensors;
  for (const direction of ['north', 'east', 'south', 'west']) {
    const value = sensors[direction];
    $(`sensor${direction[0].toUpperCase()}${direction.slice(1)}`).textContent = value === null ? '—' : value;
  }

  const completedWaypoints = data.finished ? 2 : data.task_index * 2 + data.waypoint_index;
  $('progressText').textContent = `${completedWaypoints} / ${data.task_count * 2} WAYPOINTS`;
  $('progressBar').style.width = `${Math.min(100, completedWaypoints / Math.max(1, data.task_count * 2) * 100)}%`;
  $('pickupState').textContent = completedWaypoints >= 1 ? 'DONE' : 'PENDING';
  $('dropoffState').textContent = completedWaypoints >= 2 ? 'DONE' : 'PENDING';
  $('pickupWaypoint').classList.toggle('completed', completedWaypoints >= 1);
  $('dropoffWaypoint').classList.toggle('completed', completedWaypoints >= 2);

  const status = data.finished ? 'COMPLETE' : (data.event.status || 'READY').replaceAll('_', ' ').toUpperCase();
  $('statusPill').innerHTML = `<i></i> ${status}`;
  $('statusPill').classList.toggle('complete', data.finished);
  $('eventCount').textContent = `EVENT ${String(data.event.sequence || 0).padStart(3, '0')}`;
  $('eventStatus').textContent = status;
  $('eventDetail').textContent = data.event.detail || 'Ready to start simulation';
  $('eventTime').textContent = data.event.timestamp ? new Date(data.event.timestamp).toLocaleTimeString() : '--:--:--';
  $('eventIndicator').classList.toggle('active', !data.finished && data.event.status === 'moving');
  $('stepButton').disabled = data.finished || running;
  $('runButton').disabled = data.finished && !running;
  $('runButton').innerHTML = running ? '<span aria-hidden="true">Ⅱ</span> Pause mission' : (data.finished ? '<span aria-hidden="true">✓</span> Mission complete' : '<span aria-hidden="true">▶</span> Start mission');
}

async function refresh() {
  try { render(await request('/api/state')); }
  catch (error) { showError(error); }
}

function showError(error) {
  $('eventStatus').textContent = 'API ERROR';
  $('eventDetail').textContent = error.message;
  $('eventIndicator').classList.remove('active');
  stop();
}

async function advance() {
  try {
    const next = await request('/api/step', 'POST');
    render(next);
    if (next.finished) stop();
  } catch (error) { showError(error); }
}

function stop() {
  running = false;
  if (timer) window.clearInterval(timer);
  timer = null;
  if (state) render(state);
}

$('runButton').addEventListener('click', () => {
  if (running) { stop(); return; }
  if (state?.finished) return;
  running = true;
  render(state);
  timer = window.setInterval(advance, 450);
});
$('stepButton').addEventListener('click', advance);
$('resetButton').addEventListener('click', async () => {
  stop();
  try { render(await request('/api/reset', 'POST')); }
  catch (error) { showError(error); }
});
refresh();
