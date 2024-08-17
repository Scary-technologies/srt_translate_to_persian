import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pysrt
import os
from googletrans import Translator
import time
import threading

class SRTTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("SRT Translator")

        # Set the grid layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.text = scrolledtext.ScrolledText(master)
        self.text.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.translate_button = tk.Button(master, text="Translate SRT(s)", command=self.start_translation_thread)
        self.translate_button.grid(row=1, column=0, sticky='ew', padx=10, pady=(0, 10))

        # Progress Label
        self.progress_label = tk.Label(master, text="Lines Translated: 0 | Remaining: 0")
        self.progress_label.grid(row=2, column=0, sticky='ew', padx=10)

    def start_translation_thread(self):
        threading.Thread(target=self.translate_srt).start()

    def translate_srt(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        if not filepaths:
            return

        translator = Translator()
        output_dir = "translated_srt"
        os.makedirs(output_dir, exist_ok=True)

        total_lines = 0
        for filepath in filepaths:
            subs = pysrt.open(filepath)
            total_lines += len(subs)

        translated_lines = 0

        for filepath in filepaths:
            subs = pysrt.open(filepath)
            output_path = os.path.join(output_dir, os.path.basename(filepath))

            for i, sub in enumerate(subs):
                translated_text = translator.translate(sub.text, src='en', dest='fa').text
                subs[i].text = translated_text
                translated_lines += 1
                self.text.insert(tk.END, f"Translating: {sub.text}\n")
                self.text.yview(tk.END)

                # Update progress
                remaining_lines = total_lines - translated_lines
                self.progress_label.config(text=f"Lines Translated: {translated_lines} | Remaining: {remaining_lines}")
                self.master.update_idletasks()

            subs.save(output_path, encoding='utf-8')

        messagebox.showinfo("Translation Complete", f"All translations completed and saved to '{output_dir}'.")

root = tk.Tk()
app = SRTTranslatorApp(root)
root.mainloop()
