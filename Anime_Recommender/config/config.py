import os

from dotenv import load_dotenv

load_dotenv() # loads the .env file into environment variables

# fetching API keys from environment variables and storing the value into this variable to be used across the project
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant" # find models from ehre
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

