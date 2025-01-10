from flask import Blueprint, render_template, request, flash
from recommender import Recommender
import os
import csv
import pandas as pd
from data_loader import detect_encoding  # Import the detect_encoding function

recommend_routes = Blueprint("recommend_routes", __name__)

# Paths to files
base_dir = os.path.dirname(os.path.abspath(__file__))
RATINGS_FILE = os.path.join(base_dir, "../data/ratings.csv")
SONGS_FILE = os.path.join(base_dir, "../data/songs.csv")
USERS_FILE = os.path.join(base_dir, "../data/users.csv")

# Load ratings
def load_ratings():
    if os.path.exists(RATINGS_FILE):
        encoding = detect_encoding(RATINGS_FILE)
        return pd.read_csv(RATINGS_FILE, encoding=encoding)
    return pd.DataFrame(columns=["username", "song_title", "rating"])

def load_users():
    users_file = os.path.join(base_dir, "../data/users.csv")  # Path to the users file
    if not os.path.exists(users_file):
        return []

    with open(users_file, mode="r") as file:
        reader = csv.DictReader(file)
        return [row["username"] for row in reader if "username" in row]

# Load songs
def load_songs():
    if os.path.exists(SONGS_FILE):
        encoding = detect_encoding(SONGS_FILE)
        return pd.read_csv(SONGS_FILE, encoding=encoding)
    return pd.DataFrame(columns=["title"])

# Recommendation based on song
@recommend_routes.route("/recommend/song", methods=["GET", "POST"])
def recommend_song():
    songs = load_songs()  # Load all songs
    song_data = pd.read_csv(SONGS_FILE, encoding=detect_encoding(SONGS_FILE))  # Song data with features
    print("Columns in song_data:", song_data.columns)  # Debugging line

    recommendations = []

    if request.method == "POST":
        selected_song = request.form.get("song")
        recommender = Recommender()
        recommendations = recommender.recommend_similar_songs(selected_song, song_data)

    return render_template("recommend_song.html", songs=songs["title"].tolist(), recommendations=recommendations)


# Recommendation based on ratings
@recommend_routes.route("/recommend/ratings", methods=["GET", "POST"])
def recommend_ratings():
    all_ratings = load_ratings()  # Load all ratings
    song_data = load_songs()  # Load all songs with features
    users = load_users()  # Load all usernames
    recommendations = []
    selected_user = None

    if request.method == "POST":
        selected_user = request.form.get("username")
        if selected_user:
            user_ratings = all_ratings[all_ratings["username"] == selected_user]
            recommender = Recommender()
            recommendations = recommender.recommend_for_user(user_ratings, all_ratings, song_data)

    return render_template(
        "recommend_ratings.html",
        users=users,
        recommendations=recommendations,
        selected_user=selected_user,
    )
