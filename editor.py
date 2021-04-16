'''
Module for working with audio and video files.
'''

import moviepy.editor as mp
from pydub import AudioSegment
import multiprocessing


def convert_video_to_wav(path):
    video = mp.VideoFileClip(path)
    video.audio.write_audiofile('audio.wav')


class AudioEditor:
    @staticmethod
    def split_audio_into_clips(path, directory, clip_duration):
        audio = AudioSegment.from_wav(path)

        start = 0
        for i in range(int(audio.duration_seconds//clip_duration)):
            finish = start + clip_duration * 1000
            process = multiprocessing.Process(target=AudioEditor.__export_file, args=(
                audio, f'{directory}/{i}.wav', start, finish))
            process.start()
            start = finish

    @staticmethod
    def __export_file(audio, path, start, finish):
        audio[start:finish].export(path, format='wav')
