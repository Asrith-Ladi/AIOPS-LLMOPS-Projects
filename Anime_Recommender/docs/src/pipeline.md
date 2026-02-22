# Build Pipeline Documentation

## Overview

The `build_pipeline.py` script is the core setup automation that orchestrates the entire data processing workflow. It coordinates three main operations: loading anime data from CSV, processing it into a suitable format, and building a persistent vector database for similarity searches.

## Purpose

The build pipeline performs three sequential operations:
1. **Load** - Reads anime data from the original CSV file
2. **Process** - Combines anime information into a unified text format
3. **Vectorize** - Converts processed text into embeddings and stores them in a vector database

These operations prepare the system for serving anime recommendations.

---

## Key Concepts Explained

### What is a Pipeline?

A **pipeline** is an automated sequence of steps that takes raw data and transforms it into a usable form.

**Real-World Analogy - Car Manufacturing:**

```
Raw Materials
    ↓ (Assembly Line Step 1: Weld frame)
    ↓ (Assembly Line Step 2: Add engine)
    ↓ (Assembly Line Step 3: Install wheels)
    ↓ (Final Step: Paint & Quality Check)
Finished Car
```

**Data Pipeline - Anime Recommendation:**

```
Raw CSV Data
    ↓ (Step 1: Load & Validate)
    ↓ (Step 2: Process & Combine)
    ↓ (Step 3: Create Embeddings)
    ↓ (Step 4: Store in Database)
Ready-to-Use Vector Database
```

### Why Automate the Pipeline?

**Without Automation (Manual Steps):**
```
1. User manually runs data loader script
2. User manually runs vector builder script
3. User manually verifies outputs
→ Error-prone, time-consuming, inconsistent
```

**With Automation (Pipeline):**
```
1. User runs: python pipeline/build_pipeline.py
2. All steps execute automatically
3. Logs show what happened
→ Reliable, fast, consistent, reproducible
```

### What is Path Resolution?

**Path resolution** means finding file locations correctly regardless of where the script is run from.

**The Problem:**

```
Directory Structure:
D:\Projects\AIOPS\
├── Anime_Recommender/
│   ├── pipeline/
│   │   └── build_pipeline.py (script location)
│   ├── data/
│   │   └── anime_with_synopsis.csv (data location)
│   └── ...

If script tries: open("data/anime.csv")
And user runs from: D:\Projects\AIOPS\
Result: FileNotFoundError! (It looks for D:\Projects\AIOPS\data\anime.csv)

If user runs from: D:\Projects\AIOPS\Anime_Recommender\
Result: Success! (It finds D:\Projects\AIOPS\Anime_Recommender\data\anime.csv)
```

**The Solution (Used in build_pipeline.py):**

```python
# Get the directory where THIS script lives
script_dir = Path(__file__).parent  # pipeline/
# Go up one level to project root
project_root = script_dir.parent    # Anime_Recommender/
# Construct absolute path
csv_path = project_root / "data" / "anime_with_synopsis.csv"
# Now it works from ANY directory!
```

---

## Script Structure

### Imports

```python
import sys
from pathlib import Path

# Add project root to path so imports work correctly
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException
```

**What Each Import Does:**

| Import | Purpose |
|--------|---------|
| `sys` | Allows modifying Python's import path |
| `Path` | Makes working with file paths cross-platform safe |
| `project_root` | Calculates absolute path to project root |
| `AnimeDataLoader` | Class for loading and processing CSV data |
| `VectorStoreBuilder` | Class for creating embeddings and vector database |
| `load_dotenv()` | Loads environment variables from .env file |
| `get_logger()` | Creates logging object for tracking progress |
| `CustomException` | Custom exception class for error handling |

**Example of Path Calculation:**

```
File: D:\Projects\AIOPS\Anime_Recommender\pipeline\build_pipleline.py

__file__ = D:\Projects\AIOPS\Anime_Recommender\pipeline\build_pipleline.py
Path(__file__).parent = D:\Projects\AIOPS\Anime_Recommender\pipeline\
Path(__file__).parent.parent = D:\Projects\AIOPS\Anime_Recommender\

Result: project_root = D:\Projects\AIOPS\Anime_Recommender\
```

