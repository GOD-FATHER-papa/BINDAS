# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI_MUSIC import app
from config import OWNER_ID
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType, ChatMemberStatus
from strings import get_string
from SONALI_MUSIC.utils import SonaBin
from SONALI_MUSIC.utils.database import get_assistant, get_lang
from SONALI_MUSIC.core.call import Sona

async def is_admin(_, __, message):
    try:
        chat_member = await message.chat.get_member(message.from_user.id)
        return chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except:
        return False


@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    text = "**🫣 ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ 😆**"
    add_link = f"https://t.me/{app.username}?startgroup=true"
    reply_text = f"{text}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="๏ ᴊσɪη ᴠᴄ ๏", url=add_link)]
    ])

    await msg.reply(reply_text, reply_markup=reply_markup)



@app.on_message(filters.video_chat_ended)
async def brah2(_, msg: Message):
    text = "**😤 ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ 🙁**"
    add_link = f"https://t.me/{app.username}?startgroup=true"
    reply_text = f"{text}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="๏ ᴧᴅᴅ ϻє вᴧвყ ๏", url=add_link)]
    ])

    await msg.reply(reply_text, reply_markup=reply_markup)
    
@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    text = f"➠ {message.from_user.mention}\n\n**๏ ɪɴᴠɪᴛɪɴɢ ɪɴ ᴠᴄ ᴛᴏ ๏**\n\n**➠ **"
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
            x += 1
        except Exception:
            pass

    try:
        invite_link = await app.export_chat_invite_link(message.chat.id)
        add_link = f"https://t.me/{app.username}?startgroup=true"
        reply_text = f"{text} 🤭🤭"

        await message.reply(reply_text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text= "๏ ᴊσɪη ᴠᴄ ๏", url=add_link)],
        ]))
    except Exception as e:
        print(f"Error: {e}")



@app.on_message(
    filters.command(
        ["vcuser", "vcusers", "vcmember", "vcmembers", "cu", "cm"],
        prefixes=["/", "!", ".", "V", "v"]
    ) & filters.create(is_admin)
)
async def vc_members(client, message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")

    msg = await message.reply_text(_["V_C_1"])
    userbot = await get_assistant(message.chat.id)
    TEXT = ""

    try:
        async for m in userbot.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username
            is_hand_raised = m.is_hand_raised
            is_video_enabled = m.is_video_enabled
            is_left = m.is_left
            is_screen_sharing_enabled = m.is_screen_sharing_enabled
            is_muted = bool(m.is_muted and not m.can_self_unmute)
            is_speaking = not m.is_muted

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name

            TEXT += _["V_C_2"].format(
                title,
                chat_id,
                username,
                is_video_enabled,
                is_screen_sharing_enabled,
                is_hand_raised,
                is_muted,
                is_speaking,
                is_left,
            )
            TEXT += "\n\n"

        if len(TEXT) < 4000:
            await msg.edit(TEXT or _["V_C_3"])
        else:
            link = await SonaBin(TEXT)
            await msg.edit(
                _["V_C_4"].format(link),
                disable_web_page_preview=True,
            )
    except ValueError:
        await msg.edit(_["V_C_5"])


# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
