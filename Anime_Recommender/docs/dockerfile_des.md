# Docker & Containerization Documentation

## Overview

The `Dockerfile` is a blueprint that packages the entire Anime Recommender application into a standardized container. It ensures that the application runs identically on any machine—whether it's a developer's laptop, a test server, or production infrastructure—by bundling the code, dependencies, and configuration into a single portable unit.

## Purpose

Docker containerization solves the "works on my machine" problem:

1. **Build** - Creates a container image with Python, dependencies, and the app
2. **Package** - Bundles everything needed to run the application
3. **Deploy** - Runs consistently on any system with Docker installed
4. **Isolate** - Separates application from system dependencies

---

## Key Concepts Explained

### What is Docker?

**Docker** is a containerization platform that packages applications with all their dependencies into a standardized unit called a **container**.

**Real-World Analogy - Shipping Container:**

```
Traditional Shipping (Without Containers):
Company A ships a car
  ↓
Dock worker loads it onto ship
  ↓
Ship travels
  ↓
Different dock unloads it
  ↓
Problem: Different docks have different equipment!
  ↓
Car might get damaged or not fit

Docker Containers (Standardized):
Application packaged in a "container"
  ↓
Container loaded onto any server
  ↓
Server travels (code moves from dev → test → production)
  ↓
Container runs identically everywhere
  ↓
No compatibility issues!
```

### Virtual Machines vs Containers

**Virtual Machine:**
```
Your Computer
├── Operating System (Windows/Mac/Linux)
├── Virtual Machine 1
│   ├── Guest OS (Linux)
│   ├── Libraries
│   ├── Application
│   └── Data
└── Virtual Machine 2
    ├── Guest OS (Linux)
    ├── Different libraries
    ├── Different Application
    └── Different Data

Size: Several GB per VM
```

**Docker Container:**
```
Your Computer
├── Operating System (any OS)
├── Docker Daemon (tool that runs containers)
├── Container 1
│   ├── Application
│   ├── Libraries needed ONLY for this app
│   └── Data
└── Container 2
    ├── Different Application
    ├── Different libraries
    └── Different Data

Size: 100s of MB per container
```

**Key Difference:**
- VMs: Each has its own Operating System (heavyweight)
- Containers: Share the host OS kernel (lightweight)

### Image vs Container

**Image: Blueprint**
```
Dockerfile (Instructions)
    ↓
    Build Process
    ↓
Image (Compressed snapshot)
    - Executable
    - Dependencies
    - Configuration
    - Not running yet (like a package in a box)
```

**Container: Running Instance**
```
Image (Blueprint)
    ↓
    Docker Run Command
    ↓
Container (Running application)
    - Active process
    - In memory
    - Has IP address
    - Can receive requests
```

**Analogy:**
- Image = Recipe
- Container = Cooked meal

### Dockerfile Instructions

A `Dockerfile` is a text file with instructions to build an image. Think of it like a recipe:

```
Recipe for Pizza:
1. Start with pizza dough (base)
2. Add tomato sauce (ingredient)
3. Add cheese (ingredient)
4. Add toppings (ingredient)
5. Bake for 20 minutes (instruction)
6. Serve (final instruction)

Dockerfile for Application:
1. Start with Python 3.10 (base image)
2. Set environment variables (configuration)
3. Create work directory (setup)
4. Install system dependencies (ingredients)
5. Copy application code (ingredient)
6. Install Python packages (ingredient)
7. Expose port 8501 (configuration)
8. Run the app (final instruction)
```

---

## Dockerfile Breakdown

### Line 1: Base Image

```dockerfile
FROM python:3.10-slim
```

**What This Does:**
- Starts with an existing base image
- Uses `python:3.10-slim` = Python 3.10 in a minimal Linux environment
- "slim" means only essential packages (keeps container small)

