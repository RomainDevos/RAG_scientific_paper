from dataclasses import dataclass, field
from typing import List
from pdf import PDF
from pdf_chunks import PDFChunk


@dataclass
class PDFDocument:
    """Orchestrer l'extraction et la gestion des chunks"""
    pdf_name: str
    pdf_folder: str = "pdf"
    chunks: List[PDFChunk] = field(default_factory=list)
    pdf: PDF = field(init=False)
    
    def __post_init__(self):
        """Initialise le PDF après la création"""
        self.pdf = PDF(self.pdf_name, self.pdf_folder)
    
    def extract_chunks(
        self, chunk_size: int = 1000, overlap: int = 150
    ) -> List[PDFChunk]:
        """Découpe le PDF en chunks avec chevauchement"""
        pages_text = self.pdf.extract_text()
        
        full_text = ""
        page_boundaries = []
        
        for page_num, text in pages_text:
            page_boundaries.append((len(full_text), page_num))
            full_text += text + "\n\n"
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(full_text):
            end = start + chunk_size
            
            if end < len(full_text):
                split_pos = full_text.rfind("\n", start, end)
                if split_pos == -1:
                    split_pos = full_text.rfind(" ", start, end)
                if split_pos != -1 and split_pos > start:
                    end = split_pos
            
            chunk_text = full_text[start:end].strip()
            
            if chunk_text:
                chunks.append(PDFChunk(
                    text=chunk_text,
                    chunk_index=chunk_index,
                    source=self.pdf.name,
                    page=self._get_page_for_position(start, page_boundaries),
                    start_char=start,
                    end_char=end,
                ))
                chunk_index += 1
            
            start = end - overlap
        
        self.chunks = chunks
        return chunks
    
    def get_chunks_by_page(self, page: int) -> List[PDFChunk]:
        """Récupère les chunks d'une page"""
        return [chunk for chunk in self.chunks if chunk.page == page]
    
    def search_in_chunks(self, keyword: str) -> List[PDFChunk]:
        """Recherche un mot-clé"""
        keyword_lower = keyword.lower()
        return [
            chunk for chunk in self.chunks 
            if keyword_lower in chunk.text.lower()
        ]
    
    def get_chunk_by_index(self, index: int) -> PDFChunk:
        """Accède à un chunk par index"""
        if not (0 <= index < len(self.chunks)):
            raise IndexError(f"Index {index} invalide")
        return self.chunks[index]
    
    def merge_chunks(self, start_index: int, end_index: int) -> PDFChunk:
        """Fusionne plusieurs chunks"""
        if not (0 <= start_index < end_index < len(self.chunks)):
            raise IndexError("Indices invalides")
        
        merged = self.chunks[start_index]
        for i in range(start_index + 1, end_index + 1):
            merged = merged.merge_with(self.chunks[i])
        return merged
    
    def get_statistics(self) -> dict:
        """Retourne les stats du document"""
        if not self.chunks:
            return {"total_chunks": 0, "total_words": 0, "total_chars": 0, "pages": 0}
        
        total_words = sum(chunk.get_word_count() for chunk in self.chunks)
        total_chars = sum(chunk.get_char_count() for chunk in self.chunks)
        pages = max(chunk.page for chunk in self.chunks)
        
        return {
            "total_chunks": len(self.chunks),
            "total_words": total_words,
            "total_chars": total_chars,
            "pages": pages,
        }
    
    def _get_page_for_position(self, char_pos: int, page_boundaries: list) -> int:
        """Détermine la page pour une position"""
        page_num = 1
        for boundary_pos, p_num in page_boundaries:
            if char_pos >= boundary_pos:
                page_num = p_num
        return page_num