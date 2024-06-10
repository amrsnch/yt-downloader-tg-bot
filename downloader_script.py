from pytube import *
from moviepy.editor import *
import os


# TODO: 1. Let user choose a directory where they want to save a file. (Done)
#       2. Add a dropdown to select a video quality. (irrelevant here, no Tkinter used)
#       3. Adapt scripts for particular functions. (irrelevant here, no Tkinter used)
#       4. Redesign and colouring. (irrelevant here, no Tkinter used)

def get_playlist_video(url, file_path):
    """
    Function description: Allows to download entire video playlist in the highest quality
    Approach:

    Input:
        link: playlist url
        file_path: directory where downloaded file will be stored

    Output:
        None
    """
    p = Playlist(url)
    print(f"Downloading {p.title} playlist")
    for video in p.videos:
        stream = video.streams.filter(progressive=True).get_highest_resolution()
        stream.download(file_path)


def convert_to_audio(title, file_path):
    """
    Function description: This function performs conversion of downloaded .mp4 video into .mp3 audio.

    Approach:

    Input:
        title: video title
        file_path: directory where downloaded file will be stored
    Output: .mp3 file name
    """

    # Getting rid of the "lost" symbols (apparently got fixed in later PyTube releases),at least "!"(exclamation mark)
    # in order for title input to match the file name of downloaded video
    symbols_to_delete = [",", ";", "$", ":", "/", "."]
    filename = "".join([i for i in title if i not in symbols_to_delete])

    # Create mp3 and mp4 files
    mp4_file = os.path.join(file_path, f"{filename}.mp4")
    mp3_file = os.path.join(file_path, f"{filename}.mp3")

    # Store mp3 file name separately for return statement
    file_name_str = f"{filename}.mp3"

    # Separate audio from video file
    video_clip = VideoFileClip(mp4_file)
    audio_clip = video_clip.audio

    # Write audio to a created earlier mp3 file
    audio_clip.write_audiofile(mp3_file)

    # Close all files as soon as transfer is done
    audio_clip.close()
    video_clip.close()

    # Deleting a video fragment for audio only, later will be included to a separate function
    os.remove(os.path.join(file_path, f"{filename}.mp4"))

    return file_name_str


def get_audio_only(url, file_path):
    """
    Function description: This function allows to download and extract an audio track of a particular YouTube video
    Approach:

    Input:
        link: video url
        file_path: directory where downloaded file will be stored
    """
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
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

    return convert_to_audio(stream.title, file_path)


def get_playlist_audio(url, file_path):
    """
    Function description:
    Approach:

    Input:
        link: playlist url
        file_path: directory where downloaded file will be stored

    Output:
    """
    p = Playlist(url)
    for track in p.videos:
        print(track.embed_url)
        track_file = track.streams.filter(progressive=True).get_lowest_resolution()
        track_file.download(file_path)
        convert_to_audio(track_file.title, file_path)


def get_resolutions(link):

    """
    Function description: This function extracts all possible resolutions of a given video
    Approach: We filter the streams and keep only ones with mp4 file extension, afterward we
    iterate through the resultant list and extract unique resolutions through set()

    Input:
        link: video url

    Output: None
    """
    yt = YouTube(link)
    filter_stream_list = yt.streams.filter(file_extension='mp4', only_audio=False, type="video")
    resolutions_set = set()
    for stream in filter_stream_list:
        resolutions_set.add(stream.resolution)

    print(resolutions_set)
