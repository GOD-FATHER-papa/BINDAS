# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import OWNER_ID as owner_id
from SONALI_MUSIC import app

def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@app.on_message(filters.command("bug"))
async def bugs(_, msg: Message):
    if msg.chat.username:
        chat_username = f"@{msg.chat.username}/`{msg.chat.id}`"
    else:
        chat_username = f"ᴩʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴩ/`{msg.chat.id}`"

    bugs = content(msg)
    
    user_id = msg.from_user.id
    mention = f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"
  
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    owner_user = await app.get_users(owner_id)
    owner_mention = f"[{owner_user.first_name}](tg://user?id={owner_id})"

    bug_report = f"""
**#ɴᴇᴡ_ʙᴜɢ_ʀᴇᴘᴏʀᴛ**

**ʜᴇʟʟᴏ {owner_mention} ᴀ ɴᴇᴡ ʙᴜɢ ғᴏᴜɴᴅ**

**ʀᴇᴩᴏʀᴛᴇᴅ ʙʏ :-** {mention}
**ᴜsᴇʀ ɪᴅ :-** `{user_id}`
**ᴄʜᴀᴛ :-** {chat_username}

**ʙᴜɢ :-** `{bugs}`

**ᴇᴠᴇɴᴛ sᴛᴀᴍᴩ :-** {datetimes}"""

    if msg.chat.type == "private":
        await msg.reply_text("<b>» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴩs.</b>")
        return

    if user_id == owner_id:
        if bugs:
            await msg.reply_text(
                "<b>» ᴀʀᴇ ʏᴏᴜ ᴄᴏᴍᴇᴅʏ ᴍᴇ 🤣, ʏᴏᴜ'ʀᴇ ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ʙᴏᴛ.</b>",
            )
            return
        else:
            await msg.reply_text("ᴄʜᴜᴍᴛɪʏᴀ ᴏᴡɴᴇʀ!")
    elif user_id != owner_id:
        if bugs:
            await msg.reply_text(
                f"<b>ʙᴜɢ ʀᴇᴩᴏʀᴛ : {bugs}</b>\n\n"
                "<b>» ʙᴜɢ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴩᴏʀᴛᴇᴅ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ !</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="close_data")]]
                ),
            )
            await app.send_photo(
                -1003979103138,
                photo="https://files.catbox.moe/1b1wap.jpg",
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("⌯ ᴠɪᴇᴡ ʙᴜɢ ⌯", url=f"{msg.link}"),
                        InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="close_send_photo")
                    ]
                    ]
                ),
            )
        else:
            await msg.reply_text(
                f"<b>» ɴᴏ ʙᴜɢ ᴛᴏ ʀᴇᴩᴏʀᴛ. ᴛʀʏ `/bug not work` ɪɴ ᴍsɢ ʀᴇᴘʟʏ</b>",
            )




@app.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_,  query :CallbackQuery):
    is_admin = await app.get_chat_member(query.message.chat.id, query.from_user.id)
    if not is_admin.privileges.can_delete_messages:
        await query.answer("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʀɪɢʜᴛs ᴛᴏ ᴄʟᴏsᴇ ᴛʜɪs.", show_alert=True)
    else:
        await query.message.delete()

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
