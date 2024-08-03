import re
import os
from googletrans import Translator

# Initialize the Google Translator
translator = Translator()

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

def compose_srt(subtitles):
    srt_content = ""
    for subtitle in subtitles:
        srt_content += f"{subtitle['index']}\n{subtitle['start']} --> {subtitle['end']}\n{subtitle['text']}\n\n"
    return srt_content

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

# مسیر پوشه حاوی فایل‌های SRT را به دست آورید
srt_directory = os.path.dirname(os.path.abspath(__file__))
translate_srt_files(srt_directory)
