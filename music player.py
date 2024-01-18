import os
import tkinter as tk
import pygame
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x500")
        root.resizable(True, True)
        

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Additional variables to track the current song and paused position
        self.current_song = None
        self.paused_positions = {}  # Dictionary to store paused positions for each song in the playlist
        self.playlist = []  # List to store songs

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        
        # Playlist Listbox
        # Playlist Listbox with resizable frame
        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(pady=10, expand=True, fill="both")  # Frame expands to fill space

        # Listbox with scrollbar
        self.playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE, bg="lightgray", selectbackground="darkgray")
        self.playlist_box.pack(side=tk.LEFT, expand=True, fill="both")  # Expand within the frame

        # Vertical scrollbar
        scrollbar = tk.Scrollbar(playlist_frame, command=self.playlist_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Link scrollbar to listbox
        self.playlist_box.config(yscrollcommand=scrollbar.set)


        # Button frame to keep buttons together
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        play_button = tk.Button(button_frame, text="▶", command=self.play_song)
        pause_button = tk.Button(button_frame, text="| |", command=self.pause_song)
        unpause_button = tk.Button(button_frame, text="| ▶", command=self.unpause_song)
        stop_button = tk.Button(button_frame, text="⏹", command=self.stop_song)
        add_button = tk.Button(button_frame, text="+", command=self.add_song)

        play_button.pack(side=tk.LEFT)
        pause_button.pack(side=tk.LEFT)
        unpause_button.pack(side=tk.LEFT)
        stop_button.pack(side=tk.LEFT)
        add_button.pack(side=tk.LEFT)

        # Label to display the name of the current song
        self.song_label = tk.Label(self.root, text="Song Name: ")
        self.song_label.pack(pady=5)

        # Seek Bar
        self.seek_bar = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=1000, showvalue=0, command=self.set_position)
        self.seek_bar.pack()

    def play_song(self):
        # If the current song is not playing or paused, allow the user to choose a song
        
        if not pygame.mixer.music.get_busy() and not self.paused_positions:
            if not self.playlist:
                return  # No songs in the playlist

            if self.current_song is None:
                self.current_song = self.playlist[0]  # Start with the first song in the playlist
    
            # Load and play the song from the paused position if available
            pygame.mixer.music.load(self.current_song)
            if self.current_song in self.paused_positions:
                pygame.mixer.music.play(start=self.paused_positions[self.current_song])
                self.paused_positions.pop(self.current_song)  # Remove the stored paused position
            else:
                pygame.mixer.music.play()

            # Update the song label with the current song name
            #self.song_label.config(text=f"Song Name: {self.current_song}")
            song_name = os.path.basename(self.current_song)
            self.song_label.config(text=f"Song Name: {song_name}")

            # Set the maximum value of the seek bar to the total length of the song
            self.seek_bar.config(to=pygame.mixer.Sound(self.current_song).get_length())

    def pause_song(self):
        # Pause the song and store the paused position
        if pygame.mixer.music.get_busy():
            self.paused_positions[self.current_song] = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
            pygame.mixer.music.pause()

    def unpause_song(self):
        # Unpause the song from the stored paused position
        if self.current_song in self.paused_positions:
            pygame.mixer.music.unpause()

    def stop_song(self):
        # Stop the song and reset the seek bar and paused position
        pygame.mixer.music.stop()
        self.seek_bar.set(0)
        self.paused_positions.clear()

    def set_position(self, value):
        if pygame.mixer.music.get_busy():
            position = float(value)
            pygame.mixer.music.set_pos(position)

    def add_song(self):
        # Allow the user to choose a song and add it to the playlist
        song_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if song_path:
            self.playlist.append(song_path)
            song_name = os.path.basename(song_path)
            self.playlist_box.insert(tk.END, song_name)
            print(f"Song added to playlist: {song_path}")

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
