# Anime Recommender Documentation

## Overview

The `AnimeRecommender` class is the core recommendation engine that combines vector database search with an LLM to deliver intelligent, personalized anime recommendations. It bridges two critical systems: the vector store (for finding similar anime) and the language model (for generating natural, conversational responses).

## Purpose

The anime recommender performs three critical functions:
1. **Retrieve** - Finds similar anime from the vector database based on user query
2. **Combine** - Merges retrieved anime information with the prompt template
3. **Generate** - Uses the LLM to create natural, personalized recommendation responses

---

## Key Concepts Explained

### What is a Recommender System?

A **recommender system** is software that suggests products or content based on user preferences.

**Simple Example - Movie Recommender:**

```
User: "I like action movies"
    ↓
[System finds movies like]: Top Gun, Mission Impossible, Die Hard...
    ↓
[System reasons]: These have action, explosions, adventure...
    ↓
System suggests: "You might also like Fast & Furious because it has 
                  high-speed action and thrilling car chases"
```

**Anime Recommender - Our System:**

```
User: "I want action-packed anime with romance"
    ↓
[Vector DB finds similar anime]: 
  - Attack on Titan (action)
  - Your Name (romance)
  - Demon Slayer (action scenes)
    ↓
[LLM reasons about them]
    ↓
System suggests: "I recommend Attack on Titan because it combines 
                  intense action sequences with emotional relationships..."
```

### Two-Part Architecture

The recommender works in two phases:

**Phase 1: Search (Vector Database)**
```
User Query: "romantic comedy anime"
    ↓
Vector Database Search
    ↓
Find anime embeddings similar to "romantic comedy"
    ↓
Retrieved Matches:
  - Kaguya-sama: Love is War
  - Ouran High School Host Club
  - My Love Story
```

**Phase 2: Reasoning (Language Model)**
```
Retrieved Anime + User Query + Prompt Template
    ↓
LLM Processing
    ↓
Generate natural response explaining WHY each anime matches
    ↓
"I recommend Kaguya-sama because it masterfully blends 
 romantic tension with hilarious comedy...it features two 
 brilliant characters in a high school power struggle..."
```

### Temperature (Creativity Control)

**Temperature** is a setting that controls how creative/random the LLM's responses are.

**Low Temperature (0):**
```
Temperature = 0
↓
AI is deterministic (always same answer for same question)
↓
Good for: Recommendations that should be consistent
↓
Example: Always recommend the same 3 anime for "action anime"
```

**High Temperature (0.7-0.9):**
```
Temperature = 0.7-0.9
↓
AI is creative (different answers each time)
↓
Risk: May hallucinate or "make up" anime
↓
Example: Might reference non-existent anime or plot details
```

**Our System Uses:** Temperature = 0 (deterministic, safe)

### Retrieval Chains

A **retrieval chain** is a LangChain component that orchestrates the retrieval + reasoning pipeline automatically.

**Without Retrieval Chain (Manual):**
```python
# User would do this:
results = vector_db.search(query)          # Search step
formatted_context = format(results)         # Format step
prompt = template.format(context=context)   # Prompt step
response = llm.generate(prompt)             # LLM step
```

**With Retrieval Chain (Automated):**
```python
# System does this automatically:
chain.invoke({"input": query})

# The chain handles:
# 1. Searching vector DB ✓
# 2. Formatting results ✓
# 3. Creating prompt ✓
# 4. Calling LLM ✓
```

---

## AnimeRecommender Class

### Constructor

```python
class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
```

**Parameters:**

| Parameter | Type | Purpose | Example |
|-----------|------|---------|---------|
| **retriever** | Retriever | Vector DB retriever for anime search | Chroma retriever instance |
| **api_key** | str | Groq API key for LLM access | "gsk_abc123..." |
| **model_name** | str | Which model to use | "mixtral-8x7b-32768" |

**What Happens During Initialization:**

