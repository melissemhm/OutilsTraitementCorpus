import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm

nlp = spacy.load('fr_core_news_sm')
train_df = pd.read_csv('Data/train_data.csv')
test_df = pd.read_csv('Data/test_data.csv')

def preprocess_text(text):
    """
    Cette fonction effectue la prétraitement du texte en utilisant le modèle spaCy.
    Elle tokenize le texte, le lemmatise en ne conservant que les mots alphabétiques,
    exclut les mots vides (stop words) et ne garde que les noms (NOUN) et les adjectifs (ADJ).

    Args:
    - text (str): Le texte à prétraiter.

    Returns:
    - list: Une liste de mots lemmatisés après le prétraitement.
    """
    doc = nlp(text)
    lemmatized_words = [
        token.lemma_ for token in doc
        if token.is_alpha and
        not token.is_stop and
        token.pos_ in {'NOUN', 'ADJ'} and
        token.lemma_ and
        len(token.lemma_) > 2  
    ]
    return lemmatized_words

def evaluate_corpus(df):
    """
    Cette fonction évalue un corpus de texte représenté par un DataFrame pandas.
    Elle calcule la longueur moyenne des phrases,
    la complexité moyenne des phrases, la diversité lexicale et les fréquences des noms et adjectifs les plus communs.

    Args:
    - df (DataFrame pandas): Le DataFrame contenant les données textuelles à évaluer.

    Returns:
    - tuple: Un tuple contenant les statistiques calculées : 
        - avg_length (float): La longueur moyenne des phrases.
        - avg_complexity (float): La complexité moyenne des phrases.
        - lexical_diversity (float): La diversité lexicale.
        - total_words (list): Une liste de tous les mots après le prétraitement.
    """
    lengths = []
    complexities = []
    total_words = []
    
    for sentence in tqdm(df['text'], desc="Processing corpus"):
        lemmatized_words = preprocess_text(sentence)
        lengths.append(len(lemmatized_words))
        complexities.append(len(set(lemmatized_words)))
        total_words.extend(lemmatized_words)
    
    avg_length = sum(lengths) / len(lengths)
    avg_complexity = sum(complexities) / len(complexities)
    lexical_diversity = len(set(total_words)) / len(total_words) if total_words else 0
    
    return avg_length, avg_complexity, lexical_diversity, total_words

# Évaluation de l'ensemble d'entraînement
train_avg_length, train_avg_complexity, train_lexical_diversity, train_total_words = evaluate_corpus(train_df)
print(f"Longueur moyenne des phrases (train) : {train_avg_length:.2f}")
print(f"Complexité moyenne des phrases (train) : {train_avg_complexity:.2f}")
print(f"Diversité lexicale (train) : {train_lexical_diversity:.4f}")

# Évaluation de l'ensemble de test
test_avg_length, test_avg_complexity, test_lexical_diversity, test_total_words = evaluate_corpus(test_df)
print(f"Longueur moyenne des phrases (test) : {test_avg_length:.2f}")
print(f"Complexité moyenne des phrases (test) : {test_avg_complexity:.2f}")
print(f"Diversité lexicale (test) : {test_lexical_diversity:.4f}")

# Distribution des fréquences des mots pour l'ensemble d'entraînement
train_word_freq = Counter(train_total_words)
train_common_words = train_word_freq.most_common(10)

print("10 noms et adjectifs les plus fréquents dans l'ensemble d'entraînement :")
for word, freq in train_common_words:
    print(f"{word}: {freq}")

# Distribution des fréquences des mots pour l'ensemble de test
test_word_freq = Counter(test_total_words)
test_common_words = test_word_freq.most_common(10)

print("10 noms et adjectifs les plus fréquents dans l'ensemble de test :")
for word, freq in test_common_words:
    print(f"{word}: {freq}")

# Visualiser la distribution des fréquences des mots sans stopwords
plt.figure(figsize=(12, 6))
train_words, train_counts = zip(*train_common_words)
test_words, test_counts = zip(*test_common_words)

bar_width = 0.35
index = range(len(train_words))

plt.bar(index, train_counts, bar_width, alpha=0.7, label='Train')
plt.bar([i + bar_width for i in index], test_counts, bar_width, alpha=0.7, label='Test')
plt.xlabel('Mots')
plt.ylabel('Fréquence')
plt.title('Distribution des 10 noms et adjectifs les plus fréquents')
plt.xticks([i + bar_width / 2 for i in index], train_words, rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
