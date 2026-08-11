import os 
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SQUAD_DIR = BASE_DIR / "Squad"
load_dotenv(BASE_DIR / ".env")

API_FANTASY = os.getenv("API_KEY_FANTASY")


# def get_fixtures(params, filename):
#     url = "https://v3.football.api-sports.io/fixtures"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(DATA_DIR / filename, "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data

# def get_league_standings(params, filename):
#     url = "https://v3.football.api-sports.io/standings"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(DATA_DIR / filename, "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data

# def get_injuries(params, filename):
#     url = "https://v3.football.api-sports.io/injuries"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(DATA_DIR / filename, "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data

# def get_players(params, filename):
#     url = "https://v3.football.api-sports.io/players"
#     headers = {"x-apisports-key": API_FANTASY}
#     response = requests.get(url, 
#                         headers=headers,
#                         params = params)
#     formatted_data = json.dumps(response.json(), indent=4)
#     with open(SQUAD_DIR / filename, "w", encoding="utf-8") as file:
#         file.write(formatted_data)
#     return formatted_data

def find_correct_file(data):
    season = data["season"]
    request = data["request"]
    gameweek = data["gameweek"]
    file_to_choose = f"{request}{season}.json"
    return file_to_choose, gameweek

def find_gameweek(gameweek, filename):
    new_file = filename.replace("injuries", "fixtures")
    intended_gameweek = gameweek
    with open (DATA_DIR / new_file, "r") as file:
        x = json.loads(file.read())
        gameweeks = x["response"]
        gameweek_found = False
        for rounds in gameweeks:
            round = rounds["league"]["round"]
            y = round.split()[3]
            if y == str(intended_gameweek):
                gameweek_found = True
                return y
        if gameweek_found == False:
            print(f'Gameweek found? => {gameweek_found}. Premier League has 38 Gameweeks')

def correlate_gameweek_fixtures(filename, gameweek):
    new_file = filename.replace("injuries", "fixtures")
    intended_gameweek = gameweek
    with open (DATA_DIR / new_file, "r") as file:
        x = json.loads(file.read())
        fixtures = x["response"]
        gameweek_number = find_gameweek(gameweek=intended_gameweek, filename=new_file)
        fixtures_gameweek = []
        for ids in fixtures:
            id = ids["fixture"]["id"]
            id_gameweek = ids["league"]["round"]
            id_gameweek_split = id_gameweek.split()[3]
            if gameweek_number == id_gameweek_split:
                fixtures_gameweek.append(id)
        return fixtures_gameweek

def matches_that_gameweek(filename, gameweek):
    new_file = filename.replace("injuries", "fixtures")
    intended_gameweek = gameweek
    with open (DATA_DIR / new_file, "r") as file:
        x = json.loads(file.read())
        fixtures = x["response"]
        matches = []
        match_ids = correlate_gameweek_fixtures(new_file, intended_gameweek)
        for ids in fixtures:
            id = ids["fixture"]["id"]
            home_team = ids["teams"]["home"]["name"]
            away_team = ids["teams"]["away"]["name"]
            if id in match_ids:
                matches.append([home_team, "vs", away_team])
    return matches

def find_injuries(filename, gameweek):
    with open (DATA_DIR / filename, "r") as file:
        z = json.loads(file.read())
        info = z["response"]
        fixture_id_gameweek = correlate_gameweek_fixtures(filename, gameweek)
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

