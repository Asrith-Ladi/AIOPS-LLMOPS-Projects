# Prompt Template Documentation

## Overview

The `prompt_template.py` module defines the instructions that guide the Large Language Model (LLM) on how to respond to user questions about anime recommendations. It structures how the AI should think, prioritize information, and format its responses.

## Purpose

The prompt template performs two critical roles:
1. **Control** - Sets rules and guidelines for the LLM behavior
2. **Structure** - Defines the expected format and content of responses
3. **Context** - Specifies how to use retrieved anime data in recommendations

---

## Key Concepts Explained

### What is a Prompt?

A **prompt** is an instruction you give to an AI model to tell it what to do. Think of it like giving directions to a person.

**Simple Examples:**

```
❌ Bad Prompt:
"Recommend anime"
(Too vague - AI doesn't know what you want)

✓ Good Prompt:
"Recommend 3 anime similar to Cowboy Bebop. 
Include the plot and why it's similar."
(Clear, specific, structured)
```

### What is a Prompt Template?

A **prompt template** is a reusable blueprint with placeholder variables that get filled in dynamically.

**Think of it like a form:**

```
Traditional Form (Paper):
┌─────────────────────────────────────┐
│ Name: _______________               │
│ Email: _______________              │
│ Question: _______________           │
└─────────────────────────────────────┘

Prompt Template (Digital):
┌─────────────────────────────────────┐
│ You are an anime recommender.        │
│                                     │
│ Context: {context}                  │
│ (This gets filled in dynamically)   │
│                                     │
│ User Question: {question}           │
│ (This gets filled in with real data)│
└─────────────────────────────────────┘
```

### Why Use Prompt Templates?

**Without Templates (Fragile):**
```python
# Problem: Inconsistent prompts
response1 = llm.generate("Tell me about anime")  # Weak prompt
response2 = llm.generate("Recommend anime with plot")  # Better prompt
# Results will be inconsistent!
```

**With Templates (Reliable):**
```python
# Solution: Consistent format every time
prompt_template = get_anime_prompt()
response1 = llm.generate(prompt_template.format(context=data1, question=q1))
response2 = llm.generate(prompt_template.format(context=data2, question=q2))
# Both use identical structure → Consistent quality!
```

### LLM Behavior Control

A prompt template is like giving the AI a **role and rules**:

```
Role: "You are an expert anime recommender"
      ↓
      AI knows its purpose

Rules: "Suggest exactly 3 anime"
       ↓
       AI follows constraints

Guidelines: "Include plot summary and explanation"
            ↓
            AI formats response consistently

Honesty Rule: "Don't fabricate information"
              ↓
              AI avoids hallucinations
```

---

## PromptTemplate Class (LangChain)

**PromptTemplate** is a class from the LangChain library that manages prompt templates.

### How It Works

```
PromptTemplate Object
    ↓
Stores template string with {placeholders}
    ↓
When .format() called: Replaces {placeholder} with actual data
    ↓
Returns formatted prompt string
    ↓
Sends to LLM
```

**Example:**

```python
from langchain.prompts import PromptTemplate

# Create template with placeholders
template = PromptTemplate(
    template="Hello {name}, you like {hobby}",
    input_variables=["name", "hobby"]
)

# Use template
prompt = template.format(name="Alice", hobby="anime")
# Result: "Hello Alice, you like anime"

# Use again with different data
prompt2 = template.format(name="Bob", hobby="manga")
# Result: "Hello Bob, you like manga"
```

---

## get_anime_prompt() Function

### Function Signature

```python
def get_anime_prompt():
    """
    Returns a prompt template for anime recommendations.
    
    Returns:
        PromptTemplate: Configured prompt template for anime recommendations
        
    Use this to get consistent prompts across your application
    """
```

### What This Function Does

```
Step 1: Define Template String
───────────────────────────────
Creates a multi-line instruction string
Contains:
- Role statement for the AI
- Instructions on what to do
- Placeholder variables {context} and {question}

Step 2: Create PromptTemplate Object
─────────────────────────────────────
Wraps template with LangChain's PromptTemplate class
Specifies which variables need to be filled in

Step 3: Return Template
───────────────────────
Returns configured template ready to use
Caller provides actual context and question data

Output: PromptTemplate object
      ↓
Ready to format with real data
```

### Return Value

- **Type:** PromptTemplate object
- **Usage:** Can call `.format(context="...", question="...")` to fill placeholders
- **Purpose:** Ensures consistent AI behavior across all recommendation requests

---

## Template Breakdown

The anime recommendation template has several important sections:

### Section 1: Role Definition

