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
        self.spotify_top10s_path = "C:/Users/mateu/Documents/GitHub/SztucznaInteligencjaa/data/Spotify_top10s.csv"
        self.spotify_2000s_path = "C:/Users/mateu/Documents/GitHub/SztucznaInteligencjaa/data/Spotify_2000s.csv"

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
