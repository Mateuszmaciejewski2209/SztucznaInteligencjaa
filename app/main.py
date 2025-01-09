from flask import Flask, request, jsonify
from recommender import Recommender

app = Flask(__name__)
recommender = Recommender()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Music Recommendation System!"})

@app.route("/recommend", methods=["GET"])
def recommend():
    song_name = request.args.get("song", None)
    if not song_name:
        return jsonify({"error": "Please provide a song name."}), 400

    recommendations = recommender.recommend_by_similarity(song_name)
    return jsonify({
        "song": song_name,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
