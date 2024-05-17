"""
*****************************************************
Ce script utilise la bibliothèque NLTK pour la tokenisation 
et la lemmatisation des mots, ainsi que la bibliothèque 
scipy pour le calcul des z-scores afin d'éliminer les 
données aberrantes.

Il enregistre ensuite les données filtrées dans un nouveau
fichier CSV.

Exemple d'utilisation :
python3 Scripts/donnees_00.py
*****************************************************
"""


import pandas as pd
import spacy
import fr_core_news_sm
from scipy.stats import zscore
from tqdm import tqdm

nlp = fr_core_news_sm.load()
lengths = []
complexities = []
df = pd.read_csv('Data/clean.csv')

for sentence in tqdm(df['text'], desc="Processing corpus"):
    # Tokenizer les mots de la phrase
    doc = nlp(sentence)
    words = [token.text for token in doc if token.is_alpha]
    
    # Lemmatiser les mots 
    lemmatized_words = [token.lemma_ for token in doc if token.is_alpha]
    
    # Calculer la longueur de la phrase
    lengths.append(len(lemmatized_words))
    
    # Calculer la complexité de la phrase (nombre de mots uniques)
    complexities.append(len(set(lemmatized_words)))

# Ajouter les variables temporaires au DataFrame
df['length'] = lengths
df['complexity'] = complexities

# Vérifier les outliers en utilisant les z-scores
df['length_z'] = zscore(df['length'])
df['complexity_z'] = zscore(df['complexity'])

# Filtrer les outliers (valeurs avec un z-score absolu > 3)
df_filtered = df[(df['length_z'].abs() <= 3) & (df['complexity_z'].abs() <= 3)]

# Supprimer les colonnes temporaires utilisées pour le filtrage
df_filtered = df_filtered[['text']]

# Sauvegarder les données filtrées dans un nouveau fichier CSV
df_filtered.to_csv('Data/clean_filtered.csv', index=False)

print("Données après élimination des outliers sauvegardées dans 'Data/clean_filtered.csv'")


#le fichier généré ne sera pas inclu sur le git pour ne pas le charger