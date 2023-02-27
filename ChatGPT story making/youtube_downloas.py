import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube, Playlist
from playsound import playsound
import os

class YouTubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        # Create the URL input field
        self.url_label = tk.Label(master, text="URL or Playlist URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # Create the download type selector
        self.download_type_label = tk.Label(master, text="Download Type:")
        self.download_type_label.pack()

        self.download_type = tk.StringVar(value="video")
        self.download_type_video = tk.Radiobutton(master, text="Video", variable=self.download_type, value="video")
        self.download_type_video.pack()

        self.download_type_audio = tk.Radiobutton(master, text="Audio", variable=self.download_type, value="audio")
        self.download_type_audio.pack()

        # Create the video download location selector
        self.video_download_location_label = tk.Label(master, text="Video Download Location:")
        self.video_download_location_label.pack()

        self.video_download_location_button = tk.Button(master, text="Choose Folder", command=self.choose_video_download_location)
        self.video_download_location_button.pack()

        self.video_download_location = ""

        # Create the audio download location selector
        self.audio_download_location_label = tk.Label(master, text="Audio Download Location:")
        self.audio_download_location_label.pack()

        self.audio_download_location_button = tk.Button(master, text="Choose Folder", command=self.choose_audio_download_location)
        self.audio_download_location_button.pack()

        self.audio_download_location = ""

        # Create the download button
        self.download_button = tk.Button(master, text="Download", command=self.download)
        self.download_button.pack()

        # Create the downloaded items listbox
        self.downloaded_items_label = tk.Label(master, text="Downloaded Items:")
        self.downloaded_items_label.pack()

        self.downloaded_items_listbox = tk.Listbox(master, width=100)
        self.downloaded_items_listbox.pack()

        self.downloaded_items = []

        # Create the play button
        self.play_button = tk.Button(master, text="Play", command=self.play)
        self.play_button.pack()

    def choose_video_download_location(self):
        # Show a dialog to choose the video download location
        self.video_download_location = filedialog.askdirectory()

    def choose_audio_download_location(self):
        # Show a dialog to choose the audio download location
        self.audio_download_location = filedialog.askdirectory()

    def download(self):
        # Get the URL from the input field
        url = self.url_entry.get()

        if "playlist" in url:
            # Download the playlist
            playlist = Playlist(url)

            # Select the stream to download based on the download type
            if self.download_type.get() == "video":
                for video in playlist.videos:
                    stream = video.streams.get_highest_resolution()

                    # Get the filename and download the stream to the video download location
                    filename = video.title
                    stream.download(output_path=self.video_download_location, filename=filename)

                    # Add the filename to the downloaded items list
                    self.downloaded_items.append(os.path.join(self.video_download_location, filename))

            else:
                for video in playlist.videos:
                    stream = video.streams.filter(only_audio=True).get_highest_resolution()

                    # Get the filename and download the stream to
                    filename = video.title + ".mp3"
                    stream.download(output_path=self.audio_download_location, filename=filename)

                    # Add the filename to the downloaded items list
                    self.downloaded_items.append(os.path.join(self.audio_download_location, filename))

        else:
            # Download the single video
            yt = YouTube(url)

            # Select the stream to download based on the download type
            if self.download_type.get() == "video":
                stream = yt.streams.get_highest_resolution()

                # Get the filename and download the stream to the video download location
                filename = yt.title
                stream.download(output_path=self.video_download_location, filename=filename)

                # Add the filename to the downloaded items list
                self.downloaded_items.append(os.path.join(self.video_download_location, filename))

            else:
                stream = yt.streams.filter(only_audio=True).get_highest_resolution()

                # Get the filename and download the stream to the audio download location
                filename = yt.title + ".mp3"
                stream.download(output_path=self.audio_download_location, filename=filename)

                # Add the filename to the downloaded items list
                self.downloaded_items.append(os.path.join(self.audio_download_location, filename))

        # Update the downloaded items listbox
        self.update_downloaded_items_listbox()

        # Show a message box indicating that the download is complete
        messagebox.showinfo("Download Complete", "The download has been completed successfully.")

    def update_downloaded_items_listbox(self):
        # Clear the downloaded items listbox
        self.downloaded_items_listbox.delete(0, tk.END)

        # Add the downloaded items to the listbox
        for item in self.downloaded_items:
            self.downloaded_items_listbox.insert(tk.END, item)

    def play(self):
        # Get the selected item from the downloaded items listbox
        selected_item = self.downloaded_items_listbox.get(tk.ACTIVE)

        # Play the selected item
        playsound(selected_item)

# Create the main window and start the GUI
root = tk.Tk()
my_gui = YouTubeDownloaderGUI(root)
root.mainloop()
