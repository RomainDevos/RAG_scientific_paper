import os
import re
import fitz
from dataclasses import dataclass


@dataclass
class PDF:
    """Lire un PDF et extraire le texte brut"""
    name: str
    pdf_folder: str = "pdf"
    
    def __post_init__(self):
        """Appelé après __init__ automatique"""
        self.file_path = os.path.join(self.pdf_folder, self.name)
    
    def extract_text(self) -> list[tuple[int, str]]:
        """Extrait le texte brut page par page"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"PDF non trouvé: {self.file_path}")
        
        doc = fitz.open(self.file_path)
        pages_text = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            text = self._clean_text(text)
            pages_text.append((page_num + 1, text))
        
        doc.close()
        return pages_text
    
    def _clean_text(self, text: str) -> str:
        """Nettoie le texte extrait"""
        text = re.sub(r"-\n(\w)", r"\1", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)
        return text.strip()