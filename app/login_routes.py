from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import csv
import os
import pandas as pd

login_routes = Blueprint("login_routes", __name__)

# Paths to files
base_dir = os.path.dirname(os.path.abspath(__file__))
SONGS_FILE = os.path.join(base_dir, "../data/Spotify_top10s.csv")
USERS_FILE = os.path.join(base_dir, "../data/users.csv")
RATINGS_FILE = os.path.join(base_dir, "../data/ratings.csv")

# Load users
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return {row["username"]: row["password"] for row in reader}

# Save new user
def save_user(username, password):
    with open(USERS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

# Load songs
def load_songs():
    with open(SONGS_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

# Initialize the ratings.csv file with correct headers
def initialize_ratings_file():
    if not os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "song_title", "rating"])

# Save rating
def save_rating(username, song_title, rating):
    ratings_file = RATINGS_FILE

    # Load the current ratings
    if os.path.exists(ratings_file):
        ratings = pd.read_csv(ratings_file)
    else:
        ratings = pd.DataFrame(columns=["username", "song_title", "rating"])

    # Check if this user has already rated this song
    existing_rating = (ratings["username"] == username) & (ratings["song_title"] == song_title)

    if existing_rating.any():
        # Update the rating
        ratings.loc[existing_rating, "rating"] = int(rating)
    else:
        # Add a new rating using pd.concat
        new_rating = pd.DataFrame([{"username": username, "song_title": song_title, "rating": int(rating)}])
        ratings = pd.concat([ratings, new_rating], ignore_index=True)

    # Save the updated ratings back to the file
    ratings.to_csv(ratings_file, index=False)


def load_user_ratings(username):
    if not os.path.exists(RATINGS_FILE):
        initialize_ratings_file()

    ratings = pd.read_csv(RATINGS_FILE)

    if set(ratings.columns) != {"username", "song_title", "rating"}:
        raise KeyError("The ratings.csv file does not have the correct headers.")

    user_ratings = ratings[ratings["username"] == username].set_index("song_title")["rating"].to_dict()
    return user_ratings


# Login route
@login_routes.route("/", methods=["GET", "POST"])
def login():
    users = load_users()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Both username and password are required.", "error")
            return redirect(url_for("login_routes.login"))

        if username in users:
            if users[username] == password:
                session["username"] = username  # Set the session
                flash("Logged in successfully.", "success")
                return redirect(url_for("login_routes.songs"))
            else:
                flash("Incorrect username or password.", "error")
                return redirect(url_for("login_routes.login"))
        else:
            save_user(username, password)
            session["username"] = username  # Set the session for new user
            flash("Account created successfully.", "success")
            return redirect(url_for("login_routes.songs"))

    return render_template("login.html")


# Logout route
@login_routes.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login_routes.login"))

# Songs route
@login_routes.route("/songs", methods=["GET", "POST"])
def songs():
    if "username" not in session:
        flash("You must be logged in to access this page.", "error")
        return redirect(url_for("login_routes.login"))

    # Load all songs
    songs = pd.read_csv(os.path.join(base_dir, "../data/songs.csv")).to_dict(orient="records")

    # Load user ratings
    username = session["username"]
    user_ratings = load_user_ratings(username)

    if request.method == "POST":
        song_title = request.form.get("song_title")
        rating = request.form.get("rating")

        if song_title and rating:
            save_rating(username, song_title, rating)
            flash(f"Your rating for '{song_title}' has been updated to {rating}.", "success")
            return redirect(url_for("login_routes.songs"))

    # Pass the songs and user ratings to the template
    return render_template("songs.html", songs=songs, ratings=user_ratings)

