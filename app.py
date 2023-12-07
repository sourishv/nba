from flask import Flask, render_template, request
from nba import get_player_stats
from waitress import serve
import numpy as np

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/nba')
def get_stats():
    my_player = request.args.get('my_player')

    if not bool(my_player.strip()):
        my_player = "Tyler Herro"

    nba_fcn_output = get_player_stats(my_player)
    player_stats = nba_fcn_output[0]

    return render_template(
        "nba.html",
        player = nba_fcn_output[1],
        ppg = np.round(player_stats["PTS"]/player_stats["GP"], 1),
        rpg = np.round(player_stats["REB"]/player_stats["GP"], 1),
        apg = np.round(player_stats["AST"]/player_stats["GP"], 1)
    )



#if __name__ == "__main__":
serve(app, host="0.0.0.0", port=8000)
