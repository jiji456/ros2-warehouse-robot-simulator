# Project memory

## Product intent & audience

- Project includes a Python-based warehouse simulator and a web dashboard for interacting with it
- Dashboard provides controls: start, step, reset for running simulations
- Simulator involves a warehouse map/grid (logistics domain)
- Target users likely developers/engineers using a Python-based simulation environment

## Brand personality & voice

- Insufficient context to infer; default to clear, technical, concise communication
- User communicates in Thai; respond in Thai when user writes in Thai

## Visual design & UX direction

- Dashboard has a home page with simulation control buttons (start, step, reset)
- Includes a warehouse map visualization
- Includes a client-side script file
- Backend exposes API endpoints serving the dashboard page and control actions

## Decisions, constraints & rationale

- Python environment; pip installed for package management
- Backend framework: FastAPI
- Dashboard dependencies installed in environment only; no project files modified
- In-process API testing used because live server/browser cannot be started in this environment
- Bolt preview only supports JavaScript apps (React/Vite); Python servers cannot be previewed — this is a platform limitation, not a project defect

## Open questions & assumptions

- Whether to rewrite the dashboard as a JavaScript app (e.g. React/Vite) to enable Bolt preview, or keep Python and run dashboard locally — decision pending
- If rewriting in JS, simulator logic would need to be reimplemented or kept in sync between Python and JS
- Specific simulator package/framework not identified
- Whether project files need pip integration (e.g., requirements.txt) is unresolved
- Visual appearance of dashboard not yet verified