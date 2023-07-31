import soundfile as sf
import sounddevice as sd
import time


def read_wav(file_path):
    audio_signal, sample_rate = sf.read(file_path)
    return audio_signal, sample_rate


def play_wav(file_path, duration=1):
    audio_signal, sample_rate = sf.read(file_path)  # 读取 WAV 文件的音频信号和采样率
    num_samples = int(duration * sample_rate)  # 确定要播放的样本数量
    audio_signal = audio_signal[:num_samples]  # 仅保留指定样本数量的前部分信号
    sd.play(audio_signal, sample_rate)  # 使用 sounddevice 库播放修剪后的音频信号
    sd.wait()  # 等待音频播放完毕


# file_path = "./music/chord/Ab7.wav"
file_path = "./music/爱的奉献.wav"
audio, sample_rate = read_wav(file_path)

print("Audio signal:")
print(audio)
print("Sample rate:", sample_rate)
play_wav(file_path, 20)