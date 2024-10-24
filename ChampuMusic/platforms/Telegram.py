 
import asyncio
import os
import time
from datetime import datetime, timedelta
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Voice

import config
from config import lyrical
from ChampuMusic import app

from ..utils.formatters import convert_bytes, get_readable_time, seconds_to_min

downloader = {}


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = config.TELEGRAM_DOWNLOAD_EDIT_SLEEP

    async def send_split_text(self, message, string):
        n = self.chars_limit
        out = [(string[i : i + n]) for i in range(0, len(string), n)]
        j = 0
        for x in out:
            if j <= 2:
                j += 1
                await message.reply_text(x)
        return True

    async def get_link(self, message):
        if message.chat.username:
            link = f"https://t.me/{message.chat.username}/{message.reply_to_message.id}"
        else:
            xf = str((message.chat.id))[4:]
            link = f"https://t.me/c/{xf}/{message.reply_to_message.id}"
        return link

    async def get_filename(self, file, audio: Union[bool, str] = None):
        try:
            file_name = file.file_name
            if file_name is None:
                file_name = "𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝚂𝙴𝚂 𝙳𝙾𝚂𝚈𝙰𝚂𝙸" if audio else "𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝚅𝙸̇𝙳𝙴𝙾 𝙳𝙾𝚂𝚈𝙰𝚂𝙸"

        except:
            file_name = "𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝚂𝙴𝚂 𝙳𝙾𝚂𝚈𝙰𝚂𝙸" if audio else "𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝚅𝙸̇𝙳𝙴𝙾 𝙳𝙾𝚂𝚈𝙰𝚂𝙸"
        return file_name

    async def get_duration(self, file):
        try:
            dur = seconds_to_min(file.duration)
        except:
            dur = "Unknown"
        return dur

    async def get_filepath(
        self,
        audio: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ):
        if audio:
            try:
                file_name = (
                    audio.file_unique_id
                    + "."
                    + (
                        (audio.file_name.split(".")[-1])
                        if (not isinstance(audio, Voice))
                        else "ogg"
                    )
                )
            except:
                file_name = audio.file_unique_id + "." + ".ogg"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        if video:
            try:
                file_name = (
                    video.file_unique_id + "." + (video.file_name.split(".")[-1])
                )
            except:
                file_name = video.file_unique_id + "." + "mp4"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        return file_name

    async def download(self, _, message, mystic, fname):
        left_time = {}
        speed_counter = {}
        if os.path.exists(fname):
            return True

        async def down_load():
            async def progress(current, total):
                if current == total:
                    return
                current_time = time.time()
                start_time = speed_counter.get(message.id)
                check_time = current_time - start_time
                upl = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🚦 𝙸̇𝙽𝙳𝙸̇𝚁𝙼𝙴 𝙸̇𝙿𝚃𝙰𝙻 𝙴𝙳𝙸̇𝙻𝙸̇𝚈𝙾𝚁",
                                callback_data="stop_downloading",
                            ),
                        ]
                    ]
                )
                if datetime.now() > left_time.get(message.id):
                    percentage = current * 100 / total
                    percentage = str(round(percentage, 2))
                    speed = current / check_time
                    eta = int((total - current) / speed)
                    downloader[message.id] = eta
                    eta = get_readable_time(eta)
                    if not eta:
                        eta = "0 sec"
                    total_size = convert_bytes(total)
                    completed_size = convert_bytes(current)
                    speed = convert_bytes(speed)
                    text = f"""
**{app.mention} 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝙼𝙴𝙳𝚈𝙰 𝙸̇𝙽𝙳𝙸̇𝚁𝙼𝙴 𝙰𝚁𝙰𝙲𝙸**

**𝚃𝙾𝙿𝙻𝙰𝙼 𝙳𝙾𝚂𝚈𝙰 𝙱𝙾𝚈𝚄𝚃𝚄:** {total_size}
**𝚃𝙰𝙼𝙰𝙼𝙻𝙰𝙽𝙼𝙸𝚂̧:** {completed_size} 
**𝚈𝚄̈𝚉𝙳𝙴:** {percentage[:5]}%

**𝙷𝙸𝚉:** {speed}/s
**𝙶𝙴𝙲̧𝙴𝙽 𝚂𝚄̈𝚁𝙴:** {eta}"""
                    try:
                        await mystic.edit_text(text, reply_markup=upl)
                    except:
                        pass
                    left_time[message.id] = datetime.now() + timedelta(
                        seconds=self.sleep
                    )

            speed_counter[message.id] = time.time()
            left_time[message.id] = datetime.now()

            try:
                await app.download_media(
                    message.reply_to_message,
                    file_name=fname,
                    progress=progress,
                )
                await mystic.edit_text(
                    "𝙱𝙰𝚂̧𝙰𝚁𝙸𝚈𝙻𝙰 𝙸̇𝙽𝙳𝙸̇𝚁𝙸̇𝙻𝙳𝙸̇...\n 𝚂̧𝙸̇𝙼𝙳𝙸̇ 𝙳𝙾𝚂𝚈𝙰 𝙸̇𝚂̧𝙻𝙴𝙽𝙸̇𝚈𝙾𝚁..."
                )
                downloader.pop(message.id)
            except:
                await mystic.edit_text(_["tg_2"])

        if len(downloader) > 10:
            timers = []
            for x in downloader:
                timers.append(downloader[x])
            try:
                low = min(timers)
                eta = get_readable_time(low)
            except:
                eta = "Unknown"
            await mystic.edit_text(_["tg_1"].format(eta))
            return False

        task = asyncio.create_task(down_load())
        lyrical[mystic.id] = task
        await task
        downloaded = downloader.get(message.id)
        if downloaded:
            downloader.pop(message.id)
            return False
        verify = lyrical.get(mystic.id)
        if not verify:
            return False
        lyrical.pop(mystic.id)
        return True
