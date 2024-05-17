"""
*****************************************************
Ce script utilise le modèle SpaCy afin de lemmatiser le texte
et calcule la fréquence des mots-clés (donnés aléatoirement) associés à 
trois thèmes aléatoires: drame, romance et vengeance. Il filtre ensuite
les lignes du corpus qui ont une fréquence non nulle pour
au moins l'un de ces thèmes.

Exemple d'utilisation :
python3 Scripts/classement.py 
*****************************************************
"""

import pandas as pd
import spacy

nlp = spacy.load("fr_core_news_sm")
df = pd.read_csv('Data/clean.csv')

# il faut lemmatiser le corpus pour faciliter le calcul selon les listes des lemmes donner pour chaque thème
def lemmatize_corpus(text):
    doc = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    return ' '.join(lemmatized_tokens)

df['lemmatized_text'] = df['text'].apply(lemmatize_corpus)

# listes des tokens donner à titre d'exemple pour chaque thème (les tokens peuvent être changé pour plus de précision)
keywords_drame = ['pleurer', 'souffrir', 'mourir', 'agoniser', 'désespérer', 'déchirer', 'angoisser', 'crier', 'regretter', 'affliger', 'sombrer', 'déplorer', 'anéantir', 'languir', 'tourmenter', 'déprimer', 'défaillir', 'désoler', 'abattre', 'éploré', 'se morfondre', 'se tourmenter', 'se désoler', 'se désespérer', 'se tordre', 'se lamenter', 'se déchirer', "s'effondrer", 'tragédie', 'larme', 'souffrance', 'peine', 'mort', 'solitude', 'chagrin', 'drame', 'agonie', 'plainte', 'tourment', 'détresse', 'angoisse', 'dépression', 'désarroi', 'déchirement', 'douleur', 'anxiété', 'mélancolie', 'affliction', 'désolation', 'désespoir', 'anéantissement', 'effondrement', 'déchirant', 'poignant', 'tragique', 'désespéré', 'affligeant', 'sombre', 'lugubre', 'funeste', 'accablant', 'déprimant', 'cruel', 'amer', 'implacable', 'insupportable', 'navrant', 'douloureux', 'pénible', 'désespérant', 'inconsolable', 'tragiquement', 'désespérément', 'amèrement', 'cruellement', 'implacablement', 'sombrement', 'lugubrement', 'inconsolablement', 'poignamment', 'déchiramment', 'douloureusement', 'tristement', 'déplorablement']

keywords_romance = ['aimer', 'passionner', 'étreindre', 'chérir', 'désirer', 'adorer', 'enlacer', 'courtiser', 'flirter', 'embrasser', 'caresser', 'fondre', 'enflammer', 'charmer', 'éblouir', 'ravir', 'idéaliser', 'enchanter', 'couvrir', 'enivrer', 'séduire', 'émouvoir', 'fasciner', 'envoûter', 'attirer', 'captiver', 'amour', 'cœur', 'romance', 'relation', 'attirance', 'flirt', 'douceur', 'serment', 'étreinte', 'affection', 'tendresse', 'béatitude', 'passion', 'émotion', 'émoi', 'délice', 'extase', 'ravissement', 'enchantement', 'idylle', 'bonheur', 'fascination', 'charme', 'séduction', 'romantique', 'passionné', 'amoureux', 'tendre', 'doux', 'suave', 'séduisant', 'enflammé', 'enchanteur', 'ravissant', 'idyllique', 'éblouissant', 'chaleureux', 'ensorcelant', 'enjôleur', 'affectueusement', 'chaleureusement', 'envoûtant', 'charmant', 'émouvant', 'enivrant', 'délicatement', 'captivant', 'irrésistiblement', 'doucement', 'tendrement', 'suavement', 'passionnément', 'ardemment', 'délicieusement', 'irrésistible']

keywords_vengeance = ['venger', 'punir', 'haïr', 'maudire', 'briser', 'affliger', 'tourmenter', 'exécuter', 'torturer', 'sanctionner', 'rétribuer', 'attaquer', 'abattre', 'assouvir', 'satisfaire', 'se venger', 'anéantir', 'rayer', 'effacer', 'damner', 'condamner', 'détruire', 'blesser', 'écraser', 'exterminer', 'éliminer', 'châtier', 'colère', 'justice', 'haine', 'revanche', 'destruction', 'souffrance', 'tourment', 'châtiment', 'supplice', 'rage', 'courroux', 'ressentiment', 'animosité', 'vindicte', 'représailles', 'exécution', 'rétribution', 'punition', 'dommage', 'blessure', 'traîtrise', 'rancœur', 'vengeance', 'rancune', 'coléreux', 'haineux', 'amer', 'rancunier', 'destructeur', 'brutal', 'froid', 'sombre', 'sinistre', 'sanguinaire', 'vengeur', 'cruel', 'vindicatif', 'impitoyable', 'violemment', 'férocement', 'vengeusement', 'sauvagement', 'amèrement', 'impitoyablement', 'implacablement', 'furieusement', 'froidement', 'cruellement', 'sombrement']

# fonction pour calculer la fréquence de chaque thème.
def calculate_keyword_frequency(text, keywords):
    word_count = sum(text.count(keyword) for keyword in keywords)
    if len(text.split()) > 0:
        frequency = round(word_count / len(text.split()), 2)
    else:
        frequency = 0.0
    return frequency

df['keyword_frequency_drame'] = df['lemmatized_text'].apply(lambda x: calculate_keyword_frequency(x, keywords_drame))
df['keyword_frequency_romance'] = df['lemmatized_text'].apply(lambda x: calculate_keyword_frequency(x, keywords_romance))
df['keyword_frequency_vengeance'] = df['lemmatized_text'].apply(lambda x: calculate_keyword_frequency(x, keywords_vengeance))

# Fonction pour calculer la longueur des phrases
def calculate_sentence_length(text):
    return len(text.split())

df['sentence_length'] = df['text'].apply(calculate_sentence_length)

pd.set_option('display.max_rows', None)

# Affichage des statistiques calculées
#print("Statistiques calculées :")
#print(df[['keyword_frequency_drame', 'keyword_frequency_romance', 'keyword_frequency_vengeance', 'sentence_length']])

#ajout d'une fonction qui filtre les lignes qui ont une fréquence nulle, c'est à dire qui ne sont pas classées dans ces thèmes.
def filter_non_zero_freq_rows(df):
    return df[(df['keyword_frequency_drame'] != 0) | (df['keyword_frequency_romance'] != 0) | (df['keyword_frequency_vengeance'] != 0)]

# Appliquer le filtre et afficher le résultat
filtered_df = filter_non_zero_freq_rows(df)
print("Statistiques calculées avec fréquence différente de zéro :")
print(filtered_df[['keyword_frequency_drame', 'keyword_frequency_romance', 'keyword_frequency_vengeance', 'sentence_length']])