### Main Function

```python
def main():
    try:
        # Step 1: Log start
        logger.info("Starting to build pipeline")
        
        # Step 2: Construct file paths
        csv_path = project_root / "data" / "anime_with_synopsis.csv"
        processed_csv_path = project_root / "data" / "anime_updated.csv"
        
        # Step 3: Load and process data
        loader = AnimeDataLoader(str(csv_path), str(processed_csv_path))
        processed_csv = loader.load_and_process()
        logger.info("Data loaded and processed successfully")
        
        # Step 4: Build vector store
        vector_builder = VectorStoreBuilder(csv_path=processed_csv)
        vector_builder.build_and_save_vectorstore()
        logger.info("Vector store built successfully...")
        
        # Step 5: Log completion
        logger.info("Pipeline built successfully")
        
    except Exception as e:
        logger.info(f"failed to execute pipeline {str(e)}")
        raise CustomException("Error during pipeline initialization", e)
```

---

## Execution Flow

### Step-by-Step Process

```
START: python pipeline/build_pipleline.py
    ↓
[Step 1: Path Resolution]
  Calculate: D:\Projects\AIOPS\Anime_Recommender\
  CSV path: D:\Projects\AIOPS\Anime_Recommender\data\anime_with_synopsis.csv
  Output path: D:\Projects\AIOPS\Anime_Recommender\data\anime_updated.csv
    ↓
[Step 2: Create Data Loader]
  Instantiate AnimeDataLoader with both paths
  Loader now knows:
    - Where to read original anime data
    - Where to save processed data
    ↓
[Step 3: Load and Process Data]
  Actions:
    1. Read anime_with_synopsis.csv
    2. Validate required columns exist
    3. Combine Name + Synopsis + Genres into one field
    4. Save to anime_updated.csv
  Output: Path to processed CSV
    ↓
[Step 4: Create Vector Store Builder]
  Instantiate VectorStoreBuilder with processed CSV path
  Builder now knows:
    - Where to read processed anime data
    - How to create embeddings
    ↓
[Step 5: Build and Save Vector Store]
  Actions:
    1. Load processed CSV with anime data
    2. Split text into chunks (1000 characters each)
    3. Convert chunks to embeddings (384-dimensional vectors)
    4. Store embeddings in Chroma DB
    5. Save to disk in chroma_db/ folder
    ↓
[Step 6: Verify and Log]
  Confirm all components created successfully
    ↓
END: Pipeline complete - System ready for recommendations!
```

### Visual Data Flow

```
anime_with_synopsis.csv
(Raw data with 270+ anime)
    │
    ├─→ [AnimeDataLoader.load_and_process()]
    │
    └─→ anime_updated.csv
        (Processed data: combined Title+Synopsis+Genres)
            │
            ├─→ [VectorStoreBuilder.build_and_save_vectorstore()]
            │
            └─→ chroma_db/
                (Vector database with embeddings)
                ├── chroma.sqlite3
                ├── 9d4a0c5d-3b25-4963-bd5a-81d84e70352b/
                └── ... (vector data files)
```

---

## File Outputs

### Processed CSV (anime_updated.csv)

**Location:** `data/anime_updated.csv`

**Content:** Single column with combined anime information

**Example Row:**
```
Title: Cowboy Bebop..Overview: In the year 2071, humanity has colonized...Genres : Action, Adventure, Comedy, Drama, Sci-Fi, Space
```

**Use:** Input for vector embedding generation

### Vector Database (chroma_db/)

**Location:** `chroma_db/` (created automatically)

**Structure:**
```
chroma_db/
├── chroma.sqlite3
│   └── Metadata database storing document info
├── 9d4a0c5d-3b25-4963-bd5a-81d84e70352b/
│   └── Vector embeddings and indices
└── [Internal Chroma files]
```

**Use:** Fast similarity searches for recommendation queries

