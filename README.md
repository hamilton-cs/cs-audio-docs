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

This project is designed to work in the IDE Thonny. In the Thonny package manager
(found in the tools dropdown menu) search for and install the packages 'pydub,'
'numpy,' 'matplotlib,' and 'simpleaudiohamiltoncs.'

Pip Install:
```bash
pip install pydub numpy matplotlib simpleaudiohamiltoncs
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
- Peak amplitude information
- Frequency spectrum (FFT)
- Spectrogram

<img src="docs/_images/spectrogram_graphic.png" alt="Spectrogram Example" width="60%">

*Example of a spectrogram visualization showing frequency content over time*

**Dual Audio Viewer** (when using `view_with()`):
- Overlaid waveform display showing both audio files simultaneously
- Blue line represents the first audio, red line represents the second audio
- Zoom functionality to compare specific time ranges
- Full waveform view to see both audios over their entire duration

<img src="docs/_images/dual_waveform_graphic.png" alt="Dual Waveform Example" width="60%">

*Example of dual audio waveform comparison with overlaid waveforms*

## Examples

The repository includes two interactive example files in the `examples/` directory:

### demos.py

Interactive demonstrations of various library features. Run it to see examples of:
- Waveform comparisons (sine vs. square waves)
- Speed effects on frequency
- Fade effects
- Normalization and crescendo
- Amplitude clipping
- Chord generation

When you run `demos.py`, you'll see a menu of available demonstrations. Simply enter the number corresponding to the demo you want to run. Some demos allow you to:
- Load audio from a file (provide the full path if not in the current directory)
- Generate a sine wave with custom frequency and duration
- Adjust parameters like peak amplitude

### tasks.py

Interactive exercises and tasks for learning audio manipulation. Includes implementations of:
- Amplitude clipping
- Sample silencing
- Amplitude adjustment
- Audio muting (time-based)
- Audio reversal
- Echo effects
- Normalization
- Plot replication

When you run `tasks.py`, you'll see a menu of available tasks. Enter the number of the task you want to run. For each task, you can:
- Generate a default sine wave (220 Hz, 3 seconds)
- Load an audio file from your system (provide the full path, e.g., `../samples/sample.wav` if using files from the `samples/` directory)
- Provide task-specific parameters (e.g., peak amplitude, time ranges, delay values)
- Choose to play, view, or both after the task completes

### Running Examples

The example files (`demos.py` and `tasks.py`) are designed to work with both Thonny and standard command-line execution.

#### Using Thonny

1. **Open Thonny** on your computer
2. **Open the example file**:
   - Go to `File → Open...`
   - Navigate to the `examples/` directory in the repository
   - Open `demos.py` or `tasks.py`
3. **Run the file**:
   - Click the green "Run" button
   - The interactive menu will appear in the Thonny shell at the bottom
4. **Follow the prompts** in the Thonny shell

#### Using Command Line

1. **Open a terminal** 
2. **Navigate to the examples directory**:
   ```bash
   cd path/to/cs-audio-docs/examples
   ```
3. **Run the example**:
   ```bash
   python demos.py
   # or
   python tasks.py
   ```
4. **Follow the prompts** in the terminal

**Note:** Make sure Python 3.x is installed and accessible from your command line. You may need to use `python3` instead of `python` on some systems.

**Note:** Both `demos.py` and `tasks.py` can work standalone - they automatically handle importing the library from the `src/` directory, so you can copy these files to your own projects and they will still work (just make sure the `src/` directory structure is maintained relative to the examples).

## Project Structure

```
cs-audio-docs/
├── src/                 # Core library source code
│   ├── cs101audio.py    # Main Audio class and core functionality
│   └── audio_viewer.py  # GUI visualization classes
├── examples/            # Interactive example scripts
│   ├── demo.py          # Interactive demonstrations
│   └── tasks.py         # Interactive exercises and tasks
├── samples/             # Sample audio files (optional)
│   ├── c.wav
│   └── ...
├── docs/                # Generated documentation
├── docs-setup/          # Documentation source files
├── LICENSE
└── README.md
```

### Directory Descriptions

- **`src/`** - Contains the core library code. The `Audio` class and `AudioViewer` class are located here.
- **`examples/`** - Contains interactive demonstration and task files that students can run to learn the library.
- **`samples/`** - Optional directory for sample audio files. Students can use these or provide their own audio files.
- **`docs/`** - Auto-generated documentation (do not edit manually).
- **`docs-setup/`** - Source files for generating documentation using Sphinx.

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

Full documentation is hosted at [https://hamilton-cs.github.io/cs-audio-docs/](https://hamilton-cs.github.io/cs-audio-docs/)

Documentation Build/Rebuild Instructions:
1. Make desired changes to docstrings in `cs101audio.py` and/or `audio_viewer.py` according to Sphinx format guidelines – https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html.
1. Navigate to the folder `docs-setup` in your terminal.
2. Run `make clean` to remove any existing documentation files.
3. Run `make html` to regenerate documentation files.
4. Push changes to GitHub; this will automatically re-deploy the site through GitHub Pages.


## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 hamilton-cs

## Contributors

### Core Library (`src/cs101audio.py`)
- Jack Feser
- Gwen Urbanczyk
- Matthew Dioguardi
- Madison LaPoint
- Mark Bailey
- Sarah Morrison-Smith
- Lulu Ceccon
- Charles Beard

### Audio Viewer (`src/audio_viewer.py`)
- Lulu Ceccon
- Charles Beard

### Examples (`examples/`)
- Lulu Ceccon
- Charles Beard