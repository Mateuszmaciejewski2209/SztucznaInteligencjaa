from data_loader import DataLoader
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self):
        loader = DataLoader()
        self.data = loader.load_datasets()

        self.features = ["danceability", "energy", "tempo", "valence", "loudness", "acousticness"]
        scaler = MinMaxScaler()
        self.data[self.features] = scaler.fit_transform(self.data[self.features])

    def recommend_by_similarity(self, song_name, top_n=5):
        if song_name not in self.data["title"].values:
            return ["Song not found in the dataset."]

        song_features = self.data.loc[self.data["title"] == song_name, self.features].values

        similarities = cosine_similarity(song_features, self.data[self.features])
        self.data["similarity"] = similarities[0]

        recommendations = self.data.sort_values(by="similarity", ascending=False)
        return recommendations.iloc[1:top_n+1]["title"].tolist()
