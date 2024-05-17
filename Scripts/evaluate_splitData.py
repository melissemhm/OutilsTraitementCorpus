import pandas as pd
import spacy
import numpy as np
from prettytable import PrettyTable

nlp = spacy.load("fr_core_news_sm")
train_df = pd.read_csv('Data/train_data.csv')
test_df = pd.read_csv('Data/test_data.csv')

def evaluate_corpus(df):
    """
    Cette fonction évalue le corpus représenté par un DataFrame pandas.
    Elle calcule plusieurs statistiques sur les corpus séparés train et test.

    Args:
    - df (DataFrame pandas): Le DataFrame contenant les données textuelles à évaluer.

    Returns:
    - dict: Un dictionnaire contenant les statistiques calculées.
    """
    lengths = []
    complexities = []
    num_sentences = len(df)
    total_words = 0
    unique_words = set()
    
    for sentence in df['text']:
        doc = nlp(sentence)
        lemmatized_words = [token.lemma_ for token in doc if token.is_alpha]
        
        lengths.append(len(lemmatized_words))
        complexities.append(len(set(lemmatized_words)))
        
        total_words += len(lemmatized_words)
        unique_words.update(lemmatized_words)
    
    avg_length = sum(lengths) / num_sentences
    avg_complexity = sum(complexities) / num_sentences
    median_length = np.median(lengths)
    
    return {
        "Nombre de phrases": num_sentences,
        "Nombre de mots": total_words,
        "Nombre de mots uniques": len(unique_words),
        "Nombre moyen de mots par phrase": avg_length,
        "Nombre médian de mots par phrase": median_length,
        "Complexité moyenne des phrases": avg_complexity
    }

# Évaluation de l'ensemble d'entraînement et de test
train_stats = evaluate_corpus(train_df)
train_stats["Dataset"] = "Train"
test_stats = evaluate_corpus(test_df)
test_stats["Dataset"] = "Test"

table = PrettyTable()
table.field_names = train_stats.keys()

table.add_row(train_stats.values())
table.add_row(test_stats.values())
print(table)


"""
Exemple d'utilisation : 
python3 Scripts/evaluate_splitData.py 

"""

#Les résultats observés indiquent que les deux corpus ont été divisé équitablement selon les résultats du Nombre moyen de mots par phrase | Nombre médian de mots par phrase | Complexité moyenne des phrases.