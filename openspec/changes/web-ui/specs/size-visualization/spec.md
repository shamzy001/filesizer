## ADDED Requirements

### Requirement: Display directory contents sorted by size
The UI SHALL display all files and directories in the currently viewed directory sorted by size (descending) in a list or treemap view. Each row/tile SHALL show: name, human-readable size (KB/MB/GB), percentage of parent, and a visual size bar or tile.

#### Scenario: Size list rendered on scan
- **WHEN** a scan result is returned for a directory
- **THEN** all children are displayed sorted by size descending with correct human-readable labels

#### Scenario: Percentage bars
- **WHEN** children are displayed
- **THEN** each item has a proportional visual indicator (bar or tile) relative to the largest item or parent total

### Requirement: Navigate into subdirectories
The UI SHALL allow the user to click on a directory entry to navigate into it. The displayed path (breadcrumb) SHALL update to reflect the current location, and a back/up button SHALL return to the parent.

#### Scenario: Drill into subdirectory
- **WHEN** the user clicks on a directory
- **THEN** the view refreshes to show that directory's contents with an updated breadcrumb

#### Scenario: Navigate up
- **WHEN** the user clicks the parent breadcrumb or up button
- **THEN** the view returns to the parent directory's contents

#### Scenario: Breadcrumb shows full path
- **WHEN** the user has navigated several levels deep
- **THEN** the breadcrumb displays each ancestor directory as a clickable segment

### Requirement: Select a root directory
The UI SHALL provide a text input or file picker to let the user specify a root directory path. On submission, the UI SHALL request a scan of that path and render the results.

#### Scenario: User enters a path
- **WHEN** the user types a directory path and presses Enter or clicks Scan
- **THEN** the UI sends a scan request and renders the resulting tree

#### Scenario: Invalid path feedback
- **WHEN** the server returns an error for the entered path
- **THEN** the UI displays an inline error message without crashing

### Requirement: Initiate delete from UI
The UI SHALL show a delete button (or context menu option) for each file and directory. Clicking it SHALL display a confirmation dialog before sending the delete request. After a successful delete the item SHALL be removed from the displayed list without a full re-scan.

#### Scenario: Delete with confirmation
- **WHEN** the user clicks Delete on an item and confirms
- **THEN** the UI sends `POST /api/delete`, and on success removes the item from the view

#### Scenario: Delete cancelled
- **WHEN** the user clicks Delete but cancels the confirmation dialog
- **THEN** no request is sent and the item remains in the list

#### Scenario: Delete failure shown
- **WHEN** the server returns an error for a delete request
- **THEN** the UI shows an error message without removing the item

### Requirement: Initiate move from UI
The UI SHALL allow the user to move a file or directory by specifying a destination path via an input dialog. After a successful move the item SHALL be removed from the current view.

#### Scenario: Move with destination input
- **WHEN** the user triggers Move on an item and enters a valid destination path
- **THEN** the UI sends `POST /api/move`, and on success removes the item from the current view

#### Scenario: Move conflict shown
- **WHEN** the server returns HTTP 409
- **THEN** the UI shows a conflict error and the item remains in place

### Requirement: Show loading state during scan
The UI SHALL display a loading indicator while a scan is in progress so the user knows the application is working.

#### Scenario: Loading indicator visible
- **WHEN** a scan request is sent
- **THEN** a loading spinner or progress message is shown until the response is received

#### Scenario: Loading indicator hidden on completion
- **WHEN** the scan response is received (success or error)
- **THEN** the loading indicator is hidden and replaced with results or an error message
