from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS
from AlemMuzik import app
from AlemMuzik.core.call import Alem
from AlemMuzik.utils.database import is_music_playing, music_off
from AlemMuzik.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["pause", "dur"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await Alem.pause_stream(chat_id)

    buttons = [
        [
            InlineKeyboardButton(
                text="Devam", callback_data=f"ADMIN Resume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="Yinele", callback_data=f"ADMIN Replay|{chat_id}"
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

Bu Modül Yöneticilerin Grupta Müziği Duraklatmalarını Sağlar.

Commands:
- /pause: Oynatılan Müziği Duraklatır.
- /dur: Oynatılan Müziği Duraklatır.

Note:
- Komutları Sadece Yöneticiler Kullanabilir.
"""
