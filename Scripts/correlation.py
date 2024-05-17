"""
*****************************************************
Ce script utilise la bibliothèque scikit-learn pour 
la vectorisation de texte avec TF-IDF, et la bibliothèque 
scipy pour calculer la corrélation de Pearson entre la longueur
et la complexité des phrases.

Il affiche ensuite les résultats de la corrélation.

Exemple d'utilisation :
python3 correlation.py
*****************************************************
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import pearsonr
from tqdm import tqdm

df = pd.read_csv('Data/clean.csv')

# Initialiser TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()
lengths = []
complexities = []

# Vectoriser le texte avec TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])

# Calculer la longueur et la complexité des phrases.
for sentence in tqdm(df['text'], desc="Processing corpus"):
    # Tokenizer les mots de la phrase
    words = sentence.split()
    
    # Calculer la longueur de la phrase
    lengths.append(len(words))
    
    # Calculer la complexité de la phrase (somme des valeurs TF-IDF)
    sentence_vector = tfidf_vectorizer.transform([sentence])
    complexities.append(sentence_vector.sum())

# Ajouter les variables au DataFrame
df['length'] = lengths
df['complexity'] = complexities

# Calculer la corrélation entre la longueur de la phrase et sa complexité
correlation, p_value = pearsonr(df['length'], df['complexity'])

# Afficher les résultats
print(f"Corrélation entre la longueur de la phrase et sa complexité : {correlation:.2f}")
print(f"P-valeur : {p_value:.2f}")



"""
La p-value dans mon corpus est de valeur 0.00 et le coefficient de correlation est de 0.9. 
Ces valeurs fournissent des preuves très solides que les deux variables que j'ai choisis, à savoir
la longueur de la phrase et sa complexité sont fortement corrélées. Il existe donc, une 
relation significative entre ces deux variables.
"""