```python
"You are an expert anime recommender. 
 Your job is to help users find the perfect anime 
 based on their preferences."
```

**What This Does:**
- Gives the LLM an identity and purpose
- Sets expectations for quality and relevance
- Frames the LLM as an expert (not a novice)

**Impact:**
- With role: AI provides thoughtful, relevant recommendations
- Without role: AI might give generic or unrelated suggestions

**Example Impact:**

```
Without Role:
User: "I like action anime"
AI: "There are many genres of anime"
(Generic, not helpful)

With Role:
User: "I like action anime"
AI: "You might enjoy Demon Slayer for intense action sequences..."
(Specific, knowledgeable)
```

### Section 2: Task Instructions

```python
"For each question, suggest exactly three anime titles. 
 For each recommendation, include:
 1. The anime title.
 2. A concise plot summary (2-3 sentences).
 3. A clear explanation of why this anime matches 
    the user's preferences.
 
 Present your recommendations in a numbered list 
 format for easy reading."
```

**What This Does:**
- Specifies exact number of recommendations (3)
- Defines what information to include for each anime
- Specifies output format (numbered list)

**Why Important:**
- **Consistency:** Every recommendation has same structure
- **Completeness:** Never missing plot or explanation
- **Usability:** Numbered format is easy for users to read

**Example Output Format It Produces:**

```
1. Fullmetal Alchemist
   Plot: Two brothers search for the Philosopher's Stone 
   after a failed alchemical experiment...
   Why it matches: You love action with deep character 
   development and complex plots.

2. Attack on Titan
   Plot: Humanity fights giant humanoid creatures 
   threatening their survival...
   Why it matches: Features intense action sequences and 
   high-stakes drama.

3. Demon Slayer
   Plot: A boy joins a demon-hunting organization after 
   his family is slaughtered...
   Why it matches: Combines stunning animation with 
   non-stop action and emotional storytelling.
```

### Section 3: Context Placeholder

```python
"Context:
 {context}"
```

**What This Does:**
- Tells LLM: "Here's relevant data from our database"
- `{context}` is a placeholder that gets filled with:
  - Similar anime from vector database
  - Their plots, genres, summaries
  - Information matching user preferences

**How It Gets Filled:**

```
Vector Database Search:
User asks: "I like sci-fi action"
    ↓
Vector DB finds similar anime:
- Cowboy Bebop (sci-fi, action)
- Trigun (sci-fi, action)
- Gundam (sci-fi, action)
    ↓
This becomes {context}
    ↓
Template becomes:
"Context:
 1. Cowboy Bebop - Space bounty hunter...
 2. Trigun - Outlaw with supernatural abilities...
 3. Gundam - Military sci-fi mecha battles..."
```

**Example Context:**

```
Context:
Cowboy Bebop: Space western with bounty hunters, visually stunning, 
complex characters, philosophical themes. Genres: Sci-Fi, Action, Drama

Trigun: Wandering outlaw with superhuman powers, blend of action and 
comedy, emotional depth. Genres: Sci-Fi, Action, Adventure

Gundam: Military sci-fi with giant mecha, intricate plots, moral complexity. 
Genres: Sci-Fi, Action, Military
```

### Section 4: Question Placeholder

```python
"User's question:
 {question}"
```

**What This Does:**
- Placeholder for the actual user query
- Gets filled with what user types

**Examples of {question}:**

```
❶ "I've watched Naruto and loved it. 
   What should I watch next?"

❷ "I'm looking for a romantic comedy anime 
   with good animation quality"

❸ "Recommend anime with supernatural powers 
   and action sequences"
```

### Section 5: Honesty Constraint

```python
"If you don't know the answer, respond honestly 
 by saying you don't know — 
 do not fabricate any information."
```

**What This Does:**
- Prevents the AI from making up anime that doesn't exist
- Prevents false plot summaries
- Ensures factual accuracy

**Why Critical:**
- LLMs can "hallucinate" (create false information)
- This constraint reduces that risk
- Users get reliable recommendations

**Example Prevention:**

```
❌ Without Constraint:
User: "Recommend anime about time-traveling pirates"
AI: "I recommend 'Temporal Pirates 2024' which is about..."
(PROBLEM: This anime doesn't exist! Made up by AI)

✓ With Constraint:
User: "Recommend anime about time-traveling pirates"
AI: "I don't know of a popular anime matching that exact 
description, but here are anime with time travel or pirates..."
(BETTER: Honest about limitations)
```

---

## Usage Patterns

### Pattern 1: Basic Usage

