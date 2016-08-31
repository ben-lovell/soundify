import os
import pyaudio
import wave

def play(output, sf2, midi, play_file):
    os.system('fluidsynth -F ' + output + sf2 + midi)

    CHUNK = 1024


    wf = wave.open(play_file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
