"""
Demo usage/tasks for CS 101 audio library
"""

from cs101audio import *

# Constants for 16-bit audio (signed short integer)
MAX_VAL = 32767
MIN_VAL = -32768

def compare_waves():
    sine = Audio()
    sine.from_generator(220, 1000, "sine")
    sine.play()
    sine.view()
    square = Audio()
    square.from_generator(220, 1000, "square")
    square.play()
    square.view()
    # WILL OVERLAY THEM

def speed_affects_freq(factor):
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.play()
    print(f"Pitch before chaning speed: {sine.pitch_at_time(0.5)}")
    sine.change_speed(factor)
    sine.play()
    print(f"Pitch after changing speed: {sine.pitch_at_time(0.5)}")

def fade():
    sine = Audio()
    sine.from_generator(220, 2000, "sine")
    sine.fade(1000, 1000)
    print(f"Pitch before fade: {sine.pitch_at_time(1)}")

    # View the waveform
    sine.play()
    sine.view()

    # Observe how frequency does not change => amplitude does NOT affect frequency
    print(f"Pitch after fade: {sine.pitch_at_time(1)}")

def normalize_crescendo():
    # Use normalization to give Audio room to "grow" during crescendo becuase
    # values cannot exceed 32767

    # Without normalize (audio alraedy close to max amplitude)
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.crescendo()
    sine.play()
    sine.view()

    # With normalization
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.normalize(15000)
    sine.crescendo()
    sine.play()
    sine.view()

def clip_amplitude(peak):
    three_note = Audio()
    three_note.open_audio_file("sample.wav")
    samples = three_note.get_sample_list()

    for i in range(len(samples)):
        if samples[i] > peak:
            samples[i] = peak
        elif samples[i] < - peak:
            samples[i] = - peak

    # Alternative approach:
    for i in range(len(samples)):
        samples[i] = max(min(samples[i], peak), -peak)

    three_note.from_sample_list(samples)
    three_note.play()
    three_note.view()

def chord():
    C4 = Audio()
    C4.from_generator(262, 3000, "sine")
    C4.play()

    E4 = Audio()
    E4.from_generator(330, 3000, "sine")

    G4 = Audio()
    G4.from_generator(392, 3000, "sine")

    C4.overlay(E4)
    C4.overlay(G4)
    C4.play()

def main():
    # compare_waves()
    speed_affects_freq(4)
    # fade()
    # normalize_crescendo()
    # clip_amplitude(20000)
    # chord()

    # Other audios to use
    three_note = Audio()
    three_note.open_audio_file("sample.wav")

    song = Audio()
    song.open_audio_file("Summer.wav")
    song_samples = song.get_sample_list()
    song.from_sample_list(song_samples[1000000:1500000])

if __name__ == "__main__":
    main()