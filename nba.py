from pprint import pprint
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
from difflib import get_close_matches

def get_player_stats(my_player='Tyler Herro'):

    nba_players = players.get_players()
    print("test1")

    player_names = [player['full_name'] for player in nba_players]
    my_player = get_close_matches(my_player, player_names, 1, 0)[0]
    print(my_player)

    player_dict = [
        player for player in nba_players if player['full_name'] == my_player
        ][0]

    my_id = str(player_dict["id"])
    print(type(my_id))

    my_player_stats = playercareerstats.PlayerCareerStats(player_id=my_id)

    stat_frame = my_player_stats.get_data_frames()[0]
    print(stat_frame)

    current_stat_idx = len(stat_frame)-1

    return (stat_frame.iloc[current_stat_idx], my_player)


if __name__ == "__main__":
    print('\n*** Get NBA Stats ***\n')

    my_player = input("\nPlease enter a player name: ")

    player_stats = get_player_stats(my_player)[0]

    print("\n")
    pprint(player_stats)