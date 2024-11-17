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
            'total_games': 0,
            'biggest_win_margin_fewer_3pm': 0,
            'biggest_win_margin_fewer_3pm_gm': None,
            'fewest_3pm_win': float('inf'),
            'fewest_3pm_win_gm': None,
            'most_3pm_loss': 0,
            'most_3pm_loss_gm': None,
            'more_3pm_but_loss': 0,
            'more_3pm_but_loss_gm': None,
            }

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

            # biggest win margin with fewer 3PM
            # home wins but fewer 3PM or away wins but fewer 3PM, points compared
            win_margin_fewer_3pm = None
            if home_win and home_3pm < away_3pm:
                win_margin_fewer_3pm = int(game['home_score']) - int(game['away_score'])
            elif not home_win and away_3pm < home_3pm:
                win_margin_fewer_3pm = int(game['away_score']) - int(game['home_score'])
            if win_margin_fewer_3pm is not None and abs(win_margin_fewer_3pm) > stats['biggest_win_margin_fewer_3pm']:
                stats['biggest_win_margin_fewer_3pm'] = win_margin_fewer_3pm
                stats['biggest_win_margin_fewer_3pm_gm'] = game

            # best 3PM margin in a loss
            # home wins but fewer 3PM or away wins but fewer 3PM, 3PM compared
            margin_3pt = None
            if home_win and home_3pm < away_3pm:
                margin_3pt = abs(away_3pm - home_3pm)
            elif not home_win and away_3pm < home_3pm:
                margin_3pt = abs(home_3pm - away_3pm)
            if margin_3pt is not None and margin_3pt > stats['more_3pm_but_loss']:
                stats['more_3pm_but_loss'] = margin_3pt
                stats['more_3pm_but_loss_gm'] = game

            # fewest 3PM in a win
            if home_win and home_3pm < stats['fewest_3pm_win']:
                stats['fewest_3pm_win'] = home_3pm
                stats['fewest_3pm_win_gm'] = game
            elif not home_win and away_3pm < stats['fewest_3pm_win']:
                stats['fewest_3pm_win'] = away_3pm
                stats['fewest_3pm_win_gm'] = game

            # most 3PM in a loss
            if home_win and away_3pm > stats['most_3pm_loss']:
                stats['most_3pm_loss'] = away_3pm
                stats['most_3pm_loss_gm'] = game
            elif not home_win and home_3pm > stats['most_3pm_loss']:
                stats['most_3pm_loss'] = home_3pm
                stats['most_3pm_loss_gm'] = game

            # total stats
            stats['win_more_3pa'] += home_3pa > away_3pa if home_win else away_3pa > home_3pa
            stats['win_more_3pm'] += home_3pm > away_3pm if home_win else away_3pm > home_3pm
            stats['win_more_3p_perc'] += (home_3pm / home_3pa > away_3pm / away_3pa) if home_win else (home_3pm / home_3pa < away_3pm / away_3pa)
            stats['win_more_fta'] += home_fta > away_fta if home_win else away_fta > home_fta
            stats['win_more_ftm'] += home_ftm > away_ftm if home_win else away_ftm > home_ftm
            stats['total_games'] += 1

        except Exception as e:
            print("ERROR - MISSING DATA?:", game, e.args)

    total_games = stats['total_games']
    
    print(f"Teams with more 3PA won {stats['win_more_3pa']/total_games*100:.2f}% of the games.")
    print(f"Teams with more 3PM won {stats['win_more_3pm']/total_games*100:.2f}% of the games.")
    print(f"Teams with better 3P% won {stats['win_more_3p_perc']/total_games*100:.2f}% of the games.")
    print(f"Teams with more FTA won {stats['win_more_fta']/total_games*100:.2f}% of the games.")
    print(f"Teams with more FTM won {stats['win_more_ftm']/total_games*100:.2f}% of the games.")
    print(f"Biggest point margin in a win with fewer 3PM was in {stats['biggest_win_margin_fewer_3pm_gm']['home_team']} @ {stats['biggest_win_margin_fewer_3pm_gm']['away_team']}, {stats['biggest_win_margin_fewer_3pm_gm']['home_score']}-{stats['biggest_win_margin_fewer_3pm_gm']['away_score']} ({stats['biggest_win_margin_fewer_3pm_gm']['date']}): {stats['biggest_win_margin_fewer_3pm']} points.")
    print(f"Fewest 3PM in a win: {stats['fewest_3pm_win_gm']['home_team']} @ {stats['fewest_3pm_win_gm']['away_team']}, {stats['fewest_3pm_win_gm']['home_score']}-{stats['fewest_3pm_win_gm']['away_score']} ({stats['fewest_3pm_win_gm']['date']}) at {stats['fewest_3pm_win']} 3PM.")
    print(f"Most 3PM in a loss: {stats['most_3pm_loss_gm']['home_team']} @ {stats['most_3pm_loss_gm']['away_team']}, {stats['most_3pm_loss_gm']['home_score']}-{stats['most_3pm_loss_gm']['away_score']} ({stats['most_3pm_loss_gm']['date']}) at {stats['most_3pm_loss']} 3PM")
    print(f"Best 3PM margin in a loss in {stats['more_3pm_but_loss_gm']['home_team']} @ {stats['more_3pm_but_loss_gm']['away_team']}, {stats['more_3pm_but_loss_gm']['home_score']}-{stats['more_3pm_but_loss_gm']['away_score']} ({stats['more_3pm_but_loss_gm']['date']}) at {stats['more_3pm_but_loss']}. {stats['more_3pm_but_loss_gm']['home_team']} {stats['more_3pm_but_loss_gm']['detailed_home']['fg3']} vs {stats['more_3pm_but_loss_gm']['away_team']} {stats['more_3pm_but_loss_gm']['detailed_away']['fg3']}.")

if __name__ == "__main__":
    main('2025')
