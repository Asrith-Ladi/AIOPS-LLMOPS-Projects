# AIOPS-LLMOPS-Projects

Advanced AI Operations and Large Language Model Operations projects leveraging modern ML frameworks and cloud infrastructure.

## Projects

### 🎌 Anime Recommender
An intelligent anime recommendation system powered by LLMs and vector embeddings.

**Features:**
- AI-powered anime recommendations using Groq LLM
- Vector embeddings via HuggingFace models
- Fast similarity search with Chroma DB
- Web UI with Streamlit
- Containerized deployment with Docker & Kubernetes
- Real-time monitoring with Grafana

**Tech Stack:**
- **LLM:** Groq
- **Embeddings:** HuggingFace
- **Vector DB:** Chroma DB
- **Framework:** LangChain
- **Frontend:** Streamlit
- **Deployment:** Docker, Kubernetes (Minikube)
- **Monitoring:** Grafana Cloud
- **Infrastructure:** GCP VM
- **SCM:** GitHub

## Project Structure

```
AIOPS-LLMOPS-Projects/
├── Anime_Recommender/
│   ├── src/
│   │   ├── config/
│   │   │   └── config.py
│   │   └── utils/
│   │       ├── logger.py
│   │       └── custom_exception.py
│   ├── app/
│   │   └── streamlit_app.py
│   ├── pipeline/
│   │   └── recommendation_pipeline.py
│   ├── data/
│   │   └── anime_with_synopsis.csv
│   ├── docs/
│   │   ├── utils/
│   │   │   ├── logger.md
│   │   │   └── custom_exception.md
│   │   └── SETUP.md
│   ├── images/
│   ├── requirements.txt
│   ├── setup.py
│   ├── .env (Not committed - add your API keys)
│   └── project.md
├── common/
│   ├── logger.py
│   ├── custom_exception.py
│   └── LOGGER.md
├── docs/
│   ├── utils/
│   │   └── custom_exception.md
│   └── SETUP.md
├── .gitignore
├── README.md
└── setup.py
```

## Quick Start

### Prerequisites
- Python 3.8+
- Git
- pip

### Setup Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Linux/Mac
```

### Install Dependencies

```bash
pip install -r Anime_Recommender/requirements.txt
pip install -e .
```

### Configure API Keys

1. Get Groq API key: https://console.groq.com/keys
2. Get HuggingFace token: https://huggingface.co/settings/tokens
3. Create `.env` file in `Anime_Recommender/` directory:

```
GROQ_API_KEY=your_groq_key_here
HUGGINGFACE_API_KEY=your_huggingface_token_here
```

### Run Application

```bash
cd Anime_Recommender
streamlit run app/streamlit_app.py
```

## Documentation

### Core Modules

- **[Logger Documentation](common/LOGGER.md)** - Logging and monitoring setup
- **[Custom Exception Documentation](docs/utils/custom_exception.md)** - Custom error handling
- **[Setup Documentation](docs/SETUP.md)** - Package configuration and setup

### Project Guides

- **[Project Setup Guide](Anime_Recommender/project.md)** - Complete project setup instructions
- **[Architecture Documentation](Anime_Recommender/docs/SETUP.md)** - Technical architecture overview

## Development Workflow

### 1. Clone Repository
```bash
git clone https://github.com/Asrith-Ladi/AIOPS-LLMOPS-Projects.git
cd AIOPS-LLMOPS-Projects
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r Anime_Recommender/requirements.txt
pip install -e .
```

### 4. Configure Environment
```bash
# Create .env file in Anime_Recommender/ with API keys
cp Anime_Recommender/.env.example Anime_Recommender/.env
# Edit .env and add your API keys
```

### 5. Run Tests
```bash
pytest
```

### 6. Start Development
```bash
cd Anime_Recommender
streamlit run app/streamlit_app.py
```

## Deployment

### Docker Deployment

```bash
cd Anime_Recommender
docker build -t anime-recommender .
docker run -p 8501:8501 anime-recommender
```

### Kubernetes Deployment

```bash
# Using Minikube locally
minikube start
kubectl apply -f k8s_deployment.yaml
```

### Cloud Deployment (GCP)

1. Set up GCP VM
2. Install Docker, Minikube, kubectl
3. Configure Kubernetes manifests
4. Deploy using CI/CD pipeline

## Monitoring

The project includes monitoring capabilities via Grafana Cloud:

- View cluster metrics
- Monitor application performance
- Track deployments and replicas
- Set up alerts

## Project Guidelines

### Code Standards

- **Python Style:** PEP 8 compliant
- **Documentation:** Docstrings for all functions and classes
- **Error Handling:** Use `CustomException` for custom errors
- **Logging:** Use centralized logger from `common.logger`

### Commit Message Format

```
[Feature] Brief description
[Fix] Brief description
[Docs] Brief description
[Refactor] Brief description
```

### Pull Request Process

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive messages
5. Push to GitHub
6. Create Pull Request (PR) with description

## Troubleshooting

### Virtual Environment Issues

**Problem:** venv not activating
```bash
# Ensure you're using the correct path
venv\Scripts\activate  # Windows
./venv/bin/activate    # Linux/Mac
```

### API Key Issues

**Problem:** FileNotFoundError for .env file
- Ensure .env file is in `Anime_Recommender/` directory
- File should not be committed to git (already in .gitignore)

### Dependency Issues

**Problem:** ImportError or ModuleNotFoundError
```bash
# Reinstall dependencies
pip install -r Anime_Recommender/requirements.txt --force-reinstall
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

**Ladi Asrith**
- GitHub: [@Asrith-Ladi](https://github.com/Asrith-Ladi)
- Email: your.email@example.com

## Support

For issues and questions:
- Open an [Issue](https://github.com/Asrith-Ladi/AIOPS-LLMOPS-Projects/issues)
- Check existing documentation in `/docs` folder
- Review project guides in respective project folders

## Roadmap

- [ ] Add unit tests for core modules
- [ ] Implement CI/CD pipeline
- [ ] Add more anime datasets
- [ ] Enhance recommendation algorithm
- [ ] Deploy to production GCP
- [ ] Add user authentication
- [ ] Create admin dashboard

## Changelog

### Version 1.0.0 (Current)

**Added:**
- Project structure and setup
- Core recommender logic
- Streamlit UI
- Docker containerization
- Kubernetes deployment configuration
- Documentation for all modules
- .gitignore and README

---

Last Updated: February 21, 2026
