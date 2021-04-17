'''
Module for working with audio and video files.
'''

import os
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
        processes = []
        for i in range(int(audio.duration_seconds//clip_duration)):
            finish = start + clip_duration * 1000
            process = multiprocessing.Process(target=AudioEditor.__export_file, args=(
                audio, f'{directory}/{i}.wav', start, finish))
            process.start()
            processes.append(process)
            start = finish

        for process in processes:
            process.join()

        for process in processes:
            process.kill()

    @staticmethod
    def __export_file(audio, path, start, finish):
        audio[start:finish].export(path, format='wav')

    @staticmethod
    def reduce_audio_size(path, directory, start, finish):
        audio = AudioSegment.from_wav(path)
        AudioSegment.__export_file(audio, directory, start*1000, finish*1000)
        os.remove(path)