```
Step 1: Initialize LLM
────────────────────
ChatGroq(
    model="mixtral-8x7b-32768",
    api_key="gsk_abc123...",
    temperature=0  # Deterministic, safe answers
)
Result: self.llm - Ready to process text

Step 2: Load Prompt Template
─────────────────────────────
get_anime_prompt()
Result: self.prompt - Contains instructions for LLM

Step 3: Create LLMChain
──────────────────────
LLMChain(llm=self.llm, prompt=self.prompt)
  - Combines LLM with prompt template
  - Ready to process queries with retrieved context
  
Result: self.chain - Automated recommendation pipeline
```

**Example:**

```python
from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from langchain_groq import ChatGroq

# Step 1: Get retriever from vector store
vector_builder = VectorStoreBuilder(csv_path="", persis_dir="chroma_db")
retriever = vector_builder.load_vector_store().as_retriever()

# Step 2: Initialize recommender
recommender = AnimeRecommender(
    retriever=retriever,
    api_key="your_groq_api_key",
    model_name="mixtral-8x7b-32768"
)

# Step 3: Ready to recommend!
print("Recommender initialized successfully")
```

---

## Methods

### get_recommendations(query)

Generates personalized anime recommendations based on user query.

**Method Signature:**

```python
def get_recommendations(self, query: str):
    """
    Get anime recommendations based on user query.
    
    Args:
        query: User's question or preference description
                Example: "I like action anime with magic systems"
        
    Returns:
        str: Natural language recommendation response
             Example: "I recommend Attack on Titan because..."
    """
```

**Return Value:**
- **Type:** String (natural language response)
- **Content:** 3 anime recommendations with explanations
- **Format:** Follows the prompt template structure

**How It Works:**

```
Input: "I want a romantic comedy anime"
    ↓
[Step 1: Vector DB Retrieval]
Retriever searches Chroma DB with query semantics
    ↓
Retrieved Matches (top results):
  - Kaguya-sama: Love is War
  - Ouran High School Host Club
  - My Love Story
    ↓
[Step 2: Format as Context]
Convert documents to text string:
"Title: Kaguya-sama...Synopsis: Two geniuses..."
"Title: Ouran High School..."
    ↓
[Step 3: Create Prompt Input]
Pass to LLMChain with:
  context = [formatted retrieved anime]
  question = "I want a romantic comedy anime"
    ↓
[Step 4: Apply Prompt Template]
Template automatically inserts:
"You are an expert anime recommender.
 Context: [retrieved anime]
 User's question: [user input]
 Suggest exactly 3 anime..."
    ↓
[Step 5: LLM Processing]
Groq model processes the prompt
Temperature = 0 (deterministic)
    ↓
[Step 6: Return Response]
Output: "I recommend:
         1. Kaguya-sama: Love is War
            [plot summary]
            [explanation]
         
         2. Ouran High School Host Club
         ...
         
         3. My Love Story
         ..."
```

**Example:**

```python
# Initialize recommender (as shown above)
recommender = AnimeRecommender(retriever, api_key, model_name)

# Get recommendations
query = "I like dark psychological anime with mystery"
recommendations = recommender.get_recommendations(query)

# Output example:
# I recommend:
# 
# 1. Death Note
#    Plot: A high school student finds a notebook that can kill anyone...
#    Why it matches: Combines dark themes, psychological warfare, and 
#    mystery elements as main plot drivers.
#
# 2. Steins;Gate
#    Plot: Scientists discover time travel through microwaves...
#    Why it matches: Psychological complexity, deep mysteries about 
#    causality and human relationships...
#
# 3. Monster
#    Plot: A doctor hunts a mysterious patient to stop his crimes...
#    Why it matches: Explores dark psychological human nature with 
#    intricate mystery layers...

print(recommendations)
```

---

## Usage Patterns

### Pattern 1: Basic Recommendation

```python
from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
import os

# Initialize
vector_builder = VectorStoreBuilder(csv_path="", persis_dir="chroma_db")
retriever = vector_builder.load_vector_store().as_retriever()

recommender = AnimeRecommender(
    retriever=retriever,
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768"
)

# Get recommendations
query = "comedy anime that makes me laugh"
recommendations = recommender.get_recommendations(query)
print(recommendations)
```

