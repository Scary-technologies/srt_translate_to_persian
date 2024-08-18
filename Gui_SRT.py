import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pysrt
import os
from googletrans import Translator
import threading

class SRTTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("SRT Translator")

        # Set the grid layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        # Text area for log output
        self.text = scrolledtext.ScrolledText(master, height=15)
        self.text.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Listbox for displaying selected files
        self.file_listbox = tk.Listbox(master, height=8)
        self.file_listbox.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Language selection labels and dropdowns
        self.src_lang_label = tk.Label(master, text="Source Language:")
        self.src_lang_label.grid(row=2, column=0, sticky='w', padx=10)

        self.src_lang_var = tk.StringVar(value="en")  # Default source language is English
        self.src_lang_menu = tk.OptionMenu(master, self.src_lang_var, "en", "fa", "es", "de", "fr", "zh-cn", "ar")
        self.src_lang_menu.grid(row=2, column=0, sticky='e', padx=10)

        self.dest_lang_label = tk.Label(master, text="Destination Language:")
        self.dest_lang_label.grid(row=3, column=0, sticky='w', padx=10)

        self.dest_lang_var = tk.StringVar(value="fa")  # Default destination language is Persian
        self.dest_lang_menu = tk.OptionMenu(master, self.dest_lang_var, "en", "fa", "es", "de", "fr", "zh-cn", "ar")
        self.dest_lang_menu.grid(row=3, column=0, sticky='e', padx=10)

        # Translate button
        self.translate_button = tk.Button(master, text="Translate SRT(s)", command=self.start_translation_thread)
        self.translate_button.grid(row=4, column=0, sticky='ew', padx=10, pady=(0, 10))

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=100, mode="determinate")
        self.progress.grid(row=5, column=0, sticky='ew', padx=10, pady=5)

        # Progress Label
        self.progress_label = tk.Label(master, text="Lines Translated: 0 | Remaining: 0")
        self.progress_label.grid(row=6, column=0, sticky='ew', padx=10)

    def start_translation_thread(self):
        threading.Thread(target=self.translate_srt).start()

    def translate_srt(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        if not filepaths:
            return

        # Clear previous file list
        self.file_listbox.delete(0, tk.END)
        for filepath in filepaths:
            self.file_listbox.insert(tk.END, os.path.basename(filepath))

        translator = Translator()
        output_dir = "translated_srt"
        os.makedirs(output_dir, exist_ok=True)

        total_lines = 0
        for filepath in filepaths:
            subs = pysrt.open(filepath)
            total_lines += len(subs)

        translated_lines = 0
        self.progress["maximum"] = total_lines

        src_lang = self.src_lang_var.get()
        dest_lang = self.dest_lang_var.get()

        for filepath in filepaths:
            subs = pysrt.open(filepath)
            output_path = os.path.join(output_dir, os.path.basename(filepath))

            for i, sub in enumerate(subs):
                translated_text = translator.translate(sub.text, src=src_lang, dest=dest_lang).text
                subs[i].text = translated_text
                translated_lines += 1
                self.text.insert(tk.END, f"Translating: {sub.text}\n")
                self.text.yview(tk.END)

                # Update progress
                remaining_lines = total_lines - translated_lines
                self.progress["value"] = ranslated_lines
                self.progress_label.config(text=f"Lines Translated: {translated_lines} | Remaining: {remaining_lines}")
                self.master.update_idletasks()

            subs.save(output_path, encoding='utf-8')

        messagebox.showinfo("Translation Complete", f"All translations completed and saved to '{output_dir}'.")

root = tk.Tk()
app = SRTTranslatorApp(root)
root.mainloop()
