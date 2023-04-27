#!/usr/bin/env python

import json
import requests
import os
from pathlib import Path
import numpy as np

queries = ["nightingale", "Bluethroat"]
#query = "duck"

dataset_dir = Path('datasets')
url = "https://xeno-canto.org/api/2/recordings"

def sendQuery(query):
    response = requests.get(url, params={"query": query})

    if response.ok:
        data = response.json()
        # Utiliser les données ici
        download_urls = []

        for recording in data['recordings']:
            file = recording['file']
            #print(file)
            time = np.array(recording["length"].split(':'), int)
            #print(time)
            if time[0] == 0 and time[1] <= 20:
                #print("Adding")
                download_urls.append(file)

        #print("download_urls : ", download_urls)
        return download_urls
    else:
        print("Erreur de requête (", query, "):", response.status_code)
        return False

def downloadFiles(query, urls):
    # Créer un dossier pour les téléchargements
    download_dir = dataset_dir / query
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Télécharger les fichiers
    for link in urls[:20]:
        # Obtenir le nom du fichier à partir de l'URL
        filename = query+"_"+link.split('/')[-2]+".mp3"
        filepath = os.path.join(download_dir, filename)

        # Envoyer une requête HTTP pour télécharger le fichier
        response = requests.get(link)

        # Écrire le contenu de la réponse dans un fichier
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f'Téléchargé {filename} dans le dossier {download_dir}')

for query in queries:
    download_urls = sendQuery(query)
    downloadFiles(query, download_urls)

# folder = download_dir

# for filename in os.listdir(folder):
#     if filename.endswith(".mp3") or filename.endswith(".wav") or filename.endswith(".ogg"):
#         sound = AudioSegment.from_file(os.path.join(folder, filename))
#         if len(sound) > 20000:
#             os.remove(os.path.join(folder, filename))
#             print("Le fichier", filename, "a été supprimé car il fait plus de 20 secondes.")