**Analogy:**
```
Like buying a partially constructed house instead of building from scratch:
- You don't start from bare land (OS from scratch)
- You buy a completed foundation + walls (Python + OS)
- You add your own rooms and furniture (your application)
```

**Why Use Base Images?**
```
Without base image:
1. Download and install Linux OS
2. Compile Python from source
3. Install system libraries
4. Takes hours, 1GB+ size

With python:3.10-slim base:
1. Already has Python 3.10 installed
2. Already has minimal OS
3. Ready to use
4. Takes minutes, ~200MB size
```

### Lines 3-5: Environment Variables

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

**What This Does:**
Sets Python behavior inside the container

| Variable | Purpose | Value | Why? |
|----------|---------|-------|------|
| **PYTHONDONTWRITEBYTECODE** | Don't create `.pyc` files | = 1 (enabled) | Containers are ephemeral; no point caching bytecode |
| **PYTHONUNBUFFERED** | Print immediately | = 1 (enabled) | Logs appear real-time in container logs; easier debugging |

**Example Impact:**

```python
# Without PYTHONUNBUFFERED
print("Starting application...")
# Output appears 5 seconds later (buffered)

# With PYTHONUNBUFFERED
print("Starting application...")
# Output appears immediately (unbuffered)
```

### Line 8: Work Directory

```dockerfile
WORKDIR /app
```

**What This Does:**
- Creates `/app` directory inside the container
- All subsequent commands run from this directory
- Like `cd /app` on your computer

**Container File System:**
```
Container Root /
├── bin/      (Linux executables)
├── usr/      (system files)
├── app/      ← WORKDIR (our application here)
│   ├── src/
│   ├── docs/
│   ├── data/
│   ├── pipeline/
│   ├── requirements.txt
│   └── Dockerfile
└── ...
```

**Analogy:**
Like saying "go into the `app` folder and do everything in there"

### Lines 11-14: Install System Dependencies

