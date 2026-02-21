# Custom Exception Documentation

## Overview

Custom exceptions are application-specific error classes that extend Python's built-in `Exception` class. Unlike generic built-in exceptions (ValueError, FileNotFoundError, etc.), custom exceptions allow you to identify and handle errors specific to your application's domain and processes.

## Why Custom Exceptions?

### Problem with Built-in Exceptions

When using only Python's built-in exceptions, it's difficult to determine **where** and **why** an error occurred in your application:

```python
raise ValueError("Something went wrong")  # Which process? Which file? Which line?
```

### Solution: Custom Exceptions

Custom exceptions provide context-specific error information:

```python
raise CustomException(
    "Process 1 failed due to some error",
    error_detail=FileNotFoundError("data.csv not found")
)
```

**Benefits:**
- ✓ Identify which process or component failed
- ✓ Track the original exception that caused the error
- ✓ Know exactly which file and line number the error occurred
- ✓ Provide meaningful error messages for debugging
- ✓ Enable specific error handling and recovery strategies

## CustomException Class

### Purpose

The `CustomException` class provides detailed error reporting with information about:
- Error message
- Original exception type (if any)
- File name where error occurred
- Line number where error occurred

### Constructor

```python
class CustomException(Exception):
    def __init__(self, message: str, error_detail: Exception = None):
```

**Parameters:**
- **message** (str): Custom error message describing what went wrong in your application
- **error_detail** (Exception, optional): The original exception that caused the error

**Example:**
```python
try:
    data = load_csv("anime_data.csv")
except FileNotFoundError as e:
    raise CustomException(
        message="Failed to load anime dataset - file not found",
        error_detail=e
    )
```

### Key Methods

#### get_detailed_error_message()

**Purpose:** Construct a detailed error message containing all relevant debugging information

**How it works:**
1. Captures exception details using `sys.exc_info()`
2. Extracts traceback information
3. Retrieves file name and line number from traceback
4. Constructs formatted error message

**Method Signature:**
```python
@staticmethod
def get_detailed_error_message(message: str, error_detail: Exception = None) -> str
```

**Returns:** Formatted error message string

**Output Format:**
```
{message} | Error Details: {error_detail} | File Name: {file_name} | Line Number: {line_number}
```

**Example Output:**
```
Process 1 failed due to some error | 
Error Details: FileNotFoundError: [Errno 2] No such file or directory: 'data.csv' | 
File Name: main.py | 
Line Number: 10
```

#### __str__()

**Purpose:** Return the error message when the exception is converted to string

**Usage:** Called when printing the exception or logging it

```python
try:
    # ... code ...
except CustomException as e:
    print(e)  # Calls __str__() automatically
    logger.error(str(e))
```

## Usage Patterns

### Pattern 1: Basic Error with Context

```python
from common.custom_exception import CustomException
from common.logger import get_logger

logger = get_logger(__name__)

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        return data
    except FileNotFoundError as e:
        raise CustomException(
            message=f"Data loading failed - file not found at {file_path}",
            error_detail=e
        )
```

### Pattern 2: Multiple Process Tracking

```python
def process_anime_data():
    try:
        # Process 1: Load data
        data = load_anime_csv("data/anime.csv")
    except FileNotFoundError as e:
        raise CustomException(
            message="Process 1 (Data Loading) failed",
            error_detail=e
        )
    
    try:
        # Process 2: Generate embeddings
        embeddings = generate_embeddings(data)
    except Exception as e:
        raise CustomException(
            message="Process 2 (Embedding Generation) failed",
            error_detail=e
        )
    
    try:
        # Process 3: Store in database
        store_in_chromadb(embeddings)
    except Exception as e:
        raise CustomException(
            message="Process 3 (Database Storage) failed",
            error_detail=e
        )
```

### Pattern 3: Exception Chaining

```python
def train_recommendation_model():
    try:
        data = load_data("anime_data.csv")
        model = create_model(data)
        model.train()
    except CustomException:
        # Re-raise if already a CustomException
        raise
    except Exception as e:
        # Wrap any other exception
        raise CustomException(
            message="Model training pipeline failed",
            error_detail=e
        )
```

### Pattern 4: Logging Custom Exceptions

