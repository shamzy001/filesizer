## ADDED Requirements

### Requirement: Start local HTTP server and open browser
The system SHALL start a FastAPI/uvicorn server on `127.0.0.1` at a configurable port (default 8765) and automatically open the browser to the served UI when launched via the `filesizer` CLI command.

#### Scenario: Default launch
- **WHEN** the user runs `filesizer` with no arguments
- **THEN** the server starts on port 8765, the browser opens to `http://127.0.0.1:8765`, and a directory picker is shown in the UI

#### Scenario: Launch with path argument
- **WHEN** the user runs `filesizer /some/path`
- **THEN** the server starts and the browser opens directly to the scan view for that path

#### Scenario: Port already in use
- **WHEN** port 8765 is already occupied
- **THEN** the server tries the next available port and prints the chosen port to stdout

### Requirement: Expose REST API for directory scanning
The server SHALL expose a `GET /api/scan` endpoint that accepts a `path` query parameter and returns the directory tree as JSON.

#### Scenario: Valid path scan
- **WHEN** `GET /api/scan?path=/home/user/docs` is called
- **THEN** the server returns HTTP 200 with a JSON body matching the directory-scanner output structure

#### Scenario: Invalid or non-existent path
- **WHEN** the path does not exist or is not a directory
- **THEN** the server returns HTTP 400 with an error message

#### Scenario: Depth-limited scan via query param
- **WHEN** `GET /api/scan?path=/home/user&depth=2` is called
- **THEN** the server returns the tree limited to 2 levels deep

### Requirement: Expose REST API for file operations
The server SHALL expose `POST /api/delete` and `POST /api/move` endpoints that accept JSON bodies and delegate to the file-operations module.

#### Scenario: Delete endpoint delegates correctly
- **WHEN** `POST /api/delete` is called with `{"path": "..."}` 
- **THEN** the server delegates to the file-operations delete logic and returns the appropriate HTTP status

#### Scenario: Move endpoint delegates correctly
- **WHEN** `POST /api/move` is called with `{"source": "...", "destination": "..."}`
- **THEN** the server delegates to the file-operations move logic and returns the appropriate HTTP status

### Requirement: Serve static frontend assets
The server SHALL serve the frontend `index.html` and associated static assets from a `static/` directory within the package.

#### Scenario: Root URL serves frontend
- **WHEN** a browser requests `GET /`
- **THEN** the server returns the `index.html` file with HTTP 200

### Requirement: Restrict API access to localhost
The server SHALL only bind to `127.0.0.1` and SHALL configure CORS to reject requests from any origin other than `http://127.0.0.1:<port>`.

#### Scenario: Localhost request allowed
- **WHEN** a request arrives from `127.0.0.1`
- **THEN** the server processes it normally

#### Scenario: External origin rejected
- **WHEN** a request arrives with an `Origin` header from a non-localhost domain
- **THEN** the server returns a CORS error response