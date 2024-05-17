"""
Ce script charge les données augmentées, divise le corpus en ensembles d'entraînement 
et de test selon un ratio de 80/20, puis sauvegarde ces ensembles dans des fichiers CSV distincts.

Exemple d'utilisation : 
python3 Scripts/split_train_test.py

"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Lire le fichier CSV avec les données augmentées
df_final = pd.read_csv('Data/clean_filtered_augmented.csv')

# Splitter le corpus en train et test
train_df, test_df = train_test_split(df_final, test_size=0.2, random_state=42)

# Sauvegarder les ensembles d'entraînement et de test dans des fichiers CSV
train_df.to_csv('Data/train_data.csv', index=False)
test_df.to_csv('Data/test_data.csv', index=False)

print("Données d'entraînement sauvegardées dans 'Data/train_data.csv'")
print("Données de test sauvegardées dans 'Data/test_data.csv'")
