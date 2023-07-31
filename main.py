import multiprocessing
import time
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
import numpy as np
import librosa
from pydub import AudioSegment
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 设置最大执行时间（单位：秒）
max_execution_time = 100  # 秒

# 加载GPT-2模型和Tokenizer
model_name = "gpt2-medium"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained(model_name).to(device).eval()

# 音频库路径
audio_library_path = './sound'
# 输出文件路径
output_file = 'output.mp3'


def create_chord_library():
    chords = []

    chord_files = os.listdir(audio_library_path)
    for chord_file in chord_files:
        if chord_file.endswith(".mp3"):
            chord_name = os.path.splitext(chord_file)[0]
            chords.append(chord_name)

    return chords


def generate_chord_score(chord):
    inputs = tokenizer.encode_plus(chord, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_length=50,
                                 pad_token_id=tokenizer.pad_token_id)

    score = outputs[0, -1].item()
    decoded_chord = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return score, decoded_chord


def select_chords(beats, chords):
    selected_chords = []
    for beat in beats:
        selected_chord = chords[beat % len(chords)]
        selected_chords.append(selected_chord)
    return selected_chords


def replace_with_selected_chords(audio, selected_chords):
    replaced_audio = np.zeros_like(audio)

    for i, chord_name in enumerate(selected_chords):
        chord_audio_file = os.path.join(audio_library_path, f"{chord_name}.mp3")
        chord_audio = librosa.load(chord_audio_file, mono=True, sr=44100)[0]
        replaced_audio[i:i + len(chord_audio)] = chord_audio

    return replaced_audio


def generate_combined_mp3(replaced_audio, output_file):
    librosa.output.write_wav('temp.wav', replaced_audio, sr=44100)
    combined_audio = AudioSegment.from_wav('temp.wav')
    combined_audio.export(output_file, format='mp3')


def matching_chords(selected_chords, chords, final_chords):
    for selected_chord in selected_chords:
        scores = []
        decoded_chords = []
        for chord in chords:
            score, decoded_chord = generate_chord_score(chord)
            scores.append(score)
            decoded_chords.append(decoded_chord)
        best_chord_idx = np.argmax(scores)
        final_chord = decoded_chords[best_chord_idx]
        final_chords.append(final_chord)


class StoppableProcess(multiprocessing.Process):
    def __init__(self, target):
        multiprocessing.Process.__init__(self, target=target)
        self._stop_event = multiprocessing.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def match_chords(selected_chords, chords, final_chords):
    matching_chords(selected_chords, chords, final_chords)


if __name__ == '__main__':
    # 替换给定mp3文件的拍子
    mp3_file = './music/爱的奉献.mp3'
    audio, sr = librosa.load(mp3_file, sr=44100)
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, units="time")
    beat_samples = librosa.time_to_samples(beat_frames, sr=sr)
    segment_length = len(beat_samples) // 4  # 每个小节的长度

    # 创建和弦库
    chords = create_chord_library()

    # 选择合适的和弦
    selected_chords = select_chords(beat_samples, chords)

    # 匹配最合适的和弦
    final_chords = []

    # 创建一个可停止的进程来执行和弦匹配
    process = multiprocessing.Process(target=match_chords, args=(selected_chords, chords, final_chords))
    process.start()

    start_time = time.time()

    # 检查执行时间并停止进程
    while process.is_alive():
        current_time = time.time()
        execution_time = current_time - start_time

        if execution_time >= max_execution_time:
            process.terminate()  # 终止进程
            print("程序执行时间已超过最大限制")
            break

    process.join()  # 等待进程结束

    print("Final Chords:", final_chords)

    # 替换给定mp3文件的拍子
    replaced_audio = replace_with_selected_chords(audio, final_chords)

    # 生成组合的mp3文件
    generate_combined_mp3(replaced_audio, output_file)

# import os
#
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# import librosa
# import numpy as np
# from pydub import AudioSegment
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
#
# # 加载GPT-2模型和Tokenizer
# model_name = "gpt2-medium"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# model = GPT2LMHeadModel.from_pretrained(model_name).to(device).eval()
#
# # 音频库路径
# audio_library_path = './sound'
# # 输出文件路径
# output_file = 'output.mp3'
#
#
# def create_chord_library():
#     chords = []
#
#     chord_files = os.listdir(audio_library_path)
#     for chord_file in chord_files:
#         if chord_file.endswith(".mp3"):
#             chord_name = os.path.splitext(chord_file)[0]
#             chords.append(chord_name)
#
#     return chords
#
#
# def generate_chord_score(chord):
#     inputs = tokenizer.encode_plus(chord, return_tensors="pt", padding=True, truncation=True).to(device)
#     with torch.no_grad():
#         outputs = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_length=50,
#                                  pad_token_id=tokenizer.pad_token_id)
#
#     score = outputs[0, -1].item()
#     decoded_chord = tokenizer.decode(outputs[0], skip_special_tokens=True)
#
#     return score, decoded_chord
#
#
# def select_chords(beats, chords):
#     selected_chords = []
#     for beat in beats:
#         selected_chord = chords[beat % len(chords)]
#         selected_chords.append(selected_chord)
#     return selected_chords
#
#
# def replace_with_selected_chords(audio, selected_chords):
#     replaced_audio = np.zeros_like(audio)
#
#     for i, chord_name in enumerate(selected_chords):
#         chord_audio_file = os.path.join(audio_library_path, f"{chord_name}.mp3")
#         chord_audio = librosa.load(chord_audio_file, mono=True, sr=44100)[0]
#         replaced_audio[i:i + len(chord_audio)] = chord_audio
#
#     return replaced_audio
#
#
# def generate_combined_mp3(replaced_audio, output_file):
#     librosa.output.write_wav('temp.wav', replaced_audio, sr=44100)
#     combined_audio = AudioSegment.from_wav('temp.wav')
#     combined_audio.export(output_file, format='mp3')
#
#
# # 替换给定mp3文件的拍子
# mp3_file = './music/爱的奉献.mp3'
# audio, sr = librosa.load(mp3_file, sr=44100)
# tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, units="time")
# beat_samples = librosa.time_to_samples(beat_frames, sr=sr)
# segment_length = len(beat_samples) // 4  # 每个小节的长度
#
# # 创建和弦库
# chords = create_chord_library()
#
# # 选择合适的和弦
# selected_chords = select_chords(beat_samples, chords)
#
# # 匹配最合适的和弦
# final_chords = []
# for chord in selected_chords:
#     scores = []
#     decoded_chords = []
#     for candidate_chord in chords:
#         score, decoded_chord = generate_chord_score(candidate_chord)
#         scores.append(score)
#         decoded_chords.append(decoded_chord)
#     best_chord_idx = np.argmax(scores)
#     final_chords.append(decoded_chords[best_chord_idx])
#
# print("Final Chords:", final_chords)
#
# # 替换给定mp3文件的拍子
# replaced_audio = replace_with_selected_chords(audio, final_chords)
#
# # 生成组合的mp3文件
# generate_combined_mp3(replaced_audio, output_file)
#
