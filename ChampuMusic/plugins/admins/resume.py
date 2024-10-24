from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS
from ChampuMusic import app
from ChampuMusic.core.call import Champu
from ChampuMusic.utils.database import is_music_playing, music_on
from ChampuMusic.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["resume", "devam", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Champu.resume_stream(chat_id)
    buttons_resume = [
        [
            InlineKeyboardButton(text="𝙳𝙴𝚅𝙰𝙼", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="SON", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="DUR",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
        ],
    ]
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons_resume),
    )


__MODULE__ = "Resume"
__HELP__ = """
**Resume**

This module allows administrators to resume playback of the currently paused track.

Commands:
- <b>✧ /resume</b> ᴏʀ <b>/devam</b> - Duraklatılan akışı devam ettirir.
- /cresume: Kanalda duraklatılan akışı devam ettirir.

Note:
- Only administrators can use these commands.
"""
