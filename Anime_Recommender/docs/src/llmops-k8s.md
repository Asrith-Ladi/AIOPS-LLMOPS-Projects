# Kubernetes Manifest Documentation (llmops-k8s.yaml)

## Overview

The `llmops-k8s.yaml` file contains Kubernetes configuration for deploying the Anime Recommender application. It defines two critical components:

1. **Deployment** - How to run the containerized application inside Kubernetes
2. **Service** - How to expose the application to users

This single YAML file orchestrates the entire deployment, making it easy to manage, version control, and replicate environments.

---

## Key Concepts

### What is a Manifest?

A Kubernetes manifest is a declarative configuration file describing desired state:

```
Manual Approach (Without Kubernetes):
1. SSH into server
2. Pull Docker image
3. Run container with: docker run -p 80:8501 llmops-app:latest
4. Set environment variables
5. Monitor manually
6. If container crashes, manually restart
7. Scale manually by running more containers

Kubernetes Approach (With Manifest):
1. Write manifest.yaml describing desired state
2. Apply: kubectl apply -f manifest.yaml
3. Kubernetes automatically:
   - Pulls image if needed
   - Starts container
   - Injects secrets
   - Exposes ports
   - Monitors health
   - Restarts on failure
   - Scales to desired replicas
```

### YAML Format

YAML uses indentation for structure (like Python):

```yaml
# Key-value pair
name: llmops-app

# Nested structure (indentation matters!)
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llmops

# List items start with hyphen
envFrom:
  - secretRef:
      name: llmops-secrets
```

---

## Deployment Section Breakdown

### Full Deployment Block

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llmops-app
  labels:
    app: llmops
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llmops
  template:
    metadata:
      labels:
        app: llmops
    spec:
      containers:
      - name: llmops-container
        image: llmops-app:latest
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 8501
        envFrom:
          - secretRef:
              name: llmops-secrets
```

### Line-by-Line Explanation

#### **Line 1: API Version**
```yaml
apiVersion: apps/v1
```

| Component | Meaning |
|-----------|---------|
| `apiVersion: apps/v1` | Which Kubernetes API to use |
| `apps` | Deployment is part of the "apps" API group |
| `v1` | Version 1 (stable API) |

**Context:**
```
Kubernetes has multiple API groups:
- apps/v1 → For Deployments, StatefulSets, DaemonSets
- v1 → Core: Pods, Services, Secrets
- batch/v1 → Jobs, CronJobs
- networking.k8s.io/v1 → NetworkPolicies
```

#### **Line 2: Kind**
```yaml
kind: Deployment
```

Specifies what type of Kubernetes resource we're creating.

**Different Kinds:**
```
Kind: Deployment
├─ Purpose: Run multiple copies of an app
├─ Features: Rolling updates, auto-restart, scaling
├─ Best for: Web applications, services

Kind: StatefulSet
├─ Purpose: Run apps needing persistent identity
├─ Features: Persistent storage, ordered startup
├─ Best for: Databases, caches

Kind: DaemonSet
├─ Purpose: Run one copy on each node
├─ Features: Automatic spread across cluster
├─ Best for: Monitoring agents, log collectors

Kind: Job
├─ Purpose: Run to completion once
├─ Features: Automatic cleanup
├─ Best for: Batch processing, one-time tasks
```

#### **Lines 3-5: Metadata**
```yaml
metadata:
  name: llmops-app
  labels:
    app: llmops
```

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Unique identifier for this deployment | `llmops-app` |
| `labels` | Key-value tags for organization | `app: llmops` |

**Why Labels Matter:**
```
Labels organize resources:
- kubectl get pods -l app=llmops  (Filter pods by label)
- Services use labels to find pods (selector)
- Monitoring tools use labels to track metrics
```

#### **Lines 6-8: Specification**
```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llmops
```

| Field | Purpose | Value | Meaning |
|-------|---------|-------|---------|
| `replicas` | How many copies to run | `1` | Run exactly 1 container instance |
| `selector` | How to identify pods | `matchLabels` | Find pods matching these labels |
| `matchLabels` | Pod label filter | `app: llmops` | Find pods with label `app=llmops` |

**How Deployment Finds Its Pods:**

```
Deployment (llmops-app) says:
"I am responsible for pods with label app: llmops"
     ↓
