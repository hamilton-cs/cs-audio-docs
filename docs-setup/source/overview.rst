Overview
========

CS101 Audio is a wrapper around the simpleaudio Python library designed to make audio
manipulation simple and intuitive for computer science students.

Features
--------

* Simple audio file loading and saving
* Audio generation using sine, square, sawtooth, and triangle waves
* Musical note generation with a complete note dictionary (C0-A8)
* Audio manipulation: concatenation, looping, slicing, and overlaying
* Effects: fade in/out, gain adjustment, speed changes, reversing
* Interactive visualization with AudioViewer GUI

Installation
------------

First, install the required dependencies::

    pip install pydub numpy matplotlib

You may also need to install ffmpeg for audio file format support.

Quick Start
-----------

Here's a simple example to get started::

    from cs101audio import *
    
    # Create and play a musical note
    note = generate_music_note('C4', 1000, 'Sine')
    note.play()
    
    # Load an audio file
    audio = Audio()
    audio.open_audio_file('myfile.mp3')
    
    # Visualize the audio
    audio.view()