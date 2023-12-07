from pprint import pprint
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

def get_player_stats(my_player='Tyler Herro'):

    nba_players = players.get_players()
    print("test1")
    player_dict = [
        player for player in nba_players if player['full_name'] == my_player
        ][0]
    print(player_dict)
    my_id = str(player_dict["id"])
    print(type(my_id))
    my_player_stats = playercareerstats.PlayerCareerStats(player_id=my_id)
    stat_frame = my_player_stats.get_data_frames()[0]
    print(stat_frame)
    current_stat_idx = len(stat_frame)-1
    return stat_frame.iloc[current_stat_idx]


if __name__ == "__main__":
    print('\n*** Get NBA Stats ***\n')

    my_player = input("\nPlease enter a player name: ")

    player_stats = get_player_stats(my_player)

    print("\n")
    pprint(player_stats)