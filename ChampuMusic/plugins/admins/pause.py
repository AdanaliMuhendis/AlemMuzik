from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS
from ChampuMusic import app
from ChampuMusic.core.call import Champu
from ChampuMusic.utils.database import is_music_playing, music_off
from ChampuMusic.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["pause", "dur", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await Champu.pause_stream(chat_id)

    buttons = [
        [
            InlineKeyboardButton(
                text="𝙳𝙴𝚅𝙰𝙼", callback_data=f"ADMIN Resume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="𝚃𝙴𝙺𝚁𝙰𝚁 𝙾𝚈𝙽𝙰𝚃", callback_data=f"ADMIN Replay|{chat_id}"
            ),
        ],
    ]

    await message.reply_text(
        _["admin_2"].format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


__MODULE__ = "Pause"
__HELP__ = """
**Pause Music**

This module allows administrators to pause the music playback in the group.

Commands:
- <b>✧ /pause</b> ᴏʀ <b>/dur</b> - Mevcut oynatma akışını duraklatır.
- /cpause: Kanalda Mevcut oynatma akışını duraklatır.

Note:
- Only administrators can use these commands.
"""
