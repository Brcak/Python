import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from ttkbootstrap import Style
from yt_dlp import YoutubeDL
import os
import time

# Hacker-style terminal effect
def hacker_effect(text_widget, text, delay=0.05):
    for char in text:
        text_widget.insert(tk.END, char)
        text_widget.update()
        time.sleep(delay)

# Function to import links from a text file
def import_links():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            links = file.readlines()
            for link in links:
                link_listbox.insert(tk.END, link.strip())
        hacker_effect(log_text, "Links imported successfully!\n")

# Function to download videos
def download_videos():
    download_folder = filedialog.askdirectory()
    if not download_folder:
        return

    ydl_opts = {
        'format': 'best',  # Download the best quality available
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save videos with their titles
        'quiet': True,  # Suppress yt-dlp output
    }

    for link in link_listbox.get(0, tk.END):
        try:
            hacker_effect(log_text, f"Downloading: {link}...\n")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            hacker_effect(log_text, f"Downloaded: {link}\n")
            # Add to management system
            with open("downloaded_videos.txt", "a") as f:
                f.write(f"{link}\n")
            # Add a delay to avoid rate limiting
            time.sleep(5)
        except Exception as e:
            hacker_effect(log_text, f"Error downloading {link}: {str(e)}\n")

# GUI Setup
root = tk.Tk()
root.title("YouTube Video Downloader - Hacker Style")
root.geometry("800x600")

# Apply a dark theme
style = Style(theme="darkly")

# Main Frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Link Listbox
link_listbox = tk.Listbox(main_frame, width=100, height=10, bg="black", fg="green", font=("Courier", 12))
link_listbox.pack(pady=10)

# Buttons
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

import_button = tk.Button(button_frame, text="Import Links", command=import_links, bg="black", fg="green", font=("Courier", 12))
import_button.pack(side=tk.LEFT, padx=5)

download_button = tk.Button(button_frame, text="Download Videos", command=download_videos, bg="black", fg="green", font=("Courier", 12))
download_button.pack(side=tk.LEFT, padx=5)

# Log Text Area
log_text = scrolledtext.ScrolledText(main_frame, width=100, height=20, bg="black", fg="green", font=("Courier", 12))
log_text.pack(pady=10)

# Initial Message
hacker_effect(log_text, "Welcome to YouTube Video Downloader - Hacker Edition\n")

# Run the application
root.mainloop()