**Important:** Add `chroma_db/` to `.gitignore` since it's:
- Large (hundreds of MB+)
- Auto-generated
- Contains binary vector data
- Not needed in version control

---

## Logging

The pipeline provides detailed logging at each step.

### Log File Location

**Default:** `logs/log_YYYY-MM-DD_HH-MM-SS.log`

**Example Log Output:**

```
2026-02-22 13:14:31,452 - INFO - Starting to build pipeline
2026-02-22 13:14:31,473 - INFO - Data loaded and processed successfully
2026-02-22 13:14:35,824 - INFO - Vector store built successfully...
2026-02-22 13:14:35,825 - INFO - Pipeline built successfully
```

### Understanding Log Levels

| Level | Meaning | Example |
|-------|---------|---------|
| **INFO** | Normal operation | "Starting to build pipeline" |
| **WARNING** | Something unexpected but handled | "CSV had 5 rows with missing data" |
| **ERROR** | Something failed but trying to recover | "Failed to parse column X, skipping..." |
| **CRITICAL** | Complete failure | "Cannot find CSV file - aborting" |

### Checking Logs

```bash
# View most recent log
ls logs/  # See all log files

# View specific log
type logs\log_2026-02-22_13-14-31.log

# Search for errors
findstr "ERROR\|CRITICAL" logs\log_*.log
```

---

## Error Handling

### What Can Go Wrong?

#### 1. CSV File Not Found

**Error Message:**
```
CustomException: Error during pipeline initialization | 
Error: [Errno 2] No such file or directory: '...\anime_with_synopsis.csv'
```

**Cause:** CSV file doesn't exist at the path

**Solution:**
```bash
# Check if file exists
dir data\anime_with_synopsis.csv

# If not there, get it from the repo
# Copy anime_with_synopsis.csv to Anime_Recommender/data/
```

#### 2. Missing Required Columns

**Error Message:**
```
CustomException: Error during pipeline initialization | 
Error: Missing columns {'Name', 'Genres', 'sypnopsis'} in CSV file
```

**Cause:** CSV file doesn't have required columns (note: 'sypnopsis' is misspelled in the original CSV)

**Solution:**
```python
# Check CSV columns
import pandas as pd
df = pd.read_csv('data/anime_with_synopsis.csv')
print(df.columns)

# Should show:
# Index(['MAL_ID', 'Name', 'Score', 'Genres', 'sypnopsis'], dtype='object')
```

#### 3. HuggingFace Model Download Issues

**Error Message:**
```
ConnectionError: Failed to download HuggingFace embedding model
```

**Cause:** Network issue or HuggingFace API down

**Solution:**
```bash
# Ensure internet connection
# Try again - model is cached after first download
python pipeline/build_pipleline.py
```

#### 4. Insufficient Disk Space

**Error Message:**
```
OSError: [Errno 28] No space left on device
```

**Cause:** Not enough disk space for vector database

**Solution:**
```bash
# Free up disk space
# Vector DB is typically 500MB - 2GB depending on data size

# Check disk space
dir C:\
```

### Recovery Steps

If the pipeline fails:

```python
# Step 1: Check logs
cat logs\log_*.log  # Find the error

# Step 2: Fix the issue
# Example: If CSV not found, place the file in data/

# Step 3: Re-run the pipeline
python pipeline/build_pipleline.py

# Step 4: Verify success
# Check if chroma_db/ folder was created
dir chroma_db\
```

---

## Usage Patterns

### Pattern 1: Initial Setup (First Time)

```bash
# Navigate to project directory
cd D:\Projects\AIOPS\Anime_Recommender

# Run the pipeline to create everything
python pipeline/build_pipleline.py

# Wait for completion (2-5 minutes depending on system)
# When done, you'll see: "Pipeline built successfully"
```

**What Gets Created:**
- `data/anime_updated.csv` - Processed anime data
- `chroma_db/` - Vector database with embeddings

### Pattern 2: Rebuilding After Data Update

