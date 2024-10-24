import re
from math import ceil
from typing import Union

from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from config import BANNED_USERS, START_IMG_URL
from strings import get_command, get_string
from ChampuMusic import HELPABLE, app
from ChampuMusic.utils.database import get_lang, is_commanddelete_on
from ChampuMusic.utils.decorators.language import LanguageStart
from ChampuMusic.utils.inline.help import private_help_panel

### Command
HELP_COMMAND = get_command("HELP_COMMAND")

COLUMN_SIZE = 4  # number of  button height
NUM_COLUMNS = 3  # number of button width
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
from ChampuMusic import app
from ChampuMusic.utils.decorators.language import languageCB


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


@app.on_callback_query(filters.regex("developer"))
async def about_callback(client: Client, callback_query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text=" 𝐒𝐀𝐇𝐈̇𝐏° ", user_id=config.OWNER_ID[0])
        ],
        [
            InlineKeyboardButton(text=" ɪɴsᴛᴀ ", url=f"https://www.instagram.com/AdanaliMuhendis/"),
            InlineKeyboardButton(text=" ʏᴏᴜᴛᴜʙᴇ ", url=f"https://www.youtube.com/@AdanaliMuhendis"),
        ],
        [
            InlineKeyboardButton(text="🔙 𝐆𝐄𝐑𝐢°", callback_data="about")
        ],  # Use a default label for the back button
    ]
    await callback_query.message.edit_text(
        "✦ **𝐁𝐔 𝐁𝐎𝐓, 𝐆𝐑𝐔𝐁𝐔𝐍𝐔𝐙𝐔 𝐘𝐎̈𝐍𝐄𝐓𝐌𝐄𝐘𝐈̇ 𝐊𝐎𝐋𝐀𝐘 𝐕𝐄 𝐃𝐀𝐇𝐀 𝐄𝐆̆𝐋𝐄𝐍𝐂𝐄𝐋𝐈̇ 𝐇𝐀𝐋𝐄 𝐆𝐄𝐓𝐈̇𝐑𝐌𝐄𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐘𝐄𝐓𝐄𝐍𝐄𝐊𝐋𝐈̇ 𝐁𝐈̇𝐑 𝐆𝐄𝐋𝐈̇𝐒̧𝐓𝐈̇𝐑𝐈̇𝐂𝐈̇ 𝐓𝐀𝐑𝐀𝐅𝐈𝐍𝐃𝐀𝐍 𝐘𝐀𝐏𝐈𝐋𝐌𝐈𝐒̧𝐓𝐈𝐑..**\n\n✦ **чαlnízcα вí̇rkαç tíklαmα í̇lє hєr şєчí̇ kσntrσl єdєвí̇lí̇rsí̇ní̇z (sαhí̇вí̇n αчαrlαríní αчαrlαmαk, sudσєrs'í kσntrσl єtmєk vє hαttα hαttα вí̇rkαç tíklαmα í̇lє hєr şєчí̇ kσntrσl єdєвí̇lí̇rsí̇ní̇z.) ínstαgrαm vє чσutuвє'u kєşfєdí̇n.**\n\n✦ **𝙱𝙾𝚃, 𝙶𝚁𝚄𝙱𝚄𝙽𝚄𝚉𝚄 𝚂𝙾𝚁𝚄𝙽𝚂𝚄𝚉 𝙱𝙸̇𝚁 𝚂̧𝙴𝙺𝙸̇𝙻𝙳𝙴 𝚈𝙾̈𝙽𝙴𝚃𝙼𝙴𝙽𝙸̇𝚉𝙴 𝚅𝙴 𝙼𝚄̈𝚉𝙸̇𝙶̆𝙸̇𝙽 𝙺𝙴𝚈𝙵𝙸̇𝙽𝙸̇ 𝙲̧𝙸𝙺𝙰𝚁𝙼𝙰𝙽𝙸𝚉𝙰 𝚈𝙰𝚁𝙳𝙸𝙼𝙲𝙸 𝙾𝙻𝙼𝙰𝙺 𝙸̇𝙲̧𝙸̇𝙽 𝚃𝙰𝚂𝙰𝚁𝙻𝙰𝙽𝙳𝙸. 𝚂𝙰𝙳𝙴𝙲𝙴 𝙰𝚂̧𝙰𝙶̆𝙸𝙳𝙰𝙺𝙸̇ 𝙳𝚄̈𝙶̆𝙼𝙴𝙻𝙴𝚁𝙸̇ 𝙺𝚄𝙻𝙻𝙰𝙽𝙸𝙽 𝚅𝙴 𝙽𝙴 𝙺𝙰𝙳𝙰𝚁 𝙺𝙾𝙻𝙰𝚈 𝙾𝙻𝙳𝚄𝙶̆𝚄𝙽𝚄 𝙶𝙾̈𝚁𝚄̈𝙽!**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("feature"))
async def feature_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(
                text="⚜️ 𝙱𝚎𝚗𝚒 𝙶𝚛𝚞𝚋𝚞𝚗𝚊 𝙴𝚔𝚕𝚎° ⚜️",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="🎧 𝐌𝐔̈𝐙𝐈̇𝐊° 🎧", callback_data="music"),
            InlineKeyboardButton(text="♻️ 𝐇𝐄𝐏𝐒𝐈̇° ♻️", callback_data="settings_back_helper"),
        ],
        [InlineKeyboardButton(text="✯ 𝐀𝐍𝐀 𝐌𝐄𝐍𝐔̈° ✯", callback_data="go_to_start")],
    ]
    await callback_query.message.edit_text(
        f"**𝐇𝐎𝐒̧𝐆𝐄𝐋𝐃𝐈̇𝐍𝐈̇𝐙** {app.mention}\n\n**MÜZİK DENEYİMİNİZİ GELİŞTİRMEK İÇİN TASARLANMIŞ ÇEŞİTLİ ÖZELLİKLERİ KEŞFEDİN. BOT'U KENDİ GRUBUNUZA VEYA KANALINIZA DAVET ETMEK VE KUSURSUZ MÜZİK ENTEGRASYONUNUN KEYFİNİ ÇIKARMAK İÇİN 𝙱𝚎𝚗𝚒 𝙶𝚛𝚞𝚋𝚞𝚗𝚊 𝙴𝚔𝚕𝚎° BUTONUNA TIKLAYINIZ**",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("music"))
