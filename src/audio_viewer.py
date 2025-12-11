"""
Copyright (c) 2025 hamilton-cs

MIT License - see LICENSE file for details.

Contributors:
- Lulu Ceccon
- Charles Beard
Institution: Hamilton College Computer Science Department
Last Modified: 12/08/25

AudioViewer module for CS101 Audio library.

This module provides GUI visualization capabilities for Audio objects.

AI Assistance: The tkinter GUI template, matplotlib canvas integration, and
initial class structure were created with assistance from ChatGPT (OpenAI, 2025).
Enhancements including dual audio viewer functionality, spectrogram
features, and bug fixes were developed by the contributors.
"""

# Imports for GUI plots
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AudioViewer:
    """
    GUI class for displaying waveforms from Audio object(s).
    
    This class opens a Tkinter window with Matplotlib plots for waveform,
    FFT, and spectrogram visualizations. Supports both single audio visualization
    and dual audio comparison modes.
    """
    # Matplotlib Subplot Shorthand: (Rows, Columns, Plot Position)
    FULL_PLOT_POSITION = 111 

    def __init__(self, audio_obj, audio_obj2=None):
        """
        Initializes and runs the Audio visualization GUI.

        Args:
            audio_obj (Audio): The Audio object to visualize.
            audio_obj2 (Audio, optional): Optional second Audio object for comparison.
                If provided, operates in dual/comparison mode.
        """
        # Determine mode
        self._dual_mode = audio_obj2 is not None
        
        if self._dual_mode:
            # Dual mode: two audio objects
            self._samples1 = np.array(audio_obj.get_sample_list(), dtype=np.int16)
            self._rate = audio_obj.get_frame_rate()
            self._name1 = getattr(audio_obj, 'name', 'Audio 1 (Blue)')
            
            self._samples2 = np.array(audio_obj2.get_sample_list(), dtype=np.int16)
            self._name2 = getattr(audio_obj2, 'name', 'Audio 2 (Red)')
            
            # Basic Check
            if len(self._samples1) == 0 or len(self._samples2) == 0:
                messagebox.showwarning("No Data", "One or both audio segments are empty.")
                return
        else:
            # Single mode: one audio object
            self._audio = audio_obj
            self._sample_list = np.array(self._audio.get_sample_list(), dtype=np.int16)
            self._rate = self._audio.get_frame_rate()
            if len(self._sample_list) == 0:
                messagebox.showwarning("No Data", "No samples to display.")
                return

        # Tkinter setup
        self._root = tk.Tk()
        if self._dual_mode:
            self._root.title("Dual Waveform Comparison Viewer")
        else:
            self._root.title("Audio Viewer")

        # Figure + canvas
        if self._dual_mode:
            self._fig = Figure(figsize=(10, 5), dpi=100)
        else:
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

        if self._dual_mode:
            # Dual mode controls
            tk.Button(controls, text="Full Waveform", command=self.plot_waveform).grid(row=0, column=0, padx=10)
            
            tk.Label(controls, text="Start (s):").grid(row=0, column=1, padx=5)
            self.entry_start = tk.Entry(controls, width=6)
            self.entry_start.grid(row=0, column=2)
            
            tk.Label(controls, text="End (s):").grid(row=0, column=3, padx=5)
            self.entry_end = tk.Entry(controls, width=6)
            self.entry_end.grid(row=0, column=4)
            
            tk.Button(controls, text="Zoom Waveform", command=self.plot_zoom).grid(row=0, column=5, padx=10)
        else:
            # Single mode controls
            tk.Button(controls, text="Waveform", command=self.plot_waveform).grid(row=0, column=0, padx=5)
            
            tk.Label(controls, text="Start (s):").grid(row=0, column=2, padx=5)
            self.entry_start = tk.Entry(controls, width=6)
            self.entry_start.grid(row=0, column=3)
            
            tk.Label(controls, text="End (s):").grid(row=0, column=4, padx=5)
            self.entry_end = tk.Entry(controls, width=6)
            self.entry_end.grid(row=0, column=5)
            
            tk.Button(controls, text="Zoom Waveform", command=self.plot_zoom).grid(row=0, column=6, padx=5)
            
            tk.Button(controls, text="Peak Amplitude", command=self.show_peak).grid(row=0, column=1, padx=5)
            
            tk.Button(controls, text="Frequency Spectrum (FFT)", command=self.plot_fft).grid(row=0, column=7, padx=5)
            
            tk.Button(controls, text="Spectrogram", command=self.plot_spectrogram).grid(row=0, column=8, padx=5)

    def clear_cbar(self):
        """
        Removes the color bar created by the spectrogram if it exists.
        """
        # Check if the _cbar attribute exists AND is not None
        if hasattr(self, '_cbar') and self._cbar is not None:
            # Remove all axes from the figure to ensure clean state
            for ax in self._fig.axes:
                ax.remove()
            
            # Recreate the main Axes: This ensures a clean plot area
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
        self._ax.plot(x[:len(y1)], y1, linewidth=0.5, color="blue", label=self._name1)
        
        # Plot Audio 2 (Red)
        self._ax.plot(x[:len(y2)], y2, linewidth=0.5, color="red", label=self._name2)
        
        self._ax.set_xlabel("Time (s)")
        self._ax.set_ylabel("Amplitude")
        self._ax.set_title(title)
        self._ax.grid(True)
        self._ax.legend(loc='upper right')
        self._canvas.draw_idle()

    def plot_waveform(self):
        """
        Plots the full audio waveform(s) (Amplitude vs. Time).

        .. figure:: _static/dual_waveform_graphic.png
           :width: 80%
           :align: left
           :alt: Example plot of an audio spectrogram
        """
        if self._dual_mode:
            # Dual mode: plot both waveforms overlaid
            rate = self._rate
            max_samples = max(len(self._samples1), len(self._samples2))
            duration = max_samples / rate
            x = np.linspace(0, duration, num=max_samples)
            self._plot_dual(self._samples1, self._samples2, x, "Full Overlaid Waveforms")
        else:
            # Single mode: plot single waveform
            duration = len(self._sample_list) / self._rate
            x = np.linspace(0, duration, num=len(self._sample_list))
            self.plot(self._sample_list, x, "Full waveform")

    def plot_zoom(self):
        """
        Plots a zoomed-in portion of the waveform(s) based on user input times.
        """
        try:
            start_sec = float(self.entry_start.get())
            end_sec = float(self.entry_end.get())
        except ValueError:
            if self._dual_mode:
                messagebox.showwarning("Invalid Input", "Please enter numeric times.")
            else:
                messagebox.showwarning("Invalid Input", "Enter numeric times.")
            return
        
        if self._dual_mode:
            # Dual mode: zoom both waveforms
            rate = self._rate
            max_duration = max(len(self._samples1), len(self._samples2)) / rate
            
            if not (0 <= start_sec < end_sec <= max_duration):
                messagebox.showwarning("Invalid Range", 
                                      f"Range must be within the longest audio duration ({max_duration:.3f} s).")
                return
            
            start_idx = int(start_sec * rate)
            end_idx = int(end_sec * rate)
            
            y1_zoom = self._samples1[start_idx:end_idx]
            y2_zoom = self._samples2[start_idx:end_idx]
            
            x_zoom = np.linspace(start_sec, end_sec, num=len(y1_zoom))
            
            self._plot_dual(y1_zoom, y2_zoom, x_zoom, 
                            f"Zoomed Overlaid Waveforms ({start_sec:.2f}-{end_sec:.2f}s)")
        else:
            # Single mode: zoom single waveform
            if not (0 <= start_sec < end_sec <= len(self._sample_list) / self._rate):
                messagebox.showwarning("Invalid Range", "Out of range.")
                return
            start_idx, end_idx = int(start_sec * self._rate), int(end_sec * self._rate)
            y = self._sample_list[start_idx:end_idx]
            x = np.linspace(start_sec, end_sec, num=len(y))
            self.plot(y, x, f"Zoom {start_sec:.2f}-{end_sec:.2f}s")
        
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

