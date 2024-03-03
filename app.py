import shutil
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import streamlit as st
from pytube import YouTube
import moviepy.editor as mp


# Function to empty a folder
def empty_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Function to download videos and extract audio
def download_and_extract_audio(video_url):
    folder_path = "videos"
    audio_path = "audios"



    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            # Empty the folders before downloading new files
        empty_folder(folder_path)

        stream.download(output_path=folder_path)
        st.write("Downloaded:", yt.title)
    except Exception as e:
        st.write("An error occurred:", str(e))

        # Extract audio
    vids = os.listdir(folder_path)
    auds = [vid[:-4] for vid in vids]

    clip = mp.VideoFileClip(f"{folder_path}/{vids[0]}")
    audio = clip.audio
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)
    empty_folder(audio_path)
    audio.write_audiofile(f"{audio_path}/{auds[0]}.mp3", codec='libmp3lame')

    return f"{audio_path}/{auds[0]}.mp3", yt.title






# Streamlit UI
st.title("MP3 Song Downloader")

video_url = st.text_input("Enter the link of youtube video song to download it in mp3")
if st.button("download song"):
    if video_url:

        st.write("Fetching song...")
        audio_path, title = download_and_extract_audio(video_url)
        if audio_path:
            try:
                with open(audio_path, "rb") as f:
                    bytes_data = f.read()
                st.download_button(label=f"Download {title}.mp3", data=bytes_data, file_name=f"{title}.mp3")
                st.success("Song Downloaded!")
            except Exception as e:
                st.error(f"Failed to download: {e}")
