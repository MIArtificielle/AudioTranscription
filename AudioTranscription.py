import yt_dlp
import whisper
import torch
import os
import json

# whisper_model = whisper.load_model("large-v3", "cuda")
whisper_model = whisper.load_model("./models/whisper-large-v3-french/original_model.pt", "cuda")

# Lire les URL depuis le fichier texte
video_urls = []
with open("url.lst", "r", encoding="utf-8") as file:
    video_urls = [line.strip() for line in file]

# Afficher les URL des vidéos
for url in video_urls:
  with yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': '%(id)s.%(ext)s'}) as ydl:
    info_dict = ydl.extract_info(url, download=True)
    video_file = ydl.prepare_filename(info_dict)
    if not os.path.isfile(f"{info_dict['id']}.txt"):
           result = whisper_model.transcribe(video_file, language='fr', fp16=False, prompt="Son d'une vidéo youtube d'un spécialiste de la relation amoureuse et comment récupérer son ex.")
           with open(f"{info_dict['id']}.txt", "w", encoding="utf-8") as file:
             file.write("{\n")
             file.write(f"\"<nom>\":\"{info_dict['title']}\",\n")
             description_json = json.dumps(info_dict['description'],ensure_ascii=False)
             description_json_n = description_json.replace("\\n"," ")
             description_json_nr = description_json_n.replace("\\r"," ")
             file.write(f"\"<description>\":{description_json_nr},\n")
             file.write(f"\"<url>\":\"{url}\",\n")
             file.write(f"\"<date>\":\"{info_dict['upload_date']}\",\n")
             file.write(f"\"<duration>\":\"{info_dict['duration']}\",\n")
             file.write(f"\"<views>\":\"{info_dict['view_count']}\",\n")
             file.write(f"\"<likes>\":\"{info_dict['like_count']}\",\n")
             file.write(f"\"<comments>\":\"{info_dict['comment_count']}\",\n")
             file.write(f"\"<transcription>\":\"{result['text']}\"\n")
             file.write("}\n")


