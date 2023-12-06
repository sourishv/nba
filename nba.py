from dotenv import load_dotenv
from pprint import pprint
import requests
import os
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

load_dotenv()


def get_player_stats(my_player="Tyler Herro"):

    nba_players = players.get_players()

    player_id = [player[0]["id"] for player in nba_players if player["full_name"] == my_player]

    player_stats = playercareerstats.PlayerCareerStats(player_id)

    stat_frame = player_stats.get_data_frames()[0]

    return stat_frame.iloc[-1]


if __name__ == "__main__":
    print('\n*** Get NBA Stats ***\n')

    city = input("\nPlease enter a player name: ")

    # Check for empty strings or string with only spaces
    # This step is not required here
    # if not bool(city.strip()):
    #     city = "Kansas City"

    player_stats = get_player_stats(city)

    print("\n")
    pprint(player_stats)