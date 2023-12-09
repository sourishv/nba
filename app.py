from flask import Flask, render_template, request, redirect, url_for
from nba import get_player_stats, get_player_image_url
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/nba', methods=['POST'])
def get_stats():
    if request.method == 'POST':
        player1 = request.form.get('player1')
        player2 = request.form.get('player2')
        selected_stats = request.form.getlist('stats[]')

        if not bool(player1.strip()):
            player1 = "Trae Young"
        if not bool(player2.strip()):
            player2 = "Tyler Herro"

        player1_name, player1_id, stats1 = get_player_stats(player1, selected_stats)
        player2_name, player2_id, stats2 = get_player_stats(player2, selected_stats)

        rounded_stats1 = {key: round(value, 2) if isinstance(value, (int, float)) else value for key, value in stats1.items()}
        rounded_stats2 = {key: round(value, 2) if isinstance(value, (int, float)) else value for key, value in stats2.items()}

        player1_image_url = get_player_image_url(player1_id)
        player2_image_url = get_player_image_url(player2_id)

        player1_wins = sum(1 for stat in selected_stats if stats1.get(stat) > stats2.get(stat))
        player2_wins = sum(1 for stat in selected_stats if stats1.get(stat) < stats2.get(stat))

        if player1_wins > player2_wins:
            better_player = player1_name
        elif player1_wins < player2_wins:
            better_player = player2_name
        else:
            better_player = "Neither player"

        return render_template('nba.html', title='Compare NBA Players:', player1=player1_name, player2=player2_name,
                               selected_stats=selected_stats, stats1=rounded_stats1, stats2=rounded_stats2,
                               better_player=better_player, player1_image_url=player1_image_url,
                               player2_image_url=player2_image_url)
    
    return render_template('index.html')  # Replace with your actual index template name

@app.route('/new_comparison')
def new_comparison():
    return redirect(url_for('index'))

#if __name__ == "__main__":
serve(app, host="0.0.0.0", port=8000)
