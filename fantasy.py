import os 
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")

API_FANTASY = os.getenv("API_KEY_FANTASY")


# def get_fixtures(params):
#     url = "https://v3.football.api-sports.io/fixtures"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(DATA_DIR / "fixtures.json", "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data

# def get_league_standings(params):
#     url = "https://v3.football.api-sports.io/standings"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(DATA_DIR / "standings.json", "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data

# def get_injuries(params):
#     url = "https://v3.football.api-sports.io/injuries"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(DATA_DIR / "injuries.json", "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data


def find_gameweek(gameweek):
    with open (DATA_DIR / "fixtures.json", "r") as file:
        x = json.loads(file.read())
        gameweeks = x["response"]
        gameweek_found = False
        for rounds in gameweeks:
            round = rounds["league"]["round"]
            y = round.split()[3]
            if y == gameweek:
                gameweek_found = True
                return y
        if gameweek_found == False:
            print(f'Gameweek found? => {gameweek_found}. Premier League has 38 Gameweeks')

def correlate_gameweek_fixtures():
    with open (DATA_DIR / "fixtures.json", "r") as file:
        x = json.loads(file.read())
        fixtures = x["response"]
        gameweek_number = find_gameweek(gameweek=str(input("Write a number from 1-38: ")))
        fixtures_gameweek = []
        for ids in fixtures:
            id = ids["fixture"]["id"]
            id_gameweek = ids["league"]["round"]
            id_gameweek_split = id_gameweek.split()[3]
            if gameweek_number == id_gameweek_split:
                fixtures_gameweek.append(id)
        return fixtures_gameweek

def find_injuries():
    with open (DATA_DIR / "injuries.json", "r") as file:
        z = json.loads(file.read())
        info = z["response"]
        fixture_id_gameweek = correlate_gameweek_fixtures()
        injured_players_in_gameweek = []
        for ids in info:
            injuries_id = ids["fixture"]["id"]
            player_id = ids["player"]["name"]
            player_team = ids["team"]["name"]
            available_next = ids["player"]["type"]
            injury_type = ids["player"]["reason"]
            if injuries_id in fixture_id_gameweek:
                injured_players_in_gameweek.append([player_id, player_team, injury_type, available_next])
        return injured_players_in_gameweek

# Nå får jeg kun skader i kamp 1, jeg får ikke alle skader for alle kampene i runde 1.


# get_injuries(params={"season": 2022, "league": 39})
# get_league_standings(params={"season": 2022, "league": 39})
# get_fixtures(params={"season": 2022, "league": 39})


#Seasons available: 2022, 2023, 2024
#Leagues: Prem = 39, 
#Team: Man.Utd = 33

