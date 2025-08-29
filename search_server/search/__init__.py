"""
Search server package.

This package implements the web interface for the search engine.
It makes requests to Index servers and displays search results.
"""
from flask import Flask
from search.views.main import bp as main_bp


def create_app():
    """
    Create and configure the Flask application for the Search server.

    Returns:
        A configured Flask application instance.
    """
    # Use instance_app instead of app to avoid name redefinition
    instance_app = Flask(__name__, template_folder="templates")

    # Load configuration from config.py
    instance_app.config.from_object('search.config')

    instance_app.register_blueprint(main_bp)

    return instance_app


# Create the global `app` for `FLASK_APP=search` and testing
app = create_app()
