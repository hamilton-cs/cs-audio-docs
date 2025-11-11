"""
A Pydub-based audio library for introductory computer science.

All files that use the CS101 Audio package must have the following line
at the top of the file:

from cs101audio import *
"""

from pydub import AudioSegment
from pydub.generators import Sine
from pydub.generators import Sawtooth
from pydub.generators import Square
from pydub.generators import Triangle
from pydub.playback import play
import array

import warnings # For ignoring a PyDub warning that runs everytime you run your code
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work")
warnings.filterwarnings("ignore", message="Couldn't find ffplay or avplay - defaulting to ffplay, but may not work")

from pydub import * # For the Base AudioSegment Class
from pydub.playback import * # For playing back audio
from pydub.generators import * # For generating audio waves

# Imports for GUI plots
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MAX_AMPLITUDE = 32767
MIN_AMPLITUDE = -32768

def _check_type(param, param_name, target_type):
    """
    Checks if a parameter is of the correct type and raises a TypeError if not.

    Args:
        param (any): The parameter to check.
        param_name (str): The name of the parameter (for the error message).
        target_type (type): The expected type (e.g., int, str, Audio).

    Raises:
        TypeError: If 'param' is not an instance of 'target_type'.
    """
    if not isinstance(param, target_type):
        raise TypeError("\nThe parameter '" + param_name + "' should be a " +
                        str(target_type.__name__) +
                        " but instead was a " +
                        str(type(param).__name__) + "\n" +
                        param_name + " = " + str(param))


