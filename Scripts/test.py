""" 
Un script pour essayer le scrapping du contenu textuel d'une seule URL
"""

import httpx
from lxml import html
import csv
import sys

def extract_content(root):
    content = root.xpath("/html/body/div[1]/main/div/div/div[1]/div/blockquote")
    if len(content) == 1:
        return content[0].text_content()
    return None

def main(output_file):
    url = 'https://www.etudes-litteraires.com/explications-textes/17'

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        response = httpx.get(url)
        root = html.fromstring(response.content)

            # Cibler directement les liens
        toutledoc = root.xpath("/html/body/div[1]/main/div/div/div[1]/div/ul//a/@href")
        for link in toutledoc:
            response = httpx.get(link)
            content = extract_content(html.fromstring(response.content))
            if content:
                writer.writerow({'text': content})

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test.py <output_file>")
        sys.exit(1)
    output_file = sys.argv[1]
    main(output_file)
