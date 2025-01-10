from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class Recommender:
    def __init__(self):
        pass

    def recommend_similar_songs(self, selected_song, song_data):
        features = ["tempo", "energy", "danceability", "loudness", "valence"]

        # Ensure all required features exist in the dataset
        missing_features = [feat for feat in features if feat not in song_data.columns]
        if missing_features:
            raise KeyError(f"The following required features are missing: {missing_features}")

        # Proceed with the similarity calculation as before
        feature_data = song_data[features]
        feature_data = (feature_data - feature_data.mean()) / feature_data.std()

        if selected_song not in song_data["title"].values:
            return ["Song not found in the dataset."]
        song_index = song_data[song_data["title"] == selected_song].index[0]

        similarity_matrix = cosine_similarity(feature_data)
        similar_indices = similarity_matrix[song_index].argsort()[-6:-1][::-1]

        return song_data.iloc[similar_indices]["title"].tolist()

    def recommend_for_user(self, user_ratings, all_ratings, song_data):
        """
        Recommends songs for a user based on collaborative filtering.

        Args:
            user_ratings (dict): User's ratings as a dictionary {song_title: rating}.
            all_ratings (pd.DataFrame): DataFrame with all user ratings.
            song_data (pd.DataFrame): DataFrame with all song data.

        Returns:
            list: List of recommended song titles.
        """
        # Merge ratings with song features
        merged_data = pd.merge(all_ratings, song_data, left_on="song_title", right_on="title")

        # Create a pivot table: users as rows, songs as columns
        pivot_table = merged_data.pivot_table(index="username", columns="title", values="rating").fillna(0)

        # Find the active user's ratings
        active_user = pivot_table.loc[user_ratings.name].values.reshape(1, -1)

        # Compute cosine similarity
        similarity_scores = cosine_similarity(active_user, pivot_table).flatten()

        # Sort users by similarity and find similar users
        similar_users = similarity_scores.argsort()[-2::-1]

        # Find songs rated highly by similar users but not rated by the active user
        similar_user_ratings = pivot_table.iloc[similar_users]
        unseen_songs = similar_user_ratings.loc[:, pivot_table.loc[user_ratings.name] == 0].mean(axis=0)

        # Recommend top 5 unseen songs
        recommendations = unseen_songs.sort_values(ascending=False).head(5).index.tolist()

        return recommendations
