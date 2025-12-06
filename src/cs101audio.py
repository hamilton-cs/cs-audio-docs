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

import numpy as np  # Used for FFT calculations in pitch_at_time method
from audio_viewer import AudioViewer # Import AudioViewer

def _check_type(param, param_name, target_type):
    """
    Checks if a parameter is of the correct type and raises a TypeError if not.

    Args:
        param (any): The parameter to check.
        param_name (str): The name of the parameter (for the error message).
        target_type (type or tuple): The expected type(s) (e.g., int, str, Audio, or (int, float)).

    Raises:
        TypeError: If 'param' is not an instance of 'target_type'.
    """
    if not isinstance(param, target_type):
        if isinstance(target_type, tuple):
            type_names = " or ".join([t.__name__ for t in target_type])
        else:
            type_names = target_type.__name__
        raise TypeError("\nThe parameter '" + param_name + "' should be a " +
                        type_names +
                        " but instead was a " +
                        str(type(param).__name__) + "\n" +
                        param_name + " = " + str(param))


class Audio():
    """
    Wrapper Class for the Pydub AudioSegment Class
    """

    # 16-bit PCM amplitude limits as class-level attributes
    MAX_AMPLITUDE = 32767
    MIN_AMPLITUDE = -32768

    def __init__(self, duration=0, frame_rate=44100):
        """
        Initializes a silent audio segment.

        Args:
            duration (int, optional): The length of the silent audio segment
                in milliseconds. Defaults to 0.
            frame_rate (int, optional): The frame rate in frames per second.
                Defaults to 44100.
        """
        _check_type(duration, "duration", int)
        _check_type(frame_rate, "frame_rate", int)
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
        _check_type(filename, "filename", str)
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
        _check_type(sample_lst, "sample_lst", list)
        if template is not None:
            _check_type(template, "template", Audio)
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
            try:
                import simpleaudiohamiltoncs
                playback = simpleaudiohamiltoncs.play_buffer(
                    self._audioseg.raw_data,
                    num_channels=self._audioseg.channels,
                    bytes_per_sample=self._audioseg.sample_width,
                    sample_rate=self._audioseg.frame_rate
                )
                try:
                    playback.wait_done()
                except KeyboardInterrupt:
                    playback.stop()
            except ImportError:
                pass
            else:
                return
            

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
        _check_type(audio2, "audio2", Audio)
        _check_type(position, "position", int)
        _check_type(loop, "loop", bool)
        self._audioseg = self._audioseg.overlay(audio2.get_audioseg(), position=position, loop=loop)
        
    def apply_gain(self, gain):
        """
        Applies a gain (volume change) to the audio.

        Modifies this Audio object in-place.

        Args:
            gain (int or float): The amount of gain in decibels (dB).
                Positive values make it louder, negative values make it quieter.
        """
        _check_type(gain, "gain", (int, float))
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
        _check_type(max_amplitude, "max_amplitude", int)
        if max_amplitude > Audio.MAX_AMPLITUDE:
            raise ValueError(f"Max amplitude cannot exceed 32,767. Got {max_amplitude}.")
        elif max_amplitude < 0:
            raise ValueError(f"Max amplitude must be positive. Got {max_amplitude}.")
        
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

        Args:
            start_time (float, optional): The start time of the range
                (in miliseconds). Defaults to 0.
            end_time (float, optional): The end time of the range
                (in miliseconds). Defaults to the end of the audio.

        Returns:
            float: The average absolute amplitude of the samples in the range.

        Raises:
            ValueError: If times are negative or 'start_time' >= 'end_time'
                or times are outside the audio duration.
        """
        _check_type(start_time, "start_time", (int, float))
        if end_time is not None:
            _check_type(end_time, "end_time", (int, float))
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate()
        duration = len(sample_list) * 1000 / rate
        
        # Default to full length if end_time not given
        if end_time is None:
            end_time = duration

        # Verify valid start and end times
        if start_time < 0 or end_time < 0:
            raise ValueError(f"Start and end times must be non-negative. Got start_time={start_time:.2f}s, end_time={end_time:.2f}s.")
        if start_time > duration or end_time > duration:
            if start_time > duration and end_time > duration:
                raise ValueError(f"Both start_time and end_time exceed the audio duration. Got start_time={start_time:.2f}s, end_time={end_time:.2f}s, but duration is {duration:.2f}s.")
            elif start_time > duration:
                raise ValueError(f"start_time exceeds the audio duration. Got start_time={start_time:.2f}s, but duration is {duration:.2f}s.")
            else:
                raise ValueError(f"end_time exceeds the audio duration. Got end_time={end_time:.2f}s, but duration is {duration:.2f}s.")
        if start_time >= end_time:
            raise ValueError(f"start_time must be less than end_time. Got start_time={start_time:.2f}s, end_time={end_time:.2f}s.")

        # Convert times to sample indices
        start_idx = int(start_time * rate / 1000)
        end_idx = int(end_time * rate / 1000)

        # Value verification
        start_idx = max(0, start_idx)
        end_idx = min(len(sample_list), end_idx)

        # Slice and compute mean absolute amplitude
        segment = sample_list[start_idx:end_idx]
        if len(segment) == 0:
            return 0.0
        
        avg_amp = sum(abs(x) for x in segment) / len(segment) if segment else 0.0

        return avg_amp

    def pitch_at_time(self, time, window=50):
        """
        Estimates the dominant frequency (pitch) at a specific time.

        Uses an FFT (Fast Fourier Transform) on a small window of audio
        around the specified time.

        Args:
            time (float): The time (in miliseconds) to analyze.
            window (float, optional): The size of the analysis window
            (in miliseconds). Defaults to 50 milliseconds

        Returns:
            float: The estimated dominant frequency in Hz.

        Raises:
            ValueError: If 'time' is outside the audio duration.
        """
        _check_type(time, "time", (int, float))
        _check_type(window, "window", (int, float))
        rate = self.get_frame_rate()
        samples = self._audioseg.get_array_of_samples()
        duration_ms = len(samples) * 1000 / rate
        
        # Convert ms inputs to seconds
        time_s = time / 1000.0
        window_s = window / 1000.0
        duration_s = duration_ms / 1000.0

        if time_s < 0:
            raise ValueError(f"Timestamp must be non-negative. Got {time}ms.")
        if time_s > duration_s:
            raise ValueError(f"Timestamp exceeds audio duration. Got {time}ms, but duration is {duration_ms:.0f}ms.")

        # Define segment boundaries in seconds
        start_time_s = time_s - (window_s / 2)
        end_time_s = time_s + (window_s / 2)

        # Make sure start and end time are within the audio's duration (in seconds)
        if start_time_s < 0: 
            start_time_s = 0
        if end_time_s > duration_s: 
            end_time_s = duration_s

        # Convert seconds to sample indices
        start_idx = int(start_time_s * rate)
        end_idx = int(end_time_s * rate)

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
    
    def get_amplitude_at(self, time):
        """
        Gets the raw sample amplitude at a specific time.

        Args:
            time (float): The time (in miliseconds) to get the sample from.

        Returns:
            int: The amplitude of the sample at that time.

        Raises:
            ValueError: If 'time' is outside the audio duration.
        """
        _check_type(time, "time", (int, float))
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate()
        duration_ms = len(sample_list) * 1000 / rate
        idx = int(time * rate / 1000)
        
        if idx < 0:
            raise ValueError(f"Timestamp must be non-negative. Got {time}ms.")
        if idx >= len(sample_list):
            raise ValueError(f"Timestamp exceeds audio duration. Got {time}ms, but duration is {duration_ms:.0f}ms.")
        
        return sample_list[idx]

    def set_amplitude_at(self, time, value):
        """
        Sets the raw sample amplitude at a specific time.

        Modifies this Audio object in-place. The value will be clamped to
        the valid 16-bit range (MIN_AMPLITUDE to MAX_AMPLITUDE).

        Args:
            time (float): The time (in miliseconds) of the sample to set.
            value (int): The new amplitude value to set.

        Raises:
            ValueError: If 'time' is outside the audio duration.
        """
        _check_type(time, "time", (int, float))
        _check_type(value, "value", int)
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate()
        duration_ms = len(sample_list) * 1000 / rate
        idx = int(time * rate / 1000)
        
        if idx < 0:
            raise ValueError(f"Timestamp must be non-negative. Got {time}ms.")
        if idx >= len(sample_list):
            raise ValueError(f"Timestamp exceeds audio duration. Got {time}ms, but duration is {duration_ms:.0f}ms.")

        # Clamp to legal sample range
        value = max(min(value, Audio.MAX_AMPLITUDE), Audio.MIN_AMPLITUDE)

        sample_list[idx] = value
        self.from_sample_list(sample_list)
    
    def crescendo(self, start_time=0, end_time=None, final_multiplier=1.5):
        """
        Applies a crescendo (gradual volume increase) over a time range.

        Modifies this Audio object in-place.

        Args:
            start_time (float, optional): The time (in miliseconds) to begin
                the crescendo. Defaults to 0.
            end_time (float, optional): The time (in miliseconds) to end
                the crescendo. Defaults to the end of the audio.
            final_multiplier (float, optional): The amplitude multiplier to
                reach at the end of the crescendo. (e.g., 1.5 is 1.5x louder).
                Defaults to 1.5.

        Raises:
            ValueError: If times are invalid or out of range.
        """
        _check_type(start_time, "start_time", (int, float))
        if end_time is not None:
            _check_type(end_time, "end_time", (int, float))
        _check_type(final_multiplier, "final_multiplier", (int, float))
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate() 
        
        # Calculate total duration in ms
        duration_ms = len(sample_list) * 1000 / rate 

        if end_time is None:
            end_time = duration_ms

        # Validation in ms
        if start_time < 0 or end_time < 0:
            raise ValueError(f"Start and end times must be non-negative. Got start_time={start_time}ms, end_time={end_time}ms.")
        if start_time > duration_ms or end_time > duration_ms:
            if start_time > duration_ms and end_time > duration_ms:
                raise ValueError(f"Both start_time and end_time exceed the audio duration. Got start_time={start_time}ms, end_time={end_time}ms, but duration is {duration_ms:.0f}ms.")
            elif start_time > duration_ms:
                raise ValueError(f"start_time exceeds the audio duration. Got start_time={start_time}ms, but duration is {duration_ms:.0f}ms.")
            else:
                raise ValueError(f"end_time exceeds the audio duration. Got end_time={end_time}ms, but duration is {duration_ms:.0f}ms.")
        if start_time >= end_time:
            raise ValueError(f"start_time must be less than end_time. Got start_time={start_time}ms, end_time={end_time}ms.")
        if final_multiplier < 0.0:
            raise ValueError(f"Final multiplier must be non-negative. Got {final_multiplier}.")

        start_idx = int(start_time * rate / 1000)
        end_idx   = int(end_time   * rate / 1000)

        length = end_idx - start_idx
        if length <= 0:
            return

        # Linearly ramp from 1.0 to final_multiplier
        for i in range(length):
            # progress goes from 0.0 to 1.0 across crescendo segment
            progress = i / (length - 1) 
            multiplier = 1.0 + progress * (final_multiplier - 1.0)
            new_val = int(sample_list[start_idx + i] * multiplier)

            # Clamp to safe 16-bit range
            new_val = max(min(new_val, Audio.MAX_AMPLITUDE), Audio.MIN_AMPLITUDE)
            sample_list[start_idx + i] = new_val

        self.from_sample_list(sample_list)

    def decrescendo(self, start_time=0, end_time=None, initial_multiplier=1.5):
        """
        Applies a decrescendo (gradual volume decrease) over a time range.

        Modifies this Audio object in-place.

        Args:
            start_time (float, optional): The time (in miliseconds) to begin
                the decrescendo. Defaults to 0.
            end_time (float, optional): The time (in miliseconds) to end
                the decrescendo. Defaults to the end of the audio.
            initial_multiplier (float, optional): How loud the start should 
                be (e.g., 1.5 for 50% louder)

        Raises:
            ValueError: If times are invalid or out of range.
        """
        _check_type(start_time, "start_time", (int, float))
        if end_time is not None:
            _check_type(end_time, "end_time", (int, float))
        _check_type(initial_multiplier, "initial_multiplier", (int, float))
        sample_list = self.get_sample_list()
        rate = self.get_frame_rate() 
        
        # Calculate total duration in ms
        duration_ms = len(sample_list) * 1000 / rate 

        if end_time is None:
            end_time = duration_ms

        # Validation in ms 
        if start_time < 0 or end_time < 0:
            raise ValueError(f"Start and end times must be non-negative. Got start_time={start_time}ms, end_time={end_time}ms.")
        if start_time > duration_ms or end_time > duration_ms:
            if start_time > duration_ms and end_time > duration_ms:
                raise ValueError(f"Both start_time and end_time exceed the audio duration. Got start_time={start_time}ms, end_time={end_time}ms, but duration is {duration_ms:.0f}ms.")
            elif start_time > duration_ms:
                raise ValueError(f"start_time exceeds the audio duration. Got start_time={start_time}ms, but duration is {duration_ms:.0f}ms.")
            else:
                raise ValueError(f"end_time exceeds the audio duration. Got end_time={end_time}ms, but duration is {duration_ms:.0f}ms.")
        if start_time >= end_time:
            raise ValueError(f"start_time must be less than end_time. Got start_time={start_time}ms, end_time={end_time}ms.")
        if initial_multiplier < 0.0:
            raise ValueError(f"Initial multiplier must be non-negative. Got {initial_multiplier}.")

        start_idx = int(start_time * rate / 1000)
        end_idx   = int(end_time   * rate / 1000)

        length = end_idx - start_idx
        if length <= 0:
            return

        # Linearly ramp from initial_multiplier down to 1.0
        for i in range(length):
            # progress goes from 0.0 -> 1.0 across decrescendo segment
            progress = i / (length - 1) 
            multiplier = initial_multiplier - progress * (initial_multiplier - 1.0)
            
            new_val = int(sample_list[start_idx + i] * multiplier)

            # Clamp to safe 16-bit range
            new_val = max(min(new_val, Audio.MAX_AMPLITUDE), Audio.MIN_AMPLITUDE)
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
        
        _check_type(other, "other", Audio)
        AudioViewer(self, other)



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
