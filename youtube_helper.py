'''
Module for working with youtube videos.
'''

import youtube_dl


def download_audio(link, directory):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{directory}/audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
