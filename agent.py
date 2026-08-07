import os 
from google import genai
from pathlib import Path
from dotenv import load_dotenv
import fantasy


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")
API_AGENT = os.getenv("API_KEY_AGENT")

client = genai.Client(api_key=API_AGENT)

def analyzing_with_model():
    injuries = fantasy.find_injuries()
    response = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=[f'{injuries}', "Hvilke skader skjedde denne runden av sesongen i PL? Gi meg en oppsummering på spiller, skade, potensiell lengde på skade og hvilket lag."] )

    return response.text
