from pyrogram import filters
from pyrogram.types import Message

from CHATNI import app
from CHATNI.core.call import GIRL

welcome = 20
close = 30


@app.on_message(filters.video_chat_started, group=welcome)
@app.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    await PRO.stop_stream_force(message.chat.id)
