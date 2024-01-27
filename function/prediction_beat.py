import librosa


def predict_beat(wav_file):
    # 读取音频文件
    audio, sr = librosa.load(wav_file)

    # 使用librosa库提取音频的节拍信息
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)

    # 根据节拍信息计算每小节的节拍数和每个节拍的持续时间
    frames_per_beat = len(beat_frames)
    beats_per_bar = 4  # 假设每小节的节拍数为4
    beats_per_bar = int(beats_per_bar / (tempo / 60))  # 根据实际的BPM调整每小节的节拍数

    duration_per_beat = librosa.get_duration(audio) / frames_per_beat  # 计算每个节拍的持续时间

    return beats_per_bar, duration_per_beat


# 主函数
def main():
    # 输入音频文件路径
    wav_file = '../music/爱的奉献.wav'

    # 预测节拍
    beats_per_bar, duration_per_beat = predict_beat(wav_file)

    print(f'Beats per bar: {beats_per_bar}')
    print(f'Duration per beat: {duration_per_beat} seconds')


if __name__ == '__main__':
    main()
