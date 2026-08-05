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
                print(f'Gameweek found? => {gameweek_found}. It is Gameweek: {y}')
                break
        if gameweek_found == False:
            print(f'Gameweek found? => {gameweek_found}. Premier League has 38 Gameweeks')
find_gameweek(gameweek="1")

# def find_injuries():
#     find_gameweek()
#     with open (DATA_DIR / "injuries.json", "r") as file:
#         z = json.loads(file.read())
#         info = z["response"]
#         injuries = []
#         for items in info:
#             injury_date = items["fixture"]["date"]
#             if injury_date >= startdate and injury_date <= enddate:
#                 injuries.append(items)
#             else:
#                 break
#         print(injuries[0])

# get_injuries(params={"season": 2022, "league": 39})
# get_league_standings(params={"season": 2022, "league": 39})
# get_fixtures(params={"season": 2022, "league": 39})


#Seasons available: 2022, 2023, 2024
#Leagues: Prem = 39, 
#Team: Man.Utd = 33

