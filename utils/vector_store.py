import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    """
    A simple in-memory vector store implementation using TF-IDF vectorization.
    """
    
    def __init__(self):
        """Initialize the vector store."""
        self.documents = []
        self.vectorizer = TfidfVectorizer()
        self.vectors = None
        
    def add_documents(self, documents):
        """
        Add documents to the vector store.
        
        Args:
            documents: A list of strings (document texts).
        """
        # Add to existing documents
        self.documents.extend(documents)
        
        # Recompute vectors for all documents
        self._update_vectors()
    
    def _update_vectors(self):
        """Update the vectors for all documents."""
        if not self.documents:
            self.vectors = None
            return
            
        # Fit and transform the documents
        self.vectors = self.vectorizer.fit_transform(self.documents)
    
    def search(self, query, top_k=3):
        """
        Search for documents similar to the query.
        
        Args:
            query: A string representing the search query.
            top_k: An integer representing the number of top documents to return.
            
        Returns:
            A list of tuples (document_text, similarity_score).
        """
        if not self.documents or self.vectors is None:
            return []
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Compute similarities
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top-k documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return top-k documents with their similarity scores
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Only include relevant results
                results.append((self.documents[idx], similarities[idx]))
        
        return results
    
    def clear(self):
        """Clear all documents from the vector store."""
        self.documents = []
        self.vectors = None
