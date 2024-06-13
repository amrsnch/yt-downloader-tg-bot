# Generic messages (might actually put them into a separate class and call them from there as it was taught in FIT2099
class InfoMessages:

    HELP_MSG = 'Just a help info for now...'

    WELCOME_MSG = """\
    Hi there! I am Downloader test bot, Dev version.
    Just a kind words of greetings before we start testing!\
    """

class ErrorMessages:
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