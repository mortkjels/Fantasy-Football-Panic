import os 
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv
import fantasy
import json

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
API_AGENT = os.getenv("API_KEY_AGENT")

client = genai.Client(api_key=API_AGENT)


def filter_data_before_prompt():
    with open (fantasy.DATA_DIR / "injuries.json", "r") as file:
        z = json.loads(file.read())

        # print(z['response'][0])
        for key, value in z.items():
            for item in value:
                print(item)


def analyzing_with_model():
    
    response = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=["", "Hvilke skader skjedde i runde 1 av sesongen i PL? Oppsummer spiller, skade og hvilket lag."] )

    return response.text

filter_data_before_prompt()
