# Project memory

## Product intent & audience

- Project includes a simulator and a web dashboard for interacting with it
- Dashboard provides controls: start, step, reset for running simulations
- Target users likely developers/engineers using a Python-based simulation environment

## Brand personality & voice

- Insufficient context to infer; default to clear, technical, concise communication

## Visual design & UX direction

- Dashboard has a home page with simulation control buttons (start, step, reset)
- Includes a client-side script file
- Backend exposes API endpoints serving the dashboard page and control actions

## Decisions, constraints & rationale

- Python environment; pip installed for package management
- Dashboard dependencies installed in environment only; no project files modified
- In-process API testing used because live server/browser cannot be started in this environment
- Visual verification deferred to preview

## Open questions & assumptions

- Specific simulator package/framework not identified
- Exact dependency list unknown
- Visual appearance of dashboard not yet verified
- Whether project files need pip integration (e.g., requirements.txt) is unresolved
- User occasionally writes in Thai; primary working language appears to be English