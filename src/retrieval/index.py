import faiss
import numpy as np
import pickle
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FaissIndex:
    def __init__(self, dimension: int = 384):
        # Using IndexFlatIP for Inner Product (which equals cosine similarity for normalized vectors)
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []
        
    def add(self, embeddings: np.ndarray, metadata: list[dict]):
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata must have the same length.")
        self.index.add(embeddings)
        self.metadata.extend(metadata)
        
    def save(self, index_path: Path, metadata_path: Path):
        faiss.write_index(self.index, str(index_path))
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
            
    def load(self, index_path: Path, metadata_path: Path):
        self.index = faiss.read_index(str(index_path))
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
