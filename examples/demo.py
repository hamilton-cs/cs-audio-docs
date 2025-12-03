"""
Demo usage/tasks for CS 101 audio library
"""

# Allow importing cs101audio from parent directory, as this file is in subdirectory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cs101audio import *

def compare_waves():
    """
    Demonstrates the difference in waveforms (sine vs. square) at the same frequency.
    
    Expected Observation:
    - The Sine wave will appear smooth and simple.
    - The Square wave will appear harsh and blocky, demonstrating its complex harmonics.
    """
    sine = Audio()
    sine.from_generator(220, 2000, "sine")
    # sine.play()
    square = Audio()
    square.from_generator(220, 1000, "square")
    # square.play()
    sine.view_with(square)

def speed_affects_freq(factor):
    """
    Demonstrates changing the speed of an audio object directly changes its pitch (frequency).

    Arguments:
    factor -- The multiplier used to change the speed (e.g., 2 to double speed, 
            0.5 to halve speed). (int/float)

    Expected Observation:
    - If factor > 1, the pitch increases (higher frequency).
    - If factor < 1, the pitch decreases (lower frequency).
    """
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.play()
    print(f"Pitch before chaning speed: {sine.pitch_at_time(0.5)}")
    sine.change_speed(factor)
    sine.play()
    print(f"Pitch after changing speed: {sine.pitch_at_time(0.5)}")

def fade():
    """
    Demonstrates the use of fade, which only affect the amplitude of the audio, and 
    confirms that pitch/frequency remains constant.

    Expected Observation:
    - The waveform will start and end silently, gradually increasing and decreasing volume.
    - The printed 'Pitch' (frequency) values before and after the fade will be identical.
    """
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
    """
    Demonstrates the effect of normalization before a volume manipulation (crescendo) 
    to prevent digital clipping.

    The first run shows a crescendo on an already loud signal (clipping).
    The second run normalizes the signal to a lower peak first, allowing the 
    crescendo to function correctly without distortion.
    """
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
    """
    Demonstrates manual digital clipping (distortion) by limiting the maximum 
    amplitude of every sample in the audio segment.

    Arguments:
    peak -- The maximum absolute amplitude value allowed for any sample (int)

    Expected Observation:
    - The resulting audio will sound distorted or "fuzzy" due to digital clipping.
    - The waveform plot will show flat lines at the top and bottom (the 'clipped' samples).
    """
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
    """
    Generates a clear C Major chord (C4, E4, G4) by applying negative gain 
    (volume reduction) before overlaying the notes.

    Expected Observation:
    - The code plays a clean, simultaneous chord without the harsh, 'murky' 
      distortion that results from digital clipping.
    """
    C4 = Audio()
    C4.from_generator(262, 3000, "sine")

    E4 = Audio()
    E4.from_generator(330, 3000, "sine")

    G4 = Audio()
    G4.from_generator(392, 3000, "sine")

    # Reduce volume of all clips
    C4.apply_gain(-9) 
    E4.apply_gain(-9) 
    G4.apply_gain(-9)

    C4.overlay(E4)
    C4.overlay(G4)
    C4.play()
    C4.view()

def silence_every_n(audio, n):
    """
    Silences every nth entry in the sample list by setting those samples to 0.
    
    Arguments:
    audio -- The Audio object to modify (Audio)
    n -- The interval at which to silence samples (int). Every nth sample 
         (indices 0, n, 2n, 3n, ...) will be set to 0.
    
    Modifies the Audio object in-place.
    
    Expected Observation:
    - The audio will have periodic silence points, creating a stuttering effect.
    - The waveform plot will show zero-amplitude points at regular intervals.
    """
    samples = audio.get_sample_list()
    
    # Silence every nth sample (starting from index 0)
    for i in range(0, len(samples), n):
        samples[i] = 0
    
    audio.from_sample_list(samples)

def main():
    compare_waves()
    speed_affects_freq(4)
    fade()
    # normalize_crescendo()
    # clip_amplitude(20000)
    # chord()

    sine = Audio()
    sine.from_generator(220, 2000, "sine")
    # sine.apply_gain(9)
    # sine.decrescendo(start_time="HI", end_time=2000)
    # print(sine.get_amplitude_at(1001))
    # sine.play()
    # sine.view()

if __name__ == "__main__":
    main()