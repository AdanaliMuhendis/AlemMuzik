import re
from math import ceil
from typing import Union

from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from config import BANNED_USERS, START_IMG_URL
from strings import get_command, get_string
from AlemMuzik import HELPABLE, app
from AlemMuzik.utils.database import get_lang, is_commanddelete_on
from AlemMuzik.utils.decorators.language import LanguageStart
from AlemMuzik.utils.inline.help import private_help_panel

### Command
HELP_COMMAND = get_command("HELP_COMMAND")

COLUMN_SIZE = 4
NUM_COLUMNS = 3



class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None, close: bool = False):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, x.__MODULE__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{},{})".format(
                        prefix, chat, x.__MODULE__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i : i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮",
                    callback_data="{}_prev({})".format(
                        prefix,
                        modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                    ),
                ),
                EqInlineKeyboardButton(
                    "ᴄʟᴏsᴇ" if close else "Bᴀᴄᴋ",
                    callback_data="close" if close else "feature",
                ),
                EqInlineKeyboardButton(
                    "❯",
                    callback_data="{}_next({})".format(prefix, modulo_page + 1),
                ),
            )
        ]
    else:
        pairs.append(
            [
                EqInlineKeyboardButton(
                    "ᴄʟᴏsᴇ" if close else "Bᴀᴄᴋ",
                    callback_data="close" if close else "feature",
                ),
            ]
        )

    return pairs


@app.on_message(filters.command(HELP_COMMAND) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass

        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))

        await update.edit_message_text(_["help_1"], reply_markup=keyboard)
    else:
        chat_id = update.chat.id
        if await is_commanddelete_on(update.chat.id):
            try:
                await update.delete()
            except:
                pass
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help", close=True)
        )
        if START_IMG_URL:

            await update.reply_photo(
                photo=START_IMG_URL,
                caption=_["help_1"],
                reply_markup=keyboard,
            )

        else:

            await update.reply_text(
                text=_["help_1"],
                reply_markup=keyboard,
            )


@app.on_message(filters.command(HELP_COMMAND) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return keyboard


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back\((\d+)\)", query.data)
    create_match = re.match(r"help_create", query.data)
    language = await get_lang(query.message.chat.id)
    _ = get_string(language)
    top_text = _["help_1"]

    if mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        text = (
            f"<b><u>Yardım İçin Buraya {HELPABLE[module].__MODULE__}:</u></b>\n"
            + HELPABLE[module].__HELP__
        )

        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ 𝐆𝐄𝐑𝐢°", callback_data=f"help_back({prev_page_num})"
                    ),
                    InlineKeyboardButton(text="🔄 𝐊𝐀𝐏𝐀𝐓°", callback_data="close"),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )

    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out),
        )
        await query.message.delete()

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        prev_page_num = int(back_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(prev_page_num, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))

        await query.message.edit(
            text=top_text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    await client.answer_callback_query(query.id)


# ===================================

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import BANNED_USERS
from strings import helpers
from AlemMuzik import app
from AlemMuzik.utils.decorators.language import languageCB


@app.on_callback_query(filters.regex("music_callback") & ~BANNED_USERS)
@languageCB
async def music_helper_cb(client, CallbackQuery, _):

    callback_data = CallbackQuery.data.strip()

    cb = callback_data.split(None, 1)[1]

    keyboard = back_to_music(_)

    if cb == "hb1":

        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)

    elif cb == "hb2":

        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)

    elif cb == "hb3":

        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)

    elif cb == "hb4":

        await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)

    elif cb == "hb5":

        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)

    elif cb == "hb6":

        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)

    elif cb == "hb7":

        await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)

    elif cb == "hb8":

        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)

    elif cb == "hb9":

        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)

    elif cb == "hb10":

        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)

    elif cb == "hb11":

        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)

    elif cb == "hb12":

        await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)

    elif cb == "hb13":

        await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)

    elif cb == "hb14":

        await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)

    elif cb == "hb15":

        await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)


