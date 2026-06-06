from dataclasses import dataclass, field


@dataclass
class PDFChunk:
    """Représente un chunk de texte extrait d'un PDF"""
    text: str
    chunk_index: int
    source: str
    page: int
    start_char: int
    end_char: int
    embedding: list[float] = field(default_factory=list)
    
    def get_word_count(self) -> int:
        return len(self.text.split())
    
    def get_char_count(self) -> int:
        return len(self.text)
    
    def get_summary(self, max_length: int = 100) -> str:
        if len(self.text) > max_length:
            return self.text[:max_length] + "..."
        return self.text
    
    def is_valid(self) -> bool:
        return len(self.text.strip()) > 0
    
    def has_embedding(self) -> bool:
        return len(self.embedding) > 0
    
    def merge_with(self, other: "PDFChunk") -> "PDFChunk":
        if self.source != other.source:
            raise ValueError("Sources différentes")
        return PDFChunk(
            text=self.text + " " + other.text,
            chunk_index=self.chunk_index,
            source=self.source,
            page=self.page,
            start_char=self.start_char,
            end_char=other.end_char,
        )