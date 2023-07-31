from pydub import AudioSegment
from pydub.playback import play

# 设置输入文件路径和文件名
mp3_file_path = './sound/C2.mp3'

# 使用pydub加载音频文件
audio = AudioSegment.from_mp3(mp3_file_path)

# 播放音频
play(audio)



# from pydub import AudioSegment
# from pydub.playback import play
#
#
# def play_music(file_path):
#     audio = AudioSegment.from_mp3(file_path)
#     play(audio)
#
#
# file_path = "./sound/C1.mp3"  # Path to your MP3 file
# play_music(file_path)

# from playsound import playsound
#
# file_path = "./sound/C1.mp3"  # Path to your MP3 file
# playsound(file_path)


# import pygame
#
#
# def play_music(file_path):
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play()
#
#
# file_path = "./sound/C1.mp3"  # 将此处的路径替换为你的MP3文件路径
# play_music(file_path)
