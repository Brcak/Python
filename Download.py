import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from ttkbootstrap import Style
from yt_dlp import YoutubeDL
import os
import time
import threading

# Global variables
stop_download = False
download_thread = None

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

# Function to update the progress bar
def update_progress(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str'].strip()
        progress_bar['value'] = float(percent[:-1])
        progress_label.config(text=f"Downloading: {percent}")
        root.update_idletasks()

# Function to download videos
def download_videos():
    global stop_download, download_thread

    download_folder = filedialog.askdirectory()
    if not download_folder:
        return

    stop_download = False
    download_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': True,
        'progress_hooks': [update_progress],
    }

    def download_task():
        for link in link_listbox.get(0, tk.END):
            if stop_download:
                break
            try:
                hacker_effect(log_text, f"Downloading: {link}...\n")
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                hacker_effect(log_text, f"Downloaded: {link}\n")
                with open("downloaded_videos.txt", "a") as f:
                    f.write(f"{link}\n")
                time.sleep(2)  # Delay between downloads
            except Exception as e:
                hacker_effect(log_text, f"Error downloading {link}: {str(e)}\n")
        download_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        progress_bar['value'] = 0
        progress_label.config(text="Download Complete")

    download_thread = threading.Thread(target=download_task)
    download_thread.start()

# Function to stop the current download
def stop_downloads():
    global stop_download
    stop_download = True
    hacker_effect(log_text, "Download stopped by user.\n")
    stop_button.config(state=tk.DISABLED)

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

stop_button = tk.Button(button_frame, text="Stop Download", command=stop_downloads, bg="black", fg="red", font=("Courier", 12), state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

# Progress Bar
progress_frame = tk.Frame(main_frame)
progress_frame.pack(pady=10)

progress_label = tk.Label(progress_frame, text="Download Progress", bg="black", fg="green", font=("Courier", 12))
progress_label.pack()

progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=700, mode='determinate')
progress_bar.pack()

# Log Text Area
log_text = scrolledtext.ScrolledText(main_frame, width=100, height=20, bg="black", fg="green", font=("Courier", 12))
log_text.pack(pady=10)

# Initial Message
hacker_effect(log_text, "Welcome to YouTube Video Downloader - Hacker Edition\n")

# Run the application
root.mainloop()