@app.on_callback_query(filters.regex("management_callback") & ~BANNED_USERS)
@languageCB
async def management_callback_cb(client, CallbackQuery, _):

    callback_data = CallbackQuery.data.strip()

    cb = callback_data.split(None, 1)[1]

    keyboard = back_to_management(_)

    if cb == "extra":

        await CallbackQuery.edit_message_text(helpers.EXTRA_1, reply_markup=keyboard)

    elif cb == "hb1":

        await CallbackQuery.edit_message_text(helpers.MHELP_1, reply_markup=keyboard)

    elif cb == "hb2":

        await CallbackQuery.edit_message_text(helpers.MHELP_2, reply_markup=keyboard)

    elif cb == "hb3":

        await CallbackQuery.edit_message_text(helpers.MHELP_3, reply_markup=keyboard)

    elif cb == "hb4":

        await CallbackQuery.edit_message_text(helpers.MHELP_4, reply_markup=keyboard)

    elif cb == "hb5":

        await CallbackQuery.edit_message_text(helpers.MHELP_5, reply_markup=keyboard)

    elif cb == "hb6":

        await CallbackQuery.edit_message_text(helpers.MHELP_6, reply_markup=keyboard)

    elif cb == "hb7":

        await CallbackQuery.edit_message_text(helpers.MHELP_7, reply_markup=keyboard)

    elif cb == "hb8":

        await CallbackQuery.edit_message_text(helpers.MHELP_8, reply_markup=keyboard)

    elif cb == "hb9":

        await CallbackQuery.edit_message_text(helpers.MHELP_9, reply_markup=keyboard)

    elif cb == "hb10":

        await CallbackQuery.edit_message_text(helpers.MHELP_10, reply_markup=keyboard)

    elif cb == "hb11":

        await CallbackQuery.edit_message_text(helpers.MHELP_11, reply_markup=keyboard)

    elif cb == "hb12":

        await CallbackQuery.edit_message_text(helpers.MHELP_12, reply_markup=keyboard)


@app.on_callback_query(filters.regex("tools_callback") & ~BANNED_USERS)
@languageCB
async def tools_callback_cb(client, CallbackQuery, _):

    callback_data = CallbackQuery.data.strip()

    cb = callback_data.split(None, 1)[1]

    keyboard = back_to_tools(_)

    if cb == "ai":

        await CallbackQuery.edit_message_text(helpers.AI_1, reply_markup=keyboard)

    elif cb == "hb1":

        await CallbackQuery.edit_message_text(helpers.THELP_1, reply_markup=keyboard)

    elif cb == "hb2":

        await CallbackQuery.edit_message_text(helpers.THELP_2, reply_markup=keyboard)

    elif cb == "hb3":

        await CallbackQuery.edit_message_text(helpers.THELP_3, reply_markup=keyboard)

    elif cb == "hb4":

        await CallbackQuery.edit_message_text(helpers.THELP_4, reply_markup=keyboard)

    elif cb == "hb5":

        await CallbackQuery.edit_message_text(helpers.THELP_5, reply_markup=keyboard)

    elif cb == "hb6":

        await CallbackQuery.edit_message_text(helpers.THELP_6, reply_markup=keyboard)

    elif cb == "hb7":

        await CallbackQuery.edit_message_text(helpers.THELP_7, reply_markup=keyboard)

    elif cb == "hb8":

        await CallbackQuery.edit_message_text(helpers.THELP_8, reply_markup=keyboard)

    elif cb == "hb9":

        await CallbackQuery.edit_message_text(helpers.THELP_9, reply_markup=keyboard)

    elif cb == "hb10":

        await CallbackQuery.edit_message_text(helpers.THELP_10, reply_markup=keyboard)

    elif cb == "hb11":

        await CallbackQuery.edit_message_text(helpers.THELP_11, reply_markup=keyboard)

    elif cb == "hb12":

        await CallbackQuery.edit_message_text(helpers.THELP_12, reply_markup=keyboard)


