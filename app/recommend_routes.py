from flask import Blueprint, render_template, request
from recommender import Recommender
import os
import pandas as pd

recommend_routes = Blueprint("recommend_routes", __name__)

# Ścieżki do plików
RATINGS_FILE = os.path.join("data", "ratings.csv")
SONGS_FILE = os.path.join("data", "Spotify_top10s.csv")

# Ładowanie danych
def load_ratings():
    return pd.read_csv(RATINGS_FILE)

def load_songs():
    return pd.read_csv(SONGS_FILE)

# Rekomendacja na bazie piosenki
@recommend_routes.route("/recommend/song", methods=["GET", "POST"])
def recommend_song():
    songs = load_songs()["title"].tolist()
    recommendations = []
    if request.method == "POST":
        selected_song = request.form.get("song")
        recommender = Recommender()
        recommendations = recommender.recommend_similar_songs(selected_song)
    return render_template("recommend_song.html", songs=songs, recommendations=recommendations)

# Rekomendacja na bazie ocen
@recommend_routes.route("/recommend/ratings", methods=["GET"])
def recommend_ratings():
    ratings = load_ratings()
    recommender = Recommender()
    user_id = request.args.get("user_id")
    recommendations = recommender.recommend_for_user(int(user_id)) if user_id else []
    return render_template("recommend_ratings.html", recommendations=recommendations)
