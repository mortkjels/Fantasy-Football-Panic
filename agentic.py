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
        model="gemini-3.1-flash-lite", 
        contents=[f'{question}', 'Uavhengig av hvordan spørsmålet er formulert, '
        'så skal du hente ut infoen som sesong, runde og request (skader (ute, utilgjengelig, injuries, skadet), overganger (kjøpt, salg, transfers, signeringer) etc), som et '
        'json-format. Jeg skal kun ha output fra deg som dette'
        '{"season": x, "gameweek": y, "request": z.}. '
        'Request kan komme på norsk, men returner i formatet på engelsk. Så injuries, transfers, fixtures, standings etc.'
        'Det er ekstremt viktig at du tar hensyn til request. Det viktigste er det jeg ønsker fra den visse sesongen og runden, typisk skader, overganger, fixtures osv'] )
    output = query.text
    plain_text = output.split("\n")
    plain_text_to_json = json.loads(plain_text[0])
    return plain_text_to_json

parsed_question = question_to_parse()

filename, gameweek = fantasy.find_correct_file(parsed_question)

matches = fantasy.matches_that_gameweek(filename, gameweek)

def analyzing_with_model():
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", 
        contents=[f'{matches}','Oppsummer dette til et leselig og pent format slik at jeg kan ha kontroll over byttene mine for neste runde i FPL. Jeg ønsker at du tar for deg alle lag og gir meg hvem som er skadet for hvert lag.'] )

    return response.text

print(analyzing_with_model())


