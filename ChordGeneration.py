import os
import soundfile as sf
import numpy as np
import librosa

chords = {
    'C': ['E3', 'C4', 'E4', 'G4'],
    'D': ['A3', 'D4', 'F#4', 'A4'],
    'Am': ['A2', 'C3', 'E3', 'A3'],
    'Em': ['E2', 'G3', 'B3', 'E4']
}


def generate_chord_sounds():
    chord_dir = "./music/chord"
    os.makedirs(chord_dir, exist_ok=True)

    duration = 2.0
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    for chord_name, chord_notes in chords.items():
        chord_path = os.path.join(chord_dir, f"{chord_name}.wav")

        chord_audio = np.zeros(len(t))
        for string_note in chord_notes:
            string_audio = generate_string_sound(string_note, t)
            chord_audio += string_audio

        sf.write(chord_path, chord_audio, sample_rate)
        print(f"Generated chord {chord_name} to {chord_path}")


def generate_string_sound(note, t):
    frequency = librosa.note_to_hz(note)
    audio = np.sin(2 * np.pi * frequency * t)
    return audio


if __name__ == '__main__':
    generate_chord_sounds()
