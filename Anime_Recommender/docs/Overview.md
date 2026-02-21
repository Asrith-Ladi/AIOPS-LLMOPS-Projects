# AIOPS Project Documentation

![AI Anime Recommender](images/AI%20Anime%20Recommender.png)

## Project Overview

This project is an AI-powered anime recommendation system that leverages large language models (LLMs) and vector databases to provide intelligent recommendations based on user preferences and data analysis.

---

## Tech Stack

### AI & Machine Learning
- **Groq** - Large Language Model (LLM) for processing and generating recommendations
- **HuggingFace** - Embedding model for converting text data into numerical vectors. Since LLMs cannot directly interact with CSV files, this service handles: extracting data, chunking files, converting rows into documents, generating embeddings, and storing them in a vector database
- **LangChain** - Generative AI framework that facilitates seamless interaction between the application and the LLM

### Data & Storage
- **Chroma DB** - Local vector database for storing and retrieving embeddings generated from application data

### Frontend & UI
- **Streamlit** - Framework for building the user interface and web application frontend

### Container & Orchestration
- **Docker** - Containerization technology for packaging the application for deployment
- **Minikube** - Local Kubernetes cluster setup for development and testing environments
- **kubectl** - Command-line interface for managing and interacting with Kubernetes clusters (creating nodes, pods, etc.)

### Cloud & Infrastructure
- **GCP VM** (Google Cloud Platform Virtual Machine) - Cloud-based virtual machine for hosting and running the application
- **Grafana Cloud** - Monitoring and observability platform for Kubernetes clusters (includes 14-day free trial)

### Version Control
- **GitHub** - Source code management (SCM) platform for project versioning and collaboration

---

## Project Architecture & Workflow

![Workflow](images/workflow.png)

### Phase 1: Project Setup

**API Configuration**
- Create two API keys: one for Groq account and another for HuggingFace account
- Store these credentials securely in environment variables (.env file)

### Phase 2: Core Implementation

**Configuration Module**
- Loads and manages environment variables containing API keys and model configurations
- Specifies which LLM and embedding models to use

**Data Loader**
- Extracts data from source files (CSV, JSON, etc.)
- Processes and stores the data into Chroma DB for efficient retrieval

**Prompt Template**
- Defines instructions and guidelines for the LLM
- Determines how the model should format and structure its responses

**Recommender Class**
- Core recommendation engine that processes user queries
- Implements the recommendation logic and algorithms

**Training & Recommendation Pipeline**
- Trains the recommendation system using loaded data converted to vectors
- Processes user queries and returns personalized recommendations
- Handles real-time inference and response generation

**Streamlit Application**
- Web-based user interface for interacting with the recommendation system
- Allows users to query and receive recommendations

### Phase 3: Deployment

**Containerization with Docker**
- **Dockerfile**: Contains instructions for containerizing the application, including dependencies and runtime configuration

**Kubernetes Deployment**
- **Kubernetes Manifest Files**: Define deployment specifications including:
  - Number of replicas for load balancing
  - Node requirements and configurations
  - Service definitions for accessibility
  - Short form: K8s Deploy

**Cloud Infrastructure Setup**
- **GCP VM Installation**: Sets up the virtual machine with three essential components:
  1. **Docker Engine** - Required for running containerized applications; serves as the foundation for Kubernetes
  2. **Minikube** - Creates a local Kubernetes cluster on the VM for orchestration
  3. **kubectl** - Enables command-line interaction with the Kubernetes cluster

**Security & API Management**
- **Code Versioning**: API keys are never exposed in version control
- **Kubernetes Injection**: API keys and secrets are securely injected into the Kubernetes cluster at runtime, maintaining code safety and compliance

**GitHub Integration**
- Automated pipeline that integrates with your repository
- Workflow: Code is pushed to GitHub → Docker image is built from Dockerfile → Application is deployed using Kubernetes manifests → Live application is created and updated

### Phase 4: Monitoring & Observability

**Grafana Cloud**
- Monitors the running Kubernetes cluster in real-time
- Provides visibility into:
  - Number of active nodes
  - Service status and health
  - Active deployments and replicas
  - Resource utilization and performance metrics