```python
from src.prompt_template import get_anime_prompt

# Get the prompt template
prompt_template = get_anime_prompt()

# Fill in the placeholders
anime_context = """
Cowboy Bebop: Space western bounty hunters, philosophical themes
Trigun: Outlaw with cool powers, action and comedy mix
Ghost in the Shell: Cyber espionage, deep philosophical questions
"""

user_question = "I like sci-fi anime with good action sequences"

# Format the template with real data
final_prompt = prompt_template.format(
    context=anime_context,
    question=user_question
)

# Now final_prompt is ready to send to the LLM
print(final_prompt)
```

**Output:**
```
You are an expert anime recommender. Your job is to help users 
find the perfect anime based on their preferences.

Using the following context, provide a detailed and engaging response 
to the user's question.

For each question, suggest exactly three anime titles. For each 
recommendation, include:
...
Context:
Cowboy Bebop: Space western bounty hunters...
...

User's question:
I like sci-fi anime with good action sequences
```

### Pattern 2: With LLM Integration

```python
from src.prompt_template import get_anime_prompt
from langchain_groq import ChatGroq
from langchain.chains import LLMChain

# Initialize LLM (Groq in this case)
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7
)

# Get prompt template
prompt = get_anime_prompt()

# Create LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# Use the chain
response = chain.run(
    context="Retrieved anime data here...",
    question="I like action anime"
)

print(response)
```

**What Happens:**
1. Chain receives context and question
2. Prompt template formats them together
3. Formatted prompt goes to Groq LLM
4. LLM follows template instructions
5. Returns recommendation response

### Pattern 3: In Recommendation Pipeline

```python
from src.prompt_template import get_anime_prompt
from src.vectorstore import VectorStoreBuilder
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

class AnimeRecommender:
    def __init__(self):
        # Initialize vector store
        self.vectorstore = VectorStoreBuilder(
            csv_path="data/anime_with_synopsis.csv"
        ).load_vectorstore()
        
        # Initialize LLM
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768")
        
        # Get prompt template
        self.prompt = get_anime_prompt()
    
    def recommend(self, user_query: str) -> str:
        """
        Generate anime recommendations based on user query.
        
        Args:
            user_query: What the user is looking for
            
        Returns:
            Formatted recommendations from the LLM
        """
        # Step 1: Search vector database for similar anime
        similar_anime = self.vectorstore.similarity_search(
            user_query, 
            k=5  # Get top 5 matches
        )
        
        # Step 2: Convert search results to context
        context = "\n".join([
            anime.page_content for anime in similar_anime
        ])
        
        # Step 3: Format prompt with context and question
        formatted_prompt = self.prompt.format(
            context=context,
            question=user_query
        )
        
        # Step 4: Send to LLM
        response = self.llm.invoke(formatted_prompt)
        
        return response.content

# Usage
recommender = AnimeRecommender()
recommendations = recommender.recommend(
    "I want a romantic comedy anime"
)
print(recommendations)
```

**Complete Flow:**

```
User Input: "I want romantic comedy"
    ↓
[Vector Database Search]
Find anime with "romance" and "comedy"
    ↓
Retrieve context: "Kaguya-sama...", "Love is War...", ...
    ↓
[Prompt Template Format]
Merge:
- Role: "You are an expert..."
- Instructions: "Suggest 3 anime..."
- Context: Retrieved anime data
- Question: "romantic comedy anime"
    ↓
[LLM Processing]
Groq processes the formatted prompt
Following the template's instructions
    ↓
[Generate Response]
Returns 3 anime with plots and explanations
    ↓
User sees: Numbered list with recommendations
```

### Pattern 4: Custom Modifications

If you want to modify the prompt for different use cases:

```python
from langchain.prompts import PromptTemplate

# Default anime recommender prompt
def get_anime_prompt():
    template = """..."""  # Original
    return PromptTemplate(template=template, 
                         input_variables=["context", "question"])

# Custom prompt for manga recommendations
def get_manga_prompt():
    template = """
You are an expert manga recommender...
For each recommendation, include:
1. The manga title
2. A brief description
3. Why it matches the user's preferences
...
"""
    return PromptTemplate(template=template,
                         input_variables=["context", "question"])

# Custom prompt for different style
def get_casual_anime_prompt():
    template = """
Hey! I'm your friendly anime buddy. Based on what you like, 
here are my top picks...
"""
    return PromptTemplate(template=template,
                         input_variables=["context", "question"])
```

---

## How It Works in the Pipeline

