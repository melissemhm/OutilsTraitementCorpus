import pandas as pd
import matplotlib.pyplot as plt

def describe_and_visualize_datasets(train_data_path, dev_data_path, test_data_path):
    """
    Cette fonction lit les fichiers CSV des ensembles d'entraînement, de validation et de test,
    décrit chaque ensemble de données et visualise la distribution des longueurs des textes.

    Args:
    - train_data_path (str): Le chemin vers le fichier CSV contenant les données d'entraînement.
    - dev_data_path (str): Le chemin vers le fichier CSV contenant les données de validation (dev).
    - test_data_path (str): Le chemin vers le fichier CSV contenant les données de test.

    Returns:
    - None
    """
    # Lire les fichiers CSV des ensembles d'entraînement, de validation et de test
    train_df = pd.read_csv(train_data_path)
    dev_df = pd.read_csv(dev_data_path)
    test_df = pd.read_csv(test_data_path)

    def describe_dataset(df, name):
        print(f"--- {name} Dataset ---")
        print(f"Nombre de textes : {len(df)}")
        lengths = df['text'].apply(lambda x: len(x.split()))
        print(f"Longueur moyenne des textes : {lengths.mean():.2f} mots")
        print(f"Longueur minimale des textes : {lengths.min()} mots")
        print(f"Longueur maximale des textes : {lengths.max()} mots")
        return lengths

    # Décrire chaque ensemble de données
    train_lengths = describe_dataset(train_df, "Train")
    dev_lengths = describe_dataset(dev_df, "Dev")
    test_lengths = describe_dataset(test_df, "Test")

    # Visualiser la distribution des longueurs des textes
    plt.figure(figsize=(12, 6))
    plt.hist(train_lengths, bins=30, alpha=0.6, label='Train', color='blue', edgecolor='black')
    plt.hist(dev_lengths, bins=30, alpha=0.6, label='Dev', color='orange', edgecolor='black')
    plt.hist(test_lengths, bins=30, alpha=0.6, label='Test', color='green', edgecolor='black')
    plt.xlabel('Longueur des textes (en mots)')
    plt.ylabel('Nombre de textes')
    plt.title('Distribution des longueurs des textes dans le dataset')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

# Appel de la fonction avec les chemins des fichiers CSV des ensembles de données
describe_and_visualize_datasets('Data/train_data.csv', 'Data/dev_data.csv', 'Data/test_data.csv')
