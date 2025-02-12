import time
import random
from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch
from CHATNI import app

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import config
# from CHATNI import app
from CHATNI.misc import _boot_
from CHATNI.plugins.sudo.sudoers import sudoers_list
from CHATNI.utils.database import get_served_chats, get_served_users, get_sudoers
from CHATNI.utils import bot_sys_stats
from CHATNI.utils.database import (
    add_served_chat_clone,
    add_served_user_clone,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from CHATNI.utils.decorators.language import LanguageStart
from CHATNI.utils.formatters import get_readable_time
from CHATNI.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS, OWNER_ID
from strings import get_string

from CHATNI.utils.database.clonedb import get_owner_id_from_db, get_cloned_support_chat, get_cloned_support_channel

#--------------------------

NEXI_VID = [
"https://telegra.ph/file/1a3c152717eb9d2e94dc2.mp4",
"https://graph.org/file/ba7699c28dab379b518ca.mp4",
"https://graph.org/file/83ebf52e8bbf138620de7.mp4",
"https://graph.org/file/82fd67aa56eb1b299e08d.mp4",
"https://graph.org/file/318eac81e3d4667edcb77.mp4",
"https://graph.org/file/7c1aa59649fbf3ab422da.mp4",
"https://graph.org/file/2a7f857f31b32766ac6fc.mp4",

]

YUMI_PICS = [
    "https://files.catbox.moe/4q7c4w.jpg",
    "https://files.catbox.moe/90z6sq.jpg",
    "https://files.catbox.moe/rdfi4z.jpg",
    "https://files.catbox.moe/6f9rgp.jpg",
    "https://files.catbox.moe/99wj12.jpg",
    "https://files.catbox.moe/ezpnd2.jpg",
    "https://files.catbox.moe/e7q55f.jpg",
    "https://files.catbox.moe/qyfsi7.jpg",
    "https://files.catbox.moe/kbke7s.jpg",
    "https://files.catbox.moe/7icvpu.jpg",
    "https://files.catbox.moe/4hd77z.jpg",
    "https://files.catbox.moe/yn7wje.jpg",
    "https://files.catbox.moe/kifsir.jpg",
    "https://files.catbox.moe/zi21kc.jpg",
    "https://files.catbox.moe/z0gh23.jpg",
    "https://files.catbox.moe/f2s4ws.jpg",
    "https://files.catbox.moe/26nzoq.jpg",
    "https://files.catbox.moe/fu6jk3.jpg",
]


@Client.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    a = await client.get_me()
    C_BOT_OWNER_ID = get_owner_id_from_db(a.id)

    #Cloned Bot Support Chat and channel
    C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(a.id)
    C_SUPPORT_CHAT = f"https://t.me/{C_BOT_SUPPORT_CHAT}"
    C_BOT_SUPPORT_CHANNEL = await get_cloned_support_channel(a.id)
    C_SUPPORT_CHANNEL = f"https://t.me/{C_BOT_SUPPORT_CHANNEL}"

    #new ------
    # await add_served_user_clone(message.from_user.id)
    bot_id = a.id
    await add_served_user_clone(message.from_user.id, bot_id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                random.choice(YUMI_PICS),
                caption=_["help_1"].format(C_SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)

            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, a.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=C_SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
    
    else:
        out = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{a.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["C_B_2"], user_id=C_BOT_OWNER_ID),
            InlineKeyboardButton(text=_["S_B_6"], url=C_SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper"),
        ],
    ]
        
        app_name = app.name
        app_link = f"https://t.me/{app.username}"

        # out = private_panel(_)
        await message.reply_photo(
            random.choice(YUMI_PICS),
            caption=_["c_start_2"].format(message.from_user.mention, a.mention, app_name, app_link, app_name, app_link, C_SUPPORT_CHANNEL, C_SUPPORT_CHAT),
            reply_markup=InlineKeyboardMarkup(out),
        )


@Client.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    a = await client.get_me()
    #Cloned Bot Support Chat and channel
    C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(a.id)
    C_SUPPORT_CHAT = f"https://t.me/{C_BOT_SUPPORT_CHAT}"
    C_BOT_SUPPORT_CHANNEL = await get_cloned_support_channel(a.id)
    C_SUPPORT_CHANNEL = f"https://t.me/{C_BOT_SUPPORT_CHANNEL}"
    # out = start_panel(_)
    out = [
                    [
                        InlineKeyboardButton(
                            text=_["S_B_1"], url=f"https://t.me/{a.username}?startgroup=true"
                        ),
                        InlineKeyboardButton(text=_["S_B_2"], url=C_SUPPORT_CHAT),
                    ],
                ]
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(YUMI_PICS),
        caption=_["start_1"].format(a.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    # return await add_served_chat_clone(message.chat.id)
    bot_id = a.id
    return await add_served_chat_clone(message.chat.id, bot_id)
