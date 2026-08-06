import os 
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime
import fantasy


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")
API_AGENT = os.getenv("API_KEY_AGENT")

client = genai.Client(api_key=API_AGENT)


def filter_data_before_prompt():
    injuries = fantasy.find_injuries()
    injuries.sort()
    return injuries

print(filter_data_before_prompt())

def analyzing_with_model():
    response = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=["", "Hvilke skader skjedde i runde 1 av sesongen i PL? Oppsummer spiller, skade og hvilket lag."] )

    return response.text

