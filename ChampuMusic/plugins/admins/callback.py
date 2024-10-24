import random
import config
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
)
from ChampuMusic import YouTube, app
from ChampuMusic.core.call import Champu
from ChampuMusic.misc import SUDOERS, db
from ChampuMusic.utils.database import (
    is_active_chat,
    is_music_playing,
    is_muted,
    is_nonadmin_chat,
    music_off,
    music_on,
    mute_off,
    mute_on,
    set_loop,
)
from ChampuMusic.utils.decorators.language import languageCB
from ChampuMusic.utils.formatters import seconds_to_min
from ChampuMusic.utils.inline import (
    close_markup,
    panel_markup_1,
    panel_markup_2,
    panel_markup_3,
    panel_markup_4,
    panel_markup_5,
    stream_markup,
    stream_markup2,
)
from ChampuMusic.utils.inline.play import stream_markup
from ChampuMusic.utils.stream.autoclear import auto_clean
from ChampuMusic.utils.thumbnails import get_thumb

wrong = {}
downvote = {}
downvoters = {}

# =============================FUNCTIONS==============================#


@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
@languageCB
async def markup_panel(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = CallbackQuery.message.chat.id
    buttons = panel_markup_1(_, videoid, chat_id)

    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.id] = True


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
@languageCB
async def del_back_playlists(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    buttons = stream_markup(_, videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.id] = True


@app.on_callback_query(filters.regex("MusicMarkup") & ~BANNED_USERS)
@languageCB
async def music_markup(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    buttons = stream_markup(_, videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.id] = True


@app.on_callback_query(filters.regex("Pages") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    playing = db.get(chat_id)
    
    if not playing:
        return await CallbackQuery.answer(_["queue_2"], show_alert=True)

    # Initialize pages
    pages = 0  # or any default value you see fit

    callback_request = callback_data.split(None, 1)[1]
    state, pages_str, videoid, chat = callback_request.split("|")
    pages = int(pages_str)  # Assign the parsed value to pages
    chat_id = int(chat)

    if pages == 3:
        buttons = panel_markup_4(
            _, 
            playing[0]["vidid"], 
            chat_id, 
            seconds_to_min(playing[0]["played"]), 
            playing[0]["dur"],
        )
    callback_request = callback_data.split(None, 1)[1]
    state, pages, videoid, chat = callback_request.split("|")
    chat_id = int(chat)
    pages = int(pages)
    if state == "Forw":
        if pages == 0:
            buttons = panel_markup_5(_, videoid, chat_id)
        if pages == 1:
            buttons = panel_markup_1(_, videoid, chat_id)
        if pages == 2:
            buttons = panel_markup_2(_, videoid, chat_id)

    if state == "Back":
        if pages == 1:
            buttons = panel_markup_1(_, videoid, chat_id)
        if pages == 2:
            buttons = panel_markup_5(_, videoid, chat_id)
        if pages == 0:
            buttons = panel_markup_3(_, videoid, chat_id)
        if pages == 4:
            buttons = panel_markup_
        if pages == 3:
            buttons = panel_markup_4(
                _,
                playing[0]["vidid"],
                chat_id,
                seconds_to_min(playing[0]["played"]),
                playing[0]["dur"],
            )
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return


@app.on_callback_query(filters.regex("unban_assistant"))
async def unban_assistant(_, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    userbot = await get_assistant(chat_id)

    try:
        await app.unban_chat_member(chat_id, userbot.id)
        await callback.answer(
            "𝐀𝐥𝐞𝐦 𝐌𝐮̈𝐳𝐢𝐤 𝐀𝐬𝐢𝐬𝐭𝐚𝐧ı𝐧 𝐘𝐚𝐬𝐚𝐠̆ı 𝐁𝐚𝐬̧𝐚𝐫ı𝐲𝐥𝐚 𝐊𝐚𝐥𝐝ı𝐫ı𝐥𝐝ı🥳\n\n➻ 𝐀𝐫𝐭ı𝐤 𝐒̧𝐚𝐫𝐤ı𝐥𝐚𝐫ı 𝐂̧𝐚𝐥𝐚𝐛𝐢𝐥𝐢𝐫𝐬𝐢𝐧𝐢𝐳.🔉\n\n𝐓𝐞𝐬̧𝐞𝐤𝐤𝐮̈𝐫 𝐞𝐝𝐞𝐫𝐢𝐦💝",
            show_alert=True,
        )
    except Exception as e:
        await callback.answer(
            f"𝐘𝐚𝐬𝐚𝐤𝐥𝐚𝐦𝐚 𝐘𝐞𝐭𝐤𝐢𝐦𝐢𝐦 𝐎𝐥𝐦𝐚𝐝ı𝐠̆ı 𝐈̇𝐜̧𝐢𝐧 𝐀𝐬𝐢𝐬𝐭𝐚𝐧ı𝐦ı𝐧 𝐘𝐚𝐬𝐚𝐠̆ı𝐧ı 𝐊𝐚𝐥𝐝ı𝐫𝐚𝐦𝐚𝐝ı𝐦. \n\n➻ 𝐀𝐬𝐢𝐬𝐭𝐚𝐧 𝐊𝐢𝐦𝐥𝐢𝐠̆𝐢𝐦𝐢𝐧 𝐘𝐚𝐬𝐚𝐠̆ı𝐧ı 𝐊𝐚𝐥𝐝ı𝐫𝐚𝐛𝐢𝐥𝐦𝐞𝐦 𝐈̇𝐜̧𝐢𝐧 𝐋𝐮̈𝐭𝐟𝐞𝐧 𝐁𝐚𝐧𝐚 𝐘𝐚𝐬𝐚𝐤𝐥𝐚𝐦𝐚 𝐆𝐮̈𝐜𝐮̈ 𝐒𝐚𝐠̆𝐥𝐚𝐲ı𝐧",
            show_alert=True,
        )


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_6"], show_alert=True)
    mention = CallbackQuery.from_user.mention
    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}

        voters = (upvoters[chat_id]).get(CallbackQuery.message.id)
        if not voters:
            upvoters[chat_id][CallbackQuery.message.id] = []

        vote = (votemode[chat_id]).get(CallbackQuery.message.id)
        if not vote:
            votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            (upvoters[chat_id][CallbackQuery.message.id]).remove(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            (upvoters[chat_id][CallbackQuery.message.id]).append(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] += 1
        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])
        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
            except:
                return await CallbackQuery.edit_message_text(f"ғᴀɪʟᴇᴅ.")
            try:
                if current["vidid"] != exists["vidid"]:
                    return await CallbackQuery.edit_message.text(_["admin_35"])
                if current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message.text(_["admin_35"])
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])
            try:
                await CallbackQuery.edit_message_text(_["admin_37"].format(upvote))
            except:
                pass
            command = counter
            mention = "𝐎𝐘𝐋𝐀𝐑"
        else:
            if (
                CallbackQuery.from_user.id
                in upvoters[chat_id][CallbackQuery.message.id]
            ):
                await CallbackQuery.answer(_["admin_38"], show_alert=True)
            else:
                await CallbackQuery.answer(_["admin_39"], show_alert=True)
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"👍 {get_upvotes}",
                            callback_data=f"ADMIN  UpVote|{chat_id}_{counter}",
                        )
                    ]
                ]
            )
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)
    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                if not admins:
                    return await CallbackQuery.answer(_["admin_18"], show_alert=True)
                else:
                    if CallbackQuery.from_user.id not in admins:
                        return await CallbackQuery.answer(
                            _["admin_19"], show_alert=True
                        )
    if command == "pause" or command == "dur":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await CallbackQuery.answer()
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
        await CallbackQuery.message.reply_text(
            _["admin_2"].format(mention), reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif command == "resume" or command == "devam":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await Champu.resume_stream(chat_id)
        buttons_resume = [
            [
                InlineKeyboardButton(
                    text="𝙰𝚃𝙻𝙰", callback_data=f"ADMIN Skip|{chat_id}"
                ),
                InlineKeyboardButton(
                    text="𝚂𝙾𝙽", callback_data=f"ADMIN Stop|{chat_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="𝙳𝚄𝚁",
                    callback_data=f"ADMIN Pause|{chat_id}",
                ),
            ],
        ]

        await CallbackQuery.message.reply_text(
            _["admin_4"].format(mention),
            reply_markup=InlineKeyboardMarkup(buttons_resume),
        )
    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await Champu.st_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(
            _["admin_9"].format(mention), reply_markup=close_markup(_)
        )
        await CallbackQuery.message.delete()
    elif command == "Mute":
        if await is_muted(chat_id):
            return await CallbackQuery.answer(_["admin_5"], show_alert=True)
        await CallbackQuery.answer()
        await mute_on(chat_id)
        await Champu.mute_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_6"].format(mention))
    elif command == "Unmute":
        if not await is_muted(chat_id):
            return await CallbackQuery.answer(_["admin_7"], show_alert=True)
        await CallbackQuery.answer()
        await mute_off(chat_id)
        await Champu.unmute_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_8"].format(mention))
    elif command == "Loop", "Tekrar":
        await CallbackQuery.answer()
        await set_loop(chat_id, 3)
        await CallbackQuery.message.reply_text(_["admin_25"].format(mention, 3))
    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        await CallbackQuery.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.message.reply_text(_["admin_23"].format(mention))
    elif command == "Skip" or command == "atla":
        check = db.get(chat_id)
        if command == "Skip":
            txt = f"<b>➻ 𝙿𝚊𝚛𝚌̧𝚊 𝙰𝚝𝚕𝚊𝚗𝚍ı<b> 🎄\n│ \n<b>└Tαɾαϝıɳԃαɳ :<b> {mention} 🥀"
            popped = None
            try:
                popped = check.pop(0)
                if popped:
                    await auto_clean(popped)
                if not check:
                    await CallbackQuery.edit_message_text(
                        f"<b>➻ 𝙿𝚊𝚛𝚌̧𝚊 𝙰𝚝𝚕𝚊𝚗𝚍ı<b> 🎄\n│ \n<b>└Tαɾαϝıɳԃαɳ :<b> {mention} 🥀"
                    )
                    await CallbackQuery.message.reply_text(
                        text=_["admin_10"].format(
                            mention, CallbackQuery.message.chat.title
                        ),
                        reply_markup=close_markup(_),
                    )
                    try:
                        return await Champu.st_stream(chat_id)
                    except:
                        return
            except:
                try:
                    await CallbackQuery.edit_message_text(
                        f"<b>➻ 𝙿𝚊𝚛𝚌̧𝚊 𝙰𝚝𝚕𝚊𝚗𝚍ı<b> 🎄\n│ \n<b>└Tαɾαϝıɳԃαɳ :<b> {mention} 🥀"
                    )
                    await CallbackQuery.message.reply_text(
                        text=_["admin_6"].format(
                            mention, CallbackQuery.message.chat.title
                        ),
                        reply_markup=close_markup(_),
                    )
                    return await Champu.st_stream(chat_id)
                except:
                    return
        else:
            txt = f"<b>➻ 𝚈𝚊𝚢ı𝚗 𝚃𝚎𝚔𝚛𝚊𝚛 𝙾𝚢𝚗𝚊𝚝ı𝚕𝚍ı<b> 🎄\n│ \n<b>└Tαɾαϝıɳԃαɳ :<b> {mention} 🥀"
        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        duration = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        exis = (check[0]).get("old_dur")
        if exis:
            db[chat_id][0]["dur"] = exis
            db[chat_id][0]["seconds"] = check[0]["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await CallbackQuery.message.reply_text(
                    text=_["admin_7"].format(title),
                    reply_markup=close_markup(_),
                )
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await Champu.skip_stream(chat_id, link, video=status, image=image)
            except:
                return await CallbackQuery.message.reply_text(_["call_7"])
            button = stream_markup2(_, chat_id)
            img = await get_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    duration,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))
        elif "vid_" in queued:
            mystic = await CallbackQuery.message.reply_text(
                _["call_7"], disable_web_page_preview=True
            )
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=status,
                )
            except:
                return await mystic.edit_text(_["call_7"])
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await Champu.skip_stream(chat_id, file_path, video=status, image=image)
            except:
                return await mystic.edit_text(_["call_7"])
            button = stream_markup(_, videoid, chat_id)
            img = await get_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    duration,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))
            await mystic.delete()
        elif "index_" in queued:
            try:
                await Champu.skip_stream(chat_id, videoid, video=status)
            except:
                return await CallbackQuery.message.reply_text(_["call_7"])
            button = stream_markup2(_, chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))
        else:
            if videoid == "telegram":
                image = None
            elif videoid == "soundcloud":
                image = None
            else:
                try:
                    image = await YouTube.thumbnail(videoid, True)
                except:
                    image = None
            try:
                await Champu.skip_stream(chat_id, queued, video=status, image=image)
            except:
                return await CallbackQuery.message.reply_text(_["call_7"])
            if videoid == "telegram":
                button = stream_markup2(_, chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=(
                        TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        config.SUPPORT_GROUP, title[:23], duration, user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = stream_markup2(_, chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=(
                        SOUNCLOUD_IMG_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        config.SUPPORT_GROUP, title[:23], duration, user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                button = stream_markup(_, videoid, chat_id)
                img = await get_thumb(videoid)
                run = await CallbackQuery.message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        duration,
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))

    else:
        playing = db.get(chat_id)
        if not playing:
            return await CallbackQuery.answer(_["queue_2"], show_alert=True)
        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)
        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)
        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]
        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"» 𝙸̇𝚣𝚒𝚗 𝚅𝚎𝚛𝚒𝚕𝚎𝚗 𝚂𝚞̈𝚛𝚎 𝙰𝚜̧ı𝚕𝚍ı𝚐̆ı 𝙸̇𝚌̧𝚒𝚗 𝙿𝚊𝚛𝚌̧𝚊 𝙰𝚢𝚛ı𝚗𝚝ı𝚕𝚊𝚛ı 𝙶𝚎𝚝𝚒𝚛𝚒𝚕𝚎𝚖𝚎𝚍𝚒.\n\n𝚂̧𝚄 𝙰𝙽𝙳𝙰 𝙾𝚈𝙽𝙰𝚃𝙸𝙻𝙰𝙽: :** {bet}** 𝙳𝙰𝙺𝙸̇𝙺𝙰 𝙳𝙸𝚂̧𝙸𝙽𝙳𝙰 **{duration}** 𝙳𝙰𝙺𝙸̇𝙺𝙰.",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"» 𝙸̇𝚣𝚒𝚗 𝚅𝚎𝚛𝚒𝚕𝚎𝚗 𝚂𝚞̈𝚛𝚎 𝙰𝚜̧ı𝚕𝚍ı𝚐̆ı 𝙸̇𝚌̧𝚒𝚗 𝙿𝚊𝚛𝚌̧𝚊 𝙰𝚢𝚛ı𝚗𝚝ı𝚕𝚊𝚛ı 𝙶𝚎𝚝𝚒𝚛𝚒𝚕𝚎𝚖𝚎𝚍𝚒.\n\n𝚂̧𝚄 𝙰𝙽𝙳𝙰 𝙾𝚈𝙽𝙰𝚃𝙸𝙻𝙰𝙽: :** {bet}** 𝙳𝙰𝙺𝙸̇𝙺𝙰 𝙳𝙸𝚂̧𝙸𝙽𝙳𝙰 **{duration}** 𝙳𝙰𝙺𝙸̇𝙺𝙰.",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1
        await CallbackQuery.answer()
        mystic = await CallbackQuery.message.reply_text(_["admin_32"])
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(_["admin_30"])
        try:
            await Champu.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
                playing[0]["streamtype"],
            )
        except:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = _["admin_33"].format(seconds_to_min(to_seek))
        await mystic.edit_text(f"{string}\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ : {mention} !")


