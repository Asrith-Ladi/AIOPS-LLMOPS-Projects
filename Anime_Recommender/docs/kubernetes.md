- Kubernetes files define two main components: **Deployment** (how to run your app) and **Service** (how to expose your app)

- You can create separate files for Deployment and Service, or combine them into a single YAML file

- In the Service spec, the `type` field has 3 main choices:
  1. **ClusterIP** - Internal-only access. Used when the app should only be accessible within the cluster (not exposed to the internet)
  2. **NodePort** - Exposes the app on a port of each node. Accessible from outside the cluster but requires node IP
  3. **LoadBalancer** - Exposes the app externally through a cloud provider's load balancer. Used for public internet access
### Secret Management

#### Why We Can't Include `.env` Files

```
Problem: Never commit .env files to version control
├── Contains sensitive credentials (API keys, tokens)
├── Visible to everyone with repository access
├── Major security risk if repository is public
└── Violates industry best practices (12-factor app)
```

#### How Kubernetes Handles Secrets

Instead of including `.env` files:

1. **Create a Secret in the cluster:** Store environment variables securely in Kubernetes
2. **Reference the Secret in Deployment:** Use `secretRef` to inject variables into containers
3. **App receives variables:** Container has access to environment variables without them being in the image

**Example implementation:**

```yaml
envFrom:
  - secretRef:
      name: llmops-secrets  # Reference to secret stored in cluster
```

The app reads these injected environment variables as if they were in an `.env` file, but they're stored securely in Kubernetes instead.

### Container Image Pull Policy

#### imagePullPolicy Explained

```yaml
imagePullPolicy: IfNotPresent
```

| Policy | Behavior | Use Case |
|--------|----------|----------|
| **Always** | Always pull fresh image from registry (DockerHub, GCP, ECR) | Production (ensures latest version) |
| **IfNotPresent** | Use local image if exists; pull only if not found | Local development with Minikube |
| **Never** | Only use local images; fail if not found | Testing with pre-loaded images |

**For our setup:**
- Using `IfNotPresent` because we built the image locally with Minikube
- Kubernetes first checks local Docker daemon
- If not found, would pull from external registry
- Since we're not using DockerHub/GCP registry, we rely on local build

**How to build image for Minikube:**

```bash
# Build image and load into Minikube's Docker daemon
minikube image load llmops-app:latest

# Or build directly inside Minikube
eval $(minikube docker-env)
docker build -t llmops-app:latest .
```