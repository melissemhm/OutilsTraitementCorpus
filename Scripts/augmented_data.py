"""
Ce script utilise la bibliothèque NLTK pour augmenter un corpus de texte en remplaçant certains mots par leurs synonymes.
On utilise NLTK au lieu de Spacy dans ce corpus parce que spacy n'a pas wordnet qui contient les synonymes des mots.

Il effectue les étapes suivantes :
1. Télécharge les ressources nécessaires de NLTK pour la tokenisation, la lemmatisation et la recherche de synonymes.
2. Charge les données à augmenter à partir d'un fichier CSV.
3. Augmente chaque texte du corpus en remplaçant certains mots par leurs synonymes.
4. Ajoute les données augmentées au DataFrame original.
5. Concatène les données originales et augmentées dans un nouveau DataFrame.
6. Sauvegarde les données augmentées dans un nouveau fichier CSV.

Exemple d'utilisation : 
python3 Scripts/augmented_data.py 
"""

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
import random

# Télécharger les ressources nécessaires de nltk
with tqdm(total=3, desc="Downloading NLTK Resources") as pbar:
    nltk.download('punkt')
    pbar.update(1)
    nltk.download('wordnet')
    pbar.update(1)
    nltk.download('omw-1.4')
    pbar.update(1)

lemmatizer = WordNetLemmatizer()
df_filtered = pd.read_csv('Data/clean_filtered.csv')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.add(lemma.name())
    return list(synonyms)

def augment_sentence(sentence, n=1):
    words = word_tokenize(sentence)
    new_sentence = words[:]
    for _ in range(n):
        word_to_replace = random.choice(words)
        synonyms = get_synonyms(word_to_replace)
        if synonyms:
            synonym = random.choice(synonyms)
            new_sentence = [synonym if word == word_to_replace else word for word in new_sentence]
    return ' '.join(new_sentence)

# Appliquer l'augmentation sur tout le corpus
augmented_texts = []
for text in tqdm(df_filtered['text'], desc="Augmenting data"):
    augmented_texts.append(augment_sentence(text))

# Ajouter les nouvelles données au DataFrame
df_augmented = df_filtered.copy()
df_augmented['text'] = augmented_texts

# Concaténer les données originales et augmentées
df_final = pd.concat([df_filtered, df_augmented], ignore_index=True)

# Sauvegarder les données augmentées dans un nouveau fichier CSV
df_final.to_csv('Data/clean_filtered_augmented.csv', index=False)

print("Données après augmentation sauvegardées dans 'Data/clean_filtered_augmented.csv'")
