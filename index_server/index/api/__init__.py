"""
API module for the index server.

This module contains the API endpoints for the index server.
"""
from .main import api_blueprint, load_index

# Export these names
__all__ = ['api_blueprint', 'load_index']
