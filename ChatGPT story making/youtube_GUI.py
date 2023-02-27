import tkinter as tk
from tkinter import filedialog
import pytube
import os
import subprocess
import platform

class YouTubeDownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader")

        # Initialize variables
        self.download_location = os.getcwd()
        self.video_quality = tk.StringVar(value="720p")
        self.current_item = None
        self.downloaded_items = []

        # Create widgets
        self.url_label = tk.Label(self.root, text="Video URL:")
        self.url_entry = tk.Entry(self.root, width=50)
        self.video_quality_label = tk.Label(self.root, text="Video Quality:")
        self.video_quality_menu = tk.OptionMenu(self.root, self.video_quality, "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p")
        self.download_button = tk.Button(self.root, text="Download", command=self.download)
        self.audio_button = tk.Button(self.root, text="Download Audio", command=self.download_audio)
        self.download_location_button = tk.Button(self.root, text="Choose Download Location", command=self.choose_download_location)
        self.playlist_button = tk.Button(self.root, text="Download Playlist", command=self.download_playlist)
        self.downloaded_items_label = tk.Label(self.root, text="Downloaded Items:")
        self.downloaded_items_listbox = tk.Listbox(self.root, height=10, selectmode=tk.SINGLE)
        self.play_button = tk.Button(self.root, text="Play", command=self.play)
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop)
        self.next_button = tk.Button(self.root, text="Next", command=self.next_item)
        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_item)

        # Add widgets to the grid
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.video_quality_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.video_quality_menu.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.download_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.audio_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.download_location_button.grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        self.playlist_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.downloaded_items_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.downloaded_items_listbox.grid(row=5, column=0, padx=5, pady=5, columnspan=3, sticky=tk.W+tk.E)
        self.play_button.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.pause_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)
        self.stop_button.grid(row=6, column=2, padx=5, pady=5, sticky=tk.E)
        self.previous_button.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.next_button.grid(row=7, column=2, padx=5, pady=5, sticky=tk.E)

        # Bind double-click event to listbox items
        self.downloaded_items_listbox.bind("<Double-Button-1>", self.play)

        # Start the main loop
        self.root.mainloop()

    def download(self):
        url = self.url_entry.get()
        try:
            youtube = pytube.YouTube(url)
            video = youtube.streams.filter(res=self.video_quality.get()).first()
            filename = video.download(self.download_location)
            self.downloaded_items.append(filename)
            self.downloaded_items_listbox.insert(tk.END, os.path.basename(filename))
            self.url_entry.delete(0, tk.END)
        except Exception as e:
            print(e)

    def download_audio(self):
        url = self.url_entry.get()
        try:
            youtube = pytube.YouTube(url)
            audio = youtube.streams.filter(only_audio=True).first()
            filename = audio.download(self.download_location)
            self.downloaded_items.append(filename)
            self.downloaded_items_listbox.insert(tk.END, os.path.basename(filename))
            self.url_entry.delete(0, tk.END)
        except Exception as e:
            print(e)

    def choose_download_location(self):
        self.download_location = filedialog.askdirectory()
    
    def download_playlist(self):
        url = self.url_entry.get()
        try:
            youtube = pytube.Playlist(url)
            for video in youtube.videos:
                filename = video.streams.filter(res=self.video_quality.get()).first().download(self.download_location)
                self.downloaded_items.append(filename)
                self.downloaded_items_listbox.insert(tk.END, os.path.basename(filename))
            self.url_entry.delete(0, tk.END)
        except Exception as e:
            print(e)

    def play(self, event=None):
        if self.current_item is not None:
            self.stop()
        selected_item = self.downloaded_items_listbox.curselection()
        if selected_item:
            index = selected_item[0]
            filename = self.downloaded_items[index]
            if platform.system() == "Windows":
                subprocess.Popen(["start", os.path.abspath(filename)], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", filename])
            else:
                subprocess.Popen(["xdg-open", filename])
            self.current_item = index

    def pause(self):
        if self.current_item is not None:
            if platform.system() == "Windows":
                subprocess.Popen(["taskkill", "/F", "/IM", "wmplayer.exe"], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["killall", "afplay"])
            else:
                subprocess.Popen(["killall", "mpv"])

    def stop(self):
        if self.current_item is not None:
            if platform.system() == "Windows":
                subprocess.Popen(["taskkill", "/F", "/IM", "wmplayer.exe"], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["killall", "afplay"])
            else:
                subprocess.Popen(["killall", "mpv"])
            self.current_item = None

    def next_item(self):
        if self.current_item is not None:
            index = (self.current_item + 1) % len(self.downloaded_items)
            self.play_item(index)

    def previous_item(self):
        if self.current_item is not None:
            index = (self.current_item - 1) % len(self.downloaded_items)
            self.play_item(index)

    def play_item(self, index):
        filename = self.downloaded_items[index]
        if platform.system() == "Windows":
            subprocess.Popen(["start", os.path.abspath(filename)], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", filename])
        else:
            subprocess.Popen(["xdg-open", filename])
        self.current_item = index

if __name__ == "__main__":
    app = YouTubeDownloaderGUI()

