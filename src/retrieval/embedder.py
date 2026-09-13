import numpy as np
from src.config import EMBEDDING_MODEL
import logging

logger = logging.getLogger(__name__)

class MessageEmbedder:
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading embedding model {EMBEDDING_MODEL}")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        
    def embed(self, texts: list[str], batch_size: int = 64, show_progress_bar: bool = None) -> np.ndarray:
        """Generates normalized embeddings for a list of texts."""
        if show_progress_bar is None:
            show_progress_bar = len(texts) > 1
        embeddings = self.model.encode(
            texts, 
            batch_size=batch_size, 
            show_progress_bar=show_progress_bar, 
            convert_to_numpy=True
        )
        # Normalize for inner product (cosine similarity)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / norms
