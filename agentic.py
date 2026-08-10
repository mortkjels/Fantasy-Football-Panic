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
        contents=[f'{question}', 'Uavhengig av hvordan spørsmålet er formulert, '
        'så skal du hente ut infoen som sesong, runde og request (skader (ute, utilgjengelig, injuries, skadet), overganger (kjøpt, salg, transfers, signeringer) etc), som et '
        'json-format. Jeg skal kun ha output fra deg som dette'
        '{"season": x, "gameweek": y, "request": z.}. '
        'Request kan komme på norsk, men returner i formatet på engelsk. Så injuries, transfers, fixtures, standings etc.'] )
    output = query.text
    plain_text = output.split("\n")
    plain_text_to_json = json.loads(plain_text[1])
    return plain_text_to_json

parsed_question = question_to_parse()

filename, gameweek = fantasy.find_correct_file(parsed_question)

injuries = fantasy.find_injuries(filename, gameweek)

def analyzing_with_model():
    response = client.models.generate_content(
        model="gemma-4-31b-it", 
        contents=[f'{injuries}','Oppsummer dette til et leselig og pent format slik at jeg kan ha kontroll over byttene mine for neste runde i FPL. Jeg ønsker at du tar for deg alle lag.'] )

    return response.text

print(analyzing_with_model())


# Ikke godkjent
# Hvilke spillere var ute i åpningsrunden 2023?

# Godkjent 
# Skader i runde 1 i 2022
# Hvem var skadet i første runde i 2022?
# Skader PL GW 1 2022
# Skader fra gameweek 20 i 2024

