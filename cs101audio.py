# A Pydub based audio library for introductory computer science.

"""
CS101 Audio Package
===================

A Pydub-based audio library for introductory computer science.

All files that use the CS101 Audio package must have the following line
at the top of the file::

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


# For Error Checking
def _check_type(param, param_name, target_type):
    """Check if parameter matches expected type.
    
    Args:
        param: The parameter to check
        param_name (str): Name of the parameter for error messages
        target_type (type): Expected type of the parameter
        
    Raises:
        TypeError: If param is not of target_type
    """
    if not isinstance(param, target_type):
        raise TypeError("\nThe parameter '" + param_name + "' should be a " +
                        str(target_type.__name__) +
                        " but instead was a " +
                        str(type(param).__name__) + "\n" +
                        param_name + " = " + str(param))


class Audio():
    """Wrapper Class for the Pydub AudioSegment Class.
    
    This class provides a simplified interface for working with audio in
    introductory computer science courses. It wraps the Pydub AudioSegment
    class with student-friendly methods.
    
    Attributes:
        _audioseg (AudioSegment): The underlying Pydub AudioSegment object
    """

    def __init__(self, duration=0, frame_rate=44100):
        """Initialize an Audio object with a silent audio segment.
        
        Args:
            duration (int, optional): Length of the new silent audio segment 
                in milliseconds. Defaults to 0.
            frame_rate (int, optional): Frame rate of the new audio segment 
                in frames per second. Defaults to 44100.
        """
        self._audioseg = AudioSegment.silent(duration=duration, frame_rate=frame_rate)


    def set_audioseg(self, newaudio):
        """Set the audio segment attribute of the Audio Object.
        
        Args:
            newaudio (AudioSegment): New audio segment to replace 
                the current audio segment
        """
        self._audioseg = newaudio

    def get_audioseg(self):
        """Get the Audio Object's audio segment attribute.
        
        Returns:
            AudioSegment: The underlying Pydub AudioSegment object
        """
        return self._audioseg

    def get_sample_list(self):
        """Get the sample list for the Audio Object's audio segment.
        
        Returns:
            list: List of audio sample values as integers
        """
        return self._audioseg.get_array_of_samples().tolist()
    
    def get_frame_rate(self):
        """Get the Audio Object's frame rate.
        
        Returns:
            int: Frame rate in frames per second (Hz)
        """
        return self._audioseg.frame_rate

    def __len__(self):
        """Get the length of the audio file.
        
        Returns:
            int: Length of the audio in milliseconds
        """
        return len(self._audioseg)

    def open_audio_file(self, filename):
        """Read an audio file and set this Audio object's audio segment.
        
        Args:
            filename (str): Name of the audio file to be opened
            
        Raises:
            TypeError: If filename is not a string
            FileNotFoundError: If the file doesn't exist
        """
        _check_type(filename, "filename", str)
        try:
            AudioSegment.from_file(filename)
        except FileNotFoundError:
            raise FileNotFoundError("File " + filename + " not found")

        self._audioseg = AudioSegment.from_file(filename)
        
        
    def save_to_file(self, filename):
        """Save this Audio Object's audio segment to a file.
        
        Args:
            filename (str): Name of the file to save to (must include 
                file extension like .mp3, .wav, etc.)
        """
        extendindex = filename.find(".")
        file_extension = filename[extendindex + 1:]
      
        self._audioseg.export(out_f=(filename), \
                              format=file_extension)

    def from_sample_list(self, sample_lst, template=None):
        """Create audio segment from a list of samples.
        
        Sets the Audio Object's audio segment using the provided sample list
        and metadata (sample width, frame rate, frame width, etc.) from a 
        template Audio object.
        
        Args:
            sample_lst (list or array): List of audio sample values
            template (Audio, optional): Audio object to use as a template 
                for metadata. If None, uses self's metadata. Defaults to None.
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
        """Generate audio from a wave generator.
        
        Sets the Audio Object's audio segment to audio generated by a
        sine, square, sawtooth, or triangle wave generator.
        
        Args:
            freq (int): Frequency of the wave in Hz
            duration (int): Duration of the wave in milliseconds
            wavetype (str): Type of wave to generate. Must be one of:
                'Sine', 'Square', 'Sawtooth', or 'Triangle' (case insensitive)
                
        Raises:
            TypeError: If parameters are not of the correct type
            ValueError: If wavetype is not valid
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

    def play(self):
        """Play the Audio Object's audio segment.
        
        Plays the audio if it isn't empty. Requires proper audio playback
        configuration on the system.
        """
        if len(self._audioseg) > 0:
            play(self._audioseg)
            

    def __add__(self, other_audio):
        """Concatenate two audio segments using the + operator.
        
        Args:
            other_audio (Audio): Audio object to concatenate to self
            
        Returns:
            Audio: New Audio object with concatenated audio (original 
                objects are not modified)
                
        Raises:
            TypeError: If other_audio is not an Audio object
        """ 
        _check_type(other_audio, "other_audio", Audio)

        result = Audio()

        result.set_audioseg(self._audioseg + other_audio.get_audioseg())

        return result

    def __iadd__(self, other_audio):
        """Concatenate audio segments using the += operator.
        
        Args:
            other_audio (Audio): Audio object to concatenate to self
            
        Returns:
            Audio: Self with modified audio segment
            
        Raises:
            TypeError: If other_audio is not an Audio object
        """
        _check_type(other_audio, "other_audio", Audio)

        self._audioseg += other_audio.get_audioseg()
        return self


    def __mul__(self, loopnum):
        """Loop audio segment using the * operator.
        
        Args:
            loopnum (int): Number of times to loop the audio
            
        Returns:
            Audio: New Audio object with looped audio
            
        Raises:
            TypeError: If loopnum is not an integer
        """
        _check_type(loopnum, "loopnum", int)

        result = Audio()
        result.set_audioseg(self._audioseg * loopnum)

        return result

    def __imul__(self, loopnum):
        """Loop audio segment using the *= operator.
        
        Args:
            loopnum (int): Number of times to loop the audio
            
        Returns:
            Audio: Self with modified audio segment
            
        Raises:
            TypeError: If loopnum is not an integer
        """
        _check_type(loopnum, "loopnum", int)

        self._audioseg *= loopnum
        return self

    def __getitem__(self, millisecond):
        """Index or slice audio segments using [] operator.
        
        Args:
            millisecond (int or slice): Millisecond to index or a slice object
                for slicing the audio
            
        Returns:
            Audio: New Audio object containing the indexed or sliced audio
        """
        result = Audio()
        result.set_audioseg(self._audioseg[millisecond])

        return result


    def overlay(self, audio2, position=0, loop=False):
        """Overlay another audio segment onto this one.
        
        Args:
            audio2 (Audio): Audio object to overlay onto self
            position (int, optional): Millisecond position in self's audio 
                at which to overlay audio2. Defaults to 0.
            loop (bool, optional): If True, loops audio2 until the end of 
                self's audio. Defaults to False.
        """
        self._audioseg = self._audioseg.overlay(audio2.get_audioseg(), position=position, loop=loop)
        
    def apply_gain(self, gain):
        """Change the amplitude (loudness) of the audio.
        
        Args:
            gain (int): Amount of gain in decibels. Can be negative to 
                reduce volume or positive to increase volume.
        """
        self._audioseg = self._audioseg.apply_gain(gain)
        
    def fade_in(self, fadetime):
        """Add a fade-in effect at the beginning of the audio.
        
        Args:
            fadetime (int): Length of the fade in milliseconds
            
        Raises:
            TypeError: If fadetime is not an integer
        """
        _check_type(fadetime, "fadetime", int)
        self._audioseg = self._audioseg.fade_in(fadetime)
        
    def fade_out(self, fadetime):
        """Add a fade-out effect at the end of the audio.
        
        Args:
            fadetime (int): Length of the fade in milliseconds
            
        Raises:
            TypeError: If fadetime is not an integer
        """
        _check_type(fadetime, "fadetime", int)
        self._audioseg = self._audioseg.fade_out(fadetime)
        
    def fade(self, fadeintime=0, fadeouttime=0):
        """Add fade effects to the beginning and/or end of the audio.
        
        Args:
            fadeintime (int, optional): Length of the beginning fade in 
                milliseconds. Defaults to 0.
            fadeouttime (int, optional): Length of the ending fade in 
                milliseconds. Defaults to 0.
                
        Raises:
            TypeError: If parameters are not integers
        """
        _check_type(fadeintime, "fadeintime", int)
        _check_type(fadeouttime, "fadeouttime", int)
        self._audioseg = self._audioseg.fade_in(fadeintime).fade_out(fadeouttime)
        

    def change_speed(self, factor):
        """Change the playback speed of the audio.
        
        Args:
            factor (int or float): Speed multiplier. Values < 1 slow down 
                the audio, values > 1 speed it up. For example, 2.0 doubles 
                the speed, 0.5 halves it.
                
        Raises:
            TypeError: If factor is not int or float
            ValueError: If factor is 0
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

    def reverse(self):
        """Reverse the audio by reversing the sample list."""
        self.from_sample_list(list(reversed(self.get_sample_list())))

    def view(self):
        """Open the AudioViewer GUI for visualization.
        
        Creates an AudioViewer object which opens a Tkinter window
        with various visualization options including waveforms,
        frequency spectrums, and spectrograms.
        """
        AudioViewer(self)


