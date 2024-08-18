# SRT Translator App

This is a simple Python application built with `tkinter` for translating `.srt` subtitle files. The app allows users to select one or more `.srt` files and translate them into the desired language.

## Features

- **Translate multiple SRT files:** The app supports translating multiple `.srt` files at once.
- **Language Selection:** Users can select the source and destination languages from the UI.
- **Real-time Progress Tracking:** The app displays real-time progress with a progress bar and updates the number of lines translated.
- **Log Output:** The app provides real-time logs of the ongoing translation.
- **Save Translations:** Translated files are saved in a separate folder called `translated_srt`.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- `pysrt` library
- `googletrans` library (unofficial)
- `tkinter` (comes pre-installed with most Python distributions)

You can install the required Python libraries with the following command:

```bash
pip install pysrt googletrans==4.0.0-rc1
