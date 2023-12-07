from dotenv import load_dotenv
from pprint import pprint
import requests
import os
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

load_dotenv()


def get_player_stats(my_player="Tyler Herro"):

    nba_players = players.get_players()
    print("test1")
    my_player_data = [
        player for player in nba_players if player["full_name"] == my_player
        ][0]
    print(my_player_data)
    my_id = my_player_data["id"]
    print(type(my_id))
    player_stats = playercareerstats.PlayerCareerStats(player_id=str(my_id))
    print("test3")
    stat_frame = player_stats.get_data_frames()[0]
    current_stat_idx = len(stat_frame)-1
    return stat_frame.iloc[current_stat_idx]


if __name__ == "__main__":
    print('\n*** Get NBA Stats ***\n')

    my_player = input("\nPlease enter a player name: ")

    player_stats = get_player_stats(my_player)

    print("\n")
    pprint(player_stats)