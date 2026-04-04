# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================


from SONALI_MUSIC import app
from SONALI_MUSIC.utils.database import get_assistant

from pyrogram import Client, filters, enums
from pyrogram.types import (
    ChatMemberUpdated,
    ChatJoinRequest,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

import asyncio
import random
import os
from logging import getLogger

LOGGER = getLogger(__name__)

mongo = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo["PURVI_DB"]
welcomedb = db["welcome_toggle_system"]

async def get_welcome(chat_id: int):
    data = await welcomedb.find_one({"chat_id": chat_id})
    if not data:
        return True
    return data.get("welcome", True)

async def enable_welcome(chat_id: int):
    await welcomedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome": True}},
        upsert=True
    )

async def disable_welcome(chat_id: int):
    await welcomedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome": False}},
        upsert=True
    )

class temp:
    MELCOW = {}

def circle(pfp, size=(500, 500), brightness_factor=10):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    pfp = ImageEnhance.Brightness(pfp).enhance(brightness_factor)
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chatname, id, uname, brightness_factor=1.3):
    background = Image.open("SONALI_MUSIC/assets/sona_wel.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp, brightness_factor=brightness_factor)
    pfp = pfp.resize((512, 512))

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('SONALI_MUSIC/assets/fonts.ttf', size=110)

    white = (255, 255, 255)

    draw.text((490, 778), f'{user}', fill=white, font=font)
    draw.text((315, 890), f'{id}', fill=white, font=font)
    draw.text((700, 1010), f"@{uname}", fill=white, font=font)

    background.paste(pfp, (162, 161), pfp)

    output_path = f"downloads/welcome#{id}.png"
    background.save(output_path)
    return output_path

@app.on_message(filters.command("welcome") & filters.group)
async def welcome_cmd(_, message: Message):

    chat = message.chat
    chat_id = chat.id

    user = await app.get_chat_member(chat_id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text("**» ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ʜᴀɴᴅʟᴇ ᴡᴇʟᴄᴏᴍᴇ ꜱʏꜱᴛᴇᴍ**")

    state = await get_welcome(chat_id)
    status = "ᴇɴᴀʙʟᴇᴅ" if state else "ᴅɪꜱᴀʙʟᴇᴅ"

    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data=f"wlc_on_{chat_id}"),
            InlineKeyboardButton("ᴅɪꜱᴀʙʟᴇ", callback_data=f"wlc_off_{chat_id}")
        ]
    ])

    await message.reply_text(
        f"» ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴇʟᴄᴏᴍᴇ ꜱᴛᴀᴛᴜꜱ **{status}** ɪɴ **{chat.title}**",
        reply_markup=btn
    )

@app.on_callback_query(filters.regex("wlc_"))
async def welcome_toggle(_, query):

    data = query.data.split("_")
    action = data[1]
    chat_id = int(data[2])

    member = await app.get_chat_member(chat_id, query.from_user.id)
    if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ 🥺", show_alert=True)

    if action == "on":
        await enable_welcome(chat_id)
        new_status = "ᴇɴᴀʙʟᴇᴅ"
    else:
        await disable_welcome(chat_id)
        new_status = "ᴅɪꜱᴀʙʟᴇᴅ"

    chat = await app.get_chat(chat_id)

    await query.message.edit_text(
        f"» ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ **{new_status}** ɪɴ **{chat.title}** ʙʏ :- **{query.from_user.mention}**"
    )

    await query.answer()

@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):

    chat_id = member.chat.id

    is_enabled = await get_welcome(chat_id)
    if not is_enabled:
        return

    user = member.new_chat_member.user if member.new_chat_member else None
    if not user:
        return

    if member.new_chat_member and not member.old_chat_member and member.new_chat_member.status != "kicked":

        count = await app.get_chat_members_count(chat_id)
        premium_count = 0
        deleted_count = 0
        
        async for member_user in app.get_chat_members(chat_id):
            if member_user.user.is_premium:
                premium_count += 1
            if member_user.user.is_deleted:
                deleted_count += 1

        try:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        except:
            pic = "SONALI_MUSIC/assets/upic.png"

        old = temp.MELCOW.get(f"welcome-{chat_id}")
        if old:
            try:
                await old.delete()
            except:
                pass

        welcomeimg = welcomepic(pic, user.first_name, member.chat.title, user.id, user.username)

        msg = await app.send_photo(
            chat_id,
            photo=welcomeimg,
            caption=f"""
**❅────✦ ᴡᴇʟᴄᴏᴍᴇ ✦────❅**

▰▰▰▰▰▰▰▰▰▰▰▰▰
**➻ ɢᴄ ɴᴀᴍᴇ »** {member.chat.title}
▰▰▰▰▰▰▰▰▰▰▰▰▰

**➻ ɴᴀᴍᴇ »** {user.mention}
**➻ ɪᴅ »** `{user.id}`
**➻ ᴜ_ɴᴀᴍᴇ »** @{user.username}
**➻ ᴘʀᴇᴍɪᴜᴍ »** {'ʏᴇꜱ ✨' if user.is_premium else 'ɴᴏ'}
**➻ ꜱᴄᴀᴍ »** {'ʏᴇꜱ ⚠️' if user.is_scam else 'ɴᴏ'}
**➻ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ »** `{count}`
**➻ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ »** `{premium_count}`
**➻ ᴢᴏᴍʙɪᴇ ᴜꜱᴇʀꜱ »** `{deleted_count}`

▰▰▰▰▰▰▰▰▰▰▰▰▰
**➻ ᴛʜᴀɴᴋs ғᴏʀ ᴊᴏɪɴɪɴɢ ᴜs ⚡️~!
❅─────✧❅✦❅✧─────❅**
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{app.username}?startgroup=true")],
                [
                    InlineKeyboardButton("ᴠɪᴇᴡ ᴜꜱᴇʀ", url=f"tg://openmessage?user_id={user.id}"),
                    InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/kuruvisupport")
                ]
            ])
        )

        
        async def delete_welcome():
            await asyncio.sleep(300)  
            try:
                await msg.delete()
                if f"welcome-{chat_id}" in temp.MELCOW:
                    del temp.MELCOW[f"welcome-{chat_id}"]
            except:
                pass

        asyncio.create_task(delete_welcome())
        
        temp.MELCOW[f"welcome-{chat_id}"] = msg


# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