```
User Input
    ↓
[User Types: "I like action anime with humor"]
    ↓
Vector Database Search
    ↓
[Returns relevant anime with plots]
    ↓
Prompt Template Formatting
    ↓
[get_anime_prompt() creates template]
[Fills {context} with retrieved anime]
[Fills {question} with user input]
    ↓
Complete Formatted Prompt
    ↓
Example:
"You are an expert anime recommender...
Context: Cowboy Bebop is..., Trigun is..., ...
User's question: I like action anime with humor
Your well-structured response:"
    ↓
LLM (Groq)
    ↓
[Processes prompt following instructions]
[Suggests exactly 3 anime]
[Includes plot summaries]
[Explains why they match]
    ↓
Recommendation Response
    ↓
User Receives: Numbered recommendations
```

---

## Key Template Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| **{context}** | Retrieved anime data from vector DB | Cowboy Bebop details, Trigun details, ... |
| **{question}** | What the user is asking for | "Recommend action anime" |

---

## Template Design Principles

### Principle 1: Be Specific

```
❌ Vague: "Suggest good anime"
✓ Specific: "Suggest exactly 3 anime with plot summary 
            and explanation of why it matches preferences"
```

### Principle 2: Define Output Format

```
❌ Undefined: "Tell me about anime"
✓ Defined: "Present as numbered list"
```

### Principle 3: Set Constraints

```
❌ Unlimited: "Recommend as many anime as you think"
✓ Constrained: "Recommend exactly 3 anime"
```

### Principle 4: Guard Against Errors

```
❌ Risky: "Make recommendations"
✓ Safe: "If you don't know, say you don't know — 
         don't fabricate information"
```

---

## Troubleshooting

### Issue: LLM Returns Wrong Number of Recommendations

**Cause:** Template instruction might be unclear or LLM isn't following it

**Solution:**
```python
# Make instruction more explicit
template = """
...
IMPORTANT: You MUST suggest EXACTLY THREE anime. 
Not 2, not 4, exactly 3.

Recommendation 1: [title]
...
Recommendation 2: [title]
...
Recommendation 3: [title]
...
"""
```

### Issue: LLM Fabricates Non-Existent Anime

**Cause:** Honesty constraint not emphasized enough

**Solution:**
```python
# Strengthen the constraint
template = """
...
CRITICAL: Only recommend anime that actually exist.
Do NOT invent anime titles or plot details.
If you cannot find matching anime in the context,
explicitly state: "I don't have recommendations that match this."
...
"""
```

### Issue: Inconsistent Formatting in Responses

**Cause:** Output format instruction is vague

**Solution:**
```python
# Provide exact format example
template = """
...
Format your response EXACTLY like this:

1. [Anime Title]
   Plot: [2-3 sentence summary]
   Why Match: [explanation]

2. [Anime Title]
   Plot: [2-3 sentence summary]
   Why Match: [explanation]

3. [Anime Title]
   Plot: [2-3 sentence summary]
   Why Match: [explanation]
...
"""
```

### Issue: Context Not Being Used

**Cause:** Template might need explicit instruction to use context

**Solution:**
```python
# Make context usage mandatory
template = """
...
Using ONLY the information provided in the Context section,
recommend anime. Do not use your training data for recommendations.

Context:
{context}

Based on the context above, here are 3 recommendations:
...
"""
```

---

## Best Practices

### ✓ Do's

- ✅ Be specific about number of recommendations
- ✅ Define exact output format with examples
- ✅ Set constraints to prevent errors
- ✅ Test prompt regularly with different inputs
- ✅ Include "don't know" instruction
- ✅ Keep instructions clear and concise

### ✗ Don'ts

- ❌ Don't use vague language ("good", "nice", "cool")
- ❌ Don't specify too many recommendations (>5)
- ❌ Don't skip output format definition
- ❌ Don't assume LLM will know what to do
- ❌ Don't forget honesty constraints
- ❌ Don't make template too long/complex

---

## Summary Table

| Aspect | Purpose | Example |
|--------|---------|---------|
| **Template** | Reusable blueprint with placeholders | `"{context}\n{question}"` |
| **Role** | Gives AI identity and purpose | "You are an expert..." |
| **Instructions** | Specifies what to do | "Suggest exactly 3..." |
| **Format** | Defines output structure | "Numbered list..." |
| **Constraints** | Sets limits and rules | "Exactly 3", "Don't fabricate" |
| **{context}** | Retrieved data from vector DB | Database search results |
| **{question}** | User's actual query | "I like action anime" |

---

## Next Steps

After understanding prompts, you can:
1. [Learn about the Recommender Class](recommender.md) - Uses prompts with LLM
2. [Understand Vector Store](vector_store.md) - Provides context data
3. [View Complete Pipeline](pipeline.md) - How all components work together
4. [Deploy Application](../SETUP.md) - Run the complete system
