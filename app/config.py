# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("(ERROR) Missing OpenAI API key. Make sure you have a .env file with OPENAI_API_KEY.")