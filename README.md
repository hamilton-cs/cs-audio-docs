# CS101 Audio Library

A Pydub-based audio library for introductory computer science courses. This library provides a simplified interface for working with audio files, generating waveforms, and visualizing audio data.

## Features

- **Audio Generation**: Generate audio waveforms (Sine, Square, Sawtooth, Triangle) at specified frequencies
- **File I/O**: Load and save audio files in various formats (WAV, MP3, etc.)
- **Audio Manipulation**: Apply effects like fade, normalize, change speed, overlay, reverse, and more
- **Audio Analysis**: Pitch detection, amplitude analysis, and time-based queries
- **Interactive Visualization**: GUI tools for viewing waveforms, FFT spectrums, and spectrograms
- **Musical Notes**: Generate musical notes by name (e.g., "A4", "C#5")
- **Dual Audio Comparison**: Compare two audio files side-by-side in the viewer

## Installation

### Requirements

- Python 3.x
- pydub
- numpy
- matplotlib
- tkinter (usually included with Python)

### Install Dependencies

```bash
pip install pydub numpy matplotlib
```

**Note**: pydub requires ffmpeg for some audio formats. Install ffmpeg separately if needed:
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg` (or equivalent)
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Quick Start

```python
from cs101audio import *

# Generate a sine wave at 440 Hz for 2 seconds
audio = Audio()
audio.from_generator(440, 2000, "sine")
audio.play()

# Visualize the waveform
audio.view()
```

## Basic Usage

### Generating Audio

```python
from cs101audio import *

# Generate different wave types
sine = Audio()
sine.from_generator(440, 2000, "sine")      # 440 Hz sine wave, 2 seconds

square = Audio()
square.from_generator(440, 2000, "square")  # Square wave

triangle = Audio()
triangle.from_generator(440, 2000, "triangle")  # Triangle wave
```

### Loading Audio Files

```python
audio = Audio()
audio.open_audio_file("sample.wav")
audio.play()

# Save audio to a file
audio.save_to_file("output.mp3")
```

### Audio Manipulation

```python
# Apply fade in/out
audio.fade(500, 500)  # 500ms fade in, 500ms fade out

# Normalize amplitude
audio.normalize()

# Change playback speed (affects pitch)
audio.change_speed(1.5)  # 1.5x speed

# Apply gain (volume change)
audio.apply_gain(-6)  # Reduce volume by 6 dB

# Reverse audio
audio.reverse()

# Overlay two audio files
audio1.overlay(audio2)

# Concatenate audio
combined = audio1 + audio2
```

### Musical Notes

```python
# Generate musical notes
note = generate_music_note("A4", 1000, "sine")  # A4 note, 1 second, sine wave
note.play()

# Generate a chord
C4 = generate_music_note("C4", 3000, "sine")
E4 = generate_music_note("E4", 3000, "sine")
G4 = generate_music_note("G4", 3000, "sine")

C4.overlay(E4)
C4.overlay(G4)
C4.play()
```

### Audio Analysis

```python
# Get pitch at a specific time
pitch = audio.pitch_at_time(1000)  # Pitch at 1 second (in Hz)

# Get amplitude at a specific time
amplitude = audio.get_amplitude_at(500)  # Amplitude at 0.5 seconds

# Calculate average amplitude over a range
avg_amp = audio.average_amplitude(start_time=0, end_time=1000)
```

### Visualization

```python
# View single audio
audio.view()

# Compare two audio files
audio1.view_with(audio2)
```

The viewer provides:
- Full waveform display
- Zoomed waveform views
- Frequency spectrum (FFT)
- Spectrogram
- Peak amplitude information

## Examples

See the `examples/` directory for more detailed examples:

- **`demo.py`** - Demonstrates various features including waveform generation, effects, and visualization
- **`tasks.py`** - Example tasks and exercises

To run examples from the `examples/` directory:

```bash
cd examples
python demo.py
```

## Project Structure

```
cs-audio-docs/
├── cs101audio.py      # Main Audio class and core functionality
├── audio_viewer.py     # GUI visualization classes
├── examples/           # Example scripts
│   ├── demo.py
│   └── tasks.py
├── LICENSE
└── README.md
```

## Key Classes and Functions

### Audio Class

The main class for audio manipulation. Key methods include:

- `from_generator(freq, duration, wavetype)` - Generate waveforms
- `open_audio_file(filename)` - Load audio files
- `save_to_file(filename)` - Save audio files
- `play()` - Play audio
- `view()` - Open visualization GUI
- `view_with(other)` - Compare with another audio file
- `fade(fadeintime, fadeouttime)` - Apply fade effects
- `normalize(max_amplitude)` - Normalize audio amplitude
- `change_speed(factor)` - Change playback speed
- `apply_gain(gain)` - Adjust volume
- `overlay(audio2, position, loop)` - Mix audio files
- `pitch_at_time(time, window)` - Detect pitch
- `crescendo(start_time, end_time, final_multiplier)` - Gradual volume increase
- `decrescendo(start_time, end_time, initial_multiplier)` - Gradual volume decrease

### AudioViewer Class

GUI class for visualizing audio. Automatically used by `Audio.view()` and `Audio.view_with()`.

### generate_music_note()

Function to generate musical notes:
```python
generate_music_note(note, duration, wavetype, gain=0)
```

## Constants

- `Audio.MAX_AMPLITUDE` - Maximum 16-bit PCM amplitude (32767)
- `Audio.MIN_AMPLITUDE` - Minimum 16-bit PCM amplitude (-32768)

## Documentation

```
Full documentation is hosted at https://hamilton-cs.github.io/cs-audio-docs/
```

Documentation Build/Rebuild Instructions:
1. Make desired changes to docstrings in **cs101audio.py** and/or **audio_viewer.py** according to Sphinx format guidelines – https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html.
1. Navigate to the folder **docs-setup** in your terminal.
2. Run **make clean** to remove any existing documentation files.
3. Run **make html** to regenerate documentation files.
4. Push changes to GitHub; this will automatically re-deploy the site through GitHub Pages.


## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 hamilton-cs

## Contributing

This library is designed for educational use in computer science courses. For issues, questions, or contributions, please refer to the repository's issue tracker.
