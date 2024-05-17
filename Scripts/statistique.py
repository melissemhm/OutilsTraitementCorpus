"""
*****************************************************
Ce script effectue une analyse linguistique sur un corpus en français en utilisant spaCy. Le corpus original permet de calculer les statistiques suivantes :

    - Nombre de phrases
    - Nombre de mots
    - Nombre de mots uniques
    - Nombre moyen de mots par phrase
    - Nombre médian de mots par phrase

En plus des statistiques fournies par le corpus original, le script effectue également le comptage des catégories grammaticales (POS) des mots et mesure la diversité lexicale.

Exemple d'utilisation :
python3 statistique.py ../Data/clean.csv
*****************************************************

"""

import sys
import pandas as pd
import spacy
import numpy as np
from collections import Counter
from tqdm import tqdm

def analyze_corpus(file_path):
    """
    Calculer différentes statistiques linguistiques sur mon corpus français.
    """

    nlp = spacy.load("fr_core_news_sm")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Le fichier spécifié n'existe pas.")
        return

    # Initialiser les compteurs
    total_sentences = 0
    total_words = 0
    unique_words = set()
    words_per_sentence = []
    pos_counts = Counter()

    # Utiliser la barre de progression lors du parcours de chaque ligne du corpus pour suivre l'état d'avancement
    for text in tqdm(df['text'], desc="Traitement des textes", unit="texte"):
        doc = nlp(text)
        sentences = list(doc.sents)
        total_sentences += len(sentences)

        for sentence in sentences:
            words = [token.text for token in sentence if not token.is_punct and not token.is_space]
            if words:
                total_words += len(words)
                words_per_sentence.append(len(words))
                unique_words.update(words)
                pos_counts.update([token.pos_ for token in sentence])

    num_unique_words = len(unique_words)
    mean_words_per_sentence = total_words / total_sentences if total_sentences != 0 else 0
    median_words_per_sentence = np.median(words_per_sentence) if words_per_sentence else 0
    lexical_diversity = num_unique_words / total_words if total_words != 0 else 0

    # Afficher les résultats
    print(f"Nombre de phrases : {total_sentences}")
    print(f"Nombre de mots : {total_words}")
    print(f"Nombre de mots uniques : {num_unique_words}")
    print(f"Nombre moyen de mots par phrase : {mean_words_per_sentence:.2f}")
    print(f"Nombre médian de mots par phrase : {median_words_per_sentence}")
    print(f"Diversité lexicale : {lexical_diversity:.2f}")
    print("Comptes de catégories grammaticales (POS) :")
    for pos, count in pos_counts.items():
        print(f"{pos}: {count}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 statistique.py file.csv")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_corpus(file_path)

if __name__ == "__main__":
    main()
