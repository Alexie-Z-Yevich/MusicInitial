import soundfile as sf
import sounddevice as sd
import time

def read_wav(file_path):
    audio_signal, sample_rate = sf.read(file_path)
    return audio_signal, sample_rate

def play_wav(file_path, duration=1):
    audio_signal, sample_rate = sf.read(file_path)
    num_samples = int(duration * sample_rate)
    audio_signal = audio_signal[:num_samples]
    sd.play(audio_signal, sample_rate)
    sd.wait()

file_paths = ["../wav/split_{}-{}.wav".format(i, i+1) for i in range(20)]
audios = []
sample_rates = []

for file_path in file_paths:
    audio, sample_rate = read_wav(file_path)
    audios.append(audio)
    sample_rates.append(sample_rate)

print("Audio signals:")
for audio in audios:
    print(audio)

print("Sample rates:")
for sample_rate in sample_rates:
    print(sample_rate)

for file_path in file_paths:
    play_wav(file_path, 20)