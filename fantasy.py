import os 
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")

API_FANTASY = os.getenv("API_KEY_FANTASY")


def get_fixtures(params):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_FANTASY}
    response = requests.get(url, 
                        headers=headers,
                        params = params)
    formatted_data = json.dumps(response.json(), indent=4)
    with open(DATA_DIR / "fixtures.txt", "w", encoding="utf-8") as file:
        file.write(formatted_data)
    return formatted_data

def get_league_standings(params):
    url = "https://v3.football.api-sports.io/standings"
    headers = {"x-apisports-key": API_FANTASY}
    response = requests.get(url, 
                        headers=headers,
                        params = params)
    formatted_data = json.dumps(response.json(), indent=4)
    with open(DATA_DIR / "standings.txt", "w", encoding="utf-8") as file:
        file.write(formatted_data)
    return formatted_data

def get_injuries(params):
    url = "https://v3.football.api-sports.io/injuries"
    headers = {"x-apisports-key": API_FANTASY}
    response = requests.get(url, 
                        headers=headers,
                        params = params)
    formatted_data = json.dumps(response.json(), indent=4)
    with open(DATA_DIR / "injuries.txt", "w", encoding="utf-8") as file:
        file.write(formatted_data)
    return formatted_data


get_injuries(params={"season": 2022, "league": 39})
get_league_standings(params={"season": 2022, "league": 39})
get_fixtures(params={"season": 2022, "league": 39})


#Seasons available: 2022, 2023, 2024
#Leagues: Prem = 39, 
#Team: Man.Utd = 33

