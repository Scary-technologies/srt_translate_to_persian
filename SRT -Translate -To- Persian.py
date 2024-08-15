import os
import re
from translate import Translator
from tqdm import tqdm

class SRTTranslator:
    def __init__(self, source_lang='en', target_lang='fa'):
        self.translator = Translator(from_lang=source_lang, to_lang=target_lang)

    def parse_srt(self, content):
        """
        Parse the content of an SRT file into a list of dictionaries with index, start time, end time, and text.
        """
        pattern = re.compile(
            r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+(.*?)\s*(?=\d+\s|$)',
            re.DOTALL
        )
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

    def compose_srt(self, subtitles):
        """
        Convert the list of subtitles back into the SRT file format.
        """
        srt_content = ""
        for subtitle in subtitles:
            srt_content += f"{subtitle['index']}\n{subtitle['start']} --> {subtitle['end']}\n{subtitle['text']}\n\n"
        return srt_content

    def translate_subtitle(self, subtitles):
        """
        Translate the text of each subtitle and return the translated list.
        """
        translated_subtitles = []
        for subtitle in tqdm(subtitles, desc="Translating Subtitles", unit="subtitle"):
            try:
                translated_text = self.translator.translate(subtitle['text'])
                subtitle['text'] = translated_text
            except Exception as e:
                print(f"Error translating subtitle index {subtitle['index']}: {e}")
                subtitle['text'] = f"[Translation Error: {subtitle['text']}]"
            translated_subtitles.append(subtitle)
        return translated_subtitles

    def process_srt_file(self, file_path):
        """
        Read, translate, and write back the translated SRT file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            srt_content = file.read()

        subtitles = self.parse_srt(srt_content)
        translated_subtitles = self.translate_subtitle(subtitles)
        translated_srt_content = self.compose_srt(translated_subtitles)

        translated_file_path = file_path.replace('.srt', '_fa.srt')
        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
            translated_file.write(translated_srt_content)

        return translated_file_path

    def translate_srt_files_in_directory(self, directory):
        """
        Translate all SRT files in a given directory.
        """
        for filename in os.listdir(directory):
            if filename.endswith(".srt"):
                file_path = os.path.join(directory, filename)
                translated_file_path = file_path.replace('.srt', '_fa.srt')
                
                # Skip translation if the file already exists
                if os.path.exists(translated_file_path):
                    print(f"Skipping {file_path} - translated version already exists.")
                    continue
                
                print(f"Translating: {file_path}")
                try:
                    self.process_srt_file(file_path)
                    print(f"Translated file saved to: {translated_file_path}")
                except Exception as e:
                    print(f"Failed to translate {file_path}: {e}")

if __name__ == "__main__":
    # Directory containing the SRT files
    srt_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize the SRTTranslator class
    translator = SRTTranslator()
    
    # Translate all SRT files in the specified directory
    translator.translate_srt_files_in_directory(srt_directory)
