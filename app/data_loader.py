import pandas as pd
import chardet
import os


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
        return result['encoding']


class DataLoader:

    def __init__(self):
        self.spotify_top10s_path = "C:/Users/mateu/Documents/GitHub/SztucznaInteligencjaa/data/Spotify_top10s.csv"

    def load_datasets(self):
        if not os.path.exists(self.spotify_top10s_path):
            raise FileNotFoundError(f"File not found: {self.spotify_top10s_path}")

        encoding = detect_encoding(self.spotify_top10s_path)
        print(f"Detected encoding: {encoding}")

        spotify_top10s = pd.read_csv(self.spotify_top10s_path, encoding=encoding)

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

        return spotify_top10s
