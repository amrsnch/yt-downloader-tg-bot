from pytube import *
from moviepy.editor import *
import os
import subprocess

# TODO: 1. Let user choose a directory where they want to save a file. (Done)
#       2. Add a dropdown to select a video quality. (irrelevant here, no Tkinter used)
#       3. Adapt scripts for particular functions. (irrelevant here, no Tkinter used)
#       4. Redesign and colouring. (irrelevant here, no Tkinter used)

file_name_str = ""


def get_playlist_video(link, file_path):
    """Allows to download entire playlist in the highest quality """
    p = Playlist(link)
    print(f"Downloading {p.title} playlist")
    for video in p.videos:
        stream = video.streams.filter(progressive=True).get_highest_resolution()
        stream.download(file_path)


# def convert_to_audio(title, file_path):
#     # getting rid of the "lost" symbols (apparently got fixed in later PyTube releases),at least "!"(exclamation mark)
#     symbols_to_delete = [",", ";", "$", ":", "/", "."]
#     filename = "".join([i for i in title if i not in symbols_to_delete])
#
#     # conversion to mp3
#     mp4_file = os.path.join(file_path, f"{filename}.mp4")
#     mp3_file = os.path.join(file_path, f"{filename}.mp3")
#     file_name_str = f"{filename}.mp3"
#
#     video_clip = VideoFileClip(mp4_file)
#     audio_clip = video_clip.audio
#
#     audio_clip.write_audiofile(mp3_file)
#     audio_clip.close()
#     video_clip.close()
#     # deleting a video fragment for audio only, later will be included to a separate function
#     os.remove(os.path.join(file_path, f"{filename}.mp4"))
#
#     return file_name_str


def convert_to_audio_modified(title, file_path):

    """
    Identical to the code above, however utilises ffmpeg for conversion. Might be troublesome if
    you plan to deploy it on cloud premises. But might worth a try
    """
    symbols_to_delete = [",", ";", "$", ":", "/", "."]
    filename = "".join([i for i in title if i not in symbols_to_delete])

    mp4_file = os.path.join(file_path, f"{title}.mp4")
    mp3_file = os.path.join(file_path, f"{title}.mp3")

    file_video_str = f"{title}.mp4"
    file_audio_str = f"{title}.mp3"

    subprocess.run([
        'ffmpeg',
        '-i', mp4_file,
        mp3_file
        ])

    return file_audio_str


def get_audio_only(link, file_path):
    """
    This function allows to download and extract an audio track of a particular YouTube video
    """
    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    # print(yt.streams.filter(file_extension='mp4').first())  # idk what it does but let it hang there for a while
    stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
    stream.download(file_path)

    # Bug-tracking part, according to observation script crashes because of the absence of "."(dot) symbol after the
    # download therefore we are getting "STALKER  2  Heart of Chernobyl Official Trailer.mp4" instead of
    # "S.T.A.L.K.E.R  2  Heart of Chernobyl Official Trailer.mp4" and "BoyWithUke  - Sick of U (Lyrics) ft Oliver
    # Tree.mp4" instead of "BoyWithUke  - Sick of U (Lyrics) ft. Oliver Tree.mp4"

    # with os.scandir('D:\YTLoaderTest') as entries:
    #     for entry in entries:
    #         print(entry.name)
    #         print(f'{stream.title}.mp4')
    #         if entry == (yt.title+'.mp4'):
    #             print("IT'S LITERALLY HERE, WTF IS WRONG")

    return convert_to_audio_modified(stream.title, file_path)


def get_playlist_audio(link, file_path):
    p = Playlist(link)
    for track in p.videos:
        print(track.embed_url)
        track_file = track.streams.filter(progressive=True).get_lowest_resolution()
        track_file.download(file_path)
        convert_to_audio_modified(track_file.title, file_path)


def get_resolutions(link):
    """
    This function gets all possible resolutions of a given video, used in regular video download (without conversion)
    """
    yt = YouTube(link)
    filter_stream_list = yt.streams.filter(file_extension='mp4', only_audio=False, type="video")
    resolutions_set = set()
    for stream in filter_stream_list:
        resolutions_set.add(stream.resolution)

    print(resolutions_set)