### Pattern 2: With Error Handling

```python
from src.recommender import AnimeRecommender
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

try:
    recommender = AnimeRecommender(
        retriever=retriever,
        api_key=api_key,
        model_name="mixtral-8x7b-32768"
    )
    
    query = "dark anime"
    recommendations = recommender.get_recommendations(query)
    logger.info(f"Generated recommendations for query: {query}")
    
    return recommendations
    
except ConnectionError as e:
    logger.error(f"Failed to connect to Groq API: {str(e)}")
    raise CustomException("LLM API connection failed", error_detail=e)
    
except Exception as e:
    logger.error(f"Recommendation generation failed: {str(e)}")
    raise CustomException("Failed to generate recommendations", error_detail=e)
```

### Pattern 3: In Recommendation Pipeline

```python
from pipeline.pipeline import AnimeRecommendationPipeline

# Initialize pipeline (handles recommender creation internally)
pipeline = AnimeRecommendationPipeline(persis_dir="chroma_db")

# Get recommendations
query = "I love emotional stories"
recommendations = pipeline.recommend(query)

# Returns natural language recommendations
print(recommendations)
```

### Pattern 4: Interactive Chat Loop

```python
from src.recommender import AnimeRecommender

recommender = AnimeRecommender(retriever, api_key, model_name)

# Simple chat interface
while True:
    user_input = input("\nWhat anime are you looking for? (type 'quit' to exit): ")
    
    if user_input.lower() == 'quit':
        break
    
    try:
        recommendations = recommender.get_recommendations(user_input)
        print("\n" + "="*50)
        print(recommendations)
        print("="*50)
    
    except Exception as e:
        print(f"Error getting recommendations: {e}")
```

### Pattern 5: Integration with Streamlit

```python
import streamlit as st
from src.recommender import AnimeRecommender

@st.cache_resource
def initialize_recommender():
    # Load retriever and create recommender
    vector_builder = VectorStoreBuilder(csv_path="", persis_dir="chroma_db")
    retriever = vector_builder.load_vector_store().as_retriever()
    
    return AnimeRecommender(
        retriever=retriever,
        api_key=st.secrets["GROQ_API_KEY"],
        model_name="mixtral-8x7b-32768"
    )

# Initialize
recommender = initialize_recommender()

# User interface
st.title("Anime Recommender")
user_query = st.text_input("What type of anime do you like?")

if user_query:
    with st.spinner("Finding recommendations..."):
        recommendations = recommender.get_recommendations(user_query)
        st.markdown(recommendations)
```

---

## How It Works in the Complete System

```
User Interface (Streamlit App)
    ↓
User enters: "I like action anime"
    ↓
Application calls: recommender.get_recommendations(query)
    ↓
[Retriever Retrieves]
    1. Searches vector database
    2. Finds anime embeddings similar to query
    3. Returns top 5 matching anime with metadata
    ↓
[Prompt Templates Format]
    1. Creates context from retrieved anime
    2. Inserts into prompt template
    3. Generates instruction prompt for LLM
    ↓
[LLM Processes]
    1. Groq receives formatted prompt
    2. Processes using mixtral model
    3. Temperature=0 ensures consistent output
    ↓
[Response Generated]
    1. LLM returns natural language recommendations
    2. Includes 3 anime with explanations
    3. Follows structured format
    ↓
Application returns recommendations to user
    ↓
User sees: 
    "I recommend:
     1. Attack on Titan...
     2. Demon Slayer...
     3. My Hero Academia..."
```

---

## Key Settings

### LLM Configuration

```python
self.llm = ChatGroq(
    model="mixtral-8x7b-32768",     # Fast, powerful model
    api_key=api_key,                 # Groq authentication
    temperature=0                     # Deterministic (safe)
)
```

**Why These Settings?**

| Setting | Value | Reason |
|---------|-------|--------|
| **model** | mixtral-8x7b-32768 | Fast inference, good quality |
| **temperature** | 0 | Consistent recommendations, no hallucinations |
| **api_key** | from config | Authenticates with Groq service |

