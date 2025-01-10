import os
from flask import Flask
from login_routes import login_routes
from recommend_routes import recommend_routes
from data_loader import DataLoader
from login_routes import initialize_ratings_file

# Initialize Flask app
app = Flask(__name__)

# Load secret key from environment variable
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_fallback_key")

# Register blueprints
app.register_blueprint(login_routes)
app.register_blueprint(recommend_routes)

# Generate ratings.csv during app startup
loader = DataLoader()
loader.generate_songs()
# Initialize the ratings.csv file with correct headers
initialize_ratings_file()

if __name__ == "__main__":
    app.run(debug=True)
