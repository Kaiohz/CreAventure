import argparse
import queue
import sys
import sounddevice as sd
import main as m
import json
import wave

from vosk import Model, KaldiRecognizer

q = queue.Queue()
discussionCourant = ""
messageFinal = ""


def interPreteur(fichierWave) :
    with wave.open(fichierWave,"rb") as wf :
        model = Model(model_path="model")
        record = KaldiRecognizer(model,wf.getframerate())
        while True :
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if record.AcceptWaveform(data) :
                result = record.Result()
                
                return json.loads(result)["text"]