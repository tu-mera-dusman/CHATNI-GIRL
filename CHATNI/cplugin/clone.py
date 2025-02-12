import time
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from CHATNI import app
from config import PING_IMG_URL
from .utils import StartTime
from CHATNI.utils import get_readable_time
from CHATNI.utils.decorators.language import language

APP_LINK = f"https://t.me/{app.username}"


@Client.on_message(filters.command("clone"))
@language
async def ping_clone(client: Client, message: Message, _):
    bot = await client.get_me()


    hmm = await message.reply_photo(
        photo=PING_IMG_URL, caption=_["NO_CLONE_MSG"],
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ɢᴏ ᴀɴᴅ ᴄʟᴏɴᴇ", url=APP_LINK)]
            ]
        )
    )
