"""
*****************************************************
Ce script nettoie un fichier CSV en supprimant les lignes
qui sont vides, qui contiennent peu de lettres avec de la
ponctuation, ou qui contiennent des chiffres ou des chiffres
romains. Le résultat nettoyé est écrit dans un nouveau fichier
CSV.

Ce script prend deux arguments en ligne de commande :
- Le chemin du fichier CSV d'entrée à nettoyer.
- Le chemin du fichier CSV de sortie où écrire les données nettoyées.

Exemple d'utilisation :
python3 cleaning.py raw.csv clean.csv
*****************************************************
"""


import csv  
import re   
import sys  

def is_empty_or_only_punctuation(text):
    """Vérifier si la ligne est vide ou ne contient que des signes de ponctuation."""
    if not text.strip():
        return True
    if all(char in r'. , ; : ? ! » ( ) … " ' for char in text):
        return True
    return False

def contains_few_letters_with_punctuation(text):
    """Vérifier si la ligne contient peu de lettres avec des ponctuations."""
    letters = re.findall(r'[a-zA-Z]', text)
    if len(letters) <= 5 and any(char in r' . , ; : ? ! » ( ) … " ' for char in text):
        return True
    return False

def contains_numbers_or_roman_numerals(text):
    """Vérifie si la ligne contient des chiffres ou des chiffres romains.
    Cette fonction est ajoutée pour supprimer toutes lignes qui reprèsentes des titres (contiennent le siècle du texte) ou même des numéros de page, pour ne pas avoir de problème, j'ai dû supprimer toutes les lignes.
    """
    
    arabic_digits = re.search(r'\d', text)
    roman_numerals = re.search(r'\b[IVX]+\b', text)
    
    if arabic_digits or (roman_numerals and roman_numerals.group() != text.upper()):
        return True
    return False

def process_csv(input_file, output_file):
    """Fonction pour nettoyer le fichier CSV."""
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
            reader = csv.reader(csvfile)
            writer = csv.writer(output_csv)
            for row in reader:
                if row:  
                    text = "".join(row)  
                    if is_empty_or_only_punctuation(text):
                        print(f"Supprimé (vide ou ponctuation seulement) : {text}")
                    elif contains_few_letters_with_punctuation(text):
                        print(f"Supprimé (peu de lettres avec ponctuation) : {text}")
                    elif contains_numbers_or_roman_numerals(text):
                        print(f"Supprimé (chiffres ou chiffres romains) : {text}")
                    else:
                        writer.writerow(row)  
                else:
                    print("Supprimé (ligne vide)")

if __name__ == "__main__":
    # Vérifier si deux arguments (fichiers d'entrée et de sortie) sont fournis en ligne de commande
    if len(sys.argv) != 3:
        print("Usage: python3 cleaning.py input_file.csv output_file.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_csv(input_file, output_file)
