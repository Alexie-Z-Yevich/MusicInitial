import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import librosa
import numpy as np
from pydub import AudioSegment
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

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
        outputs = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_length=12, pad_token_id=tokenizer.eos_token_id)  # 增加 max_length 的值并设置 pad_token_id
    decoded_chord = tokenizer.decode(outputs[0], skip_special_tokens=True)
    new_inputs = tokenizer.encode_plus(decoded_chord, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(new_inputs.input_ids, attention_mask=new_inputs.attention_mask, max_length=12, pad_token_id=tokenizer.eos_token_id)  # 增加 max_length 的值并设置 pad_token_id
    score = model(input_ids=outputs, attention_mask=new_inputs.attention_mask).logits[0, -1].item()
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
        replaced_audio[i:i+len(chord_audio)] = chord_audio

    return replaced_audio

def generate_combined_mp3(replaced_audio, output_file):
    librosa.output.write_wav('temp.wav', replaced_audio, sr=44100)
    combined_audio = AudioSegment.from_wav('temp.wav')
    combined_audio.export(output_file, format='mp3')

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
for chord in selected_chords:
    scores = []
    decoded_chords = []
    for candidate_chord in chords:
        score, decoded_chord = generate_chord_score(candidate_chord)
        scores.append(score)
        decoded_chords.append(decoded_chord)
    best_chord_idx = np.argmax(scores)
    final_chords.append(decoded_chords[best_chord_idx])

print("Final Chords:", final_chords)

# 替换给定mp3文件的拍子
replaced_audio = replace_with_selected_chords(audio, final_chords)

# 生成组合的mp3文件
generate_combined_mp3(replaced_audio, output_file)