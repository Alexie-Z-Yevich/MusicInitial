import subprocess
from moviepy.editor import AudioFileClip

# 设置输入文件路径和文件名
mp3_file_path = './music/爱的奉献.mp3'

# 设置输出文件路径和文件名
wav_file_path = './music/爱的奉献.wav'

# 使用moviepy加载音频文件
audio = AudioFileClip(mp3_file_path)

# 将音频文件保存为WAV格式
audio.write_audiofile(wav_file_path)

# # 指定ffmpeg可执行文件的路径
# ffmpeg_path = r'F:\PATH\ffmpeg-6.0-essentials_build\bin\ffmpeg.exe'
#
# # 构建ffmpeg命令
# cmd = ['ffmpeg', '-i', './sound/C2.mp3', './wav/C2.wav']
#
# # 执行ffmpeg命令
# subprocess.run(cmd)

#
# def convert_mp3_to_wav(mp3_file, wav_file):
#     ffmpeg.input(mp3_file).output(wav_file).run()
#
#
# # 测试
# mp3_file = './sound/C1.mp3'
# wav_file = './wav/C1.wav'
# convert_mp3_to_wav(mp3_file, wav_file)
