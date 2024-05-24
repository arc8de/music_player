from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer
import os
import random

class NoiseMaker:
    def __init__(self, root):
        self.root = root
        self.root.title('NoiseMaker')
        self.root.resizable(0, 0)

        self.mixer = mixer
        self.mixer.init()

        self.SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.ogg'}

        self.current_song = StringVar(root, value='<Not selected>')
        self.song_status = StringVar(root, value='<Not Available>')

        self.random_bg_color = self.generate_random_color()
        
        self.create_widgets()

    def generate_random_color(self):
        return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

    def create_widgets(self):
        # Frame configurations
        self.song_frame = Frame(self.root, bg=self.random_bg_color)
        self.song_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.listbox_frame = Frame(self.root, bg=self.random_bg_color)
        self.listbox_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.button_frame = Frame(self.root, bg=self.random_bg_color)
        self.button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Playlist ListBox
        self.playlist = Listbox(self.listbox_frame, font=('Helvetica', 11), selectbackground='navyblue', bg="#1E1E1E", fg="white")
        self.playlist.pack(fill=BOTH, expand=True)

        self.scroll_bar = Scrollbar(self.listbox_frame, orient=VERTICAL, command=self.playlist.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.playlist.config(yscrollcommand=self.scroll_bar.set)

        # SongFrame Labels
        Label(self.song_frame, text='CURRENTLY PLAYING:', bg=self.random_bg_color, fg="white", font=('Helvetica', 10, 'bold')).pack(pady=5)

        self.song_lbl = Label(self.song_frame, textvariable=self.current_song, bg=self.random_bg_color, fg="white", font=('Helvetica', 12))
        self.song_lbl.pack(pady=5)

        # Buttons in the main screen
        self.play_btn = Button(self.button_frame, text='Play', bg='lime', fg="black", font=("Helvetica", 11), width=10,
                               command=self.play_song)
        self.play_btn.grid(row=0, column=1, padx=5, pady=5)

        self.pause_btn = Button(self.button_frame, text='Pause', bg='orange', fg="black", font=("Helvetica", 11), width=10,
                                command=self.pause_song)
        self.pause_btn.grid(row=0, column=2, padx=5, pady=5)

        self.resume_btn = Button(self.button_frame, text='Resume', bg='green', fg="black", font=("Helvetica", 11), width=10,
                                 command=self.resume_song)
        self.resume_btn.grid(row=0, column=3, padx=5, pady=5)

        self.stop_btn = Button(self.button_frame, text='Stop', bg='#FF000D', fg="black", font=("Helvetica", 11), width=10,
                               command=self.stop_song)
        self.stop_btn.grid(row=0, column=4, padx=5, pady=5)

        self.load_btn = Button(self.button_frame, text='Load Songs', bg='navyblue', fg="white", font=("Helvetica", 11), width=10,
                               command=self.load)
        self.load_btn.grid(row=1, column=2, padx=5, pady=5)

        self.previous_btn = Button(self.button_frame, text='Previous', bg='navyblue', fg="white", font=("Helvetica", 11), width=10,
                                   command=self.previous_song)
        self.previous_btn.grid(row=0, column=0, padx=5, pady=5)

        self.next_btn = Button(self.button_frame, text='Next', bg='navyblue', fg="white", font=("Helvetica", 11), width=10,
                               command=self.next_song)
        self.next_btn.grid(row=0, column=5, padx=5, pady=5)

        # Volume control slider
        self.volume_slider = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, label="Volume", bg=self.random_bg_color, fg="white",
                                   font=("Helvetica", 11), length=300, command=self.adjust_volume, highlightthickness=0, troughcolor="Gray")
        self.volume_slider.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Set default volume level to 50
        self.volume_slider.set(50)
        self.adjust_volume(50)

        # Label at the bottom that displays the state of the music
        Label(self.root, textvariable=self.song_status, bg=self.random_bg_color, fg="white", font=('Helvetica', 9), justify=LEFT).grid(row=3, column=0, 
                                                                                                                columnspan=2, sticky="ew")

        # Configure row and column weights for resizing
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def play_song(self):
        selected_song = self.playlist.get(ACTIVE)
        if selected_song:
            self.current_song.set(selected_song)
            self.mixer.music.load(selected_song)
            self.mixer.music.play()
            self.song_status.set("Song PLAYING")

    def stop_song(self):
        self.mixer.music.stop()
        self.song_status.set("Song STOPPED")

    def load(self):
        directory = filedialog.askdirectory(title='Open a songs directory')
        if directory:
            os.chdir(directory)
            tracks = os.listdir()
            audio_tracks = [track for track in tracks if os.path.splitext(track)[1].lower() in self.SUPPORTED_EXTENSIONS]
            for track in audio_tracks:
                self.playlist.insert(END, track)

    def pause_song(self):
        self.mixer.music.pause()
        self.song_status.set("Song PAUSED")

    def resume_song(self):
        self.mixer.music.unpause()
        self.song_status.set("Song RESUMED")

    def next_song(self):
        next_index = min(self.playlist.curselection()[0] + 1, self.playlist.size() - 1)
        self.playlist.selection_clear(0, END)
        self.playlist.activate(next_index)
        self.playlist.selection_set(next_index)
        self.play_song()

    def previous_song(self):
        prev_index = max(self.playlist.curselection()[0] - 1, 0)
        self.playlist.selection_clear(0, END)
        self.playlist.activate(prev_index)
        self.playlist.selection_set(prev_index)
        self.play_song()

    def adjust_volume(self, value):
        volume_level = float(value) / 100.0
        self.mixer.music.set_volume(volume_level)

if __name__ == "__main__":
    root = Tk()
    NoiseMaker(root)
    root.mainloop()
