'''
Module for working with speech recognition.
'''

import os
import shutil
import speech_recognition as sr
import editor

r = sr.Recognizer()


def recognize_speech(path, language):
    audio_file = sr.AudioFile(path)
    with audio_file as source:
        audio = r.record(source)
    return r.recognize_google(audio, language=language)


def get_transcription_from_video(path, language):
    editor.convert_video_to_wav(path)
    transcription = get_transcription_from_audio('audio.wav', language)
    return transcription


def get_transcription_from_audio(path, language):
    clip_duration = 15
    if not os.path.exists('temp_audio'):
        os.mkdir('temp_audio')
    editor.AudioEditor.split_audio_into_clips(
        path, 'temp_audio', clip_duration)

    transcription = []
    for index in range(len([i for i in os.listdir('temp_audio')])):
        recognized_speech = recognize_speech(
            f'temp_audio/{index}.wav', language)
        current_time_in_seconds = index*clip_duration
        formatted_string = f'[{current_time_in_seconds//3600}:{current_time_in_seconds//60}:{current_time_in_seconds % 60}] ' + \
            recognized_speech
        print(formatted_string)
        transcription.append(formatted_string)

    shutil.rmtree('temp_audio')

    return transcription