```python
from common.logger import get_logger

logger = get_logger(__name__)

try:
    process_data()
except CustomException as e:
    logger.error(f"Custom exception caught: {e}")
    # Handle or re-raise
```

## Exception Information Captured

| Information | Source | Example |
|-------------|--------|---------|
| **Custom Message** | Function parameter | "Process 1 failed" |
| **Original Exception Type** | error_detail parameter | FileNotFoundError |
| **Original Exception Message** | error_detail parameter | "[Errno 2] No such file..." |
| **File Name** | sys.exc_info() traceback | main.py |
| **Line Number** | sys.exc_info() traceback | 42 |

## Related Files

- **logger.py** - Logging utility for recording exceptions
- **__init__.py** - Module initialization file

## Best Practices

### ✓ DO

1. **Always provide meaningful messages**
   ```python
   raise CustomException("Failed to process anime recommendation", error_detail=e)
   ```

2. **Use for application-specific errors**
   ```python
   raise CustomException("Invalid anime genre provided", error_detail=ValueError("genre must be string"))
   ```

3. **Catch and wrap existing exceptions**
   ```python
   try:
       risky_operation()
   except Exception as e:
       raise CustomException("Operation failed", error_detail=e)
   ```

4. **Log before re-raising**
   ```python
   try:
       process()
   except CustomException as e:
       logger.error(f"Handled error: {e}")
       raise
   ```

### ❌ DON'T

1. **Don't lose the original exception context**
   ```python
   # BAD
   except Exception:
       raise CustomException("Something failed")  # Lost original error
   
   # GOOD
   except Exception as e:
       raise CustomException("Something failed", error_detail=e)
   ```

2. **Don't use generic messages**
   ```python
   # BAD
   raise CustomException("Error", error_detail=e)
   
   # GOOD
   raise CustomException("Failed to load anime dataset from CSV", error_detail=e)
   ```

3. **Don't ignore CustomExceptions**
   ```python
   # BAD
   try:
       process()
   except:
       pass
   
   # GOOD
   try:
       process()
   except CustomException as e:
       logger.error(str(e))
       raise
   ```

## Complete Example

```python
from common.custom_exception import CustomException
from common.logger import get_logger

logger = get_logger(__name__)

class AnimeRecommender:
    def recommend(self, user_preference: str):
        try:
            logger.info(f"Starting recommendation process for: {user_preference}")
            
            # Load data
            anime_data = self._load_data()
            
            # Generate embedding
            preference_embedding = self._generate_embedding(user_preference)
            
            # Find similar anime
            recommendations = self._find_similar(anime_data, preference_embedding)
            
            logger.info(f"Successfully generated {len(recommendations)} recommendations")
            return recommendations
            
        except CustomException as e:
            logger.error(f"Recommendation process failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in recommendation: {e}")
            raise CustomException(
                "Recommendation pipeline encountered an unexpected error",
                error_detail=e
            )
    
    def _load_data(self):
        try:
            # ... load data ...
            return data
        except FileNotFoundError as e:
            raise CustomException(
                "Failed to load anime data - file not found",
                error_detail=e
            )
    
    def _generate_embedding(self, text: str):
        try:
            # ... generate embedding ...
            return embedding
        except Exception as e:
            raise CustomException(
                "Failed to generate text embedding",
                error_detail=e
            )
    
    def _find_similar(self, data, embedding):
        try:
            # ... find similar items ...
            return results
        except Exception as e:
            raise CustomException(
                "Failed to find similar anime",
                error_detail=e
            )
```

## Debugging Tips

When a CustomException is raised, you get detailed information:

```
Process 1 failed | 
Error Details: FileNotFoundError: [Errno 2] No such file or directory: 'anime.csv' | 
File Name: recommendation_engine.py | 
Line Number: 45
```

**Use this information to:**
1. Identify the exact file and line number of the error
2. Understand what the original exception was
3. Trace the error back to its root cause
4. Write targeted fix based on process that failed

## Integration with Type Hints

For better IDE support and type checking:

```python
from typing import Optional
from common.custom_exception import CustomException

def process_data() -> dict:
    try:
        # ... process ...
        return result
    except CustomException as e:
        logger.error(f"Data processing failed: {e}")
        raise
```