Kubernetes searches for all pods with app: llmops
     ↓
Found: 2 existing pods with app: llmops
     ↓
Deployment says: "I need 1 replica, but found 2"
     ↓
Action: Delete 1 pod (scale down to 1)
```

#### **Lines 9-11: Template**
```yaml
  template:
    metadata:
      labels:
        app: llmops
```

Template defines the pod structure created by this deployment.

**Pod Template Logic:**
```
Deployment (spec.replicas: 1)
     ↓
Says: "Create 1 pod from the template below"
     ↓
Template (metadata.labels.app: llmops)
     ↓
Creates pod with label app: llmops
     ↓
Pod created matches selector criteria
     ↓
Deployment tracks this pod
```

#### **Lines 12-24: Container Specification**
```yaml
    spec:
      containers:
      - name: llmops-container
        image: llmops-app:latest
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 8501
        envFrom:
          - secretRef:
              name: llmops-secrets
```

**Container Block Breakdown:**

| Field | Purpose | Value | Example |
|-------|---------|-------|---------|
| `containers` | List of containers in this pod | Array | Can have multiple containers |
| `name` | Container identifier | String | `llmops-container` |
| `image` | Container image to run | `registry/image:tag` | `llmops-app:latest` |
| `imagePullPolicy` | How to obtain the image | `Always/IfNotPresent/Never` | `IfNotPresent` |
| `containerPort` | Port the app listens on | `8501` | Streamlit default port |

**Image Pull Policy Details:**

```
imagePullPolicy: IfNotPresent
     ↓
Kubernetes checks locally first:
├─ If image exists locally → Use it
├─ If image doesn't exist → Pull from registry
├─ If registry not specified → Use DockerHub

Benefits for development:
- Faster startup (no network pull)
- Works offline if image already loaded
- Avoids registry authentication issues
```

**Environment Variables via Secrets:**

```yaml
envFrom:
  - secretRef:
      name: llmops-secrets
```

**How This Works:**

```
Kubernetes Secret (llmops-secrets) stored in cluster:
├─ GROQ_API_KEY=sk-xxx...
└─ HUGGINGFACE_API_KEY=hf_xxx...
        ↓
Container injection:
├─ Reads secret reference
├─ Mounts environment variables
└─ Container accesses as env vars

Container sees:
import os
api_key = os.getenv('GROQ_API_KEY')  # Works!
```

**Creating the Secret:**

```bash
# Create secret from environment file
kubectl create secret generic llmops-secrets \
  --from-env-file=.env

# Or create from individual key-value pairs
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY=sk-xxx... \
  --from-literal=HUGGINGFACE_API_KEY=hf_xxx...

# Verify secret exists
kubectl get secrets
kubectl describe secret llmops-secrets
```

---

## Service Section Breakdown

### Full Service Block

```yaml
apiVersion: v1
kind: Service
metadata:
  name: llmops-service
spec:
  type: LoadBalancer
  selector:
    app: llmops
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8501
```

### Service Components Explained

#### **What is a Service?**

Pods are ephemeral (temporary). When a pod crashes and is restarted, its IP address changes. Services solve this:

```
Without Service (Pod IP direct access):
Pod IP: 10.0.0.5
     ↓
User Access: http://10.0.0.5:8501
     ↓
Pod crashes, Kubernetes creates new pod
     ↓
New Pod IP: 10.0.0.7
     ↓
Old URL broken: http://10.0.0.5:8501 ✗

With Service (Stable endpoint):
Service (llmops-service) - Permanent IP/DNS
     ↓
Service -> Find pods with label app: llmops
     ↓
Pod 1 (10.0.0.5:8501)
Pod 2 (10.0.0.6:8501)
     ↓
User Access: http://llmops-service or http://service-ip
     ↓
Pod crashes, new pod created with same label
     ↓
