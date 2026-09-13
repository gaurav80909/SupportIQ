import pytest
from src.retrieval.index import FaissIndex
import numpy as np
from pathlib import Path

def test_faiss_index(tmp_path):
    idx = FaissIndex(dimension=2)
    embeddings = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    metadata = [{"id": 1}, {"id": 2}]
    
    idx.add(embeddings, metadata)
    assert idx.index.ntotal == 2
    
    ip = tmp_path / "idx.faiss"
    mp = tmp_path / "meta.pkl"
    
    idx.save(ip, mp)
    
    idx2 = FaissIndex(dimension=2)
    idx2.load(ip, mp)
    assert idx2.index.ntotal == 2
    assert idx2.metadata[0]["id"] == 1