class Audio():
    """
    Wrapper Class for the Pydub AudioSegment Class
    """

    def __init__(self, duration=0, frame_rate=44100):
        """
        Initializes a silent audio segment.

        Args:
            duration (int, optional): The length of the silent audio segment
                in milliseconds. Defaults to 0.
            frame_rate (int, optional): The frame rate in frames per second.
                Defaults to 44100.
        """
        self._audioseg = AudioSegment.silent(duration=duration, frame_rate=frame_rate)


    def set_audioseg(self, newaudio):
        """
        Sets the internal pydub.AudioSegment object.

        Args:
            newaudio (pydub.AudioSegment): The new audio segment to replace
                self._audioseg.
        """
        self._audioseg = newaudio

    def get_audioseg(self):
        """
        Gets the internal pydub.AudioSegment object.

        Returns:
            pydub.AudioSegment: The internal audio segment.
        """
        return self._audioseg

    def get_sample_list(self):
        """
        Gets the audio data as a list of samples.

        Returns:
            list[int]: The list of audio samples.
        """
        return self._audioseg.get_array_of_samples().tolist()
    
    def get_frame_rate(self):
        """
        Gets the frame rate of the audio.

        Returns:
            int: The frame rate in Hz (frames per second).
        """
        return self._audioseg.frame_rate

    def __len__(self):
        """
        Gets the length of the audio in milliseconds.

        Returns:
            int: The duration of the audio in milliseconds.
        """
        return len(self._audioseg)

    def open_audio_file(self, filename):
        """
        Opens an audio file and loads it into this Audio object.

        Args:
            filename (str): The path to the audio file to open.

        Raises:
            FileNotFoundError: If the specified file does not exist.

        .. code-block:: python

            audio = Audio()
            audio.open_audio_file("example.wav")
            audio.play()

            # create and play a new audio object using a file "example.wav"
        """
        
        _check_type(filename, "filename", str)
        try:
            AudioSegment.from_file(filename)
        except FileNotFoundError:
            raise FileNotFoundError("File " + filename + " not found")

        self._audioseg = AudioSegment.from_file(filename)
        
        
    def save_to_file(self, filename):
        """
        Saves the audio to a file.

        The file format is determined by the file extension (e.g., ".wav", ".mp3").

        Args:
            filename (str): The name of the file to save to.
        """
        extendindex = filename.find(".")
        file_extension = filename[extendindex + 1:]
      
        self._audioseg.export(out_f=(filename), \
                              format=file_extension)

    def from_sample_list(self, sample_lst, template=None):
        """
        Loads audio data from a list of samples.

        This method uses metadata (like frame rate, sample width) from a
        template Audio object. If no template is provided, it uses its own
        current metadata.

        Args:
            sample_lst (list[int]): The list of samples to generate the audio from.
            template (Audio, optional): An Audio object to use as a template
                for metadata. Defaults to self.
        """
        if isinstance(sample_lst, list):
            sample_lst = array.array('h', sample_lst)
            
        if not template:
            template = self
            
        # If an sample list is spliced, it may have a incorret total number of samples
        # When attempting to play this, an error occurs because the total sample
        # count is not a multiple of 4 and the number of channels
        # So if this occurs, we append 0s until it is a multiple
        while len(sample_lst) * template.get_audioseg().channels % 4 != 0:
            sample_lst.append(0)
            
        self._audioseg = template.get_audioseg()._spawn(sample_lst)

    def from_generator(self, freq, duration, wavetype):
        """
        Generates a wave and loads it into this Audio object.

        Args:
            freq (int): The frequency of the wave to be generated (in Hz).
            duration (int): The duration of the wave (in milliseconds).
            wavetype (str): The type of wave ("Sine", "Square", "Sawtooth",
                or "Triangle"). Case-insensitive.

        Raises:
            ValueError: If an invalid 'wavetype' is provided.
            TypeError: If 'freq' or 'duration' are not ints, or 'wavetype'
                is not a str.
        """
        _check_type(wavetype, "wavetype", str)
        _check_type(freq, "freq", int)
        _check_type(duration, "duration", int)
        self._duration = duration
        if wavetype.upper() == "SINE":
            wave = Sine(freq)
        elif wavetype.upper() == "SAWTOOTH":
            wave = Sawtooth(freq)
        elif wavetype.upper() == "SQUARE":
            wave = Square(freq)
        elif wavetype.upper() == "TRIANGLE":
            wave = Triangle(freq)
        else:
            raise ValueError("Error! Invalid Wavetype \"" + wavetype + "\" passed to from_generator")

        self._audioseg = wave.to_audio_segment(duration)
        #self._audioseg = self._audioseg.fade_in(50).fade_out(100)

    def play(self):
        """
        Plays the current audio segment, if it isn't empty.
        """
        if len(self._audioseg) > 0:
            play(self._audioseg)
            

    def __add__(self, other_audio):
        """
        Concatenates this audio with another. (Implements the + operator).

        Does not modify the original Audio objects.

        Args:
            other_audio (Audio): The audio object to append to the end of this one.

        Returns:
            Audio: A new Audio object containing the concatenated audio.
        """ 
        _check_type(other_audio, "other_audio", Audio)

        result = Audio()

        result.set_audioseg(self._audioseg + other_audio.get_audioseg())

        return result

    def __iadd__(self, other_audio):
        """
        Concatenates another audio in-place. (Implements the += operator).

        Modifies this Audio object.

        Args:
            other_audio (Audio): The audio object to append.

        Returns:
            Audio: self, modified.
        """
        _check_type(other_audio, "other_audio", Audio)

        self._audioseg += other_audio.get_audioseg()
        return self


    def __mul__(self, loopnum):
        """
        Repeats (loops) the audio segment. (Implements the * operator).

        Does not modify the original Audio object.

        Args:
            loopnum (int): The number of times to repeat the audio.

        Returns:
            Audio: A new Audio object containing the looped audio.
        """
        _check_type(loopnum, "loopnum", int)

        result = Audio()
        result.set_audioseg(self._audioseg * loopnum)

        return result

    def __imul__(self, loopnum):
        """
        Repeats (loops) the audio segment in-place. (Implements the *= operator).

        Modifies this Audio object.

        Args:
            loopnum (int): The number of times to repeat the audio.

        Returns:
            Audio: self, modified.
        """
        _check_type(loopnum, "loopnum", int)

        self._audioseg *= loopnum
        return self

    def __getitem__(self, millisecond):
        """
        Gets a slice of the audio. (Implements the [] operator).

        Args:
            millisecond (int or slice): The millisecond to index or a slice
                object (e.g., `slice(1000, 2000)` for 1s to 2s).

        Returns:
            Audio: A new Audio object containing the specified slice.
        """
        result = Audio()
        result.set_audioseg(self._audioseg[millisecond])

        return result


    def overlay(self, audio2, position=0, loop=False):
        """
        Overlays (mixes) another audio onto this one.

        Modifies this Audio object in-place.

        Args:
            audio2 (Audio): The audio object to overlay.
            position (int, optional): The time in milliseconds at which to
                start the overlay. Defaults to 0.
            loop (bool, optional): If True, loops 'audio2' to fill the
                duration of this audio. Defaults to False.
        """
        self._audioseg = self._audioseg.overlay(audio2.get_audioseg(), position=position, loop=loop)
        
    def apply_gain(self, gain):
        """
        Applies a gain (volume change) to the audio.

        Modifies this Audio object in-place.

        Args:
            gain (int or float): The amount of gain in decibels (dB).
                Positive values make it louder, negative values make it quieter.
        """
        self._audioseg = self._audioseg.apply_gain(gain)
        
    def fade_in(self, fadetime):
        """
        Applies a fade-in to the beginning of the audio.

        Modifies this Audio object in-place.

        Args:
            fadetime (int): The duration of the fade-in (in milliseconds).
        """
        _check_type(fadetime, "fadetime", int)
        self._audioseg = self._audioseg.fade_in(fadetime)
        
    def fade_out(self, fadetime):
        """
        Applies a fade-out to the end of the audio.

        Modifies this Audio object in-place.

        Args:
            fadetime (int): The duration of the fade-out (in milliseconds).
        """
        _check_type(fadetime, "fadetime", int)
        self._audioseg = self._audioseg.fade_out(fadetime)
        
    def fade(self, fadeintime=0, fadeouttime=0):
        """
        Applies both a fade-in and a fade-out.

        Modifies this Audio object in-place.

        Args:
            fadeintime (int, optional): The duration of the fade-in
                (in milliseconds). Defaults to 0.
            fadeouttime (int, optional): The duration of the fade-out
                (in milliseconds). Defaults to 0.
        """
        _check_type(fadeintime, "fadeintime", int)
        _check_type(fadeouttime, "fadeouttime", int)
        self._audioseg = self._audioseg.fade_in(fadeintime).fade_out(fadeouttime)
        

    def change_speed(self, factor):
        """
        Changes the speed of the audio without changing the pitch.

        Modifies this Audio object in-place.

        Args:
            factor (int or float): The speed multiplier.
                (e.g., 2.0 is 2x speed, 0.5 is half speed).

        Raises:
            TypeError: If 'factor' is not an int or float.
            ValueError: If 'factor' is 0.
        """
        if not (isinstance(factor, int) or isinstance(factor, float)):
            raise TypeError("\nThe parameter '" + factor + "' should be a " +
                        "int or float but instead was a " +
                        str(type(factor).__name__) + "\n" +
                        "factor" + " = " + str(factor))
        if factor == 0:
            raise ValueError("Error! Cannot change speed by a factor of 0")

        sound_with_altered_frame_rate = self._audioseg._spawn(self._audioseg.raw_data, overrides={
                                        "frame_rate": int(self._audioseg.frame_rate * factor)})
        
        self._audioseg = sound_with_altered_frame_rate.set_frame_rate(self._audioseg.frame_rate)

    def normalize(self, max_amplitude=MAX_AMPLITUDE):
        """
        Normalizes the audio to a specific peak amplitude.

        Adjusts the amplitude so the loudest sample (positive or negative)
        matches 'max_amplitude', scaling all other samples proportionally.
        This makes the audio as loud as possible without clipping.

        Modifies this Audio object in-place.

        Args:
            max_amplitude (int, optional): The target peak absolute amplitude.
                Defaults to MAX_AMPLITUDE (32767).

        Raises:
            ValueError: If 'max_amplitude' is negative or > MAX_AMPLITUDE.
            ZeroDivisionError: If the audio is completely silent (all samples are 0).
        """
        if max_amplitude > MAX_AMPLITUDE:
            raise ValueError("Max amplitude cannot exceed 32,767.")
        elif max_amplitude < 0:
            raise ValueError("Max amplitude must be positive.")
        
        sample_list = self._audioseg.get_array_of_samples().tolist()
        largest = max(sample_list)
        smallest = min(sample_list)
        peak = max(abs(smallest), abs(largest))

        if peak == 0:
            raise ZeroDivisionError("Audio is silent; normalization skipped.")
            return

        multiplier = max_amplitude / peak
        for i in range(len(sample_list)):
            sample_list[i] = int(sample_list[i] * multiplier)
        self.from_sample_list(sample_list)


    def reverse(self):
        """
        Reverses the audio.

        Modifies this Audio object in-place.
        """
        self.from_sample_list(list(reversed(self.get_sample_list())))

    def average_amplitude(self, start_time=0, end_time=None):
        """
        Calculates the average absolute amplitude over a time range.
        
        Note: This method uses seconds, unlike most others which use milliseconds.

        Args:
            start_time (float, optional): The start time of the range
                (in seconds). Defaults to 0.
            end_time (float, optional): The end time of the range
                (in seconds). Defaults to the end of the audio.

        Returns:
            float: The average absolute amplitude of the samples in the range.

        Raises:
            ValueError: If times are negative or 'start_time' >= 'end_time'
                or times are outside the audio duration.
        """
        sample_list = self.get_sample_list()
        frame_rate = self.get_frame_rate()
        duration = len(self.get_sample_list()) / frame_rate
        print(duration)
        
        # Default to full length if end_time not given
        if end_time is None:
            end_time = duration

        # Verify valid start and end times
        if start_time < 0 or end_time < 0:
            raise ValueError("Start and end times must be non-negative.")
        elif start_time >= end_time:
           raise ValueError("start_time must be less than end_time.")
        elif start_time > duration:
           raise ValueError(f"start_time ({start_time:.2f}s) exceeds audio length ({duration:.2f}s).")
        elif end_time > duration:
          raise ValueError(f"end_time ({end_time:.2f}s) exceeds audio length ({duration:.2f}s).")

        # Convert times to sample indices
        start_idx = int(start_time * frame_rate)
        end_idx = int(end_time * frame_rate)

        # Value verification
        start_idx = max(0, start_idx)
        end_idx = min(len(sample_list), end_idx)

        # Slice and compute mean absolute amplitude
        segment = sample_list[start_idx:end_idx]
        if len(segment) == 0:
            return 0.0
        
        avg_amp = sum(abs(x) for x in segment) / len(segment) if segment else 0.0

        return avg_amp
    
    import numpy as np

    def pitch_at_time(self, time, window=0.05):
        """
        Estimates the dominant frequency (pitch) at a specific time.

        Uses an FFT (Fast Fourier Transform) on a small window of audio
        around the specified time.

        Args:
            time (float): The time (in seconds) to analyze.
            window (float, optional): The size of the analysis window
                (in seconds). Defaults to 0.05 (50 milliseconds).

        Returns:
            float: The estimated dominant frequency in Hz.

        Raises:
            ValueError: If 'time' is outside the audio duration.
        """

        samples = self._audioseg.get_array_of_samples()
        rate = self.get_frame_rate()
        duration = len(samples) / rate

        if time < 0 or time > duration:
            raise ValueError("time t must be within audio duration")

        start_time = time - (window/2)
        end_time   = time + (window/2)

        # Make sure start and end time are within the audio's duration
        if start_time < 0: 
            start_time = 0
        if end_time > duration: 
            end_time = duration

        start_idx = int(start_time * rate)
        end_idx   = int(end_time * rate)

        segment = np.array(samples[start_idx:end_idx], dtype=np.float32)

        if len(segment) < 2:
            return 0.0

        # Remove direct current offset
        segment = segment - np.mean(segment)

        # FFT
        spectrum = np.fft.fft(segment)
        freqs = np.fft.fftfreq(len(spectrum), d=1.0/rate)

        # Only take the positive frequencies
        half = len(freqs)//2
        magnitudes = np.abs(spectrum[:half])
        freqs = freqs[:half]

        if not np.any(magnitudes):
            return 0.0

        # Find the dominant frequency in the window
        k = np.argmax(magnitudes)
        return float(freqs[k])
    
    def get_amplitude_at(self, time_s):
        """
        Gets the raw sample amplitude at a specific time.

        Args:
            time_s (float): The time (in seconds) to get the sample from.

        Returns:
            int: The amplitude of the sample at that time.

        Raises:
            ValueError: If 'time_s' is outside the audio duration.
        """
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate()
        idx = int(time_s * rate)
        if idx < 0 or idx >= len(sample_list):
            raise ValueError("Timestamp outside audio duration")
        return sample_list[idx]

    def set_amplitude_at(self, time_s, value):
        """
        Sets the raw sample amplitude at a specific time.

        Modifies this Audio object in-place. The value will be clamped to
        the valid 16-bit range (MIN_AMPLITUDE to MAX_AMPLITUDE).

        Args:
            time_s (float): The time (in seconds) of the sample to set.
            value (int): The new amplitude value to set.

        Raises:
            ValueError: If 'time_s' is outside the audio duration.
        """
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate()
        idx = int(time_s * rate)
        if idx < 0 or idx >= len(sample_list):
            raise ValueError("Timestamp outside audio duration")

        # clamp to legal sample range
        value = max(min(value, MAX_AMPLITUDE), -MAX_AMPLITUDE)

        sample_list[idx] = value
        self.from_sample_list(sample_list)
    
    def crescendo(self, start_time=0, end_time=None, final_multiplier=1.5):
        """
        Applies a crescendo (gradual volume increase) over a time range.

        Modifies this Audio object in-place.

        Args:
            start_time (float, optional): The time (in seconds) to begin
                the crescendo. Defaults to 0.
            end_time (float, optional): The time (in seconds) to end
                the crescendo. Defaults to the end of the audio.
            final_multiplier (float, optional): The amplitude multiplier to
                reach at the end of the crescendo. (e.g., 1.5 is 1.5x louder).
                Defaults to 1.5.

        Raises:
            ValueError: If times are invalid or out of range.
        """

        sample_list = self.get_sample_list()
        rate = self.get_frame_rate()
        duration = len(sample_list) / rate

        if end_time is None:
            end_time = duration

        # Safety checks
        if start_time < 0 or end_time < 0:
            raise ValueError("Times must be non-negative.")
        if not (0 <= start_time < end_time <= duration):
            raise ValueError("Invalid time range for crescendo.")

        start_idx = int(start_time * rate)
        end_idx   = int(end_time   * rate)

        length = end_idx - start_idx
        if length <= 0:
            return  # nothing to do

        # Linearly ramp from 1.0 to final_multiplier
        for i in range(length):
            progress = i / (length - 1)  # 0.0 → 1.0 across crescendo
            multiplier = 1.0 + progress * (final_multiplier - 1.0)
            new_val = int(sample_list[start_idx + i] * multiplier)

            # Clamp to safe 16-bit range
            new_val = max(min(new_val, MAX_AMPLITUDE), MIN_AMPLITUDE)
            sample_list[start_idx + i] = new_val

        self.from_sample_list(sample_list)

    def view(self):
        """
        Opens a GUI window to visualize this audio (waveform, FFT, etc.).
        """
        AudioViewer(self)

    def view_with(self, other):
        """
        Opens a GUI window to compare this audio with another.

        Args:
            other (Audio): The second Audio object to compare against.

        Raises:
            TypeError: If 'other' is not an Audio object.
        """
        if not isinstance(other, Audio):
            raise TypeError("\nThe parameter '" + "other" + "' should be a " +
                            str(Audio.__name__) +
                            " but instead was a " +
                            str(type(other).__name__) + "\n" +
                            "other" + " = " + str(other))

        DualAudioViewer(self, other)

