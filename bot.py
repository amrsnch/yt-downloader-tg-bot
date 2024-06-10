import os

import telebot
import downloader_script as ds
import configobj

# TODO:
# 1. Add telegram "hinting" for commands
# 2. Exception and error handling (иначе всё нахуй упадет на облаке/сервакe)
# 3. Integration with Selenium to be able to download age restricted videos (for music lol)
# 4. Figure out cloud hosting option.
# 5. Ask people if they want to have an option to download video itself, not just audio.


# extracting api key from .env file
config = configobj.ConfigObj('.env')
API_KEY = config['API_KEY']

bot = telebot.TeleBot(API_KEY)

# Generic messages

HELP_MSG = 'Just a help info for now...'

WELCOME_MSG = """\
Hi there! I am Downloader test bot, Dev version.
Just a kind words of greetings before we start testing!\
"""

AGE_ERROR_MSG = """\
Video that you're trying to converted is age restricted and
can't be downloaded at the moment (we're working very hard to resolve this issue)
\
"""

# potentailly I can return a link which leads to a downloaded file on server or increase allowed file size
# by using a loophole with local server.
SIZE_ERROR_MSG = """\
The size of the audio is more than that Telegram can handle (20MB), please choose shorter track.
\
"""

GENERAL_ERROR_MSG = """\
Unexpected error has occurred, please resubmit your request.
\
"""


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Function description: Sends welcome message upon "\start" command.
    Approach description:
    """
    bot.reply_to(message, WELCOME_MSG)


@bot.message_handler(commands=['help'])
def send_help_message(message):
    """
    Function description: Sends message with guide and instructions upon "\help" command.
    Approach description:
    """
    bot.send_message(message.chat.id, HELP_MSG)


def check_file_size(file_path):
    # in megabytes
    return os.path.getsize(file_path) / (1024 * 1024)


# Handle '/download' command
@bot.message_handler(commands=['download'])
def download_audio(message):
    """
    Function description: This function responds to "\downlaad" command and triggers get_audio_only()
    function from ./downloader_script.py and sends converted mp3 file in Telegram chat.

    Approach description:  ...

    Input:
        message: text message in form: "/download {youtube_video_url}"
    Output: None
    """

    try:
        # split input text (i.e "/download {youtube_video_url}")
        video_url = message.text.split()[1]

        # convert video and get file name
        file_name = ds.get_audio_only(video_url, "./downloaded")
        print(str(file_name))

        audio_path = f'./downloaded/{file_name}'

        # FIX THIS PART!!!
        if check_file_size(audio_path) > 50.0:
            bot.send_message(message.chat.id, SIZE_ERROR_MSG)
        else:
            # audio_path = f'./downloaded/{file_name}'
            # bot.send_audio(chat_id=message.chat.id ,audio=open(f'./downloaded/{file_name}', encoding='cp850'))

            # open audio with appropriate encoding
            audio_file = open(audio_path, 'rb')

            # send output file to user
            bot.send_audio(chat_id=message.chat.id, audio=audio_file)

    except Exception as e:
        if "age" in str(e):
            bot.send_message(message.chat.id, str(e))
            bot.send_message(message.chat.id, AGE_ERROR_MSG)
        else:
            bot.send_message(message.chat.id, GENERAL_ERROR_MSG)

    # seems like script crashes when I have something like this:
    # "𝕋𝕙𝕖 𝕃𝕠𝕤𝕥 𝕊𝕠𝕦𝕝 𝔻𝕠𝕨𝕟 𝕩 𝕃𝕠𝕤𝕥 𝕊𝕠𝕦𝕝 - ℕ𝔹𝕊ℙ𝕃𝕍 [ ℂ𝕙𝕒𝕚𝕟𝕤𝕒𝕨 𝕄𝕒𝕟 𝔾𝕚𝕣𝕝𝕤 // 𝟙 ℍ𝕠𝕦𝕣 ℂ𝕝𝕖𝕒𝕟 𝕃𝕠𝕠𝕡 ]"
    # I need to find a way to convert it to regular string without fancy bs. Oh wait, nvm.
    # Seems like vid itself is 1 hour long
    # Other thing I have to consider is deleting video when it failed to send it via telegramg. That makes sense.
    # Telegram bot file limit is 10 MB.


@bot.message_handler(commands=['playlist'])
def download_playlist(message):
    """
    Function description: This function downloads an entire playlist
    provided by user and sends back audi of each track

    Approach description:

    Input:
        message: text message in form: "/download {youtube_playlist_url}"
    Output:
    """
    playlist_url = message.text.split()[1]
    ds.get_playlist_audio(playlist_url, "./downloaded")


bot.polling(none_stop=True)
