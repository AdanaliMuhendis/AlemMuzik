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


class AlemMuzikBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"𝙰𝙻𝙴𝙼 𝙼𝚄̈𝚉𝙸̇𝙺 𝙱𝙰𝚂̧𝙻𝙸𝚈𝙾𝚁...")
        super().__init__(
            "AlemMuzik",
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
                        text="๏ 𝙱𝚎𝚗𝚒 𝙶𝚛𝚞𝚋𝚞𝚗𝚊 𝙴𝚔𝚕𝚎 ๏",
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
                    caption=f"╔════❰𝐇𝐎𝐒̧𝐆𝐄𝐋𝐃𝐈̇𝐍𝐈̇𝐙❱════❍⊱❁۪۪\n║\n║┣⪼ Yαყıɳԃαყıɱ 🌈...\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈ɪᴅ:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼ тєşєkkürlєr\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).error(f"𝙻𝚞̈𝚝𝚏𝚎𝚗 𝙱𝚘𝚝𝚞 𝙻𝚘𝚐 𝙺𝚊𝚗𝚊𝚕ı𝚗𝚊 𝙴𝚔𝚕𝚎𝚢𝚒𝚗: {e}")
                try:
                    await self.send_message(
                        config.LOGGER_ID,
                        f"╔═══❰𝐇𝐎𝐒̧𝐆𝐄𝐋𝐃𝐈̇𝐍𝐈̇𝐙❱═══❍⊱❁۪۪\n║\n║┣⪼ Yαყıɳԃαყıɱ 🌈...\n║\n║◈ {self.name}\n║\n║┣⪼🎈ɪᴅ:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼ тєşєkkürlєr \n║\n╚══════════════❍⊱❁",
                        reply_markup=button,
                    )
                except Exception as e:
                    LOGGER(__name__).error(f"𝙱𝚘𝚝 𝙷𝚊𝚝𝚊 𝚅𝚎𝚛𝚍𝚒...\n  𝚂𝚎𝚋𝚎𝚋𝚒: {e}")
            except Exception as e:
                LOGGER(__name__).error(
                    f"𝙱𝚘𝚝 𝙷𝚊𝚝𝚊 𝚅𝚎𝚛𝚍𝚒...\n  𝚂𝚎𝚋𝚎𝚋𝚒: {e}"
                )
        else:
            LOGGER(__name__).warning(
                "𝙻𝚞̈𝚝𝚏𝚎𝚗 𝙱𝚘𝚝𝚞 𝙻𝚘𝚐 𝙺𝚊𝚗𝚊𝚕ı𝚗𝚊 𝙴𝚔𝚕𝚎𝚢𝚒𝚗...."
            )

        # Setting commands
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Botu Başlat"),
                        BotCommand("help", "Yardım Menüsü"),
                        BotCommand("ping", "Bot Canlı Mı?"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "oynat", "Yayını Başlatır"),
                        BotCommand("stop", "son", "Yayını Sonlandırır"),
                        BotCommand("pause", "dur", "Yayını Duraklatır"),
                        BotCommand("resume", "devam", "Yayını Devam Ettirir"),
                        BotCommand("queue", "Parça Listesini Gösterir"),
                        BotCommand("skip", "atla", "Sıradaki Parçaya atlar"),
                        BotCommand("volume", "Müzik Sesi"),
                        BotCommand("lyrics", "Şarkı Sözleri"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "❥ ✨Botu Başlat✨"),
                        BotCommand("ping", "❥ 🍁Ping Kontrol Et🍁"),
                        BotCommand("help", "❥ 🥺Yardım🥺"),
                        BotCommand("vctag", "❥ 😇VC Tag At🙈"),
                        BotCommand("stopvctag", "❥ 📍VC Tag Durdur💢"),
                        BotCommand("tagall", "❥ 🔻Yazılarla Tag🔻"),
                        BotCommand("cancel", "❥ 🔻Tag İptal🔻"),
                        BotCommand("settings", "❥ 🔻Ayarlar🔻"),
                        BotCommand("reload", "❥ 🪐Yenileme🪐"),
                        BotCommand("play", "❥ ❣️Parça Oynatır❣️"),
                        BotCommand("vplay", "❥ ❣️Video Oynatır❣️"),
                        BotCommand("pause", "❥ 🥀Şarkıyı Duraklatır🥀"),
                        BotCommand("resume", "❥ 💖Şarkıyı Devam Ettirir💖"),
                        BotCommand("end", "❥ 🐚Yayın Sonlanır🐚"),
                        BotCommand("queue", "❥ 🤨Listeyi Kontrol Et🤨"),
                        BotCommand("playlist", "❥ 🕺Playlist Açar🕺"),
                        BotCommand("stop", "❥ ❤‍🔥Şarkı Sonlanır❤‍🔥"),
                        BotCommand("lyrics", "❥ 🕊️Şarkı Sözleri🕊️"),
                        BotCommand("song", "❥ 🔸Şarkı İndirir🔸"),
                        BotCommand("video", "❥ 🔸Video İndirir🔸"),
                        BotCommand("gali", "❥ 🔻ᴛᴏ ʀᴇᴘʟʏ ғᴏʀ ғᴜɴ🔻"),
                        BotCommand("shayri", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴀ sʜᴀʏᴀʀɪ🔻"),
                        BotCommand("love", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴀ ʟᴏᴠᴇ sʜᴀʏᴀʀɪ🔻"),
                        BotCommand("sudolist", "❥ 🌱Sudolist Kontrol Eder🌱"),
                        BotCommand("owner", "❥ 💝Sahip💝"),
                        BotCommand("update", "❥ 🐲ᴛᴏ ᴜᴘᴅᴀᴛᴇ ʙᴏᴛ🐲"),
                        BotCommand("gstats", "❥ 💘Bot İstatistikleri💘"),
                        BotCommand("repo", "❥ 🍌Repo'yu Gösterir🍌"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"𝙱𝚘𝚝 𝙷𝚊𝚝𝚊 𝚅𝚎𝚛𝚍𝚒...\n  𝚂𝚎𝚋𝚎𝚋𝚒: {e}")

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

        LOGGER(__name__).info(f"𝙰𝙻𝙴𝙼 𝙼𝚄̈𝚉𝙸̇𝙺 𝙱𝙰𝚂̧𝙻𝙰𝙳𝙸 as {self.name}")
