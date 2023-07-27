import sounddevice as sd
import time
import numpy as np
import librosa

# 定义各弦的音高
string_notes = [
    'E2', 'A2', 'D3', 'G3', 'B3', 'E4'
]

# 定义各品的半音差值
fret_distances = [
    0, 5, 10, 15
]


def play_note(note):
    # 使用sounddevice播放音频
    sample_rate = 44100  # 采样率
    duration = 1.0  # 持续时间，单位为秒
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequency = librosa.note_to_hz(note)  # 将音高转换为频率
    audio = np.sin(2 * np.pi * frequency * t)
    sd.play(audio, sample_rate)
    time.sleep(duration)


def main(string_index=0, fret_index=0):
    if fret_index == len(fret_distances):
        string_index = (string_index + 1) % len(string_notes)
        fret_index = 0

    if string_index == len(string_notes) - 1 and fret_index == len(fret_distances) - 1:
        return

    note = librosa.hz_to_note(librosa.note_to_hz(string_notes[string_index]) + fret_distances[fret_index])
    print(f"弦{string_index + 1} 品{fret_index + 1}：{note}")
    play_note(note)
    time.sleep(0.001)

    main(string_index, fret_index + 1)


if __name__ == '__main__':
    main()