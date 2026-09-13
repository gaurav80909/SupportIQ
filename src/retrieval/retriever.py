import logging
import numpy as np
from pathlib import Path
from src.retrieval.embedder import MessageEmbedder
from src.retrieval.index import FaissIndex
from src.config import TOP_K, MIN_RETRIEVAL_SIMILARITY

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, index_path: Path, metadata_path: Path):
        self.embedder = MessageEmbedder()
        self.index = FaissIndex()
        self.index.load(index_path, metadata_path)
        
    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        """Retrieves top_k similar historical conversations."""
        q_emb = self.embedder.embed([query])
        
        # Search index
        distances, indices = self.index.index.search(q_emb, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue
                
            similarity = float(distances[0][i])
            if similarity < MIN_RETRIEVAL_SIMILARITY:
                continue
                
            meta = self.index.metadata[idx].copy()
            meta['similarity'] = similarity
            # Keep string conversions safe for IDs
            meta['tweet_id'] = str(meta['tweet_id'])
            results.append(meta)
            
        return results
