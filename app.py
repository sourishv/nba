from flask import Flask, render_template, request
from nba import get_player_stats
from waitress import serve
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/nba', methods=['POST'])
def get_stats():
    if request.method == 'POST':
        player1 = request.form.get('player1', '')
        player2 = request.form.get('player2', '')
        selected_stats = request.form.getlist('stats[]')

        if not bool(player1.strip()):
            player1 = "Trae Young"
        if not bool(player2.strip()):
            player2 = "Tyler Herro"

        stats1 = get_player_stats(player1, selected_stats)
        stats2 = get_player_stats(player2, selected_stats)

        rounded_stats1 = {key: round(value, 2) if isinstance(value, (int, float)) else value for key, value in stats1.items()}
        rounded_stats2 = {key: round(value, 2) if isinstance(value, (int, float)) else value for key, value in stats2.items()}
        
        player1_wins = 0
        player2_wins = 0

        for stat in selected_stats:
            stat1_value = pd.to_numeric(stats1.get(stat, 'N/A'), errors='coerce')
            stat2_value = pd.to_numeric(stats2.get(stat, 'N/A'), errors='coerce')

            # Handle the case where both values are NaN
            if pd.isna(stat1_value) and pd.isna(stat2_value):
                continue

            # Determine the winner for the current stat
            if stat1_value > stat2_value:
                player1_wins += 1
            elif stat1_value < stat2_value:
                player2_wins += 1

        if player1_wins > player2_wins:
            better_player = player1
        elif player1_wins < player2_wins:
            better_player = player2
        else:
            better_player = "Neither player"

        return render_template('nba.html', title='Compare NBA Players:', player1=player1, player2=player2,
                           selected_stats=selected_stats, stats1=rounded_stats1, stats2=rounded_stats2,
                           better_player=better_player)
    return render_template('index.html')  # Replace with your actual index template name

# Assuming you have a Flask route for /nba in app.py


#if __name__ == "__main__":
serve(app, host="0.0.0.0", port=8000)
