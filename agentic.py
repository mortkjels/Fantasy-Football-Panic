import os 
from google import genai
from pathlib import Path
from dotenv import load_dotenv
import fantasy
import json

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")
API_AGENT = os.getenv("API_KEY_AGENT")

client = genai.Client(api_key=API_AGENT)

def question_to_parse():
    question = input("Hva vil du vite? ")

    query = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=[f'{question}', 'Gi meg svaret jeg gir på dette formatet, som et json-format: {"season": x, "gameweek": y, "request": z.} Request er typ da injuries, transfers, etc. Hva man spør etter'] )
    output = query.text
    plain_text = output.split("\n")
    plain_text_to_json = json.loads(plain_text[1])
    return plain_text_to_json

parsed_question = question_to_parse()

filename = fantasy.find_correct_file(parsed_question)
print(filename)

gameweek = fantasy.find_injuries(filename)

print(gameweek)

def analyzing_with_model():
    info = question_to_parse()
    response = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=[f'{""}'] )

    return response.text

