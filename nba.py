from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from difflib import get_close_matches
import pandas as pd

def get_player_image_url(player_id):
    return f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"

def get_player_stats(my_player='Tyler Herro', selected_stats=None):
    nba_players = players.get_players()

    player_names = [player['full_name'] for player in nba_players]
    my_player = get_close_matches(my_player, player_names, 1, 0)[0]

    player_dict = next((player for player in nba_players if player['full_name'] == my_player), None)

    if player_dict is None:
        return {"error": "Player not found."}

    my_id = str(player_dict["id"])
    my_player_stats = playercareerstats.PlayerCareerStats(player_id=my_id)

    stat_frame = my_player_stats.get_data_frames()

    # Extract data for regular season and post season
    regular_season_data = stat_frame[1]  # SeasonTotalsRegularSeason
    post_season_data = stat_frame[2]  # SeasonTotalsPostSeason
    
    # Combine regular season and post season data
    combined_data = pd.concat([regular_season_data, post_season_data], ignore_index=True)

    # Filter stats based on selected_stats
    if selected_stats:
        selected_stats = set(selected_stats)
        stats_dict = {}

        for stat in selected_stats:
            # Check if the stat is a percentage and average them
            if stat.endswith("_PCT"):
                stat_values = combined_data[stat].mean()
            else:
                # Calculate per game stats for non-percentage stats
                if stat in ['GS', 'GP']:
                    stat_values = combined_data[stat].sum()
                else:
                    stat_values = (combined_data[stat].sum())/(combined_data["GP"].sum())
            print(stat_values)
            stats_dict[stat] = stat_values

    else:
        # Convert all stats to a dictionary
        stats_dict = combined_data.to_dict()

    return my_player, my_id, stats_dict
if __name__ == "__main__":
    print('\n*** Get NBA Stats ***\n')

    my_player = input("\nPlease enter a player name: ")
    selected_stats = input("\nPlease enter selected stats (comma-separated): ").split(',')

    player_data, player_id = get_player_stats(my_player, selected_stats)

    if "error" in player_data:
        print(player_data["error"])
    else:
        player_stats = player_data["stats"]
        player_name = player_data["player_name"]
        player_image_url = get_player_image_url(player_id)

        print(f"\nStats for {player_name}:\n")
        print(player_stats)
        print(f"Player Image URL: {player_image_url}")
