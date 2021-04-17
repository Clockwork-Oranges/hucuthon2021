from flask import Flask, render_template, request, redirect
import shutil
import requests
import random as rand
import speech_recognition_helper as srh
import youtube_helper as yth
import cloud_firestore as cf

app = Flask(__name__)

transfer = []

unique_links = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    youtube = request.form.get("youtube")
    lang = request.form.get("lang")
    unique_link = ""
    # for num in range(16):
    #     unique_link += str(rand.randint(0, 9))
    unique_link = str(int.from_bytes(youtube.split('=')[1].encode(), 'little'))
    transfer.append(youtube)
    transfer.append(lang)
    special_link = "/result/" + unique_link
    if cf.get_from_database(unique_link) is None:
        cf.add_to_database(unique_link, youtube, None)
    return redirect(special_link)


@app.route("/result/<link>")
def result(link):
    try:
        data_from_link = cf.get_from_database(link)
        transcription = data_from_link['transcription']
        youtube_link = data_from_link['youtube_link']
        return render_template("registrants.html", final_link=transcription, youtube=youtube_link)
    except (KeyError, TypeError):
        directory = "main_audio"
        yth.download_audio(transfer[0], directory)
        transcription = srh.get_transcription_from_audio(
            directory+'/audio.wav', transfer[1])
        cf.add_to_database(link, transfer[0], transcription)
        shutil.rmtree(directory)
        transfer.clear()
        data_from_link = cf.get_from_database(link)
        transcription = data_from_link['transcription']
        youtube_link = data_from_link['youtube_link'].split('=')[1]
        return render_template("registrants.html", final_link=transcription, youtube=youtube_link)


if __name__ == "__main__":
    app.run(debug=True)
