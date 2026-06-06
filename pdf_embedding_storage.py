import pickle
import json
from dataclasses import dataclass
from typing import List
from pdf_chunks import PDFChunk


@dataclass
class PDFEmbeddingStorage:
    """Sauvegarde et charge les chunks avec leurs embeddings"""
    storage_file: str = "chunks_with_embeddings.pkl"
    
    def save_json(self, chunks: List[PDFChunk], json_file: str = "chunks_metadata.json"):
        """Sauvegarde les métadonnées en JSON (lisible)"""
        data = []
        for chunk in chunks:
            data.append({
                "chunk_index": chunk.chunk_index,
                "source": chunk.source,
                "page": chunk.page,
                "word_count": chunk.get_word_count(),
                "char_count": chunk.get_char_count(),
                "has_embedding": chunk.has_embedding(),
                "text_preview": chunk.get_summary(50),
            })
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f" Métadonnées sauvegardées dans {json_file}")
    
    def load(self) -> List[PDFChunk]:
        """Charge les chunks (+ embeddings) depuis le fichier"""
        with open(self.storage_file, 'rb') as f:
            chunks = pickle.load(f)
        print(f"{len(chunks)} chunks chargés depuis {self.storage_file}")
        return chunks
    
    