Service automatically routes to new pod ✓
```

#### **Service Type: LoadBalancer**

```yaml
type: LoadBalancer
```

**Three Service Types:**

| Type | Access | Use Case | Example |
|------|--------|----------|---------|
| **ClusterIP** | Internal only | Microservice communication | Database service accessed by app |
| **NodePort** | External via node IP:port | Testing, non-critical apps | `node-ip:30000` |
| **LoadBalancer** | External via cloud provider | Public-facing apps | `my-app.example.com` |

**LoadBalancer Flow:**

```
User Request: http://my-app.example.com
     ↓
Cloud Provider's Load Balancer (AWS/GCP/Azure)
├─ Distributes traffic
├─ Handles SSL/TLS
├─ Monitors health
     ↓
Routes to: Kubernetes Service (llmops-service)
     ↓
Service selects pods: label app=llmops
     ↓
Routes to: Container Port 8501
     ↓
App processes request
```

#### **Service Selector**

```yaml
selector:
  app: llmops
```

Service uses the **same labels as deployment pods**:

```
Deployment creates pods with: labels: app: llmops
Service looks for: selector: app: llmops
     ↓
Match! Service automatically routes to these pods
```

**If Labels Don't Match:**

```
Deployment creates pod with: app: llmops-api
Service looks for: app: llmops
     ↓
No match! Service has no endpoints
     ↓
Requests fail with: no endpoints available
```

#### **Port Mapping**

```yaml
ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
```

**Port Explanation:**

| Port | Layer | Direction | Purpose | Example |
|------|-------|-----------|---------|---------|
| `port: 80` | Service | External | What users access | Users connect to `:80` |
| `targetPort: 8501` | Container | Internal | Where app listens | Streamlit listens on `:8501` |

**Traffic Flow:**

```
External User: http://service-ip:80
     ↓
Service Port 80 (external interface)
     ↓
Kubernetes routing rule:
   "port 80 → targetPort 8501"
     ↓
Routed to Container Port 8501
     ↓
Streamlit App (listening on 8501)
```

**Common Port Configurations:**

```
HTTP Service:
- port: 80 (standard HTTP)
- targetPort: 8080 (app listening)

HTTPS Service:
- port: 443 (standard HTTPS)
- targetPort: 8443 (app listening)

Custom Service:
- port: 3000 (custom)
- targetPort: 3000 (app listening)
```

---

## Complete Workflow: Request to Response

```
1. User Request
   └─ http://llmops-service (or LoadBalancer IP)

2. LoadBalancer (Cloud Provider)
   ├─ Receives request on external IP
   ├─ Routes to Kubernetes Service

3. Service (llmops-service)
   ├─ Matches ports: 80 → 8501
   ├─ Selects pods: label app=llmops
   ├─ Finds available pods

4. Deployment (llmops-app)
   ├─ Created 1 pod (replicas: 1)
   ├─ Pod has label app: llmops
   ├─ Contains container llmops-container

5. Container
   ├─ Image: llmops-app:latest
   ├─ Listening on port 8501
   ├─ Environment variables injected from secret
   ├─ Ready to process request

6. Application
   ├─ Receives request on port 8501
   ├─ Loads vector database
   ├─ Uses LLM with API keys from injected env vars
   ├─ Generates recommendation

7. Response
   ├─ App returns HTML/JSON
   ├─ Service routes back to LoadBalancer
   ├─ LoadBalancer returns to user
   └─ User sees recommendation in browser
```

---

## Deploying the Application

### Prerequisites

```bash
# Install Minikube (local Kubernetes)
minikube start

# Verify cluster is running
kubectl cluster-info

# Build Docker image
docker build -t llmops-app:latest .

# Load image into Minikube (IfNotPresent requires this)
minikube image load llmops-app:latest

# Create secret for API keys
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY=sk-xxx... \
  --from-literal=HUGGINGFACE_API_KEY=hf_xxx...
```

### Deployment Commands

```bash
# Apply the manifest (create deployment + service)
kubectl apply -f llmops-k8s.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Monitor pod creation
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Access the application (port-forward)
kubectl port-forward service/llmops-service 8501:80

# Open browser
http://localhost:8501
```

### Scaling the Application

```yaml
# In llmops-k8s.yaml, change replicas:
spec:
  replicas: 3  # Run 3 copies
```

```bash
# Apply change
kubectl apply -f llmops-k8s.yaml