"""async def markup_timers():
    while not await asyncio.sleep(5):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id):
                    continue
                playing = db.get(chat_id)
                if not playing:
                    continue
                duration_seconds = int(playing[0]["seconds"])
                if duration_seconds == 0:
                    continue
                try:
                    mystic = playing[0]["markup"]
                except:
                    continue
                try:
                    check = checker[chat_id][mystic.id]
                    if check is False:
                        continue
                except:
                    pass
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")
                try:
                    mystic = playing[0]["mystic"]
                    markup = playing[0]["markup"]
                except:
                    continue
                try:
                    check = wrong[chat_id][mystic.id]
                    if check is False:
                        continue
                except:
                    pass
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")
                try:
                    mystic = playing[0]["mystic"]
                    markup = playing[0]["markup"]
                except:
                    continue
                try:
                    check = wrong[chat_id][mystic.id]
                    if check is False:
                        continue
                except:
                    pass
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")
                try:
                    buttons = (
                        stream_markup_timer(
                            _,
                            playing[0]["vidid"],
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                        if markup == "stream"
                        else stream_markup_timer2(
                            _,
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                    )
                    await mystic.send_message(
                        chat_id,
                        text="Or sab badhiya bhai song sun rhe ho na thik h suno suno",
                    )
                    await mystic.edit_reply_markup(
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except:
                    continue
            except:
                continue


asyncio.create_task(markup_timers())"""

