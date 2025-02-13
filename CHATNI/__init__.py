from .logging import LOGGER
from CHATNI.core.dir import dirr
from CHATNI.core.git import git
from CHATNI.misc import dbb, heroku

# Initialize these first
LOGGER(__name__).info("Initializing core modules...")
dirr()
git()
dbb()
heroku()

# Now import bot and other modules
from CHATNI.core.bot import GIRL
from CHATNI.core.userbot import Userbot
from SafoneAPI import SafoneAPI

# Initialize bot and APIs
app = GIRL()
api = SafoneAPI()
userbot = Userbot()

from .platforms import *

# API Instances
Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