@app.on_callback_query(filters.regex("developer"))
async def about_callback(client: Client, callback_query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="🔰 𝐒𝐀𝐇𝐈̇𝐏° 🔰", user_id=config.OWNER_ID[0]),
            InlineKeyboardButton(
                text="📍уєткι̇ℓι̇📍", url=f"https://t.me/{app.username}?start=sudo"
            ),
        ],
        [
            InlineKeyboardButton(text="✨ ɪɴsᴛᴀ ✨", url=f"https://www.instagram.com/AdanaliMuhendis/"),
            InlineKeyboardButton(text="⚡ ʏᴏᴜᴛᴜʙᴇ ⚡", url=f"https://www.youtube.com/@AdanaliMuhendis"),
        ],
        [
            InlineKeyboardButton(text="🔙 𝐆𝐄𝐑𝐢°", callback_data="about")
        ],  # Use a default label for the back button
    ]
    await callback_query.message.edit_text(
        "✦ **𝐁𝐔 𝐁𝐎𝐓, 𝐆𝐑𝐔𝐁𝐔𝐍𝐔𝐙𝐔𝐍 𝐘𝐎̈𝐍𝐄𝐓𝐈̇𝐌𝐈̇𝐍𝐈̇ 𝐊𝐎𝐋𝐀𝐘 𝐕𝐄 𝐃𝐀𝐇𝐀 𝐄𝐆̆𝐋𝐄𝐍𝐂𝐄𝐋𝐈̇ 𝐇𝐀𝐋𝐄 𝐆𝐄𝐓𝐈̇𝐑𝐌𝐄𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐘𝐄𝐓𝐄𝐍𝐄𝐊𝐋𝐈̇ 𝐆𝐄𝐋𝐈̇𝐒̧𝐓𝐈̇𝐑𝐈̇𝐂𝐈̇𝐋𝐄𝐑 𝐓𝐀𝐑𝐀𝐅𝐈𝐍𝐃𝐀𝐍 𝐘𝐀𝐏𝐈𝐋𝐌𝐈𝐒̧𝐓𝐈𝐑.**\n\n✦ **sαdєcє вí̇rkαç tíklαmα í̇lє hєr şєчí̇ kσntrσl єdєвí̇lí̇rsí̇ní̇z—ѕαнι̇ρ αуαяℓαяιиι αуαяℓαмαк, уσ̈иєтι̇¢ι̇ℓєяι̇ кσитяσℓ єтмєк νє нαттα ιиѕтαgяαм νє уσυтυвє'υ кєѕ̧fєтмєк gι̇вι̇**\n\n✦ **𝙰𝙻𝙴𝙼 𝙼𝚄̈𝚉𝙸̇𝙺 𝙱𝙾𝚃, 𝙶𝚁𝚄𝙱𝚄𝙽𝚄𝚉𝚄 𝚂𝙾𝚁𝚄𝙽𝚂𝚄𝚉 𝙱𝙸̇𝚁 𝚂̧𝙴𝙺𝙸̇𝙻𝙳𝙴 𝚈𝙾̈𝙽𝙴𝚃𝙼𝙴𝙽𝙸̇𝚉𝙴 𝚅𝙴 𝙼𝚄̈𝚉𝙸̇𝙶̆𝙸̇𝙽 𝙺𝙴𝚈𝙵𝙸̇𝙽𝙸̇ 𝙲̧𝙸𝙺𝙰𝚁𝙼𝙰𝙽𝙸𝚉𝙰 𝚈𝙰𝚁𝙳𝙸𝙼𝙲𝙸 𝙾𝙻𝙼𝙰𝙺 𝙸̇𝙲̧𝙸̇𝙽 𝚃𝙰𝚂𝙰𝚁𝙻𝙰𝙽𝙳𝙸. sαdєcє αşαğídαkí̇ düğmєlєrí̇ kullαnín vє nє kαdαr kσlαч σlduğunu gσ̈rün!**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("feature"))
async def feature_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(
                text="⚜️ 𝐄𝐊𝐋𝐄 𝐁𝐄𝐍𝐈̇° ⚜️",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text=" 𝐌𝐔̈𝐙𝐈̇𝐊° ", callback_data="music"),
            InlineKeyboardButton(text=" 𝐘𝐎̈𝐍𝐄𝐓𝐈̇𝐌° ", callback_data="management"),
        ],
        [
            InlineKeyboardButton(text=" 𝐀𝐑𝐀𝐂̧𝐋𝐀𝐑° ", callback_data="tools"),
            InlineKeyboardButton(text=" 𝐇𝐄𝐏𝐒𝐈̇° ", callback_data="settings_back_helper"),
        ],
        [InlineKeyboardButton(text="✯ 𝐀𝐍𝐀 𝐌𝐄𝐍𝐔̈° ✯", callback_data="go_to_start")],
    ]
    k = f"""**❖ 𝐇𝐄𝐘𝐘𝐘𝐎 {app.mention} ! 

━━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━━
❖ ᴛʜɪs ɪs ϻᴧηᴧɢєϻєηᴛ | ϻυsɪᴄ ʙσᴛ
❖ ησ ʟᴧɢ | ᴧᴅs ϻυsɪᴄ | ησ ᴘʀσϻσ
❖ 24x7 ʀυη | ʙєsᴛ sσυηᴅ ǫυᴧʟɪᴛʏ

Kısaca İyi Bot :)
━━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━━
❖ ᴄʟɪᴄᴋ ση ᴛʜє ʜєʟᴩ ʙυᴛᴛση ᴛσ ɢєᴛ ɪηғσ
    ᴧʙσυᴛ ϻʏ ϻσᴅυʟєs ᴧηᴅ ᴄσϻϻᴧηᴅs...!

Aşağıdaki Butonlara Dikkat et...
━━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━━**"""
    await callback_query.message.edit_text(
        text=k, reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(filters.regex("music"))
async def music_callback(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Aᴅᴍɪɴ", callback_data="music_callback hb1"),
                InlineKeyboardButton(text="Aᴜᴛʜ", callback_data="music_callback hb2"),
                InlineKeyboardButton(
                    text="Bʀᴏᴀᴅᴄᴀsᴛ", callback_data="music_callback hb3"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Bʟ-Cʜᴀᴛ", callback_data="music_callback hb4"
                ),
                InlineKeyboardButton(
                    text="Bʟ-Usᴇʀ", callback_data="music_callback hb5"
                ),
                InlineKeyboardButton(text="C-Pʟᴀʏ", callback_data="music_callback hb6"),
            ],
            [
                InlineKeyboardButton(text="G-Bᴀɴ", callback_data="music_callback hb7"),
                InlineKeyboardButton(text="Lᴏᴏᴘ", callback_data="music_callback hb8"),
                InlineKeyboardButton(
                    text="Mᴀɪɴᴛᴇɴᴀɴᴄᴇ", callback_data="music_callback hb9"
                ),
            ],
            [
                InlineKeyboardButton(text="Pɪɴɢ", callback_data="music_callback hb10"),
                InlineKeyboardButton(text="Pʟᴀʏ", callback_data="music_callback hb11"),
                InlineKeyboardButton(
                    text="Sʜᴜғғʟᴇ", callback_data="music_callback hb12"
                ),
            ],
            [
                InlineKeyboardButton(text="Sᴇᴇᴋ", callback_data="music_callback hb13"),
                InlineKeyboardButton(text="Sᴏɴɢ", callback_data="music_callback hb14"),
                InlineKeyboardButton(text="Sᴘᴇᴇᴅ", callback_data="music_callback hb15"),
            ],
            [InlineKeyboardButton(text="✯  𝐆𝐄𝐑𝐢° ✯", callback_data=f"feature")],
        ]
    )

    await callback_query.message.edit(
        f"``**dαhα fαzlα вí̇lgí̇ í̇çí̇n αşαğídαkí̇ вutσnlαrα tíklαчíníz. hєrhαngí̇ вí̇r sσrunlα kαrşílαşíчσrsαníz вurαчα чαzín [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.](t.me/SohbetAlemi)**\n\n**𝐁𝐔̈𝐓𝐔̈𝐍 𝐊𝐎𝐌𝐔𝐓𝐋𝐀𝐑𝐈 𝐁𝐔 𝐒𝐈̇𝐌𝐆𝐄 𝐈̇𝐋𝐄 𝐊𝐔𝐋𝐋𝐀𝐍𝐈𝐍: /**``",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("management"))
