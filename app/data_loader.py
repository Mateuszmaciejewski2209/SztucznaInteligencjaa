import pandas as pd
import chardet
import os


def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
        return result['encoding']


class DataLoader:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.spotify_top10s_path = os.path.join(base_dir, "../data/Spotify_top10s.csv")
        self.spotify_2000s_path = os.path.join(base_dir, "../data/Spotify_2000s.csv")
        self.songs_output_path = os.path.join(base_dir, "../data/songs.csv")

    def generate_songs(self):
        if not os.path.exists(self.spotify_top10s_path) or not os.path.exists(self.spotify_2000s_path):
            raise FileNotFoundError("Pliki Spotify_top10s.csv lub Spotify_2000s.csv nie zostały znalezione.")

        # Detect encoding
        top10s_encoding = detect_encoding(self.spotify_top10s_path)
        spotify_2000s_encoding = detect_encoding(self.spotify_2000s_path)

        # Read CSV files with detected encodings
        songs_top10s = pd.read_csv(self.spotify_top10s_path, encoding=top10s_encoding)
        songs_2000s = pd.read_csv(self.spotify_2000s_path, encoding=spotify_2000s_encoding)

        # Rename columns to ensure 'title' exists
        songs_top10s = songs_top10s.rename(columns={"Title": "title", "Artist": "artist"})
        songs_2000s = songs_2000s.rename(columns={"Title": "title", "Artist": "artist"})

        # Combine datasets with relevant columns
        combined = pd.concat([
            songs_top10s[["title", "artist"]],
            songs_2000s[["title", "artist"]]
        ])

        # Drop duplicates and save to songs.csv
        combined.drop_duplicates(subset="title", inplace=True)
        combined.to_csv(self.songs_output_path, index=False)
        print(f"Plik songs.csv został wygenerowany w folderze 'data'.")

    def load_datasets(self):
        if not os.path.exists(self.spotify_top10s_path):
            raise FileNotFoundError(f"File not found: {self.spotify_top10s_path}")
        if not os.path.exists(self.spotify_2000s_path):
            raise FileNotFoundError(f"File not found: {self.spotify_2000s_path}")

        top10s_encoding = detect_encoding(self.spotify_top10s_path)
        spotify_2000s_encoding = detect_encoding(self.spotify_2000s_path)

        spotify_top10s = pd.read_csv(self.spotify_top10s_path, encoding=top10s_encoding)
        spotify_2000s = pd.read_csv(self.spotify_2000s_path, encoding=spotify_2000s_encoding)

        spotify_top10s = spotify_top10s.rename(columns={
            "title": "title",
            "bpm": "tempo",
            "nrgy": "energy",
            "dnce": "danceability",
            "dB": "loudness",
            "live": "liveness",
            "val": "valence",
            "dur": "duration_ms",
            "acous": "acousticness",
            "spch": "speechiness",
            "pop": "popularity"
        })

        spotify_2000s = spotify_2000s.rename(columns={
            "Title": "title",
            "Artist": "artist",
            "Top Genre": "top genre",
            "Year": "year",
            "Beats Per Minute (BPM)": "tempo",
            "Energy": "energy",
            "Danceability": "danceability",
            "Loudness (dB)": "loudness",
            "Liveness": "liveness",
            "Valence": "valence",
            "Length (Duration)": "duration_ms",
            "Acousticness": "acousticness",
            "Speechiness": "speechiness",
            "Popularity": "popularity"
        })

        combined_data = pd.concat([spotify_top10s, spotify_2000s], ignore_index=True)

        combined_data = combined_data.drop_duplicates(subset="title").reset_index(drop=True)

        return combined_data
