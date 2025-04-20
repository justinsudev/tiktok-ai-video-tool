"""
Index server package.
"""
import os
from flask import Flask
from pathlib import Path

# Create the Flask app
app = Flask(__name__)

# Set default index path configuration
INDEX_DIR = Path(__file__).parent/"inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",  # Environment variable name
    str(INDEX_DIR/"inverted_index_1.txt")  # Default value
)

# Import directly from the module
from index.api.main import api_blueprint, load_index

# Register the blueprint
app.register_blueprint(api_blueprint, url_prefix="/api/v1")

# Load inverted index, stopwords, and pagerank into memory
load_index()