async def music_callback(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="YÖNETiCi°", callback_data="music_callback hb1"),
                InlineKeyboardButton(text="YETKİLİ°", callback_data="music_callback hb2"),
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
            [InlineKeyboardButton(text="✯ 𝐆𝐄𝐑𝐢° ✯", callback_data=f"feature")],
        ]
    )

    await callback_query.message.edit(
        f"**DAHA FAZLA BİLGİ İÇİN AŞAĞIDAKİ BUTONLARA TIKLAYINIZ. HERHANGİ BİR SORUNLA KARŞILAŞIYORSANIZ [SUPPORT CHAT](t.me/AdanaliMuhendis)**\n\n**BÜTÜN KOMUTLAR ŞUNLARLA KULLANILABİLİR: /**",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("back_to_music"))
async def feature_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(
                text="⚜️ 𝙱𝚎𝚗𝚒 𝙶𝚛𝚞𝚋𝚞𝚗𝚊 𝙴𝚔𝚕𝚎° ⚜️",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="🎧 𝐌𝐔̈𝐙𝐈̇𝐊° 🎧", callback_data="music"),
            InlineKeyboardButton(text="♻️ 𝐇𝐄𝐏𝐒𝐈̇° ♻️", callback_data="settings_back_helper"),
        ],
        [InlineKeyboardButton(text="✯ 𝐀𝐍𝐀 𝐌𝐄𝐍𝐔̈° ✯", callback_data="go_to_start")],
    ]
    await callback_query.message.edit_text(
        f"**𝐇𝐎𝐒̧𝐆𝐄𝐋𝐃𝐈̇𝐍𝐈̇𝐙** {app.mention}\n\n**MÜZİK DENEYİMİNİZİ GELİŞTİRMEK İÇİN TASARLANMIŞ ÇEŞİTLİ ÖZELLİKLERİ KEŞFEDİN. BOT'U KENDİ GRUBUNUZA VEYA KANALINIZA DAVET ETMEK VE KUSURSUZ MÜZİK ENTEGRASYONUNUN KEYFİNİ ÇIKARMAK İÇİN 𝙱𝚎𝚗𝚒 𝙶𝚛𝚞𝚋𝚞𝚗𝚊 𝙴𝚔𝚕𝚎° BUTONUNA TIKLAYINIZ**",
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


@app.on_callback_query(filters.regex("about"))
async def about_callback(client: Client, callback_query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="✨𝐒𝐀𝐇𝐈̇𝐏°✨", callback_data="developer"),
            InlineKeyboardButton(text="⚡𝐎̈𝐙𝐄𝐋𝐋𝐈̇𝐊°⚡", callback_data="feature"),
        ],
        [
            InlineKeyboardButton(text="📓𝐓𝐄𝐌𝐄𝐋 𝐊𝐈𝐋𝐀𝐕𝐔𝐙°📓", callback_data="basic_guide"),
            InlineKeyboardButton(text="⚜️𝐁𝐀𝐆̆𝐈𝐒̧°⚜️", callback_data="donate"),
        ],
        [InlineKeyboardButton(text="🔙 𝐆𝐄𝐑𝐢°", callback_data="go_to_start")],
    ]
    await callback_query.message.edit_text(
        f"**Selamlar {app.mention} ✨**\n\n**𝙶𝚁𝚄𝙿𝙻𝙰𝚁𝙸𝙽𝙸𝚉 𝙸̇𝙲̧𝙸̇𝙽 𝚂𝙿𝙰𝙼'𝚂𝙸𝚉 𝚅𝙴 𝙴𝙶̆𝙻𝙴𝙽𝙲𝙴𝙻𝙸̇ 𝙱𝙸̇𝚁 𝙾𝚁𝚃𝙰𝙼 𝚂𝚄𝙽𝙰𝙽 𝙶𝚄̈𝙲̧𝙻𝚄̈ 𝚅𝙴 𝙼𝚄𝙷𝚃𝙴𝚂̧𝙴𝙼 𝙱𝙸̇𝚁 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝙶𝚁𝚄𝙿 𝚈𝙾̈𝙽𝙴𝚃𝙸̇𝙼𝙸̇ 𝚅𝙴 𝙼𝚄̈𝚉𝙸̇𝙺 𝙲̧𝙰𝙻𝙰𝚁 :)**\𝚗\𝚗**● 𝙺𝚄𝙻𝙻𝙰𝙽𝙸𝙲𝙸𝙻𝙰𝚁𝙸 𝙺𝙸𝚂𝙸𝚃𝙻𝙰𝚈𝙰𝙱𝙸̇𝙻𝙸̇𝚁𝙸̇𝙼.**\𝚗**● 𝙺𝚄𝙻𝙻𝙰𝙽𝙸𝙲𝙸𝙻𝙰𝚁𝙸 𝚂̧𝚄𝙽𝙻𝙰𝚁𝙻𝙰 𝚂𝙴𝙻𝙰𝙼𝙻𝙰𝚈𝙰𝙱𝙸̇𝙻𝙸̇𝚁𝙸̇𝙼 𝙾̈𝚉𝙴𝙻𝙻𝙴𝚂̧𝚃𝙸̇𝚁𝙸̇𝙻𝙴𝙱𝙸̇𝙻𝙸̇𝚁 𝙷𝙾𝚂̧𝙶𝙴𝙻𝙳𝙸̇𝙽𝙸̇𝚉 𝙼𝙴𝚂𝙰𝙹𝙻𝙰𝚁𝙸 𝚅𝙴 𝙷𝙰𝚃𝚃𝙰 𝙱𝙸̇𝚁 𝙶𝚁𝚄𝙿 𝙺𝚄𝚁𝙰𝙻𝙻𝙰𝚁𝙸 𝙱𝙴𝙻𝙸̇𝚁𝙻𝙴𝚈𝙸̇𝙽.**\𝚗**● 𝙱𝙸̇𝚁 𝙼𝚄̈𝚉𝙸̇𝙺 𝙾𝚈𝙽𝙰𝚃𝙸𝙲𝙸 𝚂𝙸̇𝚂𝚃𝙴𝙼𝙸̇𝙼 𝚅𝙰𝚁.**\𝚗**● 𝙽𝙴𝚁𝙴𝙳𝙴𝚈𝚂𝙴 𝚃𝚄̈𝙼 𝙱𝙴𝙺𝙻𝙴𝙽𝙴𝙽 𝙶𝚁𝚄𝙿 𝚈𝙾̈𝙽𝙴𝚃𝙸̇𝙼 𝙾̈𝚉𝙴𝙻𝙻𝙸̇𝙺𝙻𝙴𝚁𝙸̇𝙼 𝚅𝙰𝚁, 𝙱𝙰𝙽, 𝚂𝙴𝚂𝚂𝙸̇𝚉, 𝙷𝙾𝚂̧𝙶𝙴𝙻𝙳𝙸̇𝙽𝙸̇𝚉, 𝙺𝙸𝙲𝙺, 𝙵𝙴𝙳𝙴𝚁𝙰𝚂𝚈𝙾𝙽, 𝚅𝙴 𝙳𝙰𝙷𝙰 𝙵𝙰𝚉𝙻𝙰𝚂𝙸.**\𝚗**● 𝙱𝙸̇𝚁 𝙽𝙾𝚃 𝚃𝚄𝚃𝙼𝙰 𝚂𝙸̇𝚂𝚃𝙴𝙼𝙸̇𝙼, 𝙺𝙰𝚁𝙰 𝙻𝙸̇𝚂𝚃𝙴𝙻𝙴𝚁𝙸̇𝙼 𝚅𝙴 𝙷𝙰𝚃𝚃𝙰 𝙱𝙴𝙻𝙸̇𝚁𝙻𝙸̇ 𝙰𝙽𝙰𝙷𝚃𝙰𝚁 𝙺𝙴𝙻𝙸̇𝙼𝙴𝙻𝙴𝚁𝙻𝙴 𝙸̇𝙻𝙶𝙸̇𝙻𝙸̇ 𝙾̈𝙽𝙲𝙴𝙳𝙴𝙽 𝙱𝙴𝙻𝙸̇𝚁𝙻𝙴𝙽𝙼𝙸̇𝚂̧ 𝙲𝙴𝚅𝙰𝙿𝙻𝙰𝚁𝙸𝙼 𝚅𝙰𝚁.**\𝚗**● 𝙷𝙴𝚁𝙷𝙰𝙽𝙶𝙸̇ 𝙱𝙸̇𝚁 𝙺𝙾𝙼𝚄𝚃 𝚅𝙴 𝙳𝙰𝙷𝙰 𝙵𝙰𝚉𝙻𝙰 𝚂̧𝙴𝚈𝙸̇ 𝚈𝚄̈𝚁𝚄̈𝚃𝙼𝙴𝙳𝙴𝙽 𝙾̈𝙽𝙲𝙴 𝚈𝙾̈𝙽𝙴𝚃𝙸̇𝙲𝙸̇𝙻𝙴𝚁𝙸̇𝙽 𝙸̇𝚉𝙸̇𝙽𝙻𝙴𝚁𝙸̇𝙽𝙸̇ 𝙺𝙾𝙽𝚃𝚁𝙾𝙻 𝙴𝙳𝙸̇𝙽. **\𝚗\𝚗**➻ 𝙱𝙾𝚃 𝙷𝙰𝙺𝙺𝙸𝙽𝙳𝙰 𝙳𝙰𝙷𝙰 𝙵𝙰𝚉𝙻𝙰 𝙱𝙸̇𝙻𝙶𝙸̇ 𝙰𝙻𝙼𝙰𝙺 𝙸̇𝙲̧𝙸̇𝙽 𝙳𝚄̈𝙶̆𝙼𝙴𝚈𝙴 𝚃𝙸𝙺𝙻𝙰𝚈𝙸𝙽 🦚.**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# If the back button has different meanings in various panels, you can set different callbacks
@app.on_callback_query(filters.regex("support"))
async def back_button_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(text="🎭𝐒𝐀𝐇𝐈̇𝐏°🎭", user_id=config.OWNER_ID[0]),
            InlineKeyboardButton(
                text="🌱ɢɪᴛʜᴜʙ🌱",
                url="https://github.com/AdanaliMuhendis",
            ),
        ],
        [
            InlineKeyboardButton(text="⛅𝐆𝐑𝐔𝐏°⛅", url=f"{config.SUPPORT_GROUP}"),
            InlineKeyboardButton(text="🎄𝐊𝐀𝐍𝐀𝐋°🎄", url=f"{config.SUPPORT_CHANNEL}"),
        ],
        [InlineKeyboardButton(text="✯ 𝐀𝐍𝐀 𝐌𝐄𝐍𝐔̈° ✯", callback_data="go_to_start")],
    ]

    await callback_query.message.edit_text(
        "**๏ 𝐇𝐀𝐊𝐊𝐈𝐌𝐃𝐀 𝐃𝐀𝐇𝐀 𝐅𝐀𝐙𝐋𝐀 𝐁𝐈̇𝐋𝐆𝐈̇ 𝐀𝐋𝐌𝐀𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐃𝐔̈𝐆̆𝐌𝐄𝐘𝐄 𝐓𝐈𝐊𝐋𝐀𝐘𝐈𝐍**\𝐧\𝐧**𝐁𝐎𝐓'𝐓𝐀 𝐇𝐄𝐑𝐇𝐀𝐍𝐆𝐈̇ 𝐁𝐈̇𝐑 𝐇𝐀𝐓𝐀 𝐕𝐄𝐘𝐀 𝐇𝐀𝐓𝐀 𝐁𝐔𝐋𝐔𝐑𝐒𝐀𝐍𝐈𝐙 𝐕𝐄𝐘𝐀 𝐁𝐎𝐓 𝐇𝐀𝐊𝐊𝐈𝐍𝐃𝐀 𝐇𝐄𝐑𝐇𝐀𝐍𝐆𝐈̇ 𝐁𝐈̇𝐑 𝐆𝐄𝐑𝐈̇ 𝐁𝐈̇𝐋𝐃𝐈̇𝐑𝐈̇𝐌 𝐕𝐄𝐑𝐌𝐄𝐊 𝐈̇𝐒𝐓𝐈̇𝐘𝐎𝐑𝐒𝐀𝐍𝐈𝐙 𝐃𝐄𝐒𝐓𝐄𝐊 𝐆𝐑𝐔𝐁𝐔𝐍𝐀 𝐆𝐄𝐋𝐈̇𝐍𝐈̇𝐙 (✿◠‿◠)* *",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("donate"))
