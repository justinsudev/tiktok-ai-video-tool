"""Index server package."""
import os
from pathlib import Path
from index.api.main import api_blueprint, load_index
from flask import Flask

# Create the Flask app
app = Flask(__name__)

# Set default index path configuration
INDEX_DIR = Path(__file__).parent/"inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",  # Environment variable name
    str(INDEX_DIR/"inverted_index_1.txt")  # Default value
)


# Register the blueprint
app.register_blueprint(api_blueprint, url_prefix="/api/v1")

# Load inverted index, stopwords, and pagerank into memory
load_index()
