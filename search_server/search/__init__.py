from flask import Flask


def create_app():
    """
    Factory to create and configure the Flask application for the Search server.
    """
    app = Flask(__name__, template_folder="templates")
    # Load configuration from config.py
    app.config.from_object('search.config')

    # Register the main blueprint
    from search.views.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# Create the global `app` for `FLASK_APP=search` and testing
app = create_app()