async def settings_back_callback(client: Client, callback_query: CallbackQuery):
    close = [[InlineKeyboardButton(text="✯ 𝐊𝐀𝐏𝐀𝐓° ✯", callback_data="close")]]
    await callback_query.message.reply_photo(
        photo="https://te.legra.ph/Alem-Music-05-27",
        caption=f"**𝐀𝐥𝐞𝐦 𝐌𝐮̈𝐳𝐢𝐤 𝐁𝐨𝐭 HER GEÇEN GÜN DAHA DA GELİŞMEYE DEVAM EDECEKTİR!**",
        reply_markup=InlineKeyboardMarkup(close),
    )

#CAPTION AÇIKLAMASI : BOT'UMUN ÖZELLİKLERİNİ VE GELİŞİMİNİ GELİŞTİRMEYE YARDIMCI OLMAK İÇİN DOĞRUDAN BAĞIŞ YAPARAK KODLAMA YOLCULUĞUMU DESTEKLEYİN.**\n\n** KATKILARINIZ YENİLİKÇİ, KULLANICI DOSTU ARAÇLARIN VE HEYECAN VERİCİ BOT KABİLİYETLERİNİN OLUŞTURULMASINA DOĞRUDAN FON VERECEKTİR.**\n\n* *KODU TARAYIN VE ÖDEME YAPIN; ZORLUK YOK, YENİ ÖZELLİKLERİ HAYATA GETİRMENİN VE DESTEKLEMENİN HIZLI BİR YOLU.**\n\n** HER BAĞIŞ, BÜYÜK VEYA KÜÇÜK, BU PROJEYİ İLERLEMEDE ÇOK YOL AÇAR İLERİ. BU HEYECAN VERİCİ YOLCULUK OLDUĞUNUZ İÇİN TEŞEKKÜR EDERİZ!

