import os
from pydub import AudioSegment

def merge_wav_to_mp3(wav_directory, output_file):
    combined_audio = AudioSegment.empty()

    for filename in os.listdir(wav_directory):
        if filename.endswith(".wav"):
            file = os.path.join(wav_directory, filename)
            audio = AudioSegment.from_wav(file)
            combined_audio += audio

    combined_audio.export(output_file, format="mp3", parameters=["-b:a", "128k", "-ac", "2"])

# 设置输入的WAV文件目录和输出的MP3文件名
wav_directory = "../wav"
output_file = "../output.mp3"

# 调用合成函数
merge_wav_to_mp3(wav_directory, output_file)