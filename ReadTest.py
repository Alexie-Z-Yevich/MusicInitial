import soundfile as sf
import sounddevice as sd


def read_wav(file_path):
    audio_signal, sample_rate = sf.read(file_path)
    return audio_signal, sample_rate


file_path = "./music/chord/C.wav"
audio, sample_rate = read_wav(file_path)


def play_wav(file_path):
    audio_signal, sample_rate = sf.read(file_path)
    sd.play(audio_signal, sample_rate)
    sd.wait()


print("Audio signal:")
print(audio)
print("Sample rate:", sample_rate)
play_wav(file_path)