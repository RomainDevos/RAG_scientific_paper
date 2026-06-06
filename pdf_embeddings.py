from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from pdf_chunk import PDFChunk


@dataclass
class PDFEmbedding:
    """Service pour générer des embeddings"""
    model_name: str = "all-MiniLM-L6-v2"
    model: SentenceTransformer = None
    
    def __post_init__(self):
        """Charge le modèle après création"""
        print(f"📥 Téléchargement du modèle {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        print(f"✓ Modèle prêt!")
    
    def embed_chunk(self, chunk: PDFChunk) -> list[float]:
        """Embedding pour UN chunk"""
        embedding = self.model.encode(chunk.text)
        return embedding.tolist()
    
    def embed_chunks_batch(self, chunks: list[PDFChunk]) -> list[list[float]]:
        """Embeddings pour TOUS les chunks (rapide)"""
        texts = [chunk.text for chunk in chunks]
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Retourne la dimension des vecteurs"""
        test = self.model.encode("test")
        return len(test)