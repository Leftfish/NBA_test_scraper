import json
import os
import re
from math import ceil
from time import sleep
import requests
from script_constants import *

def get_all_boxscores(season):
    boxscore_ids = []
    for url_template in ALLSCORES:
        url = url_template.format(season)
        raw_html = requests.get(url, timeout=5).text
        boxscore_ids.extend(re.findall(RE_BOXSCORE, raw_html))
    return boxscore_ids

def get_boxscore(date_teams):
    url = BOXSCORE_STR.format(date_teams)
    return requests.get(url, timeout=5).text

def get_teams_and_scores(raw_boxscore):
    return re.findall(RE_GAME, raw_boxscore)[0]

def get_detailed_stats(raw_boxscore):
    raw_stats = re.findall(RE_TOTALS, raw_boxscore)
    allgame_away_idx = 0
    allgame_home_idx = ceil(len(raw_stats) / 2)

    raw_away = re.findall(RE_STAT, raw_stats[allgame_away_idx])
    raw_home = re.findall(RE_STAT, raw_stats[allgame_home_idx])

    stats_away = {}
    for stat, value in raw_away:
        stats_away[stat] = value

    stats_home = {}
    for stat, value in raw_home:
        stats_home[stat] = value

    return stats_away, stats_home


def read_game_data(date_teams):
    raw_boxscore = get_boxscore(date_teams)
    teams_scores = get_teams_and_scores(raw_boxscore)
    date = date_teams[:-4]
    away = teams_scores[0]
    away_score = teams_scores[1]
    home = teams_scores[2]
    home_score = teams_scores[3]
    stats_away, stats_home = get_detailed_stats(raw_boxscore)

    game_data = {}
    game_data['date'] = date
    game_data['home_team'] = home
    game_data['home_score'] = home_score
    game_data['away_team'] = away
    game_data['away_score'] = away_score
    game_data['detailed_home'] = stats_home
    game_data['detailed_away'] = stats_away

    return {date_teams: game_data}

def update_data(season, data):
    for boxscore in get_all_boxscores(season):
        if boxscore in data:
            print(f'{boxscore} currently in data. No need to update!')
        elif boxscore not in data:
            print(f'{boxscore} currently not in data. Fetching and parsing...', end=' ')
            new_game = read_game_data(boxscore)
            print('Updating...', end=' ')
            data.update(new_game)
            print(f'Done! Sleep {SLEEP} seconds per Basketball Reference rules.')
            sleep(SLEEP)
    return data

def main(season):
    datafile_name = FILENAME.format(season)
    if not os.path.exists(datafile_name):
        print("Data file not detected. Creating empty data file...")
        with open(datafile_name, mode="w", encoding="utf-8") as file:
            file.write(json.dumps({}))

    with open(datafile_name, mode="r", encoding="utf-8") as file:
        print("Reading game data from the data file...")
        data = json.loads(file.read())

    print("Updating data from Basketball Reference...")
    data = update_data(season, data)

    with open(datafile_name, mode="w", encoding="utf-8") as file:
        print(f"Saving the updated data to {datafile_name}.")
        file.write(json.dumps(data))

if __name__ == "__main__":
    main('2025')
