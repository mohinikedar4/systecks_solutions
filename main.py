import tkinter as tk
from tkinter import filedialog, messagebox
from tts_engine import TTSEngine
import threading

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Application")
        self.tts_engine = TTSEngine()

        self.create_widgets()

    def create_widgets(self):
        self.text_label = tk.Label(self.root, text="Enter Text:")
        self.text_label.pack()

        self.text_entry = tk.Text(self.root, height=10, width=50)
        self.text_entry.pack()

        self.voice_label = tk.Label(self.root, text="Select Voice:")
        self.voice_label.pack()

        self.voice_var = tk.StringVar()
        self.voice_menu = tk.OptionMenu(self.root, self.voice_var, *self.get_voice_names())
        self.voice_menu.pack()

        self.rate_label = tk.Label(self.root, text="Speech Rate:")
        self.rate_label.pack()

        self.rate_scale = tk.Scale(self.root, from_=100, to=300, orient=tk.HORIZONTAL)
        self.rate_scale.pack()

        self.volume_label = tk.Label(self.root, text="Volume:")
        self.volume_label.pack()

        self.volume_scale = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.volume_scale.pack()

        self.speak_button = tk.Button(self.root, text="Speak", command=self.speak_text)
        self.speak_button.pack()

        self.save_button = tk.Button(self.root, text="Save as Audio", command=self.save_audio)
        self.save_button.pack()

        self.play_button = tk.Button(self.root, text="Play Audio", command=self.play_audio)
        self.play_button.pack()

    def get_voice_names(self):
        voices = self.tts_engine.voices
        return [voice.name for voice in voices]

    def speak_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            self.tts_engine.set_voice(self.get_selected_voice_id())
            self.tts_engine.set_rate(self.rate_scale.get())
            self.tts_engine.set_volume(self.volume_scale.get())
            threading.Thread(target=self.tts_engine.speak, args=(text,)).start()
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def get_selected_voice_id(self):
        selected_voice = self.voice_var.get()
        for voice in self.tts_engine.voices:
            if voice.name == selected_voice:
                return voice.id
        return None

    def save_audio(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                     filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
            if file_path:
                self.tts_engine.save_audio(text, file_path)
                messagebox.showinfo("Success", "Audio file saved successfully.")
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def play_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3"), ("All files", "*.*")])
        if file_path:
            threading.Thread(target=self.tts_engine.play_audio, args=(file_path,)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()