async def management_callback(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="єxᴛʀᴧ", callback_data="management_callback extra"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ʙᴧη", callback_data="management_callback hb1"
                ),
                InlineKeyboardButton(
                    text="ᴋɪᴄᴋs", callback_data="management_callback hb2"
                ),
                InlineKeyboardButton(
                    text="ϻυᴛє", callback_data="management_callback hb3"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴘɪη", callback_data="management_callback hb4"
                ),
                InlineKeyboardButton(
                    text="sᴛᴧғғ", callback_data="management_callback hb5"
                ),
                InlineKeyboardButton(
                    text="sєᴛ υᴘ", callback_data="management_callback hb6"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="zσϻʙɪє", callback_data="management_callback hb7"
                ),
                InlineKeyboardButton(
                    text="ɢᴧϻє", callback_data="management_callback hb8"
                ),
                InlineKeyboardButton(
                    text="ɪϻᴘσsᴛєʀ", callback_data="management_callback hb9"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="sᴧηɢ ϻᴧᴛᴧ", callback_data="management_callback hb10"
                ),
                InlineKeyboardButton(
                    text="ᴛʀᴧηsʟᴧᴛє", callback_data="management_callback hb11"
                ),
                InlineKeyboardButton(
                    text="ᴛ-ɢʀᴧᴘʜ", callback_data="management_callback hb12"
                ),
            ],
            [InlineKeyboardButton(text="✯  𝐆𝐄𝐑𝐢° ✯", callback_data=f"feature")],
        ]
    )

    await callback_query.message.edit(
        f"``**dαhα fαzlα вí̇lgí̇ í̇çí̇n αşαğídαkí̇ вutσnlαrα tíklαчíníz. hєrhαngí̇ вí̇r sσrunlα kαrşílαşíчσrsαníz вurαчα чαzín [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.](t.me/SohbetAlemi)**\n\n**𝐁𝐔̈𝐓𝐔̈𝐍 𝐊𝐎𝐌𝐔𝐓𝐋𝐀𝐑𝐈 𝐁𝐔 𝐒𝐈̇𝐌𝐆𝐄 𝐈̇𝐋𝐄 𝐊𝐔𝐋𝐋𝐀𝐍𝐈𝐍: /**``",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("tools"))
