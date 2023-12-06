from flask import Flask, render_template, request
from nba import get_player_stats
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/nba')
def get_stats():
    my_player = request.args.get('my_player')

    # Check for empty strings or string with only spaces
    if not bool(my_player.strip()):
        # You could render "City Not Found" instead like we do below
        my_player = "Tyler Herro"

    player_stats = get_player_stats(my_player)

    # City is not found by API
    #if not player_stats == 200:
      #  return render_template('player-not-found.html')

    return render_template(
        "nba.html",
        player = player_stats["full_name"],
        PTS = player_stats["PTS"],
        REB = player_stats["REB"],
        AST = player_stats["AST"]
    )



#if __name__ == "__main__":
serve(app, host="0.0.0.0", port=8000)
