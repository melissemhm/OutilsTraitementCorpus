import pandas as pd
from sklearn.model_selection import train_test_split

def split_test_data(test_data_path, dev_ratio=0.5, random_seed=42):
    """
    Cette fonction divise l'ensemble de test en ensembles de développement (dev) et de test,
    puis sauvegarde les ensembles divisés dans des fichiers CSV distincts.

    Args:
    - test_data_path (str): Le chemin vers le fichier CSV contenant les données de test.
    - dev_ratio (float): Le ratio de l'ensemble de test à utiliser pour l'ensemble de dev. Par défaut, 0.5.
    - random_seed (int): La graine aléatoire pour garantir la reproductibilité de la division. Par défaut, 42.

    Returns:
    - None
    """
    # Charger les données de test depuis le fichier CSV
    test_df = pd.read_csv(test_data_path)
    
    # Diviser l'ensemble de test en dev et test
    dev_df, final_test_df = train_test_split(test_df, test_size=dev_ratio, random_state=random_seed)
    
    # Sauvegarder les ensembles dans des fichiers CSV distincts
    dev_df.to_csv('Data/dev_data.csv', index=False)
    final_test_df.to_csv('Data/test_data.csv', index=False)
    
    print("Données divisées et sauvegardées dans 'Data/dev_data.csv' et 'Data/test_data.csv'.")

# Appel de la fonction avec le chemin vers le fichier de test
split_test_data('Data/test_data.csv')



"""
Exemple d'utilisation : 
python3 dev_split.py
"""