async def tools_callback(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="ᴄʜᴧᴛɢᴘᴛ", callback_data="tools_callback ai")],
            [
                InlineKeyboardButton(text="ɢσσɢʟє", callback_data="tools_callback hb1"),
                InlineKeyboardButton(
                    text="ᴛᴛs-ᴠσɪᴄє", callback_data="tools_callback hb2"
                ),
                InlineKeyboardButton(text="ɪηꜰσ", callback_data="tools_callback hb3"),
            ],
            [
                InlineKeyboardButton(text="ғσηᴛ", callback_data="tools_callback hb4"),
                InlineKeyboardButton(text="ϻᴧᴛʜ", callback_data="tools_callback hb5"),
                InlineKeyboardButton(text="ᴛᴧɢᴧʟʟ", callback_data="tools_callback hb6"),
            ],
            [
                InlineKeyboardButton(text="ɪϻᴧɢє", callback_data="tools_callback hb7"),
                InlineKeyboardButton(text="ʜᴧsᴛᴧɢ", callback_data="tools_callback hb8"),
                InlineKeyboardButton(
                    text="sᴛɪᴄᴋєʀs", callback_data="tools_callback hb9"
                ),
            ],
            [
                InlineKeyboardButton(text="ғυη", callback_data="tools_callback hb10"),
                InlineKeyboardButton(
                    text="ǫυσᴛʟʏ", callback_data="tools_callback hb11"
                ),
                InlineKeyboardButton(
                    text="ᴛʀ - ᴅʜ", callback_data="tools_callback hb12"
                ),
            ],
            [InlineKeyboardButton(text="✯  𝐆𝐄𝐑𝐢° ✯", callback_data=f"feature")],
        ]
    )

    await callback_query.message.edit(
        f"``**dαhα fαzlα вí̇lgí̇ í̇çí̇n αşαğídαkí̇ вutσnlαrα tíklαчíníz. hєrhαngí̇ вí̇r sσrunlα kαrşílαşíчσrsαníz вurαчα чαzín [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.](t.me/SohbetAlemi)**\n\n**𝐁𝐔̈𝐓𝐔̈𝐍 𝐊𝐎𝐌𝐔𝐓𝐋𝐀𝐑𝐈 𝐁𝐔 𝐒𝐈̇𝐌𝐆𝐄 𝐈̇𝐋𝐄 𝐊𝐔𝐋𝐋𝐀𝐍𝐈𝐍: /**``",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("back_to_music"))
