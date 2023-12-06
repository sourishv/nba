from flask import Flask, render_template, request
from nba import get_player_stats
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/player_stats')
def player_stats():
    player = request.args.get('my_player')

    # Check for empty strings or string with only spaces
    if not bool(player.strip()):
        # You could render "City Not Found" instead like we do below
        my_player = "Tyler Herro"

    player_stats = get_player_stats(my_player)

    # City is not found by API
    if not player_stats['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "nba.html",
        player = player_stats["full_name"],
        PTS = player_stats["PTS"],
        REB = player_stats["REB"],
        AST = player_stats["AST"]
    )



if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
