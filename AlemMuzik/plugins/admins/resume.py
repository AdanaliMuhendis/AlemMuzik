from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS
from AlemMuzik import app
from AlemMuzik.core.call import Alem
from AlemMuzik.utils.database import is_music_playing, music_on
from AlemMuzik.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["resume", "devam"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Alem.resume_stream(chat_id)
    buttons_resume = [
        [
            InlineKeyboardButton(text="Atla", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="Son", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="Dur",
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

Bu Modül Duraklatılmış Parçanın Tekrar Oynatılmasına Olanak Tanır.

Commands:
- /resume: Duraklatılmış parçanın Yeniden Oynatılmasını Sağlar.
- /devam: Duraklatılmış parçanın Yeniden Oynatılmasını Sağlar.

Note:
- Komutları Sadece Yöneticiler Kullanabilir.
"""
