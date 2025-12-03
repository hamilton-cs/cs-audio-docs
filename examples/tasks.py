"""
Demo tasks for CS 101 audio library
"""

# Allow importing cs101audio from parent directory, as this file is in subdirectory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
    sine = Audio()
    sine.from_generator(220, 3000, "sine")
    # sine = clip_amplitude(sine, 1000)
    # sine = silence_every_n_sample(sine, 5)
    # sine = mute_chunk(sine, 1000, 2000)
    # sine = plot_to_replicate(sine)
    # sine.play()
    # sine.view()

    # replicated = Audio()
    # replicated.from_generator(220, 3000, "sine")
    # replicated = replicate_plot(replicated, 1000)
    # replicated.play()
    # replicated.view()

    three_note = Audio()
    three_note.open_audio_file("sample.wav")
    three_note.play()
    three_note = reverse(three_note)
    three_note.play()

    # three_note = echo(three_note)
    # three_note = adjust_amplitude_additively(three_note, 1000)
    # three_note = normalize(three_note, 10000)

    # three_note.play()
    # three_note.view()


if __name__ == "__main__":
    main()