import json
from script_constants import FILENAME

def main(season):
    with open(FILENAME.format(season), mode="r", encoding="utf-8") as file:
        game_data = json.loads(file.read())

    stats = {'win_more_3pa': 0,
            'win_more_3pm': 0,
            'win_more_3p_perc': 0,
            'win_few_3pa_more_fta': 0,
            'win_few_3pm_more_ftm': 0,
            'win_more_fta': 0,
            'win_more_ftm': 0,
            'total_games': 0}

    for game_id in game_data:
        game = game_data[game_id]
        try:
            home_win = int(game['home_score']) > int(game['away_score'])
            home_3pa = int(game['detailed_home']['fg3a'])
            away_3pa = int(game['detailed_away']['fg3a'])
            home_3pm = int(game['detailed_home']['fg3'])
            away_3pm = int(game['detailed_away']['fg3'])
            home_fta = int(game['detailed_home']['fta'])
            home_ftm = int(game['detailed_home']['ft'])
            away_fta = int(game['detailed_away']['fta'])
            away_ftm = int(game['detailed_away']['ft'])

            stats['win_more_3pa'] += home_3pa > away_3pa if home_win else away_3pa > home_3pa
            stats['win_more_3pm'] += home_3pm > away_3pm if home_win else away_3pm > home_3pm
            stats['win_more_3p_perc'] += (home_3pm / home_3pa > away_3pm / away_3pa) if home_win else (home_3pm / home_3pa < away_3pm / away_3pa)
            stats['win_more_fta'] += home_fta > away_fta if home_win else away_fta > home_fta
            stats['win_more_ftm'] += home_ftm > away_ftm if home_win else away_ftm > home_ftm
            stats['total_games'] += 1

        except:
            print("ERROR - MISSING DATA?:", game)

    total_games = stats['total_games']
    win_more_3pa = stats['win_more_3pa']
    win_more_3pm = stats['win_more_3pm']
    win_more_3pacc = stats['win_more_3p_perc']
    win_more_fta = stats['win_more_fta']
    win_more_ftm = stats['win_more_ftm']

    print(f'Teams with more 3PA won {win_more_3pa/total_games*100:.2f}% of the games.')
    print(f'Teams with more 3PM won {win_more_3pm/total_games*100:.2f}% of the games.')
    print(f'Teams with better 3P% won {win_more_3pacc/total_games*100:.2f}% of the games.')
    print(f'Teams with more FTA won {win_more_fta/total_games*100:.2f}% of the games.')
    print(f'Teams with more FTM won {win_more_ftm/total_games*100:.2f}% of the games.')


if __name__ == "__main__":
    main('2025')
