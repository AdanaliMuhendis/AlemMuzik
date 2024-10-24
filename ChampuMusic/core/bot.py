import uvloop

uvloop.install()

import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config

from ..logging import LOGGER


class ChampuBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"𝙰𝙻𝙴𝙼 𝙼𝚄̈𝚉𝙸̇𝙺 𝙱𝙰𝚂̧𝙻𝙸𝚈𝙾𝚁...")
        super().__init__(
            "ChampuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )
    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        # Create the button
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # Try to send a message to the logger group
        if config.LOGGER_ID:
            try:
                await self.send_photo(
                    config.LOGGER_ID,
                    photo=config.START_IMG_URL,
                    caption=f"╔════❰𝐇𝐎𝐒̧𝐆𝐄𝐋𝐃𝐈̇𝐍𝐈̇𝐙❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝙰𝙻𝙴𝙼 𝙼𝚄̈𝚉𝙸̇𝙺 𝙱𝙰𝚂̧𝙻𝙰𝙳𝙸🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈ɪᴅ:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖Keyifli Dinlemeler...😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).error(f"Bot cannot write to the log group: {e}")
                try:
                    await self.send_message(
                        config.LOGGER_ID,
                        f"╔═══❰𝐇𝐎𝐒̧𝐆𝐄𝐋𝐃𝐈̇𝐍𝐈̇𝐙❱═══❍⊱❁۪۪\n║\n║┣⪼🥀𝙰𝙻𝙴𝙼 𝙼𝚄̈𝚉𝙸̇𝙺 𝙱𝙰𝚂̧𝙻𝙰𝙳𝙸🎉\n║\n║◈ {self.name}\n║\n║┣⪼🎈ɪᴅ:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖Keyifli Dinlemeler...😍\n║\n╚══════════════❍⊱❁",
                        reply_markup=button,
                    )
                except Exception as e:
                    LOGGER(__name__).error(f"Failed to send message in log group: {e}")
            except Exception as e:
                LOGGER(__name__).error(
                    f"Unexpected error while sending to log group: {e}"
                )
        else:
            LOGGER(__name__).warning(
                "LOGGER_ID is not set, skipping log group notifications."
            )

        # Setting commands
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("help", "ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ"),
                        BotCommand("ping", "ᴄʜᴇᴄᴋ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "oynat", "Start playing requested song"),
                        BotCommand("stop", "son", "Stop the current song"),
                        BotCommand("pause", "dur", "Pause the current song"),
                        BotCommand("resume", "devam", "Resume the paused song"),
                        BotCommand("queue", "Check the queue of songs"),
                        BotCommand("skip", "atla", "Skip the current song"),
                        BotCommand("volume", "Adjust the music volume"),
                        BotCommand("lyrics", "Get lyrics of the song"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "❥ ✨ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ✨"),
                        BotCommand("ping", "❥ 🍁ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘɪɴɢ🍁"),
                        BotCommand("help", "❥ 🥺ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ🥺"),
                        BotCommand("vctag", "❥ 😇ᴛᴀɢᴀʟʟ ғᴏʀ ᴠᴄ🙈"),
                        BotCommand("stopvctag", "❥ 📍sᴛᴏᴘ ᴛᴀɢᴀʟʟ ғᴏʀ ᴠᴄ 💢"),
                        BotCommand("tagall", "❥ 🔻ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ʙʏ ᴛᴇxᴛ🔻"),
                        BotCommand("cancel", "❥ 🔻ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴛᴀɢɢɪɴɢ🔻"),
                        BotCommand("settings", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴛʜᴇ sᴇᴛᴛɪɴɢs🔻"),
                        BotCommand("reload", "❥ 🪐ᴛᴏ ʀᴇʟᴏᴀᴅ ᴛʜᴇ ʙᴏᴛ🪐"),
                        BotCommand("play", "oynat", "❥ ❣️ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ sᴏɴɢ❣️"),
                        BotCommand("vplay", "❥ ❣️ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ ᴍᴜsɪᴄ ᴡɪᴛʜ ᴠɪᴅᴇᴏ❣️"),
                        BotCommand("pause", "dur", "❥ 🥀ᴛᴏ ᴘᴀᴜsᴇ ᴛʜᴇ sᴏɴɢs🥀"),
                        BotCommand("resume", "devam", "❥ 💖ᴛᴏ ʀᴇsᴜᴍᴇ ᴛʜᴇ sᴏɴɢ💖"),
                        BotCommand("end", "son", "❥ 🐚ᴛᴏ ᴇᴍᴘᴛʏ ᴛʜᴇ ϙᴜᴇᴜᴇ🐚"),
                        BotCommand("queue", "❥ 🤨ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ϙᴜᴇᴜᴇ🤨"),
                        BotCommand("playlist", "❥ 🕺ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ🕺"),
                        BotCommand("stop", "dur", "❥ ❤‍🔥ᴛᴏ sᴛᴏᴘ ᴛʜᴇ sᴏɴɢs❤‍🔥"),
                        BotCommand("lyrics", "❥ 🕊️ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟʏʀɪᴄs🕊️"),
                        BotCommand("song", "bul", "music", "❥ 🔸ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ sᴏɴɢ🔸"),
                        BotCommand("video", "❥ 🔸ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴠɪᴅᴇᴏ sᴏɴɢ🔸"),
                        BotCommand("gali", "❥ 🔻ᴛᴏ ʀᴇᴘʟʏ ғᴏʀ ғᴜɴ🔻"),
                        BotCommand("shayri", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴀ sʜᴀʏᴀʀɪ🔻"),
                        BotCommand("love", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴀ ʟᴏᴠᴇ sʜᴀʏᴀʀɪ🔻"),
                        BotCommand("sudolist", "❥ 🌱ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ sᴜᴅᴏʟɪsᴛ🌱"),
                        BotCommand("owner", "❥ 💝ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴏᴡɴᴇʀ💝"),
                        BotCommand("update", "❥ 🐲ᴛᴏ ᴜᴘᴅᴀᴛᴇ ʙᴏᴛ🐲"),
                        BotCommand("gstats", "❥ 💘ᴛᴏ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ💘"),
                        BotCommand("repo", "❥ 🍌ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ 𝚁𝙴𝙿𝙾🍌"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")

        # Check if bot is an admin in the logger group
        if config.LOGGER_ID:
            try:
                chat_member_info = await self.get_chat_member(
                    config.LOGGER_ID, self.id
                )
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error(
                        "𝙻𝚞̈𝚝𝚏𝚎𝚗 𝙱𝚘𝚝𝚞𝚗 𝙲̧𝚊𝚕ı𝚜̧𝚖𝚊𝚜ı 𝙸̇𝚌̧𝚒𝚗 𝚈𝚎𝚝𝚔𝚒 𝚅𝚎𝚛𝚒𝚗..."
                    )
            except Exception as e:
                LOGGER(__name__).error(f"Error occurred while checking bot status: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
