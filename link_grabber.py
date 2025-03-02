import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os

def grab_youtube_links(channel_url):
    """Grabs video links from the given YouTube channel URL."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        video_links = []

        if 'entries' in result:
            for entry in result['entries']:
                video_links.append(entry['url'])

    return video_links

def save_links_to_txt(links, filename="video_links.txt"):
    """Saves the video links to a text file in a specified directory."""
    # Get the current working directory (the folder where the script is run)
    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, filename)  # Save the file in the same folder as the script
    
    with open(filepath, 'w') as f:
        for link in links:
            f.write(link + "\n")
    
    return filepath

def on_grab_button_click():
    """Handles the button click event to grab the video links."""
    channel_url = url_entry.get()

    if not channel_url:
        messagebox.showerror("Error", "Please enter a valid YouTube channel URL.")
        return

    try:
        video_links = grab_youtube_links(channel_url)
        
        if video_links:
            filepath = save_links_to_txt(video_links)
            messagebox.showinfo("Success", f"Found {len(video_links)} video links and saved them to {filepath}.")
        else:
            messagebox.showwarning("No Videos", "No videos found on this channel.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("YouTube Video Link Grabber")

# URL input field
url_label = tk.Label(root, text="Enter YouTube Channel URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Grab button
grab_button = tk.Button(root, text="Grab Video Links", command=on_grab_button_click)
grab_button.pack(pady=20)

# Run the GUI
root.mainloop()
