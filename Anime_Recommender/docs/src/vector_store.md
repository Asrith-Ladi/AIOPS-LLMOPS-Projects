# Vector Store Documentation

## Overview

The `VectorStoreBuilder` class is responsible for converting processed anime text data into vector embeddings and storing them in a vector database. This enables intelligent similarity searches and semantic recommender operations.

## Purpose

The vector store performs three critical operations:
1. **Convert** - Transforms text data into numerical vectors (embeddings) that capture semantic meaning
2. **Store** - Saves these vectors in a persistent vector database for efficient retrieval
3. **Load** - Retrieves stored vectors for use in recommendation matching and queries

---

## Key Concepts Explained

### What is an Embedding?

An **embedding** is a numerical representation of text that captures its semantic meaning. Instead of treating text as just characters, embeddings convert words and sentences into numbers (vectors) that computers can understand and compare.

**Simple Example:**

Imagine you have three anime descriptions:
- "A cool action adventure with robots"
- "An exciting sci-fi battle with amazing visuals"
- "A romantic story about friendship"

An embedding converts each description into a list of numbers like:
```
Anime 1: [0.2, 0.8, 0.1, 0.9, ...]
Anime 2: [0.25, 0.75, 0.15, 0.88, ...]
Anime 3: [0.05, 0.1, 0.9, 0.2, ...]
```

**Why Useful?**
- Anime 1 and 2 have very similar numbers (vectors are close in meaning) → Both are action/sci-fi
- Anime 3 is very different (far from Anime 1 & 2) → It's a romance, not action
- This allows recommendations: "Show me anime similar to Anime 1" → System finds Anime 2!

### What is a Vector Database?

A **vector database** is like a specialized library system that stores and quickly finds similar things based on their vector representations.

**Traditional Database (like CSV):**
```
ID | Name | Genre
1  | Cowboy Bebop | Sci-Fi
2  | Trigun | Sci-Fi
```
Can only search by exact matches: "Find anime with name = 'Cowboy Bebop'"

**Vector Database (like Chroma):**
```
ID | Embedding Vector | Metadata
1  | [0.2, 0.8, 0.1...] | Cowboy Bebop
2  | [0.25, 0.75, 0.15...] | Trigun
```
Can search by semantic similarity: "Find anime similar to 'Sad sci-fi action show'"

### Text Chunking

**Text Chunking** breaks large documents into smaller, manageable pieces before creating embeddings.

**Why Split?**
- A full anime synopsis might be 500+ words
- Too long → AI models struggle and embeddings become less accurate
- Solution: Split into chunks (e.g., 1000 characters each)

**Example:**

Original synopsis:
```
"In the year 2071, humanity has colonized the planets. 
Spike Spiegel, a laid-back bounty hunter, travels with his 
spaceship crew seeking out criminals for reward money. 
The series follows their adventures across the galaxy..."
```

After chunking (chunk_size=1000):
```
Chunk 1: "In the year 2071, humanity has colonized the planets. 
          Spike Spiegel, a laid-back bounty hunter, travels with his 
          spaceship crew seeking out criminals for reward money."

Chunk 2: "The series follows their adventures across the galaxy..."
```

Each chunk gets its own embedding, allowing more precise searches.

### Persistence

**Persistence** means saving data so it remains available even after the program stops running.

**Without Persistence:**
```
Program Starts → Create vectors → Load into memory → Program Stops → Data is Lost!
```

**With Persistence (Using Chroma):**
```
Program Starts → Create vectors → Save to disk (chroma_db) → Program Stops → Data Saved!
Next Run → Load from disk → Continue using data
```

---

## HuggingFace Embeddings

The system uses **HuggingFace's `sentence-transformers/all-MiniLM-L6-v2` model** to generate embeddings.

**Model Details:**
- **Name:** all-MiniLM-L6-v2
- **Purpose:** Converts text sentences/documents into numerical vectors
- **Output:** Each text becomes a vector of 384 numbers
- **Advantage:** Fast, efficient, and works well for similarity searches

**How it Works:**

```
Input Text: "An action-packed anime with amazing visuals"
           ↓
Tokenization: Break into words ["An", "action-packed", "anime", ...]
           ↓
Embedding Model: Convert to numbers [0.2, 0.8, 0.1, 0.9, ... (384 total)]
           ↓
Output Vector: [0.2, 0.8, 0.1, 0.9, ..., -0.3]
```

---

## Chroma DB