class AudioViewer:
    """GUI class for displaying waveforms from an Audio object.
    
    Provides an interactive Tkinter-based interface for visualizing audio
    data including waveforms, zoomed views, frequency spectrums (FFT),
    spectrograms, and peak amplitude information.
    
    Attributes:
        audio (Audio): The Audio object being visualized
        sample_list (numpy.ndarray): Array of audio samples
        rate (int): Sample rate in Hz
        root (tk.Tk): Main Tkinter window
        fig (Figure): Matplotlib figure for plotting
        ax (Axes): Matplotlib axes for plotting
        canvas (FigureCanvasTkAgg): Canvas for displaying plots
    """

    def __init__(self, audio_obj):
        """Initialize the AudioViewer and create the visualization window.

        Extracts the sample list and frame rate from the provided Audio object,
        then builds a Tkinter window with an embedded Matplotlib canvas for 
        displaying plots. Initializes all control buttons and starts the 
        Tkinter main loop.
        
        Args:
            audio_obj (Audio): Audio object whose waveform and frequency 
                data will be visualized
        """
        self.audio = audio_obj
        self.sample_list = np.array(self.audio.get_sample_list(), dtype=np.int16)
        self.rate = self.audio.get_frame_rate()
        if len(self.sample_list) == 0:
            messagebox.showwarning("No Data", "No samples to display.")
            return

        # Tkinter setup
        self.root = tk.Tk()
        self.root.title("Audio Viewer")

        # Figure + canvas
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Controls
        self._make_controls()

        self.root.mainloop()

    def _make_controls(self):
        """Create the control buttons and input fields for the interface.
        
        Creates buttons for different visualization modes and input fields
        for specifying time ranges for zoomed views.
        """
        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        tk.Button(controls, text="Waveform", command=self.plot_waveform).grid(row=0, column=0, padx=5)

        tk.Label(controls, text="Start (s):").grid(row=0, column=2, padx=5)
        self.entry_start = tk.Entry(controls, width=6)
        self.entry_start.grid(row=0, column=3)

        tk.Label(controls, text="End (s):").grid(row=0, column=4, padx=5)
        self.entry_end = tk.Entry(controls, width=6)
        self.entry_end.grid(row=0, column=5)
        
        tk.Button(controls, text="Zoomed Waveform", command=self.plot_zoom).grid(row=0, column=6, padx=5)
        
        tk.Button(controls, text="Peak Amplitude", command=self.show_peak).grid(row=0, column=1, padx=5)

        tk.Button(controls, text="Frequency Spectrum (FFT)", command=self.plot_fft).grid(row=0, column=7, padx=5)
        
        tk.Button(controls, text="Spectrogram", command=self.plot_spectrogram).grid(row=0, column=8, padx=5)


    def _plot(self, y, x, title):
        """Display data on the Matplotlib canvas.
        
        Args:
            y (array-like): Amplitude data to plot
            x (array-like): Corresponding time values in seconds
            title (str): Title of the plot
        """
        self.ax.clear()
        self.ax.plot(x, y, linewidth=0.5, color="blue")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title(title)
        self.ax.grid(True)
        self.canvas.draw_idle()

    def plot_waveform(self):
        """Display the complete waveform of the audio signal.
        
        Plots the amplitude of each sample in the audio over time.
        X-axis represents time in seconds, Y-axis represents amplitude.
        """
        duration = len(self.sample_list) / self.rate
        x = np.linspace(0, duration, num=len(self.sample_list))
        self._plot(self.sample_list, x, "Full waveform")

    def plot_zoom(self):
        """Display a zoomed-in waveform for a specified time interval.

        The start and end times (in seconds) are entered by the user in 
        the GUI input fields. The function extracts the corresponding range 
        of samples and plots amplitude versus time for that segment.
        
        Raises:
            ValueError: If entered times are not numeric
            Warning: If time range is invalid or out of bounds
        """
        try:
            start = float(self.entry_start.get())
            end = float(self.entry_end.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Enter numeric times.")
            return
        if not (0 <= start < end <= len(self.sample_list) / self.rate):
            messagebox.showwarning("Invalid Range", "Out of range.")
            return
        start_idx, end_idx = int(start * self.rate), int(end * self.rate)
        y = self.sample_list[start_idx:end_idx]
        x = np.linspace(start, end, num=len(y))
        self._plot(y, x, f"Zoom {start:.2f}-{end:.2f}s")
        
    def plot_fft(self):
        """Create a Fast Fourier Transform (FFT) plot.
        
        Displays the frequency spectrum of the audio. X-axis shows frequency 
        in Hz, Y-axis shows magnitude (how much each frequency is present 
        in the audio).
        """
        # Compute FFT
        spectrum = np.fft.fft(self.sample_list)
        freqs = np.fft.fftfreq(len(spectrum), d=1/self.rate)

        # Only keep positive frequencies
        positive_freqs = freqs[:len(freqs)//2]
        magnitude = np.abs(spectrum[:len(freqs)//2])

        # Clear and plot inside Tkinter canvas
        self.ax.clear()
        self.ax.plot(positive_freqs, magnitude, color="red", linewidth=1)
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude")
        self.ax.set_title("Frequency Spectrum (FFT)")
        self.ax.grid(True)
        self.canvas.draw_idle()
        
    def plot_spectrogram(self):
        """Create a spectrogram plot.
        
        Displays how the frequency content of the audio changes over time
        by performing FFT on small time windows. X-axis shows time, 
        Y-axis shows frequency in Hz, and color intensity represents magnitude.
        """
        self.ax.clear()
        Pxx, freqs, bins, im = self.ax.specgram(self.sample_list, Fs=self.rate, NFFT=1024, noverlap=512, cmap="magma")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Frequency (Hz)")
        self.ax.set_title("Spectrogram")

        self._cbar = self.fig.colorbar(im, ax=self.ax, label="Intensity (dB)")

        self.canvas.draw_idle()

    def show_peak(self):
        """Display the peak amplitude and its timestamp.
        
        Shows a message box with the maximum absolute amplitude of the 
        audio signal and the time at which it occurs. If the same peak 
        occurs multiple times, only the first occurrence is shown.
        """
        # Find index of maximum absolute amplitude
        max_index = int(np.argmax(np.abs(self.sample_list)))
        # Actual max amplitude
        max_amp = int(self.sample_list[max_index])
        # Convert index to timestamp (in seconds)
        timestamp = max_index / self.rate

        messagebox.showinfo(
            "Max Amplitude",
            f"Peak amplitude: {max_amp}\nTime: {timestamp:.3f} s"
        )


# Dictionary for the frequencies of musical notes
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



def generate_music_note(note, duration, wavetype, gain=0):
    """Generate a musical note as an Audio object.
    
    Creates an audio segment containing a musical note of the specified
    duration and waveform type. Automatically applies fade-in and fade-out
    effects for smooth playback.
    
    Args:
        note (str): Musical note in the format [A-G](#|b|)[0-8], where
            # indicates sharp and b indicates flat (e.g., 'C4', 'F#5', 'Bb3').
            Case insensitive.
        duration (int): Duration of the note in milliseconds
        wavetype (str): Type of wave to generate. Must be one of:
            'Sine', 'Square', 'Sawtooth', or 'Triangle' (case insensitive)
        gain (int, optional): Gain to apply to note in decibels. 
            Can be negative to reduce volume. Defaults to 0.
            
    Returns:
        Audio: New Audio object containing the generated musical note
        
    Raises:
        TypeError: If parameters are not of the correct type
        ValueError: If note or wavetype is invalid
        
    Example::
    
        # Generate middle C for 1 second using a sine wave
        c_note = generate_music_note('C4', 1000, 'Sine')
        c_note.play()
        
        # Generate a quieter A above middle C
        a_note = generate_music_note('A4', 500, 'Sine', gain=-6)
    """
    _check