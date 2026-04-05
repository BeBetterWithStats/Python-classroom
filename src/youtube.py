import yt_dlp
import os
from datetime import date
from datetime import datetime


##########################################################################
# FONCTION UTILITAIRE A RECOPIER
##########################################################################


# RETOURNER LES NOMS DES FICHIERS D'UN REPERTOIRE PASSE EN PARAMETRE

# MESSAGE DE DEMARRAGE DU PROGRAMME
def start_program():
    print()
    print()
    print("#############################################################")
    print("#                                                           #")
    print("#                  YOUTUBE DOWNLOADER                       #")
    print("#                                                           #")
    print("#     $ python3 youtube-downloader.py <URL youtube>         #")
    print("#                                                           #")
    print("#############################################################")
    print()
    return datetime.now()


# MESSAGE DE FIN DU PROGRAMME
def end_program():
    print()
    print("#############################################################")
    return datetime.now()


# TEMPS D'EXECUTION DU PROGRAMME
def print_executionTime(_start, _finish):
    print()
    print(f"[INFO] Execution = {_finish - _start}")
    print()


##########################################################################

def list_formats(video_url):
    ydl_opts = {
        'listformats': True,  # Liste tous les formats disponibles
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_url, download=False)

def download(video_url, format_code):
    ydl_opts = {
        'format': format_code,  # Utilise le format spécifié
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


############ MAIN #############
def main():

    start = start_program()

    # Demander l'URL de la vidéo à l'utilisateur
    video_url = input("Entrer l'URL de la vidéo youtube à télécharger : ").strip()

    # Lister les formats disponibles
    list_formats(video_url)

    # Demander le code du format souhaité
    format_code = input("Entrer le(s) code(s) du format à télécharger (ex: 137+140) : ").strip()


    try:
        print(f"[INFO] Téléchargement de la vidéo dans le format {format_code}...")
        download(video_url, format_code)
        print("[INFO] Téléchargement terminé avec succès.")

    except ValueError as e:
        print(f"[ERROR] Une erreur est survenue lors du téléchargement : ")
        print(type(e))
        print(e.args[0])

    end = end_program()
    print_executionTime(start, end)

    return True


############ FIN - MAIN #############

if __name__ == "__main__":
    main()
