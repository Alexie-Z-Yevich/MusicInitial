from pydub import AudioSegment


def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format='wav')


if __name__ == '__main__':
    mp3_file = './sound/C1.mp3'
    wav_file = './wav/output.wav'
    convert_mp3_to_wav(mp3_file, wav_file)
    print(f"MP3 file '{mp3_file}' converted to WAV file '{wav_file}'")