async def feature_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(
                text="⚜️ 𝐄𝐊𝐋𝐄 𝐁𝐄𝐍𝐈̇° ⚜️",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text=" 𝐌𝐔̈𝐙𝐈̇𝐊° ", callback_data="music"),
            InlineKeyboardButton(text=" 𝐘𝐎̈𝐍𝐄𝐓𝐈̇𝐌° ", callback_data="management"),
        ],
        [
            InlineKeyboardButton(text=" 𝐀𝐑𝐀𝐂̧𝐋𝐀𝐑° ", callback_data="tools"),
            InlineKeyboardButton(text=" 𝐇𝐄𝐏𝐒𝐈̇° ", callback_data="settings_back_helper"),
        ],
        [InlineKeyboardButton(text="✯ 𝐀𝐍𝐀 𝐌𝐄𝐍𝐔̈° ✯", callback_data="go_to_start")],
    ]

    k = f"""**❖ 𝐇𝐄𝐘𝐘𝐘𝐎 {app.mention} ! 

━━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━━
❖ ᴛʜɪs ɪs ϻᴧηᴧɢєϻєηᴛ | ϻυsɪᴄ ʙσᴛ
❖ ησ ʟᴧɢ | ᴧᴅs ϻυsɪᴄ | ησ ᴘʀσϻσ
❖ 24x7 ʀυη | ʙєsᴛ sσυηᴅ ǫυᴧʟɪᴛʏ

Kısaca İyi Bot :)
━━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━━
❖ ᴄʟɪᴄᴋ ση ᴛʜє ʜєʟᴩ ʙυᴛᴛση ᴛσ ɢєᴛ ɪηғσ
    ᴧʙσυᴛ ϻʏ ϻσᴅυʟєs ᴧηᴅ ᴄσϻϻᴧηᴅs...!

Aşağıdaki Butonlara Dikkat et...
━━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━━**"""
    await callback_query.message.edit_text(
        text=k,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def back_to_music(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"music",
                ),
            ]
        ]
    )
    return upl


def back_to_tools(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"tools",
                ),
            ]
        ]
    )
    return upl


def back_to_management(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"management",
                ),
            ]
        ]
    )
    return upl


