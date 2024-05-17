"""
****************************************************
En faisant le TP de la séance 3, j'avais l'erreur comme quoi 
des lignes dans mon fichier CSV contiennt plus d'une colonne
c'est pourquoi j'ai ajouté ce script colonne.py

Ce script regroupe les colonnes d'un fichier CSV en une seule.
Le résultat est enregistré dans un nouveau fichier CSV.

Ce script prend deux arguments en ligne de commande :
- Le chemin du fichier CSV d'entrée à traiter.
- Le chemin du fichier CSV de sortie où écrire les données
  avec les colonnes regroupées.

Exemple d'utilisation :
python3 colonne.py input_file.csv clean.csv
****************************************************
"""


import csv  
import sys  

def group_columns(input_file, output_file):
    """Cette fonction regroupe les colonnes d'un fichier CSV en une seule colonne."""
    with open(input_file, 'r', newline='') as f_input:
        with open(output_file, 'w', newline='') as f_output:
            csv_input = csv.reader(f_input)
            csv_output = csv.writer(f_output)

            for row in csv_input:
                if len(row) > 1:
                    text = ' '.join(row)
                    csv_output.writerow([text])
                else:
                    # Écrire la ligne telle quelle si elle contient une seule colonne
                    csv_output.writerow(row)

    print("Le regroupement des colonnes a été effectué avec succès. Le résultat est enregistré dans", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 colonne.py input_file.csv output_file.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    group_columns(input_file, output_file)
