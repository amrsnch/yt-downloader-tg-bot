import telebot
import downloader_script as ds
import configobj

#TODO:
# 1. Add telegram "hinting" for commands
# 2. Exception and error handling (иначе всё нахуй упадет на облаке)
# 3. Integration with Selenium to be able to download age restricted videos (for music lol)
# 4. Figure out cloud hosting option.
# 5. Ask people if they want to have an option to download video itself, not just audio.


# extracting api key from .env file
config = configobj.ConfigObj('.env')
API_KEY = config['API_KEY']

bot = telebot.TeleBot(API_KEY)
HELP = 'Just a help info for now...'

WELCOME_MSG = """\
Hi there! I am Downloader test bot, Dev version.
Just a kind words of greetings before we start testing!\
"""

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_MSG)


@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.send_message(message.chat.id, HELP)


#Handle '/download' command
@bot.message_handler(commands=['download'])
def download_audio(message):
    video_url = message.text.split()[1]
    file_name = ds.get_audio_only(video_url, "./downloaded")
    print(str(file_name))

    audio_path = f'./downloaded/{file_name}'
    # audio_path = f'./downloaded/{file_name}'
    # bot.send_audio(chat_id=message.chat.id ,audio=open(f'./downloaded/{file_name}', encoding='cp850'))
    audio_file = open(audio_path, 'rb')
    bot.send_audio(chat_id=message.chat.id, audio=audio_file)

    # seems like shit crashes when I have something like this:
    # "𝕋𝕙𝕖 𝕃𝕠𝕤𝕥 𝕊𝕠𝕦𝕝 𝔻𝕠𝕨𝕟 𝕩 𝕃𝕠𝕤𝕥 𝕊𝕠𝕦𝕝 - ℕ𝔹𝕊ℙ𝕃𝕍 [ ℂ𝕙𝕒𝕚𝕟𝕤𝕒𝕨 𝕄𝕒𝕟 𝔾𝕚𝕣𝕝𝕤 // 𝟙 ℍ𝕠𝕦𝕣 ℂ𝕝𝕖𝕒𝕟 𝕃𝕠𝕠𝕡 ]"
    # I need to find a way to convert it to regular string without fancy bs. Oh wait, nvm.
    # Seems like vid itself is 1 hour long
    # Other thing I gotta consider is deleting video when it failed to send it via tg. That makes sense.

@bot.message_handler(commands=['playlist'])
def download_playlist(message):
    pass


bot.polling(none_stop=True)
