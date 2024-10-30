import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import InviteRequestSent

from AlemMuzik import app
from AlemMuzik.misc import SUDOERS
from AlemMuzik.utils.database import get_assistant
from AlemMuzik.utils.alem_ban import admin_filter

links = {}


@app.on_message(
    filters.group & filters.command(["userbotjoin", "ujoin"]) & ~filters.private
)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)
    userbot_id = userbot.id
    done = await message.reply("**Lütfen Bekleyiniz Aistan Davet Ediliyor...**")
    await asyncio.sleep(1)
    # Get chat member object
    chat_member = await app.get_chat_member(chat_id, app.id)

    # Condition 1: Group username is present, bot is not admin
    if (
        message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅ Asistan Katıldı...**")

        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(chat_id, userbot_id)
            except Exception:
                pass
        except Exception as e:
            await done.edit_text("**Asistanı Davet Edebilmem İçin Yetki Veriniz!**")

    # Condition 2: Group username is present, bot is admin, and Userbot is not banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅ Asistan Katıldı...**")
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(chat_id, userbot_id)
            except Exception:
                pass
        except Exception as e:
            await done.edit_text(str(e))

    # Condition 3: Group username is not present/group is private, bot is admin and Userbot is banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await done.edit_text("**Asistanın Yasağı Kaldırıldı...**")
                await userbot.join_chat(message.chat.username)
                await done.edit_text(
                    "**Asistan Banlanmıştı, Banı Açıldı ve Gruba Katıldı...✅**"
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(chat_id, userbot_id)
                except Exception:
                    pass
            except Exception as e:
                await done.edit_text(
                    "**Hata! Ban Yetkisine Ship Herhangi Bir Yönetici Tekrar İşlem Yapsın...**"
                )
        return

    # Condition 4: Group username is not present/group is private, bot is not admin
    if (
        not message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        await done.edit_text("**Asistanı Davet Edebilmem İçin Yetki Veriniz!**")

    # Condition 5: Group username is not present/group is private, bot is admin
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            try:
                userbot_member = await app.get_chat_member(chat_id, userbot.id)
                if userbot_member.status not in [
                    ChatMemberStatus.BANNED,
                    ChatMemberStatus.RESTRICTED,
                ]:
                    await done.edit_text("**✅ Asistan Katılım Sağlamış**")
                    return
            except Exception as e:
                await done.edit_text("**Lütfen Bekleyiniz Asistan Davet Ediliyor...**")
                await done.edit_text("**Lütfen Bekleyiniz Asistan Davet Ediliyor...**")
                invite_link = await app.create_chat_invite_link(
                    chat_id, expire_date=None
                )
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text("**✅ Asistan Katıldı...**")
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(chat_id, userbot_id)
            except Exception:
                pass
        except Exception as e:
            await done.edit_text(
                f"**➻ Aslında Alem Müzik Bot Asistanını Gruba Davet Edemedim. Çünkü Şu An Herhangi Bir Yetkiye Sahip Değilim. Düzgün bir Şekilde Çalışabilmem İçin Beni Admin Yapınız!**\n\n**➥ ɪᴅ »** @{userbot.username}"
            )

    # Condition 6: Group username is not present/group is private, bot is admin and Userbot is banned
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await done.edit_text(
                    "Asistanın Banı Açıldı**\n**Tekrar Yaz:- /userbotjoin.**"
                )
                invite_link = await app.create_chat_invite_link(
                    chat_id, expire_date=None
                )
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text(
                    "**Asistan Banlanmıştı, Banı Açıldı ve Gruba Katıldı...✅**"
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(chat_id, userbot_id)
                except Exception:
                    pass

            except Exception as e:
                await done.edit_text(
                    f"**➻ Aslında Alem Müzik Bot Asistanını Gruba Davet Edemedim. Çünkü Şu An Herhangi Bir Yetkiye Sahip Değilim. Düzgün bir Şekilde Çalışabilmem İçin Beni Admin Yapınız!**\n\n**➥ ɪᴅ »** @{userbot.username}"
                )
        return


@app.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await app.send_message(
            message.chat.id, "**✅ Bot Gruptan Ayrıldı...**"
        )
    except Exception as e:
        print(e)


@app.on_message(filters.command(["leaveall"]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **ᴜsᴇʀʙᴏᴛ** ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs !")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002221176435:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"**ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴀʟʟ ɢʀᴏᴜᴘ...**\n\n**ʟᴇғᴛ:** {left} ᴄʜᴀᴛs.\n**ғᴀɪʟᴇᴅ:** {failed} ᴄʜᴀᴛs."
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"**ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ...**\n\n**ʟᴇғᴛ:** {left} chats.\n**ғᴀɪʟᴇᴅ:** {failed} chats."
                )
            await asyncio.sleep(3)
    finally:
        await app.send_message(
            message.chat.id,
            f"**✅ ʟᴇғᴛ ғʀᴏᴍ:* {left} chats.\n**❌ ғᴀɪʟᴇᴅ ɪɴ:** {failed} chats.",
        )


__MODULES__ = "Userbotjoin"
__HELP__ = """
/ᴜsᴇʀʙᴏᴛᴊᴏɪɴ: Iɴᴠɪᴛᴇs ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴛᴏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ.
/ᴜsᴇʀʙᴏᴛᴇᴀᴠᴇ: Mᴀᴋᴇs ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴇᴀᴠᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ.
/ᴇᴀᴠᴇᴀ: Mᴀᴋᴇs ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴇᴀᴠᴇ ᴀ ɢʀᴏᴜᴘs ᴡʜᴇʀᴇ ɪᴛ ɪs ᴘʀᴇsᴇɴᴛ (ᴀᴄᴄᴇssɪʙᴇ ᴏɴʏ ᴛᴏ SUDOERS)."""