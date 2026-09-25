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

    prompt = f"""
Du er en query-parser for et fotballdatasett.

Bruk kun informasjonen i brukerens spørsmål.

Brukerens spørsmål:
{question}

Trekk ut nøyaktig disse tre feltene:

- season: sesongen brukeren spør om
- gameweek: runden brukeren spør om
- request: hva brukeren faktisk ønsker informasjon om

Tillatte request-verdier er:
- injuries
- transfers
- fixtures
- standings

Regler:
1. Ikke svar på selve spørsmålet.
2. Ikke forklar noe.
3. Ikke legg til informasjon som ikke finnes i spørsmålet.
4. Hvis brukeren bruker norsk, oversett request til engelsk.
5. "skader", "skadet", "utilgjengelig", "skadde spillere" betyr injuries.
6. "overganger", "kjøp", "salg", "signeringer" betyr transfers.
7. "kamper", "kampprogram", "fixtures" betyr fixtures.
8. "tabell", "stilling", "standings" betyr standings.
9. Returner KUN gyldig JSON.
10. JSON skal ha nøyaktig denne strukturen:

{{
    "season": "YYYY-YY",
    "gameweek": integer,
    "request": "injuries|transfers|fixtures|standings"
}}
"""

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt
    )

    output = response.text.strip()

    return json.loads(output)


parsed_question = question_to_parse()

filename, gameweek = fantasy.find_correct_file(parsed_question)

matches = fantasy.matches_that_gameweek(filename, gameweek)


def analyzing_with_model():
    request = parsed_question["request"]

    prompt = f"""
Du er en fotballanalyse-assistent.

Brukeren ønsker informasjon om:
{request}

DATA:
{matches}

OPPGAVE:
Analyser KUN dataene som er relevante for requesten "{request}".

Viktige regler:
- Ikke finn på informasjon som ikke finnes i DATA.
- Ikke bruk kunnskap utenfor DATA.
- Ikke bland inn andre typer informasjon enn det brukeren ba om.
- Ta med alle relevante lag som finnes i DATA.
- Hvis et lag ikke har relevant informasjon, ikke finn på noe.
- Vær konkret og presis.
- Presenter resultatet på norsk.
- Bruk overskrifter og punktlister.
- Hvis DATA ikke inneholder informasjon som svarer på forespørselen, si tydelig fra om det.

Returner kun den ferdige analysen til brukeren.
"""

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt
    )

    return response.text


print(analyzing_with_model())



