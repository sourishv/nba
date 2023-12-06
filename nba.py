from dotenv import load_dotenv
from pprint import pprint
import requests
import os
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

load_dotenv()


def get_player_stats(player="Tyler Herro"):

    player_id = [player for player in nba_players if player["full_name"] == "player"][0]

    player_stats = playercareerstats.PlayerCareerStats(player_id="203076")

    return player_stats


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