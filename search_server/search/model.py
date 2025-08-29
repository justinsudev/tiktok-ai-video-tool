"""
Database model for the Search server.

This module provides functions for database connection management
and document metadata retrieval.
"""
import sqlite3
from flask import current_app, g


def get_db():
    """
    Open new database connection if none yet for current application context.

    Returns:
        SQLite connection object with row factory set to sqlite3.Row.
    """
    if 'db' not in g:
        # Connect and set row factory for dict-like access
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_=None):
    """
    Close the database connection for the current application context.

    Args:
        _: Ignored parameter, here for Flask teardown_appcontext compatibility
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    """
    Register application teardown to close the database connection.

    Args:
        app: Flask application instance
    """
    app.teardown_appcontext(close_db)


def get_doc(docid: int) -> dict:
    """
    Fetch the document metadata (title, url, summary) for the given docid.

    Args:
        docid: Document ID to look up

    Returns:
        A dict with keys 'title', 'url', and 'summary'.
        If no row is found, returns empty strings for fields.
    """
    db = get_db()
    row = db.execute(
        'SELECT title, url, summary FROM documents WHERE docid = ?',
        (docid,)
    ).fetchone()
    if row is None:
        return {'title': '', 'url': '', 'summary': ''}
    return {
        'title': row['title'],
        'url': row['url'],
        'summary': row['summary'] or ''
    }