### Prompt Configuration

```python
self.prompt = get_anime_prompt()
```

**What Template Includes:**
- Role: "You are an anime recommender expert"
- Instructions: "Suggest exactly 3 anime"
- Guidelines: Include plot, explanation, format
- Safety: "Don't fabricate information"

### Retriever Configuration

```python
retriever = vector_db.as_retriever()
```

**Retrieval behaviors:**
- Uses cosine similarity on embeddings
- Default: Returns top 4 documents
- Customizable: Can adjust k parameter

---

## Error Scenarios & Solutions

### Scenario 1: API Key Invalid

**Error:**
```
AuthenticationError: Invalid API key provided
```

**Cause:** GROQ_API_KEY in .env is wrong or expired

**Solution:**
```bash
# Check .env file
cat .env

# Verify key format
# Should look like: GROQ_API_KEY=gsk_abc123...

# Get new key from: https://console.groq.com/keys
```

### Scenario 2: No Matching Anime

**Error:**
```
ValueError: No similar anime found
```

**Cause:** Query too obscure or specific

**Solution:**
```python
# Try broader query
query = "action anime"  # Instead of "anime about ninja cyborgs with romance"

# System will find similar anime and LLM will explain matches
```

### Scenario 3: Slow Response

**Cause:** LLM is slow or network latency

**Solution:**
```python
# Groq is fast, but network can be slow
# Solution: Add timeout and retry logic
# Example:
try:
    recommendations = recommender.get_recommendations(query)
except TimeoutError:
    print("Taking longer than expected, please wait...")
    # Retry after delay
```

### Scenario 4: Hallucinated Recommendations

**Cause:** Should not happen with temperature=0, but if prompt issues

**Solution:**
```python
# Check prompt template safety constraints
# Ensure it includes: "Don't fabricate, only use provided context"
# System is designed to prevent this
```

---

## Performance Considerations

### Latency Breakdown

Typical recommendation request takes:

```
Query Input
  ↓ (0.1s)
Vector DB Search
  ↓ (0.2s)
Format Context
  ↓ (0.1s)
LLM Request (Groq)
  ↓ (2-5s)  ← Most time here
Format Response
  ↓ (0.1s)
Return to User
─────────────
Total: 2.6-5.6 seconds
```

### Optimization Tips

```python
# 1. Cache retriever
@st.cache_resource
def get_retriever():
    # Load once, reuse many times
    return vector_store.as_retriever()

# 2. Batch queries if possible
# Instead of multiple single requests,
# process in batches

# 3. Monitor token usage
# Groq charges by tokens, optimize prompts
```

---

## Troubleshooting Checklist

| Problem | Check | Fix |
|---------|-------|-----|
| Import fails | Is langchain updated? | `pip install --upgrade langchain langchain-groq` |
| API errors | Is GROQ_API_KEY set? | Check `.env` file, verify key is valid |
| No results | Is vector DB built? | Run `python pipeline/build_pipleline.py` first |
| Slow responses | Network ok? | Check internet, Groq API status page |
| Same responses | Is temperature 0? | Yes, this is correct for consistency |
| Bad recommendations | Query clear? | Try more specific descriptions |

---

## Summary

The `AnimeRecommender` class:

1. **Combines** vector search with LLM reasoning
2. **Retrieves** relevant anime from vector database
3. **Reasons** about why they match user preferences
4. **Generates** naturallanguage recommendations
5. **Returns** formatted, 3 anime suggestions with explanations

It's the final step that transforms raw similarity scores into human-friendly recommendations.

---

## Next Steps

After understanding the recommender:

1. [Review Complete Pipeline](pipeline.md) - How all components work together
2. [Learn Prompt Template](prompt_template.md) - Controls recommendation format
3. [Understand Vector Store](vector_store.md) - Provides the search capability
4. [Deploy Application](../SETUP.md) - Run the Streamlit web app
5. [View Data Loader](data_loader.md) - Understands data pipeline
