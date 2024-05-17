"""
*****************************************************
Ce script récupère les textes littéraires
à partir du site https://www.etudes-litteraires.com/ et
les écrit dans un fichier CSV. Chaque texte
est découpée en phrases individuelles et écrite comme une
ligne distincte dans le fichier CSV.

Ce script prend un argument en ligne de commande, qui est
le chemin du fichier CSV dans lequel écrire les données.

Exemple d'utilisation :
python3 scrapping.py raw.csv
*****************************************************
"""

import httpx 
from lxml import html  
import csv 
import re  
import sys  

def get_urls(url):
    """Cette fonction accède à un lien spécifique puis récuppère tous les liens qui y existe mais filtre seulement ceux qui concernent l'explication des textes en utilisant une regex."""
    with httpx.Client(verify=False) as client:
        response = client.get(url)
        tree = html.fromstring(response.content)
        # Extraire les liens contenant "/explications-textes/" suivis de deux chiffres à la fin
        links = tree.xpath('//a[contains(@href, "/explications-textes/")]/@href')
        filtered_links = [link for link in links if re.search(r'/explications-textes/\d{2}$', link)]
        return filtered_links

def extract_specific_links(url):
    """Cette fonction extrait à parir des liens de la premère fonction des liens spécifiques qui contiennent les textes qu'on veut extraire."""
    with httpx.Client(verify=False) as client:
        response = client.get(url)
        tree = html.fromstring(response.content)
        # Extraire les liens à partir de l'emplacement spécifié avec ce chemin XPATH
        specific_links = tree.xpath('/html/body/div[1]/main/div/div/div[1]/div/ul//a/@href')
        return specific_links

def extract_content(root):
    """Cette fonction extrait le contenu texte des liens récupérés par la 2ème fonction à partir d'un élément racine donné."""
    content = root.xpath("/html/body/div[1]/main/div/div/div[1]/div/blockquote")
    #il ya des liens qui contiennent deux partie de blockquote (voire plus, et c'est difficile de mettre un chemin xpath général si y'en a plusieurs); sans cette conditoon, la fonction peut extraire un contenu autre que le texte voulu, c'est pourquoi, j'ai mis la condition d'ignorer les liens qui ont plus d'une partie  blockquote.
    if len(content) == 1:
        return content[0].text_content()
    return None

def write_to_csv(writer, text):
    """Cette fonction écrit le texte dans un fichier CSV, chaque phrase étant une ligne."""
    # Diviser le texte à chaque point et écrire chaque phrase comme une nouvelle ligne
    sentences = text.split('.')
    for sentence in sentences:
        trimmed_sentence = sentence.strip()
        if trimmed_sentence:  # s'assurer qu'aucune phrase vide n'est écrite
            writer.writerow({'text': trimmed_sentence + '.'})

def process_links_and_write_data(writer, urls):
    """Cette fonction traite les liens et écrit les données extraites dans le fichier CSV."""
    for url in urls:
        print(f"Processing {url}")
        specific_links = extract_specific_links(url)
        for link in specific_links:
            response = httpx.get(link)
            content = extract_content(html.fromstring(response.content))
            if content:
                write_to_csv(writer, content)

def main(output_file):
    """Cette fonction coordonne le processus d'extraction et d'écriture."""
    main_url = 'https://www.etudes-litteraires.com/explications-textes/'
    initial_urls = get_urls(main_url)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        process_links_and_write_data(writer, initial_urls)

if __name__ == "__main__":
    # voici la structure de la commande
    if len(sys.argv) != 2:
        print("Usage: python3 scrapping.py <output_file>")
        sys.exit(1)
    output_file = sys.argv[1]
    main(output_file)
