import soundfile as sf
import os

def split_wav(input_file, output_folder, duration, max_duration):
    # 读取wav文件
    audio_data, sr = sf.read(input_file)
    total_duration = min(audio_data.shape[0]/sr, max_duration)  # 取最小值，防止超过音频总时长
    start_time = 0

    # 拆分wav文件
    while start_time < total_duration:
        # 计算拆分的结束时间
        end_time = start_time + duration
        if end_time > total_duration:
            end_time = total_duration

        # 拆分音频片段
        output_file = os.path.join(output_folder, f"split_{start_time}-{end_time}.wav")
        start_frame = int(start_time * sr)
        end_frame = int(end_time * sr)
        audio_segment = audio_data[start_frame:end_frame]
        sf.write(output_file, audio_segment, sr)

        # 更新起始时间
        start_time = end_time

# 测试例子
input_file = "../music/爱的奉献.wav"  # 输入的wav文件名
output_folder = "../wav"  # 输出的文件夹名
duration = 1  # 拆分的时长（秒）
max_duration = 20  # 最大切割长度（秒）

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 拆分wav文件
split_wav(input_file, output_folder, duration, max_duration)