**Chroma** is a lightweight vector database that stores embeddings and allows fast similarity searches.

**Key Features:**
- **Persistent:** Saves vectors to disk in the `chroma_db` folder
- **Offline:** Works without internet connection
- **Fast:** Optimized for quick similarity searches
- **Simple API:** Easy to use with just a few method calls

**How Chroma Stores Data:**

```
chroma_db/
├── index.bin (binary file with vector data)
├── metadata.sqlite (database with document info)
└── ... (other internal files)
```

You don't need to manage these files directly—Chroma handles them automatically!

---

## VectorStoreBuilder Class

### Constructor

```python
class VectorStoreBuilder:
    def __init__(self, csv_path: str, persis_dir: str = "chroma_db"):
```

**Parameters:**
- **csv_path** (str): Path to the CSV file containing processed anime data
- **persis_dir** (str): Directory where vector database will be saved (default: `chroma_db`)

**What Happens During Initialization:**
1. Stores the CSV file path
2. Stores the persistence directory path
3. Initializes the HuggingFace embedding model
4. The model is now ready to convert text to vectors

**Example:**

```python
from src.vectorstore import VectorStoreBuilder

# Create a builder with default persistence directory
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")

# Or, create a builder with custom persistence directory
builder_custom = VectorStoreBuilder(
    csv_path="data/anime_with_synopsis.csv",
    persis_dir="my_custom_chroma_db"
)
```

**Visual Representation:**

```
VectorStoreBuilder(
    csv_path="data/anime_with_synopsis.csv",
    persis_dir="chroma_db"
)
        ↓
[Initialization Complete]
        ↓
Ready to:
  • Load and process CSV data
  • Create embeddings
  • Save to vector database
```

---

### Methods

#### build_and_save_vectorstore()

Creates embeddings from CSV data and saves them to the vector database.

**Method Signature:**

```python
def build_and_save_vectorstore(self):
    """
    Load CSV data, create embeddings, and save to vector database.
    
    Process:
    1. Load CSV file
    2. Split text into chunks
    3. Generate embeddings for each chunk
    4. Save to vector database
    5. Persist to disk
    
    Returns:
        None (saves data to disk)
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        Exception: If embedding generation fails
    """
```

**What This Method Does (Step-by-Step):**

```
Step 1: Load CSV
─────────────────
Read CSV file with UTF-8 encoding
Input CSV:
┌─────────────────────────────────────────┐
│ combined_info                           │
├─────────────────────────────────────────┤
│ Title: Cowboy Bebop...Overview: In the  │
│ year 2071... Genres: Sci-Fi, Action... │
│                                         │
│ Title: Trigun...Overview: Vash the...  │
│ Genres: Sci-Fi, Adventure...           │
└─────────────────────────────────────────┘

Step 2: Split into Chunks
──────────────────────────
CharacterTextSplitter breaks long text into 1000-character chunks
Output:
┌─────────────────────────────────────────┐
│ Chunk 1: "Title: Cowboy Bebop..."       │
├─────────────────────────────────────────┤
│ Chunk 2: "...Genres: Sci-Fi, Action..."│
├─────────────────────────────────────────┤
│ Chunk 3: "Title: Trigun..."             │
└─────────────────────────────────────────┘

Step 3: Generate Embeddings
────────────────────────────
HuggingFace converts each chunk to 384-number vector
Chunk 1 → [0.2, 0.8, 0.1, ..., -0.3] (384 numbers)
Chunk 2 → [0.15, 0.75, 0.2, ..., -0.25] (384 numbers)
Chunk 3 → [0.3, 0.7, 0.05, ..., -0.1] (384 numbers)

Step 4 & 5: Save and Persist
─────────────────────────────
Chroma saves all embeddings and metadata to chroma_db folder
Files created on disk (chroma_db/)
Data is now available for future use
```

**Processing Details:**

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| **Encoding** | UTF-8 | Handles special characters properly |
| **Chunk Size** | 1000 characters | Default size for each text chunk |
| **Chunk Overlap** | 0 | No overlap between consecutive chunks |
| **Embedding Dimension** | 384 | Each chunk becomes 384 numbers |

**Example:**

```python
from src.vectorstore import VectorStoreBuilder

# Initialize builder
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")

# Build and save vector store
builder.build_and_save_vectorstore()

print("✓ Vector store created and saved successfully!")
print("✓ Vectors stored in: chroma_db/")
print("✓ Ready for similarity searches and recommendations")
```

