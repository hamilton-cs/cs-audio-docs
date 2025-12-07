"""
Demo tasks for CS 101 audio library
"""

# Allow importing cs101audio from src directory in parent folder
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cs101audio import *

# Constants for 16-bit audio (signed short integer)
MAX_AMPLITUDE = 32767
MIN_AMPLITUDE = -32768

def clip_amplitude(audio, peak):
    '''
    TASK: "Clip" amplitudes of an audio by replacing all values greater than the peak 
    with the peak value. Return the updated Audio object.
    '''
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
    return audio

def silence_every_n_sample(audio, n):
    '''
    TASK: Set every n sample of an audio to 0. Reutrn the updated Audio object.
    '''
    samples = audio.get_sample_list()
    for i in range(0, len(samples), n):
        samples[i] = 0

    audio.from_sample_list(samples)
    return audio

def adjust_amplitude_additively(audio, amount):
    '''
    TASK: Increase the volume for all the positive values and decrease the 
    volume for all the negative values by a given amount. Return the updated Audio object.
    '''
    samples = audio.get_sample_list()
    for i in range(len(samples)):
        if samples[i] > 0:
            samples[i] = min(MAX_AMPLITUDE, samples[i] + amount)
        elif samples[i] < 0:
            samples[i] = max(MIN_AMPLITUDE, samples[i] - amount)

    audio.from_sample_list(samples)
    return audio

def mute_chunk(audio, start_time, end_time):
    '''
    TASK: Mute the audio from start_time to end_time (milliseconds). Return the 
    updated Audio object.
    '''

    samples = audio.get_sample_list()
    frame_rate = audio.get_frame_rate()

    # Find index numbers
    start_idx = int((start_time * frame_rate) / 1000)
    end_idx = int((end_time * frame_rate) / 1000)

    # Mute the audio in the calculated range
    for i in range(start_idx, end_idx):
        samples[i] = 0
    
    audio.from_sample_list(samples)
    return audio

def reverse(audio):
    '''
    TASK: Reverse the audio. Return the updated Audio object.
    '''
    samples = audio.get_sample_list()
    # Approach 1
    reversed_samples = list(reversed(samples))
    # Approach 2
    reversed_samples = samples[::-1]
    audio.from_sample_list(reversed_samples)
    return audio

def echo(audio, delay=11000, decay=0.5):
    '''
    TASK: Create an echo effect by adding a delayed, quieted copy of 
    the audio signal back into the original signal.
    '''
    original_samples = audio.get_sample_list()
    echoed = original_samples.copy()  # make a copy so we preserve original values

    # Error checking if delay is longer than length of audio (for loop would return error)
    if delay >= len(original_samples):
        print("Delay is longer than the length of audio.")
        return original_samples
    
    for i in range(delay, len(original_samples)):
        # Apply the echo effect
        new_sample_value = original_samples[i] + int(decay * original_samples[i - delay])
        
        # Implement Clipping (Clamp the value within the 16-bit range)
        if new_sample_value > MAX_AMPLITUDE:
            echoed[i] = MAX_AMPLITUDE
        elif new_sample_value < MIN_AMPLITUDE:
            echoed[i] = MIN_AMPLITUDE
        else:
            echoed[i] = new_sample_value

    audio.from_sample_list(echoed)

    # Alternatively, can clip the audio after replacing values by calling clip_amplitude
    # return clip_amplitude(audio, MAX_AMPLITUDE)

    return audio

def normalize(audio, max_amp=MAX_AMPLITUDE):
    '''
    TASK: Adjust the amplitude of all samples in the Audio object so that the largest 
    positive or negative sample (the peak amplitude) exactly matches the specified 
    maximum amplitude (default is 32767 for 16-bit audio). This ensures the sound is 
    as loud as possible without distortion.
    '''
    samples = audio.get_sample_list()
    largest = max(samples)
    smallest = min(samples)
    max_abs = max(abs(smallest), abs(largest))

    # Handle the edge case of a silent (all-zero) audio clip
    if max_abs == 0:
        return audio

    multiplier = max_amp / max_abs

    for i in range(len(samples)):
        samples[i] = int(samples[i] * multiplier)

    audio.from_sample_list(samples)
    return audio

def plot_to_replicate(audio):
    '''
    Creates plot for student to view and replicate with thier own function.
    '''
    audio.normalize(15000)
    audio.crescendo()
    
    return audio


