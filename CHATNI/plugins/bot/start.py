import time
import random
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from CHATNI import app
from CHATNI.misc import _boot_
from CHATNI.plugins.sudo.sudoers import sudoers_list
from CHATNI.utils.database import get_served_chats, get_served_users, get_sudoers
from CHATNI.utils import bot_sys_stats
from CHATNI.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from CHATNI.utils.decorators.language import LanguageStart
from CHATNI.utils.formatters import get_readable_time
from CHATNI.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

TANYA = [
    "https://files.catbox.moe/jrupn9.jpg",
    "https://files.catbox.moe/5z141p.jpg",
    "https://files.catbox.moe/fnl0h7.jpg",
    "https://files.catbox.moe/1lz1go.jpg",
    "https://files.catbox.moe/avackl.jpg",
    "https://files.catbox.moe/1yrzwz.jpg",
    "https://files.catbox.moe/6y22qw.jpg",
    "https://files.catbox.moe/gnnsf2.jpg",
    "https://files.catbox.moe/ss6r60.jpg",
    "https://files.catbox.moe/yuob18.jpg",
    "https://files.catbox.moe/i9xrrp.jpg",
    "https://files.catbox.moe/a9tx8f.jpg"
    "https://files.catbox.moe/wlt26x.jpg",
    "https://files.catbox.moe/c1lylh.jpg",
    "https://files.catbox.moe/82eymp.jpg",
]

CHATNI_GIRL = [
    "CAACAgUAAxkBAAEBYw5m7G9P80t1_j2B3Yd92giEZl5pUAACDQsAAu5MeVcOK7bEmdSlUB4E",
    "CAACAgUAAxkBAAEBYwxm7G9LVcg14qUcZZA3UW_DD8b5EwACpwsAAo1FeFfhiv4M5X_-sR4E",
    "CAACAgUAAxkBAAEBYwdm7G9B0AQOHXTL2YqQPS_1v9aoKwACGw0AAu3GeVeciSOmGXW1Mx4E",
    "CAACAgUAAxkBAAEBYw9m7G9UNbKd5uykZTX8lZ4Cr8LAzAACrQsAAovseFe_Dx9-6uc6Ux4E",
    "CAACAgUAAxkBAAEBYwpm7G9GSePQOKa6J19IJmN4aQdd6wAC-QoAAmpLeFeIwvGei64Sph4E",
    "CAACAgUAAxkBAAEBYwlm7G9F_WH00zaCrHCrOE0hPNVwzgACGAwAAgLieFfTOC4m1R4KvR4E",
    "CAACAgUAAxkBAAEBYyBm7G-lKV7aHgEF3nJFkAfn56C6cwACgAkAArWleFcq3_E-UPFIzh4E",
    "CAACAgUAAxkBAAEBYw1m7G9NGhPaRs7LQ1qNjukWtqleMgAC9QkAAqeOeFeHI7lMCMruQR4E",
    "CAACAgUAAxkBAAEBYwhm7G9C5a3pRXGlnxmd-bPpk6wPTgACKwoAAqDYeVd8I_IUW4LCkx4E",
    "CAACAgUAAxkBAAEBYyFm7G-rzbXl2VpA37MJevvoJ3712QACbQoAAktbeFfdKoQ_a4J2PR4E",
    "CAACAgUAAxkBAAEBYyJm7G-9KCjUg2MsRKZVTpR_aqn9lwACYA4AAqTycVdmzhfCS8nEPx4E",
    "CAACAgUAAxkBAAEBYyNm7G_FwL1o8EbUs4wtYlMwIxAgCAACDQwAAncPeVe97cDgXeKF4B4E",
]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_sticker(
            random.choice(CHATNI_GIRL),)
            return await message.reply_photo(
                random.choice(TANYA),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"✦ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
                )
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
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(

chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"✦ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_sticker(
        random.choice(CHATNI_GIRL),)
        await message.reply_photo(
            random.choice(TANYA),
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM,served_users,served_chats),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"✦ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_sticker(
    random.choice(CHATNI_GIRL),)
    await message.reply_photo(
        random.choice(TANYA),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_sticker(
                random.choice(CHATNI_GIRL),)
                await message.reply_photo(
                    random.choice(TANYA),
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
