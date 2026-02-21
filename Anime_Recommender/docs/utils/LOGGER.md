# Logger Module Documentation

## Overview
The `logger.py` module provides centralized logging functionality for the AIOPS project. It configures Python's built-in `logging` module to write all log messages to timestamped log files in the `logs/` directory.

## What This Module Does

- **Automatically creates a logs directory** if it doesn't exist
- **Generates timestamped log files** with format: `log_YYYY-MM-DD_HH-MM-SS.log`
- **Initializes logging configuration** at INFO level and above
- **Provides a utility function** to create logger instances

## Configuration Details

### Log File Location
- **Directory**: `logs/` (created in project root)
- **Format**: `log_{timestamp}.log`
- **Example**: `log_2026-02-21_14-30-45.log`

### Log Format
```
%(asctime)s - %(levelname)s - %(message)s
```
- **asctime**: Timestamp of the log message
- **levelname**: Severity level (INFO, WARNING, ERROR, CRITICAL)
- **message**: The actual log message

### Logging Level: INFO
The module logs messages at **INFO level and above**:
- ✓ **DEBUG** - Detailed debugging information (not logged by default)
- ✓ **INFO** - Confirmation that things are working as expected
- ✓ **WARNING** - Something unexpected or concerning
- ✓ **ERROR** - A serious problem, something failed
- ✓ **CRITICAL** - A very serious error, program may not continue

## How to Use

### Basic Usage
```python
from common.logger import get_logger

# Create a logger for your module
logger = get_logger(__name__)

# Log messages at different levels
logger.info("This is an informational message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```

### In a Class
```python
from common.logger import get_logger

class MyService:
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def do_something(self):
        self.logger.info("Service started")
        # Your code here
        self.logger.info("Service completed")
```

### In Multiple Modules
```python
# In module1.py
from common.logger import get_logger
logger = get_logger(__name__)  # Creates logger for 'module1'

# In module2.py
from common.logger import get_logger
logger = get_logger(__name__)  # Creates logger for 'module2'

# All logs go to the same file in logs/ directory
```

## Log File Examples

**Output in log file:**
```
2026-02-21 14:30:45,123 - INFO - Application started
2026-02-21 14:30:46,456 - INFO - Processing request #1001
2026-02-21 14:30:47,789 - WARNING - Cache miss for key 'user_data'
2026-02-21 14:30:48,012 - ERROR - Failed to connect to database
```

## Key Points to Remember

1. **One log file per execution** - A new log file is created each time your application runs
2. **Automatic directory creation** - The `logs/` directory is created automatically if missing
3. **All modules share one file** - All loggers write to the same log file for the execution session
4. **INFO level and above** - DEBUG messages won't appear in logs by default
5. **Timestamp format** - Logs include both file timestamp (creation time) and message timestamp (log time)

## Changing Configuration

If you need to modify logging behavior:

- **Change log level**: Modify `level=logging.INFO` in `basicConfig()` to `logging.DEBUG`, `logging.WARNING`, etc.
- **Change log format**: Modify the `format` string in `basicConfig()`
- **Add file rotation**: Could extend this module to use `logging.handlers.RotatingFileHandler`
- **Add console output**: Could add a console handler in addition to file handler

## Common Patterns

### Log at function entry/exit
```python
def process_data(data):
    logger.info(f"Processing data: {data}")
    try:
        # Process here
        logger.info("Data processing completed")
    except Exception as e:
        logger.error(f"Failed to process data: {str(e)}")
        raise
```

### Log with variables
```python
user_id = 123
logger.info(f"User {user_id} logged in successfully")
```

### Log errors with traceback
```python
import logging
try:
    risky_operation()
except Exception as e:
    logger.exception(f"Operation failed: {str(e)}")  # Includes stack trace
```

## File Structure
```
project_root/
├── common/
│   ├── logger.py          (This module)
│   ├── LOGGER.md          (This documentation)
│   ├── __init__.py
│   └── custom_exception.py
├── logs/                  (Auto-created by logger.py)
│   ├── log_2026-02-21_10-30-45.log
│   ├── log_2026-02-21_14-45-12.log
│   └── ...
└── setup.py
```
