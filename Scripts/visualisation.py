"""
*****************************************************
Ce script utilise la bibliothèque pandas pour charger
les données d'un fichier CSV nettoyé et la bibliothèque
matplotlib pour visualiser deux aspects des données :
la distribution de la longueur des phrases et la loi de
Zipf des mots fréquents.

- La distribution de la longueur des phrases est représentée
  par un histogramme montrant le nombre de mots dans chaque
  phrase.

- La loi de Zipf des mots fréquents est représentée par un
  graphique logarithmique du rang des mots par rapport à leur
  fréquence.

Ce script charge les données, les analyse et génère des
visualisations pour aider à comprendre la nature du texte.

*****************************************************
"""


import pandas as pd  
import matplotlib.pyplot as plt  
import sys 

def visualize_text_data(csv_file):
    """Cette fonction charge les données du corpus qui est en fichier CSV et visualise la distribution de la longueur des phrases
    ainsi que la loi de Zipf des mots fréquents."""
    df = pd.read_csv(csv_file)
    text_lengths = df['text'].apply(lambda x: len(x.split()))

    # Visualisation de la distribution de la longueur des phrases
    plt.figure(figsize=(10, 6))
    plt.hist(text_lengths, bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution de la longueur des phrases')
    plt.xlabel('Nombre de mots')
    plt.ylabel('Nombre de phrases')
    plt.grid(True)
    plt.show()

    # Calculer la fréquence des mots dans l'ensemble du texte
    word_counts = df['text'].str.split(expand=True).stack().value_counts()

    # Visualisation de la loi de Zipf des mots fréquents
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(word_counts) + 1), word_counts.values, marker='o', linestyle='-', color='orange')
    plt.title('Distribution de Zipf des mots fréquents')
    plt.xlabel('Rang du mot (log)')
    plt.ylabel('Fréquence du mot (log)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 visualisation.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    visualize_text_data(csv_file)
