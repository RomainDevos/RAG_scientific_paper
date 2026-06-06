from pdf_document import PDFDocument
from pdf_embeddings import PDFEmbedding
from pdf_embedding_storage import PDFEmbeddingStorage


def main():
    print("=" * 70)
    print("WORKFLOW COMPLET")
    print("=" * 70)
    print()
    
    # EXTRAIRE LES CHUNKS
    print("Extraction des chunks...")
    doc = PDFDocument("test.pdf")
    chunks = doc.extract_chunks(chunk_size=1000, overlap=150)
    print(f"{len(chunks)} chunks créés\n")
    
    # 2️⃣ GÉNÉRER LES EMBEDDINGS
    print("Génération des embeddings...")
    embedder = PDFEmbedding("all-MiniLM-L6-v2")
    embeddings = embedder.embed_chunks_batch(chunks)
    
    for chunk, embedding in zip(chunks, embeddings):
        chunk.embedding = embedding
    
    print(f"Dimension: {embedder.get_embedding_dimension()}\n")
    
    # AFFICHER UN EXEMPLE
    print("=" * 70)
    print("Exemple: Premier chunk")
    print("=" * 70)
    chunk = chunks[0]
    print(f"Texte: {chunk.get_summary(80)}")
    print(f"Mots: {chunk.get_word_count()}")
    print(f"Embedding: {chunk.embedding[:5]}...\n")
    
    # SAUVEGARDER
    print("=" * 70)
    print("Sauvegarde")
    print("=" * 70)
    storage = PDFEmbeddingStorage()
    storage.save(chunks)
    storage.save_json(chunks)
    print()
    
    # 5️⃣ CHARGER
    print("=" * 70)
    print("5️⃣ Chargement")
    print("=" * 70)
    loaded_chunks = storage.load()
    print(f"✓ Vérification: {loaded_chunks[0].has_embedding()}")


if __name__ == "__main__":
    main()