```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

**What This Does:**
- `apt-get update`: Update package list (like Windows Update)
- `apt-get install`: Install packages needed
  - `build-essential`: Tools for compiling C/C++ packages
  - `curl`: Tool to download files
- `rm -rf /var/lib/apt/lists/*`: Delete cache to reduce container size

**Why Needed?**
```
Some Python packages (like sentence-transformers) need to compile C code
Need system tools to build them:
  - gcc (C compiler)
  - make (build tool)
  - libc-dev (C libraries)
These are in build-essential
```

**Container Size Optimization:**
```
Bad:
RUN apt-get update
RUN apt-get install -y build-essential
# Leaves cache files taking 200MB

Good:
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
# Removes cache immediately, saves 200MB

Our approach:
We use the "good" pattern with &&
```

### Line 17: Copy Files

```dockerfile
COPY . .
```

**What This Does:**
- Copies everything from your computer (`.`) to container (`.`)
- Copies from: `/Anime_Recommender/` on your computer
- Copies to: `/app/` inside container

**Container After Copy:**
```
Container /app/
├── src/
│   ├── data_loader.py
│   ├── vector_store.py
│   ├── recommender.py
│   └── prompt_template.py
├── data/
│   ├── anime_with_synopsis.csv
│   └── anime_updated.csv
├── docs/
├── pipeline/
│   └── pipeline.py
├── app/
│   └── app.py
├── requirements.txt
├── setup.py
└── README.md
```

### Line 20: Install Python Packages

```dockerfile
RUN pip install --no-cache-dir -e .
```

**What This Does:**
1. Runs `pip install -e .`
   - `pip`: Python package installer
   - `-e`: "Editable" install (development mode)
   - `.`: Current directory (has `setup.py`)
2. `--no-cache-dir`: Don't cache wheels (saves space)

**How It Works:**
```
Step 1: pip reads setup.py
Step 2: setup.py lists dependencies (requirements.txt entries)
Step 3: pip downloads and installs each package:
         - langchain
         - langchain-community
         - langchain-groq
         - chromadb
         - streamlit
         - pandas
         - python-dotenv
         - sentence-transformers
         - langchain_huggingface
Step 4: Packages installed in /usr/local/lib/python3.10/site-packages/
```

**Why `-e` (editable)?**
```
Normal install (`pip install .`):
  - Installs package files in site-packages
  - Not ideal for development

Editable install (`pip install -e .`):
  - Creates link to /app/ directory
  - Changes to code are reflected immediately
  - Good for development/testing
```

### Line 23: Expose Port

```dockerfile
EXPOSE 8501
```

**What This Does:**
- Tells Docker this container will listen on port 8501
- Documents which port the app uses
- Doesn't actually open the port (that's done with `-p` flag when running)

**Port Explanation:**
```
Port = Door number on a computer
  - Port 80 = HTTP web requests
  - Port 443 = HTTPS web requests
  - Port 8501 = Streamlit default port

Application listens on port 8501
  Users can access at: http://localhost:8501
```

**Analogy:**
```
EXPOSE is like putting a sign on your house that says:
"Visitors can enter through door #8501"

But the sign alone doesn't open the door.
The `-p` flag when launching container opens the door:
docker run -p 8501:8501 anime-recommender
          (host port):(container port)
```

### Line 26: Run Command

```dockerfile
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0","--server.headless=true"]
```

**What This Does:**
Runs the Streamlit application when container starts

**Command Breakdown:**

| Part | Meaning |
|------|---------|
| `streamlit` | The program to run |
| `run` | Streamlit's run subcommand |
| `app/app.py` | Which app file to run |
| `--server.port=8501` | Use port 8501 |
| `--server.address=0.0.0.0` | Listen on all network interfaces (not just localhost) |
| `--server.headless=true` | Run without browser opening |

**What Happens:**
```
Container Starts
    ↓
Dockerfile CMD executes
    ↓
streamlit run app/app.py starts
    ↓
Application loads:
  1. Imports all modules
  2. Loads pipeline (vector DB, models)
  3. Initializes Streamlit web server
    ↓
Server listens on port 8501
    ↓
User can access at: http://localhost:8501
```

**Why `0.0.0.0`?**
```
localhost (127.0.0.1):
  - Only accessible from your machine
  - Can't access from another computer

0.0.0.0 (all interfaces):
  - Accessible from inside container
  - Accessible from host machine
  - Accessible from other machines on network
  
Perfect for Docker because:
- Host machine calls: http://localhost:8501
- Routing automatically reaches container
```

---

## How to Build the Docker Image

### Step-by-Step Build Process

```
Dockerfile
    ↓
[Read FROM → download python:3.10-slim]
    ↓
[Run ENV → set environment variables]
    ↓
[Run WORKDIR → create /app directory]
    ↓
[Run apt-get update && install build-essential, curl]
    ↓
[Run COPY → copy all files to /app]
    ↓
[Run pip install → download and install Python packages]
    ↓
[Run EXPOSE → document port 8501]
    ↓
[Store CMD → when container runs, execute this]
    ↓
[Complete] → Image created!
```

### Build Command

```bash
docker build -t anime-recommender:latest .
```

**Parameters:**
- `build`: Docker command to build an image
- `-t anime-recommender:latest`: Tag the image with name:version
- `.`: Build from current directory (where Dockerfile is)

**Output Example:**
```
[1/7] FROM docker.io/library/python:3.10-slim
[2/7] ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
[3/7] WORKDIR /app
[4/7] RUN apt-get update && apt-get install -y...
[5/7] COPY . .
[6/7] RUN pip install --no-cache-dir -e .
[7/7] EXPOSE 8501
Successfully tagged anime-recommender:latest
```

---

## How to Run the Docker Container

### Basic Run

```bash
docker run -p 8501:8501 anime-recommender:latest
```

**Parameters:**
- `run`: Start a container
- `-p 8501:8501`: Map port
  - Left 8501: Port on your machine
  - Right 8501: Port in container
- `anime-recommender:latest`: Which image to use

**What Happens:**
```
1. Docker creates container from image
2. Container starts (CMD executes)
3. Streamlit starts listening on 8501
4. Browser can access: http://localhost:8501
5. Ctrl+C to stop
```

### Run in Background

```bash
docker run -d -p 8501:8501 --name anime-app anime-recommender:latest
```

**Parameters:**
- `-d`: Detached mode (background)
- `--name anime-app`: Give container a name
- Returns a container ID

**Manage Container:**
```bash
# Check if running
docker ps

# View logs
docker logs anime-app

# Stop container
docker stop anime-app

# Start container again
docker start anime-app

# Remove container
docker rm anime-app
```

### Run with Environment Variables

```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=gsk_abc123... \
  -e HUGGINGFACE_API_KEY=hf_xyz789... \
  anime-recommender:latest
```

**Note:** Never hardcode secrets! Use environment variables or Docker secrets in production.

### Run with Volume Mount (for development)

```bash
docker run -p 8501:8501 \
  -v D:/Projects/AIOPS/Anime_Recommender:/app \
  anime-recommender:latest
```

**Parameters:**
- `-v host_path:container_path`: Mount folder
- Changes to code are reflected immediately
- Great for developing inside a container

---

## Container Lifecycle

```
Image → Container Start → Running → Container Stop → Removed
  ↓                           ↓
Blueprint              Actual process

Image never changes         Container is ephemeral
(stored on disk)            (can be created/destroyed)
```

**Analogy:**
```
Image = Blueprint of a house
Container = Actual built house

You can:
- Have multiple containers from same image
- Delete a container and rebuild it
- Image stays the same
- Each container is independent
```

---

## Complete Workflow

### Development → Production

```
Local Development:
  python app/app.py
  
Containerized:
  docker build -t anime-recommender .
  docker run -p 8501:8501 anime-recommender
  
Production Deployment:
  Push image to Docker Registry (Docker Hub, AWS ECR)
  Pull image to production server
  docker run -d -p 8501:8501 anime-recommender
  Kubernetes/Docker Compose orchestrates multiple containers
```

### File Inclusion in Container

```
Your Machine (Anime_Recommender/)          Container (/app/)
├── src/                            →      ├── src/
├── docs/                           →      ├── docs/
├── data/                           →      ├── data/
├── pipeline/                       →      ├── pipeline/
├── app/                            →      ├── app/
├── config/                         →      ├── config/
├── utils/                          →      ├── utils/
├── requirements.txt                →      ├── requirements.txt
├── setup.py                        →      ├── setup.py
├── Dockerfile  (not copied)               ├── Dockerfile
├── .env        (NOT copied!)              ├── chroma_db/     (created at runtime)
└── venv/       (NOT copied!)              └── logs/          (created at runtime)
```

**Important:** 
- `.env` not in container (use environment variables instead)
- `venv/` not in container (pip install recreates packages)
- `chroma_db/` created at runtime
- `logs/` created when app runs

---

## Optimization Tips

### Reduce Image Size

**Current Size:** ~1.5-2GB (all dependencies)

**To Reduce:**

1. Use `slim` variant (already doing this)
2. Multi-stage builds (not needed for simple apps)
3. Remove development dependencies:
```dockerfile
# Option: Install only production dependencies
RUN pip install --no-cache-dir \
  langchain langchain-community langchain-groq \
  chromadb streamlit pandas python-dotenv \
  sentence-transformers langchain_huggingface
```

### Speed Up Build

Current build takes 5-10 minutes. To speed up:

1. **Order matters:** Put less-changing lines first
```dockerfile
# Good:
FROM python:3.10-slim
RUN apt-get update && apt-get install...  (changes rarely)
COPY . .  (copied when code changes)
RUN pip install...  (changes often)

# Bad:
COPY . .  (copied first, invalidates cache)
RUN pip install...  (always rebuilds)
RUN apt-get...  (always reinstalls)
```

2. **Separate requirements:**
```dockerfile
# Separate layer for dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Separate layer for code
COPY . .
RUN pip install --no-cache-dir -e .
```

---

## Troubleshooting

### Issue: "Port 8501 already in use"

**Cause:** Another container or app using port 8501

**Solution:**
```bash
# Use different port
docker run -p 8502:8501 anime-recommender

# Or find/stop other service using 8501
docker ps
docker stop <container_id>
```

### Issue: "Module not found" inside container

**Cause:** Missing dependency in setup.py or requirements.txt

**Solution:**
```bash
# Rebuild image
docker build --no-cache -t anime-recommender .

# Verify setup.py has all dependencies
cat setup.py

# Or install manually:
docker run -it anime-recommender /bin/bash
pip install missing_package
```

### Issue: "Can't access localhost:8501"

**Cause:** Container not properly exposed

**Check:**
```bash
# Verify port mapping
docker ps -a

# Should show: 0.0.0.0:8501->8501/tcp

# Check container logs
docker logs container_id

# Try accessing from container
docker exec container_id curl http://localhost:8501
```

### Issue: "No API key" error

**Cause:** Environment variables not passed to container

**Solution:**
```bash
# Pass from .env
docker run -p 8501:8501 \
  --env-file .env \
  anime-recommender

# Or individual variables
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  anime-recommender
```

### Issue: "Chroma DB not found"

**Cause:** Vector database needs to be built first

**Solution:**
```bash
# In container, run pipeline
docker run -it anime-recommender python pipeline/build_pipleline.py

# Or mount volume with chroma_db folder
docker run -p 8501:8501 \
  -v D:/Projects/AIOPS/Anime_Recommender/chroma_db:/app/chroma_db \
  anime-recommender
```

---

## Best Practices

### ✓ Do's

- ✅ Use specific Python version (3.10, not latest)
- ✅ Use slim base image (lighter than full image)
- ✅ Clean up package cache (`rm -rf /var/lib/apt/lists/*`)
- ✅ Use environment variables for configuration
- ✅ Expose only necessary ports
- ✅ Include .dockerignore file
- ✅ Build with meaningful tag names
- ✅ Document how to run the container

### ✗ Don'ts

- ❌ Don't hardcode API keys in Dockerfile
- ❌ Don't use root user unnecessarily
- ❌ Don't run multiple services in one container
- ❌ Don't forget to commit Dockerfile to version control
- ❌ Don't mount entire filesystem for production
- ❌ Don't use `latest` tag in production

---

## Docker vs Kubernetes

### Docker (This Project)

```
What: Containerization tool
Where: Run single container on single machine
Use: Development, testing, small deployments

docker run anime-recommender
    ↓
One container on your machine
```

### Kubernetes (Mentioned in Overview.md)

```
What: Container orchestration platform
Where: Manage many containers across many machines
Use: Production, scaling, high availability

kubernetes deploy anime-recommender
    ↓
Multiple containers across multiple machines
    ↓
Auto-scaling, load balancing, failover
```

The Dockerfile we created is the foundation for both!

---

## Summary

The `Dockerfile`:

1. **Packages** the application with all dependencies
2. **Automates** the entire setup process
3. **Ensures** consistency across all environments
4. **Simplifies** deployment
5. **Isolates** the application in a container
6. **Enables** Docker Compose and Kubernetes use

After building the image, you get a self-contained package that runs identically everywhere.

---

## Next Steps

After understanding the Dockerfile:

1. [Learn Docker Compose](../SETUP.md) - Run multiple containers together
2. [Deploy to Cloud](../SETUP.md) - Run on GCP, AWS, Azure
3. [Kubernetes Basics](../SETUP.md) - Scale across machines
4. [CI/CD Pipeline](../SETUP.md) - Automatically build and deploy
5. [Monitor with Grafana](../SETUP.md) - Track container health
