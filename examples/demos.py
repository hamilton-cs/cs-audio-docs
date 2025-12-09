"""
Demo usage/tasks for CS 101 audio library
"""

# Allow importing cs101audio from src directory in parent folder
from errno import EILSEQ
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cs101audio import *

# Constants for 16-bit audio (signed short integer)
MAX_AMPLITUDE = 32767
MIN_AMPLITUDE = -32768

def compare_waves():
    """
    Demonstrates the difference in waveforms (sine vs. square) at the same frequency.
    
    Expected Observation:
    - The Sine wave will appear smooth and simple.
    - The Square wave will appear harsh and blocky, demonstrating its complex harmonics.
    """
    sine = Audio()
    sine.from_generator(220, 2000, "sine")
    print("Playing sine wave...")
    sine.play()
    square = Audio()
    square.from_generator(220, 1000, "square")
    print("Playing square wave...")
    square.play()
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
    print("Playing original audio...")
    sine.play()
    print(f"Pitch before changing speed: {sine.pitch_at_time(500):.2f}")
    sine.change_speed(factor)
    print("Playing modified audio...")
    sine.play()
    print(f"Pitch after changing speed: {sine.pitch_at_time(500):.2f}")

def fade():
    """
    Demonstrates the use of fade, which only affect the amplitude of the audio, and 
    confirms that pitch/frequency remains constant.

    Expected Observation:
    - The waveform will start and end silently, gradually increasing and decreasing volume.
    - The printed 'Pitch' (frequency) values before and after the fade will be identical.
    """
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.fade(1000, 1000)
    print(f"Pitch before fade: {sine.pitch_at_time(500)}")

    # Play the modified sine wave
    sine.play()

    # Observe how frequency does not change => amplitude does NOT affect frequency
    print(f"Pitch after fade: {sine.pitch_at_time(500)}")
    
    # View the waveform
    sine.view()

def normalize_crescendo():
    """
    Demonstrates the effect of normalization before a volume manipulation (crescendo) 
    to prevent digital clipping.

    The first run shows a crescendo on an already loud signal (clipping).
    The second run normalizes the signal to a lower peak first, allowing the 
    crescendo to function correctly without distortion.
    """
    # Without normalize (audio already close to max amplitude)
    print("Part 1: Playing audio with crescendo and without normalization (will cause clipping)...")
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.crescendo()
    sine.play()
    sine.view()

    # With normalization
    print("\nPart 2: Playing audio with normalization and crescendo (no clipping)...")
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    sine.normalize(5000)
    sine.crescendo(final_multiplier=6)
    sine.play()
    sine.view()

def clip_amplitude(peak):
    """
    Demonstrates manual digital clipping (distortion) by limiting the maximum 
    amplitude of every sample in the audio segment.
    
    Automatically loads three_note.wav from the samples directory.

    Arguments:
    peak -- The maximum absolute amplitude value allowed for any sample (int)

    Expected Observation:
    - The resulting audio will sound distorted or "fuzzy" due to digital clipping.
    - The waveform plot will show flat lines at the top and bottom (the 'clipped' samples).
    """
    audio = Audio()
    try:
        audio.open_audio_file("../samples/three_note.wav")
        print("Loaded: ../samples/three_note.wav")
    except FileNotFoundError:
        try:
            audio.open_audio_file("samples/three_note.wav")
            print("Loaded: samples/three_note.wav")
        except FileNotFoundError:
            print("Error: Could not find three_note.wav. Please ensure it exists in the samples directory.")
            return
    
    samples = audio.get_sample_list()

    for i in range(len(samples)):
        if samples[i] > peak:
            samples[i] = peak
        elif samples[i] < - peak:
            samples[i] = - peak

    # Alternative approach:
    for i in range(len(samples)):
        samples[i] = max(min(samples[i], peak), -peak)

    audio.from_sample_list(samples)
    audio.play()
    audio.view()
    return audio

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
    print("Playing a C Major chord (C4, E4, G4)...")
    C4.play()
    C4.view()

def main():
    # Get available functions
    available_functions = {
        '1': ('compare_waves', compare_waves, []),
        '2': ('speed_affects_freq', speed_affects_freq, ['factor']),
        '3': ('fade', fade, []),
        '4': ('normalize_crescendo', normalize_crescendo, []),
        '5': ('clip_amplitude', clip_amplitude, ['peak']),
        '6': ('chord', chord, [])
    }
    
    # Show menu
    print("\nAvailable demo functions:")
    for key, (name, func, params) in available_functions.items():
        # Show params but exclude 'audio' from display (it's handled separately)
        display_params = [p for p in params if p != 'audio']
        param_str = f" (needs: {', '.join(display_params)})" if display_params else ""
        print(f"  {key}. {name}{param_str}")
    
    # Get user choice
    choice = input("\nEnter function number: ").strip()
    
    # Find function by number
    if choice not in available_functions:
        print(f"Invalid function number: {choice}")
        return
    
    name, func, params = available_functions[choice]
    
    # Get parameters if needed
    args = []
    if 'factor' in params:
        factor = input("Enter speed factor (default 4.0): ").strip()
        args.append(float(factor) if factor else 4.0)
    elif 'peak' in params:
        peak = input(f"Enter peak amplitude (default {10000}): ").strip()
        args.append(int(peak) if peak else 10000)
    
    # Run the function
    print(f"\nRunning {name}...")
    func(*args)

if __name__ == "__main__":
    main()
