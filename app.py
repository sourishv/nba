from flask import Flask, render_template, request, redirect, url_for, json, jsonify
from nba import get_player_stats, get_player_image_url, names_list
from waitress import serve
from fuzzywuzzy import process

app = Flask(__name__)

player_names = names_list()
player_names_json = json.dumps(player_names)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', player_names=player_names_json)

@app.route('/nba', methods=['POST'])
def get_stats():
    player1 = request.form.get('player1')
    player2 = request.form.get('player2')
    selected_stats = request.form.getlist('stats[]')
    season_type = request.form.get('seasonType')

    if season_type is None:
        season_type = 'Regular Season'

    player1_name, player1_id, stats1, stat_ids = get_player_stats(player1, selected_stats, season_type)
    player2_name, player2_id, stats2, stat_ids = get_player_stats(player2, selected_stats, season_type)

    print(stats1)
    print(stats2)

    rounded_stats1 = {key: round(value, 2) for key, value in stats1.items()}
    rounded_stats2 = {key: round(value, 2) for key, value in stats2.items()}

    player1_image_url = get_player_image_url(player1_id)
    player2_image_url = get_player_image_url(player2_id)

    player1_wins = sum(1 for stat in stat_ids if stats1.get(stat) > stats2.get(stat))
    player2_wins = sum(1 for stat in stat_ids if stats1.get(stat) < stats2.get(stat))

    if player1_wins > player2_wins:
        better_player = player1_name
    elif player1_wins < player2_wins:
        better_player = player2_name
    else:
        better_player = "Neither player"

    grouped_stats = zip(selected_stats, stat_ids)
    return render_template('nba.html', title='Compare NBA Players:', player1=player1_name, player2=player2_name,
                            grouped_stats=grouped_stats, selected_stats = selected_stats,stats1=rounded_stats1, stats2=rounded_stats2,
                            better_player=better_player, player1_image_url=player1_image_url,
                            player2_image_url=player2_image_url)
    
@app.route('/new_comparison')
def new_comparison():
    return redirect(url_for('index'))

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    partial_input = request.args.get('partial_name', '')
    matches = process.extract(partial_input, player_names, limit=5)
    suggestions = [match[0] for match in matches]
    
    # Print suggestions to console for debugging
    print('Suggestions:', suggestions)

    return jsonify(suggestions)

#if __name__ == "__main__":
serve(app, host="0.0.0.0", port=8000)
