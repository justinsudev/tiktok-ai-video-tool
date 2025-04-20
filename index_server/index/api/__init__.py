"""
API package for the Index server.
"""
# Import and expose functions/objects from main
from .main import api_blueprint, load_index

# Export these names
__all__ = ['api_blueprint', 'load_index']