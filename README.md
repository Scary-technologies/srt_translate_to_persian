# Document for SRT Subtitle Translation Script

## Overview

This script is designed to automate the translation of SRT subtitle files from English to Persian (Farsi) using the Google Translate API. It processes all SRT files in the directory where the script is located, translating each file unless a translated version already exists.

## Requirements

- Python 3.x
- `googletrans` library

## Installation

To install the required `googletrans` library, use the following pip command:

```bash
pip install googletrans==4.0.0-rc1
```

## Script Explanation

### Imports

```python
import re
import os
from googletrans import Translator
```

- `re`: Used for regular expressions to parse the SRT file content.
- `os`: Used for interacting with the operating system, such as reading files from a directory.
- `googletrans`: A library to access the Google Translate API.

### Initialize the Translator

```python
translator = Translator()
```

Creates an instance of the Translator object from the `googletrans` library.

### Parse SRT Content

```python
def parse_srt(content):
    pattern = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+(.*?)\s*(?=\d+\s|$)', re.DOTALL)
    matches = pattern.findall(content)
    subtitles = []
    for match in matches:
        subtitles.append({
            'index': match[0],
            'start': match[1],
            'end': match[2],
            'text': match[3].replace('\n', ' ')
        })
    return subtitles
```

- `parse_srt(content)`: Parses the content of an SRT file.
- Uses regular expressions to extract subtitle index, timestamps, and text.
- Returns a list of dictionaries, each representing a subtitle.

### Compose SRT Content

```python
def compose_srt(subtitles):
    srt_content = ""
    for subtitle in subtitles:
        srt_content += f"{subtitle['index']}\n{subtitle['start']} --> {subtitle['end']}\n{subtitle['text']}\n\n"
    return srt_content
```

- `compose_srt(subtitles)`: Takes a list of subtitles and converts it back into the SRT file format.
- Returns the SRT formatted string.

### Translate Subtitle

```python
def translate_subtitle(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    subtitles = parse_srt(srt_content)
    
    for subtitle in subtitles:
        translated_text = translator.translate(subtitle['text'], dest='fa').text
        subtitle['text'] = translated_text
    
    translated_srt_content = compose_srt(subtitles)
    
    translated_file_path = file_path.replace('.srt', '_fa.srt')
    with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
        translated_file.write(translated_srt_content)
    
    return translated_file_path
```

- `translate_subtitle(file_path)`: Reads the SRT file, translates the content, and writes the translated subtitles to a new file.
- The new file has the same name as the original but with `_fa` appended before the `.srt` extension.

### Translate SRT Files in Directory

```python
def translate_srt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            file_path = os.path.join(directory, filename)
            translated_file_path = file_path.replace('.srt', '_fa.srt')
            if not os.path.exists(translated_file_path):
                print(f"Translating: {file_path}")
                translate_subtitle(file_path)
                print(f"Translated file saved to: {translated_file_path}")
            else:
                print(f"Skipping {file_path} - translated version already exists.")
```

- `translate_srt_files(directory)`: Scans the specified directory for SRT files and translates them if a translated version does not already exist.

### Main Execution

```python
srt_directory = os.path.dirname(os.path.abspath(__file__))
translate_srt_files(srt_directory)
```

- `srt_directory`: Sets the directory to the location of the script.
- Calls `translate_srt_files(srt_directory)` to process all SRT files in the directory.

## Usage

1. Place the script in the directory containing your SRT files.
2. Run the script:

```bash
python your_script_name.py
```

3. The script will process each SRT file in the directory, translating it to Persian if a translated version does not already exist.

By following these steps, you can automate the translation of your SRT subtitle files efficiently.
