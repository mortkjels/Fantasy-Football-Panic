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

def question_to_parse():
    question = input("Hva vil du vite? ")

    query = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=[f'{question}', 'Gi meg svaret jeg gir på dette formatet, som et dictionary: season: x, gameweek: y, request: z. '] )
    return query.text

print(question_to_parse())

def analyzing_with_model():
    info = question_to_parse()
    response = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=[f'{""}'] )

    return response.text

