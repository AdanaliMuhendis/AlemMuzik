from AlemMuzik.core.bot import AlemMuzikBot
from AlemMuzik.core.dir  dirr
from AlemMuzik.core.git import git
from AlemMuzik.core.userbot import Userbot
from AlemMuzik.misc import dbb, heroku, sudo

from .logging import LOGGER

dirr()

git()

dbb()

heroku()

sudo()

app = AlemMuzikBot()

userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}
