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

        self.translate_button = tk.Button(master, text="Translate SRT", command=self.start_translation_thread)
        self.translate_button.grid(row=1, column=0, sticky='ew', padx=10)

    def start_translation_thread(self):
        threading.Thread(target=self.translate_srt).start()

    def translate_srt(self):
        filepath = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
        if not filepath:
            return

        subs = pysrt.open(filepath)
        translator = Translator()
        output_dir = "translated_srt"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(filepath))

        start_time = time.time()
        for i, sub in enumerate(subs):
            translated_text = translator.translate(sub.text, src='en', dest='fa').text
            subs[i].text = translated_text
            self.text.insert(tk.END, f"Translating: {sub.text}\n")
            self.text.yview(tk.END)

        subs.save(output_path, encoding='utf-8')

        elapsed_time = time.time() - start_time
        messagebox.showinfo("Translation Complete", f"Translated SRT saved to {output_path}\nTime taken: {elapsed_time:.2f} seconds")

root = tk.Tk()
app = SRTTranslatorApp(root)
root.mainloop()