**Output (in your file system):**
```
chroma_db/
├── index.bin
├── metadata.sqlite
└── ... (vector data)
```

#### load_vectorstore()

Loads the previously saved vector database into memory for use in recommendations.

**Method Signature:**

```python
def load_vectorstore(self):
    """
    Load vector store from disk.
    
    Returns:
        Chroma: Vector database object ready for similarity searches
        
    Raises:
        FileNotFoundError: If persistence directory doesn't exist
    """
```

**What This Method Does:**

```
Step 1: Connect to Persistence Directory
─────────────────────────────────────────
Look for chroma_db/ folder and its data

Step 2: Load Embeddings from Disk
──────────────────────────────────
Read all saved vector data from chroma_db/

Step 3: Reinitialize HuggingFace Embeddings
────────────────────────────────────────────
Set up the embedding model for similarity matching

Step 4: Return Chroma Object
─────────────────────────────
Return ready-to-use vector database object

Output: Chroma object
      ↓
Used for: Similarity searches, recommendation matching
```

**Return Value:**
- **Type:** Chroma database object
- **Purpose:** Enables similarity searches and vector operations
- **Methods Available:** `similarity_search()`, `search()`, etc.

**Example:**

```python
from src.vectorstore import VectorStoreBuilder

# Initialize builder
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")

# Load existing vector store from disk
vectorstore = builder.load_vectorstore()

print(f"✓ Vector store loaded successfully!")
print(f"✓ Ready for similarity searches")

# Now you can use it for recommendations
# Example: Find similar anime
results = vectorstore.similarity_search("action-packed sci-fi adventure", k=5)
for result in results:
    print(f"- {result.page_content}")
```

---

## Usage Patterns

### Pattern 1: Basic Vector Store Creation

```python
from src.vectorstore import VectorStoreBuilder

# Step 1: Create builder
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")

# Step 2: Build and save vectors
builder.build_and_save_vectorstore()

# Step 3: Load vectors for use
vectorstore = builder.load_vectorstore()

print("Vector store ready!")
```

**When to Use:**
- First time setting up the system
- After updating anime data

### Pattern 2: Load Existing Vector Store (Production)

```python
from src.vectorstore import VectorStoreBuilder

# Skip building, directly load existing vectors
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")
vectorstore = builder.load_vectorstore()

# Use for similarity searches
results = vectorstore.similarity_search("romantic comedy anime", k=5)
```

**When to Use:**
- Running the application in production
- Vectors already created and saved
- Want to reduce startup time

### Pattern 3: With Error Handling

```python
from src.vectorstore import VectorStoreBuilder
from utils.custom_exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")
    
    # Build vector store with progress feedback
    logger.info("Building vector store from anime data...")
    builder.build_and_save_vectorstore()
    logger.info("✓ Vector store created and persisted successfully")
    
    # Load for verification
    vectorstore = builder.load_vectorstore()
    logger.info("✓ Vector store loaded and ready for use")
    
except FileNotFoundError as e:
    raise CustomException(
        "Anime data file not found. Check the CSV path.",
        error_detail=e
    )
    
except Exception as e:
    raise CustomException(
        "Vector store creation failed",
        error_detail=e
    )
```

**Features:**
- Informative logging at each step
- Proper error handling
- Exception details captured

### Pattern 4: In a Recommendation Pipeline

```python
from src.vectorstore import VectorStoreBuilder
from langchain.chains import RetrievalQA

class AnimeRecommendationPipeline:
    def __init__(self):
        """Initialize the recommendation pipeline."""
        self.builder = VectorStoreBuilder(
            csv_path="data/anime_with_synopsis.csv"
        )
        self.vectorstore = None
    
    def setup(self):
        """Setup vector store (called once at startup)."""
        # Check if vectors exist, if not create them
        try:
            self.vectorstore = self.builder.load_vectorstore()
            print("✓ Using existing vector store")
        except FileNotFoundError:
            print("Creating new vector store...")
            self.builder.build_and_save_vectorstore()
            self.vectorstore = self.builder.load_vectorstore()
            print("✓ Vector store created")
    
    def get_recommendations(self, user_query: str, k: int = 5):
        """
        Get anime recommendations based on user query.
        
        Args:
            user_query: What the user is looking for (e.g., "action adventure")
            k: Number of recommendations to return
            
        Returns:
            List of similar anime
        """
        if not self.vectorstore:
            self.setup()
        
        # Find similar anime using vector similarity
        results = self.vectorstore.similarity_search(user_query, k=k)
        return results

# Usage
pipeline = AnimeRecommendationPipeline()
pipeline.setup()

# Get recommendations
recommendations = pipeline.get_recommendations(
    user_query="magical girl action", 
    k=5
)

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec.page_content}")
```