# Kubernetes automatically:
# 1. Creates 2 more pods (3 - 1 = 2 new)
# 2. Service load-balances across 3 pods
# 3. If one pod fails, 2 others continue serving
```

### Updating the Application

```bash
# Build new version
docker build -t llmops-app:v1.1 .
minikube image load llmops-app:v1.1

# Update manifest
# In llmops-k8s.yaml, change image to:
# image: llmops-app:v1.1

# Apply rolling update
kubectl apply -f llmops-k8s.yaml

# Kubernetes automatically:
# 1. Starts new pod with v1.1
# 2. Waits for health check
# 3. Stops old pod (v1.0)
# 4. Zero downtime!
```

---

## Common Issues & Troubleshooting

### Issue 1: ImagePullBackOff Error

```bash
Error: ImagePullBackOff
Reason: Failed to pull image "llmops-app:latest"
```

**Cause:** Image not found in registry or locally

**Solution:**
```bash
# Verify image exists locally
docker images | grep llmops-app

# If not found, build it
docker build -t llmops-app:latest .

# Load into Minikube
minikube image load llmops-app:latest

# Verify it's loaded
minikube image list | grep llmops-app
```

### Issue 2: CrashLoopBackOff Error

```bash
Error: CrashLoopBackOff
Reason: Container keeps crashing
```

**Cause:** Application crashes due to missing env vars or configuration

**Solution:**
```bash
# Check logs
kubectl logs <pod-name>

# Verify secret exists
kubectl get secrets
kubectl describe secret llmops-secrets

# If secret missing, create it
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY=your-key \
  --from-literal=HUGGINGFACE_API_KEY=your-key

# Restart pod to pick up secret
kubectl delete pod <pod-name>
```

### Issue 3: Service Has No Endpoints

```bash
Service: llmops-service
Endpoints: <none>
```

**Cause:** Service can't find pods (labels don't match)

**Solution:**
```bash
# Check deployment pods have correct labels
kubectl get pods --show-labels

# Verify service selector matches pod labels
kubectl get service llmops-service -o yaml

# Example fix - labels must match:
# Deployment pod labels: app: llmops
# Service selector: app: llmops

# If mismatch, update one of them to match
```

### Issue 4: Can't Access Application

```bash
Error: Cannot connect to http://service-ip:80
```

**Solution:**
```bash
# Use port-forward for local testing
kubectl port-forward service/llmops-service 8501:80

# Access via localhost
http://localhost:8501

# For cloud (AWS/GCP):
# Get external IP of LoadBalancer service
kubectl get service llmops-service

# Access via external IP
http://<EXTERNAL-IP>
```

---

## Best Practices

### 1. Always Use Labels and Selectors
```yaml
# ✓ Good - Consistent labels everywhere
metadata:
  labels:
    app: llmops
    version: v1
    
selector:
  matchLabels:
    app: llmops
```

### 2. Never Hardcode Secrets
```yaml
# ✗ Bad - Secrets in manifest!
env:
  - name: GROQ_API_KEY
    value: sk-xxxx  # EXPOSED!

# ✓ Good - Reference secrets
envFrom:
  - secretRef:
      name: llmops-secrets
```

### 3. Use Specific Image Tags
```yaml
# ✗ Bad - "latest" is unpredictable
image: llmops-app:latest

# ✓ Good - Specific version
image: llmops-app:v1.2.3
```

### 4. Set Resource Requests and Limits
```yaml
# ✓ Good - Tell Kubernetes resource needs
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### 5. Add Health Checks
```yaml
# ✓ Good - Kubernetes knows if app is healthy
livenessProbe:
  httpGet:
    path: /health
    port: 8501
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## Summary

| Component | Purpose | File Location |
|-----------|---------|-----------------|
| **Deployment** | Runs app containers with replicas | llmops-k8s.yaml (lines 1-37) |
| **Service** | Exposes app to users/external traffic | llmops-k8s.yaml (lines 39-50) |
| **Secret** | Stores API keys securely in cluster | Created separately via `kubectl create secret` |
| **Image** | Containerized application | Built with Dockerfile, loaded to Minikube |

The manifest demonstrates a production-ready architecture:
- Replicated pods for reliability
- Service for stable networking
- Secret injection for secure credentials
- LoadBalancer for external access