- Eliminates the need for manual VM monitoring

---

---

## Phase 1: Development Environment Setup

### Creating Virtual Environment

Create an isolated Python environment to manage project dependencies independently:

```bash
python -m venv venv
```

**What this does:**
- Creates a new virtual environment named `venv` in the current folder
- Isolates project dependencies from system Python

![venv creation](images/venv.png)

### Activating Virtual Environment

Activate the virtual environment to use isolated Python:

```bash
venv\Scripts\activate
```

**Post-activation prompt:**
```
(venv) D:\Projects\AIOPS\Anime_Recommender>
```

The `(venv)` prefix indicates the virtual environment is active.

---

## Phase 2: API Configuration & Setup

### Groq API Key

**Purpose:** LLM API for generating recommendations

**Setup Steps:**
1. Visit: [Groq Console](https://console.groq.com/keys)
2. Sign up or log in to your Groq account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save the key securely

![Groq API Key](images/Groq_API_key.png)

### HuggingFace API Key

**Purpose:** Embedding model for converting text to vectors

**Setup Steps:**
1. Visit: [HuggingFace Tokens](https://huggingface.co/settings/tokens)
2. Click on your profile picture in the top-right corner
3. Select "Access tokens" from the dropdown menu
4. Create a new token
5. Copy and save the token securely

![HuggingFace API Key](images/HuggingFaceKey.png)

### Environment File (.env) Creation

Store your API keys securely in a `.env` file (add to `.gitignore` to prevent exposure):

![Environment File Format](images/env_key_format.png)

**.env File Location:** `Anime_Recommender/.env`

**Format:**
```
GROQ_API_KEY=your_groq_key_here
HUGGINGFACE_API_KEY=your_huggingface_token_here
```

---

## Phase 3: Data Preparation

### Dataset Location

**Path:** `Anime_Recommender/data/anime_with_synopsis.csv`

**Data Source:** My Anime List database

**How it works:**
- Raw anime data containing titles, genres, and synopses
- Recommendation engine uses genre and synopsis similarity
- Example: Users who like "Naruto" often enjoy "Black Clover" or "Bleach"
- Similar recommendations apply across the anime catalog

**Data Processing:**
- CSV file is loaded and processed by the Data Loader
- Text is converted into embeddings via HuggingFace
- Embeddings are stored in Chroma DB for fast similarity search

---

## Phase 4: Project Structure & Dependencies

### requirements.txt

**Location:** `Anime_Recommender/requirements.txt`

**Purpose:** Lists all Python libraries required for the project

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### Project Directory Structure

```
Anime_Recommender/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py          # API and database configuration
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging utilities
│       └── custom_exception.py # Custom exception handling
├── data/
│   └── anime_with_synopsis.csv
├── requirements.txt
├── setup.py
├── .env                        # API keys (add to .gitignore)
└── .gitignore
```

**Directory Descriptions:**
- **config/** - Manages API credentials and database connection setup
- **utils/** - Contains helper functions and utilities
  - `logger.py` - Centralized logging configuration
  - `custom_exception.py` - Custom exception classes for error handling
- **data/** - Dataset files for training and recommendations
- `.env` - Environment variables (API keys) - **Never commit to version control**

### setup.py Installation

**Location:** `Anime_Recommender/setup.py`

**Installation command:**
```bash
pip install -e .
```

**What this does:**
- Reads `setup.py` configuration
- Installs the project in editable mode (`-e` flag)
- Automatically installs all dependencies from `requirements.txt`
- Allows code changes to take effect immediately without reinstalling

![setup.py Installation](images/setup.py.png)

---

## Phase 5: Configuration Module

### config.py Setup

The `config.py` module centralizes all configuration management:

**Location:** `Anime_Recommender/src/config/config.py`

**Responsibilities:**
- Load environment variables from `.env` file
- Manage API keys for Groq and HuggingFace
- Configure database connection parameters (Chroma DB)
- Store model configurations and paths
- Provide centralized access to all settings

**Example structure:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
CHROMA_DB_PATH = "data/chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

---
