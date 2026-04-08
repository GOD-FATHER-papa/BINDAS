# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# ======================================================
from pyrogram.enums import ParseMode
import os
from pyrogram import filters, enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from SONALI_MUSIC import app


@app.on_message(filters.command('id'))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**● [ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**● [ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**● [ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"
        except Exception:
            return await message.reply_text("● ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**● [ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n" if chat.username else f"**● ᴄʜᴀᴛ ɪᴅ:** `{chat.id}`\n\n"

    if (
        reply
        and not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**● [ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**● [ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"● ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"

    if reply and reply.sender_chat:
        text += f"● ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]]
        )
    )



INFO_TEXT = """
<u><b>👤 ᴜꜱᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b></u>

<b>● ғɪʀsᴛ ɴᴀᴍᴇ ➠</b> {first}
<b>● ʟᴀsᴛ ɴᴀᴍᴇ ➠</b> {last}
<b>● ᴜꜱᴇʀ ɪᴅ ➠</b> <code>{id}</code>
<b>● ᴜꜱᴇʀɴᴀᴍᴇ ➠</b> @{username}
<b>● ᴍᴇɴᴛɪᴏɴ ➠</b> {mention}
<b>● ꜱᴛᴀᴛᴜꜱ ➠</b> {status}
<b>● ᴅᴄ ɪᴅ ➠</b> {dcid}
<b>● ᴘʀᴇᴍɪᴜᴍ ➠</b> {premium}
<b>● ꜱᴄᴀᴍ ➠</b> {scam}

<b>● ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➠ <a href="@KURUVI_TELE">ᴋᴜʀᴜᴠɪ-ʙᴏᴛꜱ</a></b>
"""


# --- user online status ---
async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "ʀᴇᴄᴇɴᴛʟʏ"
        elif x == enums.UserStatus.LAST_WEEK:
            return "ʟᴀꜱᴛ ᴡᴇᴇᴋ"
        elif x == enums.UserStatus.LONG_AGO:
            return "ʟᴏɴɢ ᴀɢᴏ"
        elif x == enums.UserStatus.OFFLINE:
            return "ᴏꜰꜰʟɪɴᴇ"
        elif x == enums.UserStatus.ONLINE:
            return "ᴏɴʟɪɴᴇ"
    except:
        return "ᴇʀʀᴏʀ"


@app.on_message(filters.command(["info", "information", "userinfo", "whois"], prefixes=["/", "!"]))
async def userinfo(_, message: Message):
    try:
        
        if not message.reply_to_message and len(message.command) == 2:
            user_id = message.text.split(None, 1)[1]
        elif message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) == 1:
            return await message.reply_text("**✦ ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴜꜱᴇʀɴᴀᴍᴇ, ɪᴅ ᴏʀ ʀᴇᴘʟʏ ᴀꜰᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ.**")
        else:
            user_id = message.from_user.id

        
        user = await app.get_users(user_id)
        status = await userstatus(user.id)

        scam = "ʏᴇꜱ" if user.is_scam else "ɴᴏ"
        premium = "ʏᴇꜱ" if user.is_premium else "ɴᴏ"

        profile_url = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"

       
        await message.reply_text(
            text=INFO_TEXT.format(
                first=user.first_name or "N/A",
                last=user.last_name or "N/A",
                id=user.id,
                username=user.username or "N/A",
                mention=user.mention,
                status=status,
                dcid=user.dc_id or "N/A",
                premium=premium,
                scam=scam,
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{user.first_name}", url=profile_url)]]
            ),
            disable_web_page_preview=True,
        )

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