def replicate_plot(audio, duration):
    '''
    TASK: View the plot created by the plot_to_replicate function. Return the updated
    Audio object.
    '''
    samples = audio.get_sample_list()
    frame_rate = audio.get_frame_rate()

    duration_in_samples = int((duration * frame_rate) / 1000)
    
    for i in range(duration_in_samples):
        multiplier = i / duration_in_samples
        scaled = samples[i] * multiplier
        samples[i] = int(scaled)

    audio.from_sample_list(samples)
    return audio

def main():
    # Get available functions with their parameters
    available_functions = {
        '1': ('clip_amplitude', clip_amplitude, ['peak']),
        '2': ('silence_every_n_sample', silence_every_n_sample, ['n']),
        '3': ('adjust_amplitude_additively', adjust_amplitude_additively, ['amount']),
        '4': ('mute_chunk', mute_chunk, ['start_time', 'end_time']),
        '5': ('reverse', reverse, []),
        '6': ('echo', echo, ['delay', 'decay']),
        '7': ('normalize', normalize, ['max_amp']),
        '8': ('plot_to_replicate', plot_to_replicate, []),
        '9': ('replicate_plot', replicate_plot, ['duration'])
    }
    
    # Show menu
    print("\nAvailable task functions:")
    for key, (name, func, params) in available_functions.items():
        param_str = f" (needs: {', '.join(params)})" if params else ""
        print(f"  {key}. {name}{param_str}")
    
    # Get user choice
    choice = input("\nEnter function number (or name): ").strip()
    
    # Try to find by number or name
    if choice in available_functions:
        name, func, params = available_functions[choice]
    else:
        # Try to find by name
        found = None
        for key, (name, func, params) in available_functions.items():
            if name == choice:
                found = (name, func, params)
                break
        if not found:
            print(f"Unknown function: {choice}")
            return
        name, func, params = found
    
    # Create or load audio
    print("\nAudio source:")
    print("  1. Generate sine wave (default)")
    print("  2. Load from file")
    audio_choice = input("Enter choice (1 or 2, default 1): ").strip()
    
    audio = Audio()
    if audio_choice == '2':
        filename = input("Enter audio filename: ").strip()
        try:
            audio.open_audio_file(filename)
            print(f"Loaded: {filename}")
        except FileNotFoundError:
            print(f"File not found: {filename}. Using default sine wave.")
            audio.from_generator(220, 3000, "sine")
    else:
        audio.from_generator(220, 3000, "sine")
        print("Using default sine wave (220 Hz, 3 seconds)")
    
    # Get parameters if needed
    args = []
    if 'peak' in params:
        peak = input("Enter peak amplitude (default 1000): ").strip()
        args.append(int(peak) if peak else 1000)
    elif 'n' in params:
        n = input("Enter n value (default 5): ").strip()
        args.append(int(n) if n else 5)
    elif 'amount' in params:
        amount = input("Enter amount (default 1000): ").strip()
        args.append(int(amount) if amount else 1000)
    elif 'start_time' in params:
        start_time = input("Enter start time in ms (default 1000): ").strip()
        args.append(int(start_time) if start_time else 1000)
        end_time = input("Enter end time in ms (default 2000): ").strip()
        args.append(int(end_time) if end_time else 2000)
    elif 'delay' in params:
        delay = input("Enter delay in samples (default 11000): ").strip()
        args.append(int(delay) if delay else 11000)
        decay = input("Enter decay factor (default 0.5): ").strip()
        args.append(float(decay) if decay else 0.5)
    elif 'max_amp' in params:
        max_amp = input(f"Enter max amplitude (default {MAX_AMPLITUDE}): ").strip()
        args.append(int(max_amp) if max_amp else MAX_AMPLITUDE)
    elif 'duration' in params:
        duration = input("Enter duration in ms (default 1000): ").strip()
        args.append(int(duration) if duration else 1000)
    
    # Run the function
    print(f"\nRunning {name}...")
    audio = func(audio, *args)
    
    # Ask if user wants to play/view
    print("\nWhat would you like to do with the result?")
    print("  1. Play audio")
    print("  2. View audio")
    print("  3. Both")
    print("  4. Nothing (just return)")
    action = input("Enter choice (1-4, default 4): ").strip()
    
    if action == '1' or action == '3':
        audio.play()
    if action == '2' or action == '3':
        audio.view()

if __name__ == "__main__":
    main()