@app.on_callback_query(filters.regex("about"))
async def about_callback(client: Client, callback_query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="✨ 𝐘𝐀𝐙𝐈𝐋𝐈𝐌° ✨", callback_data="developer"),
            InlineKeyboardButton(text="⚡ 𝐎̈𝐙𝐄𝐋𝐋𝐈̇𝐊𝐋𝐄𝐑° ⚡", callback_data="feature"),
        ],
        [
            InlineKeyboardButton(text="📓 𝐊𝐔𝐋𝐋𝐀𝐍𝐌𝐀 𝐊𝐋𝐀𝐕𝐔𝐙𝐔° 📓", callback_data="basic_guide"),
            InlineKeyboardButton(text="⚜️ 𝐘𝐀𝐑𝐃𝐈𝐌° ⚜️", callback_data="donate"),
        ],
        [InlineKeyboardButton(text="🔙 𝐆𝐄𝐑𝐢° ", callback_data="go_to_start")],
    ]
    await callback_query.message.edit_text(
        f"**𝐇𝐄𝐘𝐘𝐘𝐎 {app.mention} ✨**\n\n**ɢʀᴜʙᴜɴᴜᴢ ɪ̇ᴄ̧ɪ̇ɴ sɪ̇ᴢᴇ sᴘᴀᴍ'sɪᴢ ᴠᴇ ᴇɢ̆ʟᴇɴᴄᴇʟɪ̇ ʙɪ̇ʀ ᴏʀᴛᴀᴍ sᴜɴᴀɴ ɢᴜ̈ᴄ̧ʟᴜ̈ ᴠᴇ ʜᴀʀɪ̇ᴋᴀ ʙɪ̇ʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴜᴘ ʏᴏ̈ɴᴇᴛɪ̇ᴍɪ̇ ᴠᴇ ᴍᴜ̈ᴢɪ̇ᴋ ᴄ̧ᴀʟᴀʀ ʙᴏᴛᴜ :)**\n\n**● kullαnícílαrí kísítlαчαвí̇lí̇rí̇m.**\n**● kullαnícílαrí kí̇şí̇sєllєştí̇rí̇lєвí̇lí̇r hσşgєldí̇ní̇z mєsαjlαríчlα sєlαmlαчαвí̇lí̇r vє hαttα вí̇r grup kurαllαrí вєlí̇rlєчєвí̇lí̇rí̇m.**\n**● müzí̇k çαlαr sí̇stєmí̇m vαr.**\n**● вαn, mutє, hσşgєldí̇ní̇z, kíck, fєdєrαsчσn dαhα вí̇rçσk gí̇вí̇ grup чσ̈nєtí̇m σ̈zєllí̇klєrí̇ní̇n hєmєn tümünє sαhí̇вí̇m.**\n**● вí̇r nσt tutmα sí̇stєmí̇m, kαrα lí̇stєlєrí̇m vє hαttα вєlí̇rlí̇ αnαhtαr kєlí̇mєlєrє í̇lí̇şkí̇n σ̈ncєdєn вєlí̇rlєnmí̇ş cєvαplαrím vαr.**\n**● hєrhαngí̇ вí̇r kσmutu vє dαhα fαzlα í̇şlєmí̇ чürütmєdєn σ̈ncє чσ̈nєtí̇cí̇ í̇zí̇nlєrí̇ní̇ kσntrσl єdí̇чσrum. **\n\n**➻ 𝐁𝐎𝐓 𝐇𝐀𝐊𝐊𝐈𝐍𝐃𝐀 𝐃𝐀𝐇𝐀 𝐅𝐀𝐙𝐋𝐀 𝐁𝐈̇𝐋𝐆𝐈̇ 𝐀𝐋𝐌𝐀𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐃𝐔̈𝐆̆𝐌𝐄𝐘𝐄 𝐓𝐈𝐊𝐋𝐀𝐘𝐈𝐍 🦚.**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# If the back button has different meanings in various panels, you can set different callbacks
@app.on_callback_query(filters.regex("support"))
async def back_button_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(text="🎭ᴏᴡɴᴇʀ🎭", user_id=config.OWNER_ID[0]),
            InlineKeyboardButton(
                text="🌱ɢɪᴛʜᴜʙ🌱",
                url="https://github.com/AdanaliMuhendis",
            ),
        ],
        [
            InlineKeyboardButton(text="⛅ɢʀᴏᴜᴘ⛅", url=f"{config.SUPPORT_GROUP}"),
            InlineKeyboardButton(text="🎄ᴄʜᴀɴɴᴇʟ🎄", url=f"{config.SUPPORT_CHANNEL}"),
        ],
        [InlineKeyboardButton(text="✯ 𝐀𝐍𝐀 𝐌𝐄𝐍𝐔̈° ✯", callback_data="go_to_start")],
    ]

    await callback_query.message.edit_text(
        "**๏ 𝐇𝐀𝐊𝐊𝐈𝐌𝐃𝐀 𝐃𝐀𝐇𝐀 𝐅𝐀𝐙𝐋𝐀 𝐁𝐈̇𝐋𝐆𝐈̇ 𝐀𝐋𝐌𝐀𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐃𝐔̈𝐆̆𝐌𝐄𝐘𝐄 𝐓𝐈𝐊𝐋𝐀𝐘𝐈𝐍**\n\n**вσt'tα hєrhαngí̇ вí̇r hαtα, sσrun вulursαníz vєчα вσt hαkkíndα hєrhαngí̇ вí̇r gєrí̇ вí̇ldí̇rí̇m чαpmαk í̇stєrsєní̇z dєstєk gruвumuzα gєlєвí̇lí̇rsí̇ní̇z  (✿◠‿◠)**",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("donate"))