**What Happens:**
1. Initialize pipeline with vector store builder
2. On first run: Create vectors and save to disk
3. On subsequent runs: Load existing vectors (fast!)
4. Use vectors to find similar anime based on user queries

---

## Data Flow

```
anime_with_synopsis.csv (Processed Data)
        ↓
[CSVLoader] - Reads the CSV file
        ↓
Documents with text content
        ↓
[CharacterTextSplitter] - Breaks into 1000-char chunks
        ↓
Text chunks (Chunk 1, Chunk 2, Chunk 3, ...)
        ↓
[HuggingFaceEmbeddings] - Converts each chunk to 384-number vector
   └─ sentence-transformers/all-MiniLM-L6-v2
        ↓
Vector embeddings (numerical representation of meaning)
        ↓
[Chroma.from_documents] - Stores vectors with metadata
        ↓
Vector Database (In Memory)
        ↓
[db.persist()] - Saves to disk
        ↓
chroma_db/ (Persisted on Disk)
├── index.bin (vector data)
├── metadata.sqlite (document info)
└── ...
        ↓
[Later: load_vectorstore()] - Reload from disk
        ↓
Ready for Similarity Searches & Recommendations
```

---

## Directory Structure

**Before Vector Store Creation:**
```
Anime_Recommender/
├── data/
│   └── anime_with_synopsis.csv (processed data)
└── src/
    └── vectorstore.py
```

**After Vector Store Creation:**
```
Anime_Recommender/
├── data/
│   └── anime_with_synopsis.csv
├── src/
│   └── vectorstore.py
└── chroma_db/ ← Created by VectorStoreBuilder
    ├── index.bin
    ├── metadata.sqlite
    └── ... (other files)
```

**Important:** Add `chroma_db/` to `.gitignore` since it's automatically generated and large.

---

## Troubleshooting

### Issue: FileNotFoundError - CSV file not found

**Cause:** The CSV path is incorrect

**Solution:**
```python
# ❌ Wrong
builder = VectorStoreBuilder(csv_path="anime.csv")

# ✓ Correct (use relative path from project root)
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")

# ✓ Or use absolute path
import os
csv_path = os.path.join(os.getcwd(), "data", "anime_with_synopsis.csv")
builder = VectorStoreBuilder(csv_path=csv_path)
```

### Issue: FileNotFoundError - chroma_db/ not found when loading

**Cause:** Vector store hasn't been created yet

**Solution:**
```python
# First time setup: build before loading
builder = VectorStoreBuilder(csv_path="data/anime_with_synopsis.csv")
builder.build_and_save_vectorstore()  # Create vectors first
vectorstore = builder.load_vectorstore()  # Then load

# Or check if exists first
import os
if not os.path.exists("chroma_db"):
    builder.build_and_save_vectorstore()
vectorstore = builder.load_vectorstore()
```

### Issue: Memory or performance issues

**Cause:** Chunk size might be too large or too small

**Solution:**
```python
# Current default: chunk_size=1000
# If too slow: use larger chunks (1500-2000)
# If poor quality: use smaller chunks (500-800)

# Note: Modify this in vectorstore.py if needed
splitter = CharacterTextSplitter(
    chunk_size=1500,  # Adjust as needed
    chunk_overlap=0
)
```

---

## Summary

| Concept | Purpose | Example |
|---------|---------|---------|
| **Embedding** | Text → Numbers | "action anime" → [0.2, 0.8, ...] |
| **Chunking** | Single document → Multiple chunks | 2000-char synopsis → 2-3 chunks |
| **Vector DB** | Stores & searches vectors | Chroma stores anime embeddings |
| **Persistence** | Save vectors to disk | chroma_db/ folder |
| **VectorStoreBuilder** | Main utility class | Creates and loads vector database |

---

## Next Steps

After setting up the vector store, you can:
1. [Learn about the Recommender Class](recommender.md) - Uses vector store for recommendations
2. [Understand the Complete Pipeline](pipeline.md) - How components work together
3. [Deploy with Docker](../SETUP.md) - Package the application with vectors included
