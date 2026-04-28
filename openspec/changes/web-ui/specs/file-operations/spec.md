## ADDED Requirements

### Requirement: Delete file or directory
The system SHALL delete a specified file or directory. By default it SHALL move the item to the OS recycle bin / trash using `send2trash`. If `send2trash` is unavailable, it SHALL fall back to permanent deletion only after the client sends an explicit `permanent: true` flag.

#### Scenario: Successful trash deletion
- **WHEN** the client sends a delete request for a valid path without `permanent: true`
- **THEN** the item is moved to the OS trash, the server returns HTTP 200, and the item no longer appears in a subsequent directory scan

#### Scenario: Permanent deletion fallback
- **WHEN** `send2trash` is not installed and the client sends `permanent: true`
- **THEN** the item is permanently removed and the server returns HTTP 200

#### Scenario: Missing `permanent` flag when send2trash unavailable
- **WHEN** `send2trash` is not installed and the client does NOT send `permanent: true`
- **THEN** the server returns HTTP 400 with a message explaining that permanent deletion must be confirmed

#### Scenario: Path outside root rejected
- **WHEN** the requested delete path resolves outside the originally scanned root directory
- **THEN** the server returns HTTP 403 and no file system changes are made

#### Scenario: Non-existent path
- **WHEN** the requested path does not exist
- **THEN** the server returns HTTP 404

### Requirement: Move file or directory
The system SHALL move a specified file or directory to a new destination path. The destination MUST be within the same root directory that was scanned.

#### Scenario: Successful move
- **WHEN** the client sends a move request with a valid source and destination
- **THEN** the item is moved using `shutil.move`, the server returns HTTP 200, and a subsequent scan reflects the new location

#### Scenario: Destination outside root rejected
- **WHEN** the destination path resolves outside the scanned root
- **THEN** the server returns HTTP 403 and the source remains unchanged

#### Scenario: Destination already exists
- **WHEN** the destination path already contains an item with the same name
- **THEN** the server returns HTTP 409 and no file system changes are made

#### Scenario: Source does not exist
- **WHEN** the source path does not exist
- **THEN** the server returns HTTP 404

### Requirement: Validate all paths against scan root
The system SHALL resolve all incoming file operation paths to absolute paths and verify they are within the active scan root before performing any operation.

#### Scenario: Path traversal attempt blocked
- **WHEN** a client sends a path containing `..` segments that would escape the root
- **THEN** the server returns HTTP 403 and logs a warning