async def settings_back_callback(client: Client, callback_query: CallbackQuery):
    close = [[InlineKeyboardButton(text="✯ 𝐊𝐀𝐏𝐀𝐓° ✯", callback_data="close")]]
    await callback_query.message.reply_video(
        video="assets/AdanaliMuhendis.mp4",
        caption=f"**вσt'umun σ̈zєllí̇klєrí̇nє vє gєlí̇şí̇mí̇nє чαrdímcí σlmαk í̇çí̇n dσğrudαn вαnα mєsαj αtαвí̇lí̇rsí̇ní̇z...**\n\n** @AdanaliMuhendis",
        reply_markup=InlineKeyboardMarkup(close),
    )


@app.on_callback_query(filters.regex("basic_guide"))
async def settings_back_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton(text="✯ 𝐆𝐄𝐑𝐢°  ✯", callback_data="about")]]
    guide_text = f"**𝐇𝐄𝐘 ! 𝐁𝐔 𝐇𝐈𝐙𝐋𝐈 𝐕𝐄 𝐁𝐀𝐒𝐈̇𝐓 𝐁𝐈̇𝐑 𝐊𝐔𝐋𝐋𝐀𝐍𝐈𝐌 𝐊𝐈𝐋𝐀𝐕𝐔𝐙𝐔𝐃𝐔𝐑** {app.mention} **🎉**\n\n**𝟷. ᴛɪᴋʟᴀʏɪɴɪᴢ '⚜️ 𝐄𝐊𝐋𝐄 𝐁𝐄𝐍𝐈̇° ⚜️' ʙᴜᴛᴏɴᴜɴᴀ...**\n**𝟸. ʙᴏᴛᴜ ᴇᴋʟᴇʏᴇᴄᴇɢ̆ɪ̇ɴɪ̇ᴢ ɢʀᴜᴘ ɪ̇sᴍɪ̇ɴɪ̇ sᴇᴄ̧ɪ̇ɴɪ̇ᴢ...**\n**𝟹. ʙᴏᴛ'ᴀ sᴏʀᴜɴsᴜᴢ ᴠᴇ ᴛᴀᴍ ɪ̇şʟᴇᴠsᴇʟʟɪ̇ᴋ ɪ̇ᴄ̧ɪ̇ɴ ɢᴇʀᴇᴋʟɪ̇ ᴛᴜ̈ᴍ ɪ̇ᴢɪ̇ɴʟᴇʀɪ̇ ᴠᴇʀɪ̇ɴ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀᴀ ᴇʀɪ̇şᴍᴇᴋ ɪ̇ᴄ̧ɪ̇ɴ ᴍᴜ̈ᴢɪ̇ᴋ ᴠᴇʏᴀ ʏᴏ̈ɴᴇᴛɪ̇ᴍ ᴛᴇʀᴄɪ̇ʜʟᴇʀɪ̇ ᴀʀᴀsɪɴᴅᴀ sᴇᴄ̧ɪ̇ᴍ ʏᴀᴘᴀʙɪ̇ʟɪ̇ʀsɪ̇ɴɪ̇ᴢ.**\n**𝐇𝐄𝐑𝐇𝐀𝐍𝐆𝐈̇ 𝐁𝐈̇𝐑 𝐒𝐎𝐑𝐔𝐍𝐋𝐀 𝐊𝐀𝐑𝐒̧𝐈𝐑𝐒𝐀𝐍𝐈𝐙 𝐃𝐄𝐒𝐓𝐄𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐁𝐈̇𝐙𝐄 𝐔𝐋𝐀𝐒̧𝐌𝐀𝐊𝐓𝐀𝐍 𝐂̧𝐄𝐊𝐈̇𝐍𝐌𝐄𝐘𝐈̇𝐍...✨**"
    await callback_query.message.edit_text(
        text=guide_text, reply_markup=InlineKeyboardMarkup(keyboard)
    )