from flask import Flask, render_template, request, redirect
import requests
import random as rand
import speech_recognition_helper as srh
import youtube_helper as yth

app = Flask(__name__)

result = ""

unique_links = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    youtube = request.form.get("youtube")
    lang = request.form.get("lang")
    unique_link = ""
    for num in range(16):
        unique_link += str(rand.randint(0, 9))
    directory = "main_audio"
    yth.download_audio(youtube, directory)
    transcription = srh.get_transcription_from_audio(directory+'/audio.wav', lang)
    result = transcription
    unique_links[unique_link] = result
    special_link = "/result/" + unique_link
    return redirect(special_link)

@app.route("/result/<link>")
def result(link):
    unique_link = None
    if link in unique_links:
        unique_link = unique_links[link]
    return render_template("registrants.html", final_link=unique_link)


if __name__ == "__main__":
    app.run(debug=True)
