import os
import re
import fitz  # PyMuPDF


class PDF:
    def __init__(self, name: str):
        self.name = name
        self.file_path = os.path.join("pdf", name)

    def extract_chunks(self, chunk_size: int = 1000, overlap: int = 150) -> list[dict]:
        """
        Extrait le texte du PDF et le découpe en chunks avec overlap.
        Retourne une liste de dicts avec le texte et les métadonnées.
        """
        doc = fitz.open(self.file_path)
        
        # 1. Extraire et nettoyer le texte page par page
        pages_text = []
        for page_num in range(len(doc)):
            text = doc.load_page(page_num).get_text()
            text = self._clean_text(text)
            pages_text.append((page_num + 1, text))
        
        doc.close()

        # 2. Concaténer tout le texte en gardant une trace des pages
        full_text = ""
        page_boundaries = []  # [(start_char, page_num), ...]
        for page_num, text in pages_text:
            page_boundaries.append((len(full_text), page_num))
            full_text += text + "\n\n"

        # 3. Découper en chunks avec overlap
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(full_text):
            end = start + chunk_size

            # Couper proprement sur un saut de ligne ou espace
            if end < len(full_text):
                split_pos = full_text.rfind("\n", start, end)
                if split_pos == -1:
                    split_pos = full_text.rfind(" ", start, end)
                if split_pos != -1:
                    end = split_pos

            chunk_text = full_text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "chunk_index": chunk_index,
                    "source": self.name,
                    "page": self._get_page_for_position(start, page_boundaries),
                    "start_char": start,
                    "end_char": end,
                })
                chunk_index += 1

            # Avancer en soustrayant l'overlap
            start = end - overlap

        return chunks

    def _clean_text(self, text: str) -> str:
        """Nettoie le texte extrait d'un PDF scientifique."""
        # Recoller les mots coupés en fin de ligne (tirets de césure)
        text = re.sub(r"-\n(\w)", r"\1", text)
        # Normaliser les sauts de ligne multiples
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Supprimer les espaces multiples
        text = re.sub(r" {2,}", " ", text)
        return text.strip()

    def _get_page_for_position(self, char_pos: int, page_boundaries: list) -> int:
        """Retourne le numéro de page correspondant à une position dans le texte."""
        page_num = 1
        for boundary_pos, p_num in page_boundaries:
            if char_pos >= boundary_pos:
                page_num = p_num
        return page_num