class AudioViewer:
    """
    GUI class for displaying waveforms from an Audio object.
    
    This class opens a Tkinter window with Matplotlib plots for waveform,
    FFT, and spectrogram visualizations.
    """
    # Matplotlib Subplot Shorthand: (Rows, Columns, Plot Position)
    FULL_PLOT_POSITION = 111 

    def __init__(self, audio_obj):
        """
        Initializes and runs the single Audio visualization GUI.

        Args:
            audio_obj (Audio): The Audio object to visualize.
        """
        self._audio = audio_obj
        self._sample_list = np.array(self._audio.get_sample_list(), dtype=np.int16)
        self._rate = self._audio.get_frame_rate()
        if len(self._sample_list) == 0:
            messagebox.showwarning("No Data", "No samples to display.")
            return

        # Tkinter setup
        # Add audio name
        self._root = tk.Tk()
        self._root.title("Audio Viewer")

        # Figure + canvas
        self._fig = Figure(figsize=(8, 4), dpi=100)
        self._ax = self._fig.add_subplot(AudioViewer.FULL_PLOT_POSITION)
        self._canvas = FigureCanvasTkAgg(self._fig, master=self._root)
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Controls
        self.make_controls()

        self._root.mainloop()

    def make_controls(self):
        """
        Creates the control buttons and input fields for the Tkinter interface.
        """
        controls = tk.Frame(self._root)
        controls.pack(pady=10)

        # Create "Waveform" button
        tk.Button(controls, text="Waveform", command=self.plot_waveform).grid(row=0, column=0, padx=5)

        # Create "Zoomed Waveform" button and time entiries 
        tk.Label(controls, text="Start (s):").grid(row=0, column=2, padx=5)
        self.entry_start = tk.Entry(controls, width=6)
        self.entry_start.grid(row=0, column=3)

        tk.Label(controls, text="End (s):").grid(row=0, column=4, padx=5)
        self.entry_end = tk.Entry(controls, width=6)
        self.entry_end.grid(row=0, column=5)
        
        tk.Button(controls, text="Zoomed Waveform", command=self.plot_zoom).grid(row=0, column=6, padx=5)
        
        # Create "Display Peak Amplitude" button
        tk.Button(controls, text="Peak Amplitude", command=self.show_peak).grid(row=0, column=1, padx=5)

        # Create button for FFT (Fast Fourier Transform) plot
        tk.Button(controls, text="Frequency Spectrum (FFT)", command=self.plot_fft).grid(row=0, column=7, padx=5)
        
        # Create button for spectrogram plot
        tk.Button(controls, text="Spectrogram", command=self.plot_spectrogram).grid(row=0, column=8, padx=5)

    def clear_cbar(self):
        """
        Removes the color bar created by the spectrogram if it exists.
        """
        # Check if the _cbar attribute was exists AND is not None
        if hasattr(self, '_cbar') and self._cbar is not None:
            # Recreate the Axes: This is the critical step.
            self._ax = self._fig.add_subplot(AudioViewer.FULL_PLOT_POSITION)
            # Nullify the reference: Tells the class the cbar is gone.
            self._cbar = None 

    def plot(self, y, x, title):
        """
        Helper function to draw a plot on the Matplotlib canvas.

        Args:
            y (array-like): The Y-axis data (amplitude).
            x (array-like): The X-axis data (time in seconds).
            title (str): The title for the plot.
        """
        self._ax.clear()
        self.clear_cbar()
        self._ax.plot(x, y, linewidth=0.5, color="blue")
        self._ax.set_xlabel("Time (s)")
        self._ax.set_ylabel("Amplitude")
        self._ax.set_title(title)
        self._ax.grid(True)
        self._canvas.draw_idle()

    def plot_waveform(self):
        """
        Plots the full audio waveform (Amplitude vs. Time).
        """
        duration = len(self._sample_list) / self._rate
        x = np.linspace(0, duration, num=len(self._sample_list))
        self.plot(self._sample_list, x, "Full waveform")

    def plot_zoom(self):
        """
        Plots a zoomed-in portion of the waveform based on user input times.
        """
        try:
            start = float(self.entry_start.get())
            end = float(self.entry_end.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Enter numeric times.")
            return
        if not (0 <= start < end <= len(self._sample_list) / self._rate): # check this works
            messagebox.showwarning("Invalid Range", "Out of range.")
            return
        start_idx, end_idx = int(start * self._rate), int(end * self._rate)
        y = self._sample_list[start_idx:end_idx]
        x = np.linspace(start, end, num=len(y))
        self.plot(y, x, f"Zoom {start:.2f}-{end:.2f}s")
        
    def plot_fft(self):
        """
        Plots the frequency spectrum (FFT) of the entire audio.
        """
        # Compute FFT
        spectrum = np.fft.fft(self._sample_list)
        freqs = np.fft.fftfreq(len(spectrum), d=1/self._rate)

        # Only keep positive frequencies
        positive_freqs = freqs[:len(freqs)//2]
        magnitude = np.abs(spectrum[:len(freqs)//2])

        # Clear and plot inside Tkinter canvas
        self._ax.clear()
        self.clear_cbar()
        self._ax.plot(positive_freqs, magnitude, color="red", linewidth=1)
        self._ax.set_xlabel("Frequency (Hz)")
        self._ax.set_ylabel("Magnitude")
        self._ax.set_title("Frequency Spectrum (FFT)")
        self._ax.grid(True)
        self._canvas.draw_idle()
        
    def plot_spectrogram(self):
        """
        Plots a spectrogram (Frequency vs. Time, with amplitude as color).

        .. figure:: _static/spectrogram_graphic.png
           :width: 80%
           :align: left
           :alt: Example plot of an audio spectrogram
        """
        self._ax.clear()
        self.clear_cbar()
        Pxx, freqs, bins, im = self._ax.specgram(self._sample_list, Fs=self._rate, NFFT=1024, noverlap=512, cmap="magma")
        self._ax.set_xlabel("Time (s)")
        self._ax.set_ylabel("Frequency (Hz)")
        self._ax.set_title("Spectrogram")

        self._cbar = self._fig.colorbar(im, ax=self._ax, label="Intensity (dB)")

        self._canvas.draw_idle()

    def show_peak(self):
        """
        Displays the peak (maximum absolute) amplitude of the audio signal
        and the timestamp at which it occurs.
        
        If the same peak occurs more than once, only the first time is shown.
        """
        # Find index of maximum absolute amplitude
        max_index = int(np.argmax(np.abs(self._sample_list)))
        # Actual max amplitude
        max_amp = int(self._sample_list[max_index])
        # Convert index to timestamp (in seconds)
        timestamp = max_index / self._rate

        messagebox.showinfo(
            "Max Amplitude",
            f"Peak amplitude: {max_amp}\nTime: {timestamp:.3f} s"
        )

class DualAudioViewer:
    """
    GUI class for displaying and comparing two audio waveforms.

    Audio 1 is plotted in Blue, Audio 2 is plotted in Red.
    Provides options for full waveform and zoomed waveform comparison.
    """
    FULL_PLOT_POSITION = 111 

    def __init__(self, audio_obj1, audio_obj2):
        """
        Initializes and runs the dual Audio comparison GUI.

        Args:
            audio_obj1 (Audio): The first Audio object (plotted in blue).
            audio_obj2 (Audio): The second Audio object (plotted in red).
        """
        # --- Data Extraction and Validation ---
        
        # Audio 1 Data
        self._samples1 = np.array(audio_obj1.get_sample_list(), dtype=np.int16)
        self._rate = audio_obj1.get_frame_rate()
        self._name1 = getattr(audio_obj1, 'name', 'Audio 1 (Blue)')
        
        # Audio 2 Data
        self._samples2 = np.array(audio_obj2.get_sample_list(), dtype=np.int16)
        self._name2 = getattr(audio_obj2, 'name', 'Audio 2 (Red)')

        # Basic Check
        if len(self._samples1) == 0 or len(self._samples2) == 0:
            messagebox.showwarning("No Data", "One or both audio segments are empty.")
            return

        # --- Tkinter setup ---
        self._root = tk.Tk()
        self._root.title("Dual Waveform Comparison Viewer")

        # Figure + canvas setup
        self._fig = Figure(figsize=(10, 5), dpi=100)
        self._ax = self._fig.add_subplot(DualAudioViewer.FULL_PLOT_POSITION)
        
        self._canvas = FigureCanvasTkAgg(self._fig, master=self._root)
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Controls and main loop
        self.make_controls()

        self._root.mainloop()

    def make_controls(self):
        """
        Creates the control buttons and input fields for the Tkinter interface.
        """
        controls = tk.Frame(self._root)
        controls.pack(pady=10)

        # 1. Full Waveform Button
        tk.Button(controls, text="Full Waveform", command=self.plot_waveform).grid(row=0, column=0, padx=10)

        # 2. Zoomed Waveform Controls
        tk.Label(controls, text="Start (s):").grid(row=0, column=1, padx=5)
        self.entry_start = tk.Entry(controls, width=6)
        self.entry_start.grid(row=0, column=2)

        tk.Label(controls, text="End (s):").grid(row=0, column=3, padx=5)
        self.entry_end = tk.Entry(controls, width=6)
        self.entry_end.grid(row=0, column=4)
        
        tk.Button(controls, text="Zoom Waveform", command=self.plot_zoom).grid(row=0, column=5, padx=10)
        
        # Legend/Color Key Display
        tk.Label(controls, fg="darkblue", font=('Arial', 10, 'bold')).grid(row=1, columnspan=6, pady=5)

    def _plot_dual(self, y1, y2, x, title):
        """
        Helper function to draw two overlaid plots on the Matplotlib canvas.

        Args:
            y1 (array-like): The Y-axis data for the first audio (blue).
            y2 (array-like): The Y-axis data for the second audio (red).
            x (array-like): The common X-axis data (time in seconds).
            title (str): The title for the plot.
        """
        self._ax.clear()
        
        # Plot Audio 1 (Blue)
        # We plot the data against the full time axis 'x'
        self._ax.plot(x[:len(y1)], y1, linewidth=0.5, color="blue", label=self._name1)
        
        # Plot Audio 2 (Red)
        # The shorter line will naturally end at its last index
        self._ax.plot(x[:len(y2)], y2, linewidth=0.5, color="red", label=self._name2)

        self._ax.set_xlabel("Time (s)")
        self._ax.set_ylabel("Amplitude")
        self._ax.set_title(title)
        self._ax.grid(True)
        self._ax.legend(loc='upper right') # Show the label key
        self._canvas.draw_idle()

    def plot_waveform(self):
        """
        Displays the complete, overlaid waveform of both audio signals.

        .. figure:: _static/dual_waveform_graphic.png
           :width: 80%
           :align: left
           :alt: Example plot of an audio waveform
        """
        rate = self._rate
        
        # Use the maximum sample count for the time axis length
        max_samples = max(len(self._samples1), len(self._samples2))
        duration = max_samples / rate
        x = np.linspace(0, duration, num=max_samples)

        self._plot_dual(self._samples1, self._samples2, x, "Full Overlaid Waveforms")

    def plot_zoom(self):
        """
        Displays a zoomed-in, overlaid waveform for a specified time interval.
        """
        try:
            start_sec = float(self.entry_start.get())
            end_sec = float(self.entry_end.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter numeric times.")
            return

        rate = self._rate
        duration1 = len(self._samples1) / rate
        duration2 = len(self._samples2) / rate

        # Use the duration of the longest audio for range checking
        max_duration = max(len(self._samples1), len(self._samples2)) / rate
        
        if not (0 <= start_sec < end_sec <= max_duration): 
            messagebox.showwarning("Invalid Range", 
                                  f"Range must be within the longest audio duration ({max_duration:.3f} s).")
            return

        # Calculate sample indices
        start_idx = int(start_sec * rate)
        end_idx = int(end_sec * rate)
        
        # Slice the data for both audios
        y1_zoom = self._samples1[start_idx:end_idx]
        y2_zoom = self._samples2[start_idx:end_idx]
        
        # Create the time axis for the zoomed segment
        x_zoom = np.linspace(start_sec, end_sec, num=len(y1_zoom))
        
        self._plot_dual(y1_zoom, y2_zoom, x_zoom, 
                        f"Zoomed Overlaid Waveforms ({start_sec:.2f}-{end_sec:.2f}s)")

# Dictionary for the frequncies of musical notes
music_note_dict = {"C0":16, "C#0":17, "Db0": 17, "D0":18, "D#0":19, "Eb0":19, "E0":21,
                   "F0":22, "F#0":23, "Gb0":23, "G0": 25, "G#0":26, "Ab0":26, "A0":28,
                   "A#0":29, "Bb0":29, "B0":31, "C1":33, "C#1":35, "Db1":35, "D1":37,
                   "D#1":39, "E1":41, "F1":44, "F#1":46, "Gb1": 46, "G1": 49, "G#1":52,
                   "Ab1":52, "A1":55, "A#1":58, "Bb1":58, "B1":62, "C2":65, "C#2":69,
                   "Db2":69, "D2":73, "D#2":78, "Eb2":78, "E2":82, "F2":87, "F#2":92, "Gb2":92,
                   "G2":98, "G#2":104, "Ab2":104, "A2":110, "A#2":116, "Bb2":116, "B2":123,
                   "C3":131, "C#3":139, "Db3":139, "D3":147, "D#3":156, "Eb3":156,"E3":165,
                   "F3":175, "F#3":185, "Gb3": 185, "G3":196, "G#3":208, "Ab3":208, "A3":220,
                   "A#3":233, "Bb3":233, "B3":247, "C4":262, "C#4":277, "Db4":277, "D4":294,
                   "D#4":311, "Eb4":311, "E4":330, "F4":349, "F#4":370, "Gb4":370, "G4":392,
                   "G#4":415, "Ab4":415, "A4":440, "A#4":466, "Bb4":466, "B4": 494, "C5":523,
                   "C#5":554, "Db5":554, "D5":587, "D#5":622, "Eb5":622, "E5":659, "F5":699,
                   "F#5":740, "Gb5":740, "G5":784, "G#5":831, "Ab5":831, "A5":880, "A#5":932,
                   "Bb5":932, "B5":988, "C6":1047, "C#6":1109, "Db6":1109, "D6":1175, "D#6":1245,
                   "Eb6":1245, "E6":1319, "F6":1397, "F#6":1480, "Gb6":1480, "G6":1568, "G#6":1661,
                   "Ab6":1664, "A6":1760, "A#6":1865, "Bb6":1865, "B6":1976, "C7":2093, "C#7":2217,
                   "Db7":2217, "D7":2349, "D#7":2489, "Eb7":2489, "E7":2637, "F7":2794, "F#7":2960,
                   "Gb7":2960, "G7":3136, "G#7":3322, "Ab7":3322, "A7":3520, "A#7":3729, "Bb7":3729,
                   "B7":3951, "C8":4186, "C#8":4435, "Db8":4435, "D8":4699, "D#8":4978, "Eb8":4978,
                   "E8":5274, "F8":5588, "F#8":5920, "Gb8":5920, "G8":6272, "G#8":6645, "Ab8":6645,
                   "A8":7040, "A#8":7459, "B8":7902}
"""A dictionary mapping musical note names (e.g., "A4") to frequencies (in Hz)."""



def generate_music_note(note, duration, wavetype, gain=0): #MAKE THIS ANOTHER CONSTRUCTOR?? ASK CLIENT
    """
    Generates a single musical note as a new Audio object.

    Args:
        note (str): The note to generate (e.g., "A4", "C#5", "Eb3").
            Case-insensitive.
        duration (int): The duration of the note in milliseconds.
        wavetype (str): The type of wave ("Sine", "Square", "Sawtooth",
            or "Triangle"). Case-insensitive.
        gain (int or float, optional): Gain to apply in decibels (dB).
            Defaults to 0.

    Returns:
        Audio: A new Audio object containing the note.

    Raises:
        ValueError: If the 'note' or 'wavetype' is invalid.
        TypeError: If parameters are not of the correct type.
    """
    _check_type(note, "note", str)
    _check_type(duration, "duration", int)
    _check_type(wavetype, "wavetype", str)
    try:
        note = note[0].upper() + note[1:]
        freq = music_note_dict[note]
    except KeyError:
        raise ValueError("Error! Invalid note \"" + note + "\" passed to generate_music_note")

    audio_result = Audio()

    audio_result.from_generator(freq, duration, wavetype)

    audio_result.fade(50, 100)
    audio_result.apply_gain(gain)

    return audio_result

# CITE: ChatGPT for AudioViewer outline
