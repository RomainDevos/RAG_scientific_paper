# RAG Scientific Paper 📚

Système de traitement et de recherche intelligente dans des articles scientifiques en utilisant le RAG (Retrieval Augmented Generation).

## 📋 Description

Ce projet permet de :
- Extraire le texte de fichiers PDF (articles scientifiques)
- Découper le texte en chunks intelligents avec chevauchement
- Générer des embeddings pour chaque chunk
- Sauvegarder et charger les chunks avec leurs embeddings

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/RomainDevos/RAG_scientific_paper.git
cd RAG_scientific_paper
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### 1. Ajouter un PDF
Placer ton fichier PDF dans le dossier `pdf/`.

### 2. Lancer le traitement
```bash
python main.py
```

### 3. Ce que ça fait
- Extrait le texte du PDF page par page
- Découpe en chunks (1000 caractères, overlap 150)
- Génère les embeddings avec `all-MiniLM-L6-v2`
- Sauvegarde les chunks dans `chunks_with_embeddings.pkl`

## 📦 Classes

| Classe | Rôle |
|--------|------|
| `PDF` | Lit le fichier PDF et extrait le texte brut |
| `PDFChunk` | Représente un morceau de texte avec ses métadonnées |
| `PDFDocument` | Gère la collection entière de chunks |
| `PDFEmbedding` | Transforme le texte en vecteurs numériques |
| `PDFEmbeddingStorage` | Sauvegarde et charge les chunks |

## 🔧 Dépendances

| Package | Version | Rôle |
|---------|---------|------|
| PyMuPDF | 1.23.8 | Lecture des PDFs |
| sentence-transformers | 2.2.2 | Génération des embeddings |
| reportlab | 4.0.9 | Création de PDFs de test |

## 🧠 Modèle d'embedding

Le projet utilise `all-MiniLM-L6-v2` de Hugging Face :
- Léger et rapide
- Tourne sur CPU (pas besoin de GPU)
- 384 dimensions
- Téléchargé automatiquement au premier lancement

## 👤 Auteur

Romain Devos