__MODULE__ = "Adᴍɪɴ"
__HELP__ = """

<b>c sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ.</b>

<b>✧ /pause</b> ᴏʀ <b>/dur</b> - Mevcut oynatma akışını duraklatır.
<b>✧ /resume</b> ᴏʀ <b>/devam</b> - Duraklatılan akışı devam ettirir.
<b>✧ /mute</b> ᴏʀ <b>/cmute</b> - Müziği sessize alır.
<b>✧ /unmute</b> ᴏʀ <b>/cunmute</b> - Müziğin sesini açar.
<b>✧ /skip</b> ᴏʀ <b>/atla</b> - Mevcut oynatma akışını atlar ve sıradaki parçayı oynatmaya başlar.
<b>✧ /stop</b> ᴏʀ <b>/son</b> - Listeyi temizler ve mevcut oynatma akışını sonlandırır.
<b>✧ /shuffle</b> ᴏʀ <b>/cshuffle</b> - Parça Listesini karıştırır.
<b>✧ /seek</b> ᴏʀ <b>/cseek</b> - Parça süresini ileri atlar.
<b>✧ /seekback</b> ᴏʀ <b>/cseekback</b> - Parça süresini geri alır.
<b>✧ /reboot</b> - Rᴇʙᴏᴏᴛ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ.

<b>✧ /skip</b> ᴏʀ <b>/atla</b> [Nᴜᴍʙᴇʀ (ᴇxᴀᴍᴘʟᴇ: 𝟹)] - Belli bir sıradaki parçaya atlar. Örneğin: <b>/atla 𝟹</b> Parça listesindeki 3.parçaya geçecektir. 1. ve 2. parçalar iptal olacaktır.

<b>✧ /loop</b> ᴏʀ <b>/tekrar</b> [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] ᴏʀ [Nᴜᴍʙᴇʀs ʙᴇᴛᴡᴇᴇɴ 𝟷-𝟷𝟶] - Verilen değer için döngüyü etkinleştirir. Örneğin 𝟷𝟶 tekrar yapar."""
