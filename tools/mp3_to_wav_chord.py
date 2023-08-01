import os
from moviepy.editor import AudioFileClip

# 设置输入文件夹路径
mp3_folder = './sound'

# 设置输出文件夹路径
wav_folder = './music/chord'

# 遍历输入文件夹中的所有文件
for filename in os.listdir(mp3_folder):
    if filename.endswith('.mp3'):
        # 构建输入和输出文件的完整路径
        mp3_file_path = os.path.join(mp3_folder, filename)
        wav_file_path = os.path.join(wav_folder, filename[:-4] + '.wav')

        # 使用moviepy加载音频文件
        audio = AudioFileClip(mp3_file_path)

        # 将音频文件保存为WAV格式
        audio.write_audiofile(wav_file_path)