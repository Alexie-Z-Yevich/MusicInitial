import os
import glob
import numpy as np
import librosa
from sklearn.metrics import pairwise_distances_argmin_min
import soundfile as sf
import sounddevice as sd
import scipy.spatial.distance as dist

from function.similarCompare import similarCompare


def get_wav_files(directory):
    # 获取目录下所有的wav文件
    wav_files = glob.glob(os.path.join(directory, "*.wav"))
    return wav_files


def audio_matching(target_file, b_directory):
    # 加载目标文件
    target, sr = librosa.load(target_file, sr=None)

    # 将目标文件切分成1秒一段
    target_segments = []
    duration = 1  # 切分后每段的时长
    n_samples = len(target)
    n_segments = int(n_samples / (sr * duration))
    for i in range(n_segments):
        start = i * sr * duration
        end = min(start + sr * duration, n_samples)
        segment = target[start:end]
        target_segments.append(segment)

    # 切分版本
    # 加载B集合中的文件
    b_files = get_wav_files(b_directory)
    b_segments = []
    b_filenames = []
    for b_file in b_files:
        audio, _ = librosa.load(b_file, sr=sr)

        # 将B集合中的文件切分成1秒一段
        n_samples = len(audio)
        n_segments = int(n_samples / (sr * duration))
        for i in range(n_segments):
            start = i * sr * duration
            end = min(start + sr * duration, n_samples)
            segment = audio[start:end]
            b_segments.append(segment)
            b_filenames.append(os.path.basename(b_file))

    # # 不切分版本
    # # 加载B集合中的文件
    # b_files = get_wav_files(b_directory)
    # b_segments = []
    # b_filenames = []
    #
    # for b_file in b_files:
    #     audio, _ = librosa.load(b_file, sr=sr)
    #     b_segments.append(audio)
    #     b_filenames.append(os.path.basename(b_file))

    # 计算目标文件每段与B集合每段的相似度
    similarities = []
    for target_segment in target_segments:
        segment_similarities = []
        for b_segment in b_segments:
            # 提取MFCC特征
            target_mfcc = librosa.feature.mfcc(y=target_segment, sr=sr)
            b_mfcc = librosa.feature.mfcc(y=b_segment, sr=sr)

            # 对特征进行调整，使其具有相同的形状
            max_frames = max(target_mfcc.shape[1], b_mfcc.shape[1])
            target_mfcc = np.pad(target_mfcc, ((0, 0), (0, max_frames - target_mfcc.shape[1])), mode='constant')
            b_mfcc = np.pad(b_mfcc, ((0, 0), (0, max_frames - b_mfcc.shape[1])), mode='constant')

            # 计算MFCC特征之间的距离
            similarity = similarCompare(target_mfcc, b_mfcc)
            print(similarity)
            segment_similarities.append(similarity)
        similarities.append(segment_similarities)
        if len(similarities) > 20:
            break

    # 选出每段中最相似的B中的音频
    matched_indices = [min(enumerate(similarity), key=lambda x: x[1])[0] for similarity in similarities]
    matched_files = [b_filenames[index] for index in matched_indices]

    return matched_files


def play_wav(file_path, duration=1):
    file_path = os.path.join(b_directory, file_path)  # 构建完整的文件路径
    audio_signal, sample_rate = sf.read(file_path)  # 读取 WAV 文件的音频信号和采样率
    num_samples = int(duration * sample_rate)  # 确定要播放的样本数量
    audio_signal = audio_signal[:num_samples]  # 仅保留指定样本数量的前部分信号
    sd.play(audio_signal, sample_rate)  # 使用 sounddevice 库播放修剪后的音频信号
    sd.wait()  # 等待音频播放完毕

# 设置目标文件和B集合所在的目录
target_file = "../music/爱的奉献.wav"
b_directory = "../music/chord"

# 进行音频匹配
matched_files = audio_matching(target_file, b_directory)

# 打印匹配结果
for i, matched_file in enumerate(matched_files):
    print(f"第 {i + 1} 秒: 匹配到文件 {matched_file}")
    play_wav(matched_file, 2)
