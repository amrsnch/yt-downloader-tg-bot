import os
import telebot
import downloader_script as ds
import configobj
from info_messages import *

# TODO:
# 1. Integration with Selenium to be able to download age restricted videos (for music lol)
# 2. Figure out cloud hosting option.
# 3. Ask people if they want to have an option to download video itself, not just audio.


# extracting api key from .env file
config = configobj.ConfigObj('.env')
API_KEY = config['API_KEY']

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Function description: Sends welcome message upon "/start" command.
    Approach description:
    """
    bot.reply_to(message, InfoMessages.WELCOME_MSG)


@bot.message_handler(commands=['help'])
def send_help_message(message):
    """
    Function description: Sends message with guide and instructions upon "/help" command.
    Approach description:
    """
    bot.send_message(message.chat.id, InfoMessages.HELP_MSG)


def get_file_size(file_path):
    """
    Function gets files size in megabytes and further we check if the
    fits withing the Telegram's file size limit.
    """

    return os.path.getsize(file_path) / (1024 * 1024) # in megabytes

# Handle '/download' command
@bot.message_handler(commands=['download'])
def start_download(message):
    """
    Function description: This function responds to the "/download" command and prompts
    the user to send a YouTube video URL.

    Input:
        message: text message containing the "/download" command
    Output: None
    """
    bot.send_message(message.chat.id, "Please send the YouTube video URL you want to download")

    # awaits for the message after
    bot.register_next_step_handler(message, download_audio)


def download_audio(message):
    """
    Function description: This function responds to "/download" command and triggers get_audio_only()
    function from ./downloader_script.py and sends converted mp3 file in Telegram chat.

    Note: Telegram bot file limit is 10 - 20 MB.
    Approach description:

    Input:
        message: text message in form: "/download {youtube_video_url}"
    Output: None
    """
    try:
        # split input text (i.e "/download {youtube_video_url}")
        video_url = message.text

        # convert video and get file name
        file_name = ds.get_audio_only(video_url, "./assets")
        print(str(file_name))

        audio_path = f'./assets/{file_name}'

        if get_file_size(audio_path) > 50.0:
            bot.send_message(message.chat.id, ErrorMessages.SIZE_ERROR_MSG)
        else:

            # open audio with appropriate encoding
            audio_file = open(audio_path, 'rb')

            # send output file to user
            bot.send_audio(chat_id=message.chat.id, audio=audio_file)

    except Exception as e:
        if "age" in str(e):
            bot.send_message(message.chat.id, ErrorMessages.AGE_ERROR_MSG)
        else:
            bot.send_message(message.chat.id, ErrorMessages.GENERAL_ERROR_MSG)


@bot.message_handler(commands=['download'])
def start_playlist_download(message):
    """
    Function description: This function responds to the "/download" command and prompts
    the user to send a YouTube video URL.

    Input:
        message: text message containing the "/download" command
    Output: None
    """
    bot.send_message(message.chat.id, "Please send the YouTube playlist URL you want to download")

    # awaits for the message after
    bot.register_next_step_handler(message, download_playlist)


@bot.message_handler(commands=['playlist'])
def download_playlist(message):
    """
    Function description: This function downloads an entire playlist
    provided by user and sends back audi of each track


    Just a thought: Maybe I should use queue ADT from FIT1008...? Might actually work
    Approach description:

    Input:
        message: text message in form: "/download {youtube_playlist_url}"
    Output:
    """

    playlist_url = message.text
    ds.get_playlist_audio(playlist_url, "./downloaded")


bot.polling(none_stop=True)
