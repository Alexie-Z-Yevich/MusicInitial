import librosa
import numpy as np
import torch
import torchaudio
from transformers import Wav2Vec2Processor

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")

def similarCompare(target_audio, b_audio):


    # 预处理音频并指定sampling_rate
    target_input = processor(target_audio, return_tensors="pt", padding=True, sampling_rate=16000)
    b_input = processor(b_audio, return_tensors="pt", padding=True, sampling_rate=16000)

    # 计算相似度（可以使用余弦相似度或其他度量方法）
    target_embedding = target_input.input_values.squeeze(0).mean(dim=0).unsqueeze(0)
    b_embedding = b_input.input_values.squeeze(0).mean(dim=0).unsqueeze(0)
    similarity = torch.cosine_similarity(target_embedding, b_embedding).item()

    return abs(similarity)