@app.on_callback_query(filters.regex("basic_guide"))
async def settings_back_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton(text="✯ 𝐆𝐄𝐑𝐢° ✯", callback_data="about")]]
    guide_text = f"**𝐇𝐄𝐘! 𝐁𝐔 𝐇𝐈𝐙𝐋𝐈 𝐕𝐄 𝐁𝐀𝐒𝐈̇𝐓 𝐁𝐈̇𝐑 𝐊𝐔𝐋𝐋𝐀𝐍𝐈𝐌 𝐊𝐈𝐋𝐀𝐕𝐔𝐙𝐔𝐃𝐔𝐑** {app.mention} **🎉**\n\n**1. '𝙱𝚎𝚗𝚒 𝙶𝚛𝚞𝚋𝚞𝚗𝚊 𝙴𝚔𝚕𝚎°' Butonuna tıklayınız.**\n**2. Botu eklemek istediğiniz Grup/Kanal ismine tıklayınız.**\n**3. SORUNSUZ VE TAM İŞLEVSELLİK İÇİN BOT'A GEREKLİ TÜM İZİNLERİ VERİN.**\n\n**Kσmutlαrα єrí̇şmєk í̇çí̇n müzí̇k vєчα чσ̈nєtí̇m tєrcí̇hlєrí̇ αrαsíndα sєçí̇m чαpαвí̇lí̇rsí̇ní̇z.**\n**𝐇𝐀𝐋𝐀 𝐇𝐄𝐑𝐇𝐀𝐍𝐆𝐈̇ 𝐁𝐈̇𝐑 𝐒𝐎𝐑𝐔𝐍𝐋𝐀 𝐊𝐀𝐑𝐒̧𝐈𝐋𝐀𝐒̧𝐈𝐘𝐎𝐑𝐒𝐀𝐍𝐈𝐙 𝐃𝐄𝐒𝐓𝐄𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐁𝐈̇𝐙𝐄 𝐔𝐋𝐀𝐒̧𝐈𝐍𝐈𝐙... ✨**"
    await callback_query.message.edit_text(
        text=guide_text, reply_markup=InlineKeyboardMarkup(keyboard)
    )