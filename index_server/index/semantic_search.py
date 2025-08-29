"""
Semantic Search Module for Enhanced Search Engine.

This module provides semantic search capabilities using sentence transformers
to understand query intent and match documents based on meaning, not just keywords.
Integrates with existing TF-IDF and PageRank scoring for hybrid search results.

Author: Enhanced by semantic layer integration
"""
import os
import pickle
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticSearchEngine:
    """
    Semantic search engine using sentence transformers for query understanding.
    
    This class handles:
    - Document embedding generation and storage
    - Query embedding and similarity computation
    - Integration with existing search infrastructure
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the semantic search engine.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self.doc_embeddings = None
        self.doc_metadata = {}
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
        # File paths for storing embeddings
        self.embeddings_file = None
        self.metadata_file = None
        
    def initialize(self, index_dir: str):
        """
        Initialize the semantic search engine with the given index directory.
        
        Args:
            index_dir: Directory containing index files
        """
        self.embeddings_file = os.path.join(index_dir, "semantic_embeddings.npy")
        self.metadata_file = os.path.join(index_dir, "semantic_metadata.pkl")
        
        logger.info(f"Initializing semantic search with model: {self.model_name}")
        
        try:
            # Load the sentence transformer model
            self.model = SentenceTransformer(self.model_name)
            logger.info("Sentence transformer model loaded successfully")
            
            # Try to load existing embeddings
            self._load_embeddings()
            
        except Exception as e:
            logger.error(f"Error initializing semantic search: {e}")
            # Fallback: semantic search will be disabled
            self.model = None
    
    def _load_embeddings(self):
        """Load pre-computed embeddings from disk if available."""
        try:
            if os.path.exists(self.embeddings_file) and os.path.exists(self.metadata_file):
                self.doc_embeddings = np.load(self.embeddings_file)
                with open(self.metadata_file, 'rb') as f:
                    self.doc_metadata = pickle.load(f)
                logger.info(f"Loaded {len(self.doc_metadata)} document embeddings")
            else:
                logger.info("No existing embeddings found, will generate on first use")
        except Exception as e:
            logger.warning(f"Error loading embeddings: {e}")
            self.doc_embeddings = None
            self.doc_metadata = {}
    
    def _save_embeddings(self):
        """Save computed embeddings to disk."""
        try:
            if self.doc_embeddings is not None and self.doc_metadata:
                np.save(self.embeddings_file, self.doc_embeddings)
                with open(self.metadata_file, 'wb') as f:
                    pickle.dump(self.doc_metadata, f)
                logger.info(f"Saved {len(self.doc_metadata)} document embeddings")
        except Exception as e:
            logger.error(f"Error saving embeddings: {e}")
    
    def build_document_embeddings(self, db_path: str):
        """
        Build semantic embeddings for all documents in the database.
        
        Args:
            db_path: Path to the SQLite database containing document metadata
        """
        if not self.model:
            logger.warning("Semantic search not available: model not loaded")
            return
            
        logger.info("Building document embeddings...")
        
        try:
            # Connect to database and fetch all documents
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT docid, title, summary FROM documents")
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                logger.warning("No documents found in database")
                return
            
            # Prepare texts for embedding
            doc_texts = []
            doc_ids = []
            
            for docid, title, summary in documents:
                # Combine title and summary for richer semantic content
                text = f"{title or ''} {summary or ''}".strip()
                if text:  # Only include documents with meaningful text
                    doc_texts.append(text)
                    doc_ids.append(docid)
            
            if not doc_texts:
                logger.warning("No meaningful text found in documents")
                return
            
            # Generate embeddings in batches for memory efficiency
            batch_size = 32
            embeddings = []
            
            for i in range(0, len(doc_texts), batch_size):
                batch_texts = doc_texts[i:i + batch_size]
                batch_embeddings = self.model.encode(batch_texts, convert_to_numpy=True)
                embeddings.append(batch_embeddings)
                
                if i % (batch_size * 10) == 0:
                    logger.info(f"Processed {i + len(batch_texts)}/{len(doc_texts)} documents")
            
            # Combine all embeddings
            self.doc_embeddings = np.vstack(embeddings)
            
            # Store metadata mapping
            self.doc_metadata = {
                'doc_ids': doc_ids,
                'model_name': self.model_name,
                'embedding_dim': self.embedding_dim,
                'total_docs': len(doc_ids)
            }
            
            # Save to disk
            self._save_embeddings()
            
            logger.info(f"Successfully built embeddings for {len(doc_ids)} documents")
            
        except Exception as e:
            logger.error(f"Error building document embeddings: {e}")
    
    def semantic_search(self, query: str, top_k: int = 100) -> List[Dict[str, Any]]:
        """
        Perform semantic search for the given query.
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries with docid and semantic_score
        """
        if not self.model or self.doc_embeddings is None:
            logger.warning("Semantic search not available")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query], convert_to_numpy=True)
            
            # Compute cosine similarities
            similarities = cosine_similarity(query_embedding, self.doc_embeddings)[0]
            
            # Get top-k results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Filter out very low similarity scores
                    docid = self.doc_metadata['doc_ids'][idx]
                    results.append({
                        'docid': docid,
                        'semantic_score': float(similarities[idx])
                    })
            
            logger.info(f"Semantic search returned {len(results)} results for query: '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def is_available(self) -> bool:
        """
        Check if semantic search is available.
        
        Returns:
            True if semantic search is ready to use, False otherwise
        """
        return (self.model is not None and 
                self.doc_embeddings is not None and 
                len(self.doc_metadata) > 0)

# Global instance for the semantic search engine
semantic_engine = SemanticSearchEngine()

def initialize_semantic_search(index_dir: str, db_path: str = None):
    """
    Initialize semantic search functionality.
    
    Args:
        index_dir: Directory containing index files
        db_path: Path to SQLite database (optional, for building embeddings)
    """
    semantic_engine.initialize(index_dir)
    
    # Build embeddings if database path is provided and embeddings don't exist
    if (db_path and os.path.exists(db_path) and 
        not semantic_engine.is_available()):
        semantic_engine.build_document_embeddings(db_path)

def get_semantic_results(query: str, top_k: int = 100) -> List[Dict[str, Any]]:
    """
    Get semantic search results for a query.
    
    Args:
        query: Search query string
        top_k: Number of top results to return
        
    Returns:
        List of semantic search results
    """
    return semantic_engine.semantic_search(query, top_k)

def is_semantic_available() -> bool:
    """Check if semantic search is available."""
    return semantic_engine.is_available()
