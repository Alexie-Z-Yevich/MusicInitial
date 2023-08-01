import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa
import os

# 定义各弦的音高
string_notes = [
    'E2', 'A2', 'D3', 'G3', 'B3', 'E4'
]

# 定义各品的半音差值
fret_distances = [
    0, 5, 10, 15
]

# 定义父目录路径
parent_dir = "../music/"

def play_note(note, file_path):
    # 使用 sounddevice 播放音频
    sample_rate = 44100  # 采样率
    duration = 1.0  # 持续时间，单位为秒
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequency = librosa.note_to_hz(note)  # 将音高转换为频率
    audio = np.sin(2 * np.pi * frequency * t)

    # 保存为 WAV 文件
    sf.write(file_path, audio, sample_rate)

def generate_guitar_sounds():
    for fret_index, fret_distance in enumerate(fret_distances):
        # 生成品位目录
        fret_dir = os.path.join(parent_dir, f"{fret_index+1}Point")
        os.makedirs(fret_dir, exist_ok=True)

        for string_index, string_note in enumerate(string_notes):
            # 转换品位为音符
            note = librosa.hz_to_note(librosa.note_to_hz(string_note) + fret_distance)
            file_name = f"{string_index+1}.wav"  # 生成文件名
            file_path = os.path.join(fret_dir, file_name)  # 文件路径
            print(f"Generating {note} to {file_path}")
            play_note(note, file_path)

if __name__ == '__main__':
    generate_guitar_sounds()