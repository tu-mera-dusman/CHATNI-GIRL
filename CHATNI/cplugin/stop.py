from pyrogram import filters, Client
from pyrogram.types import Message

from CHATNI import app
from CHATNI.core.call import GIRL
from CHATNI.utils.database import set_loop
from CHATNI.utils.decorators import AdminRightsCheck
from CHATNI.utils.inline import close_markup
from config import BANNED_USERS


@Client.on_message(
    filters.command(
        ["end", "stop", "cend", "cstop"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await GIRL.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
