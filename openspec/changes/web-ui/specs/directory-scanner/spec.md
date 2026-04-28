## ADDED Requirements

### Requirement: Scan directory tree recursively
The system SHALL recursively traverse a given root directory and compute the cumulative size (in bytes) for every file and directory within it. Symlinks SHALL be followed but cycles SHALL be detected and skipped.

#### Scenario: Successful scan of flat directory
- **WHEN** the scanner is called with a path containing 3 files of known sizes
- **THEN** it returns an entry for each file with the correct size in bytes and the directory entry with the sum of all three sizes

#### Scenario: Nested directories
- **WHEN** the scanner is called with a path containing subdirectories
- **THEN** each subdirectory's size equals the sum of all files recursively within it

#### Scenario: Symlink cycle detection
- **WHEN** the directory tree contains a symlink that creates a cycle
- **THEN** the scanner skips the cyclic link and completes without hanging or raising an unhandled exception

#### Scenario: Permission-denied entry
- **WHEN** a file or subdirectory cannot be read due to OS permissions
- **THEN** that entry is skipped, a warning is logged, and the scan continues for remaining entries

### Requirement: Return structured scan results
The scanner SHALL return results as a nested data structure where each node contains: `name`, `path` (absolute), `size` (bytes), `is_dir` (bool), and `children` (list, empty for files).

#### Scenario: File node structure
- **WHEN** a file node is returned
- **THEN** it has `is_dir: false`, an empty `children` list, and `size` equal to the file's on-disk size

#### Scenario: Directory node structure
- **WHEN** a directory node is returned
- **THEN** it has `is_dir: true`, a `children` list with all direct children, and `size` equal to the sum of all descendant file sizes

### Requirement: Depth-limited scan
The scanner SHALL accept an optional `max_depth` parameter. When provided, it SHALL not recurse deeper than that level and SHALL mark truncated directories with a `truncated: true` flag.

#### Scenario: Depth limit respected
- **WHEN** `max_depth=1` is passed and the root has nested subdirectories
- **THEN** direct children are returned but their children are not, and each unexpanded directory has `truncated: true`

#### Scenario: No depth limit
- **WHEN** `max_depth` is not provided
- **THEN** the full tree is returned and no node has `truncated: true`