import json
import requests
import os
from pydub import AudioSegment

query = "nightingale"
#query = "duck"

url = "https://xeno-canto.org/api/2/recordings"

response = requests.get(url, params={"query": query})

if response.ok:
    data = response.json()
    # Utiliser les données ici
    download_urls = []

    for recording in data['recordings']:
        file = recording['file'] 
        #print(file)
        download_urls.append(file)

    #print("download_urls : ", download_urls)
else:
    print("Erreur de requête :", response.status_code)

# Créer un dossier pour les téléchargements
download_dir = 'datasets/' + query
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Télécharger les fichiers
for link in download_urls:
    # Obtenir le nom du fichier à partir de l'URL
    filename = query+"_"+link.split('/')[-2]+".mp3"
    filepath = os.path.join(download_dir, filename)

    # Envoyer une requête HTTP pour télécharger le fichier
    response = requests.get(link)

    # Écrire le contenu de la réponse dans un fichier
    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f'Téléchargé {filename} dans le dossier {download_dir}')
    

folder = download_dir

for filename in os.listdir(folder):
    if filename.endswith(".mp3") or filename.endswith(".wav") or filename.endswith(".ogg"):
        sound = AudioSegment.from_file(os.path.join(folder, filename))
        if len(sound) > 20000:
            os.remove(os.path.join(folder, filename))
            print("Le fichier", filename, "a été supprimé car il fait plus de 20 secondes.")