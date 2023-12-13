from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from fuzzywuzzy import process
#import cProfile



def get_player_image_url(player_id):
    return f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"

def names_list():
    nba_players = players.get_players()
    return [player['full_name'] for player in nba_players]

def get_player_stats(my_player="LeBron James", selected_stats="PTS", season_type="Regular"):
    #with cProfile.Profile() as pr:
    nba_players = players.get_players()

    player_names = [player['full_name'] for player in nba_players]

    # Find close matches using fuzzywuzzy
    #need to find a good way to not have to go through 71 players (most common name)
    close_matches = process.extract(my_player, player_names, limit=20)
    print(close_matches)
    top_match_pct = close_matches[0][1]

    for i in range(20):
        if close_matches[i][1] != top_match_pct:
            close_matches = close_matches[:i]
            break

    # Sort close matches by points per game (you might need to replace 'PTS' with the actual stat you want to use)
    close_matches = sorted(close_matches, key=lambda x: get_points_per_game(x[0], season_type), reverse=True)

    # Select the top match
    my_player = close_matches[0][0]
    print(my_player)

    my_id = get_player_id_by_name(my_player)
    my_player_stats = playercareerstats.PlayerCareerStats(player_id=my_id)

    stat_frame = my_player_stats.get_data_frames()

    # Extract data for regular season and post season
    regular_season_data = stat_frame[1]  # SeasonTotalsRegularSeason
    post_season_data = stat_frame[2]  # SeasonTotalsPostSeason
    
    # Combine regular season and post season data
    selected_data = regular_season_data if season_type == "Regular" else post_season_data

    # Filter stats based on selected_stats
    selected_stats = set(selected_stats)
    stats_dict = {}

    for stat in selected_stats:
        # Check if the stat is a percentage and average them
        if stat in ['GS', 'GP']:
            stat_values = selected_data[stat].sum()
        elif stat.endswith("_PCT"):
            stat_values = selected_data[stat].sum()*100
        else:
            stat_values = (selected_data[stat].sum()) / (selected_data["GP"].sum())
        
        stats_dict[stat] = stat_values
    #pr.print_stats()

    return my_player, my_id, stats_dict

def get_points_per_game(player_name, season_type="Regular"):
    player_id = get_player_id_by_name(player_name)
    if not player_id:
        return 0  # Return 0 PPG if player ID is not found

    player_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    stat_frame = player_stats.get_data_frames()

    # Extract data for regular season and post season
    regular_season_data = stat_frame[1]  # SeasonTotalsRegularSeason
    post_season_data = stat_frame[2]  # SeasonTotalsPostSeason

    # Choose the selected season type
    selected_data = regular_season_data if season_type == "Regular" else post_season_data

    total_points = selected_data["PTS"].sum()
    games_played = selected_data["GP"].sum()

    return total_points / games_played if games_played > 0 else 0
def get_player_id_by_name(player_name):
    player = next((player for player in players.get_players() if player['full_name'] == player_name), None)
    return str(player["id"])