```bash
# If you update the anime data source:
python pipeline/build_pipleline.py

# This will:
# 1. Delete old processed files
# 2. Create new processed data
# 3. Rebuild vector database
# 4. Preserve all embeddings
```

### Pattern 3: Running from Different Directories

The script works from ANY directory because of path resolution:

```bash
# From project root
python pipeline/build_pipleline.py  ✓ Works!

# From parent directory
cd D:\Projects\AIOPS
python Anime_Recommender/pipeline/build_pipleline.py  ✓ Works!

# From anywhere with full path
python D:\Projects\AIOPS\Anime_Recommender\pipeline\build_pipleline.py  ✓ Works!
```

### Pattern 4: Integration with Jupyter Notebook

```python
import subprocess
import sys

# Run pipeline from notebook
result = subprocess.run(
    [sys.executable, "pipeline/build_pipleline.py"],
    cwd="D:\Projects\AIOPS\Anime_Recommender\",
    capture_output=True,
    text=True
)

# Check result
if result.returncode == 0:
    print("✓ Pipeline successful!")
else:
    print("✗ Pipeline failed!")
    print(result.stderr)
```

---

## Best Practices

### ✓ Do's

- ✅ Run pipeline before starting the recommendation system
- ✅ Check logs if pipeline fails
- ✅ Keep `.env` file secure with API keys
- ✅ Add `chroma_db/` to `.gitignore`
- ✅ Run occasionally to update vector database with new data
- ✅ Monitor disk space - vector DB can grow large

### ✗ Don'ts

- ❌ Don't modify anime CSV column names without updating data_loader.py
- ❌ Don't delete chroma_db manually - let pipeline manage it
- ❌ Don't run multiple pipeline instances simultaneously
- ❌ Don't interrupt the pipeline midway (Ctrl+C)
- ❌ Don't assume the script is instant - embedding takes time
- ❌ Don't commit chroma_db/ to version control

---

## Performance Tips

### Reduce Processing Time

The pipeline takes 2-5 minutes depending on system specs. Here's how to optimize:

```python
# For faster processing (fewer anime):
# 1. Reduce CSV size before running pipeline
# 2. Use faster hardware (SSD > HDD)
# 3. Ensure sufficient RAM (8GB+ recommended)
```

### Monitor Progress

```bash
# While pipeline runs, monitor logs in real-time
# (In another terminal window)
tail -f logs\log_*.log  # Linux/Mac
Get-Content logs\log_*.log -Wait  # PowerShell
```

### Cache Management

The HuggingFace model downloads once and is cached:

```
~/.cache/huggingface/
├── hub/
│   └── models--sentence-transformers--all-MiniLM-L6-v2/
│       └── (cached model files ~300MB)
```

After first run, subsequent runs skip model download.

---

## Troubleshooting Checklist

| Problem | Check | Solution |
|---------|-------|----------|
| Path errors | Is anime_with_synopsis.csv in data/? | Move file to correct location |
| Import errors | Are all packages installed? | Run: pip install -r requirements.txt |
| Slow performance | CPU usage high? | Close other programs |
| Disk space errors | Enough free space? | Free up 2GB+ space |
| Encoding errors | CSV encoding correct? | Ensure UTF-8 encoding |
| Network errors | Internet working? | Check connection, retry |

---

## Summary

The `build_pipeline.py` script:

1. **Automates** the entire data setup process
2. **Handles** all path resolution correctly
3. **Logs** each step for debugging
4. **Validates** data integrity
5. **Creates** a ready-to-use vector database
6. **Enables** fast anime recommendation searches

After running this pipeline, your system is ready to serve intelligent anime recommendations through the recommender class.

---

## Next Steps

After the pipeline completes successfully:

1. [Learn about the Recommender Class](recommender.md) - Uses the vector database
2. [Review Prompt Template](prompt_template.md) - Controls LLM behavior
3. [Understand Vector Store](vector_store.md) - Created by this pipeline
4. [View Data Loader](data_loader.md) - First step of pipeline
5. [Deploy Application](../SETUP.md) - Run the complete system
