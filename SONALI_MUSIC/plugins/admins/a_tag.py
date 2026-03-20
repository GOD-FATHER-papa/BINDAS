# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from SONALI_MUSIC import app

SPAM_CHATS = []

async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    return user_id in admin_ids

async def tag_all_admins(_, message):
    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "**» ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴏᴘ sᴏ ᴜsᴇ :-** `/cancel`"
        )

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "**ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ ᴀᴅᴍɪɴs, ʟɪᴋᴇ »** `@admin Hi Friends`"
        )
        return

    usernum = 0
    usertxt = ""
    text = message.text.split(None, 1)[1] if not replied else ""

    try:
        SPAM_CHATS.append(message.chat.id)
        async for m in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if message.chat.id not in SPAM_CHATS:
                break
            if m.user.is_deleted or m.user.is_bot:
                continue
            usernum += 1
            usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
            if usernum == 7:
                if replied:
                    await replied.reply_text(usertxt, disable_web_page_preview=True)
                else:
                    await app.send_message(
                        message.chat.id, f"{text}\n{usertxt}", disable_web_page_preview=True
                    )
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        if usernum != 0:
            if replied:
                await replied.reply_text(usertxt, disable_web_page_preview=True)
            else:
                await app.send_message(
                    message.chat.id, f"{text}\n\n{usertxt}", disable_web_page_preview=True
                )
    except FloodWait as e:
        await asyncio.sleep(e.value)
    finally:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass

@app.on_message(
    filters.command(["admin", "atag", "report"], prefixes=["/", "@"]) & filters.group
)
async def admintag_with_reporting(client, message):
    if not message.from_user:
        return
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    admins = [
        admin.user.id
        async for admin in client.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    if message.command[0] == "report" and from_user_id in admins:
        return await message.reply_text(
            "**» ᴏᴘᴘs! ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ!**\n\n**ʏᴏᴜ ᴄᴀɴ'ᴛ ʀᴇᴘᴏʀᴛ ᴀɴʏ ᴜsᴇʀs ᴛᴏ ᴀᴅᴍɪɴ**"
        )

    if from_user_id in admins:
        return await tag_all_admins(client, message)

    if len(message.text.split()) <= 1 and not message.reply_to_message:
        return await message.reply_text("**» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ᴛʜᴀᴛ ᴜsᴇʀ.**")

    reply = message.reply_to_message or message
    reply_user_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
    linked_chat = (await client.get_chat(chat_id)).linked_chat

    if reply_user_id == app.id:
        return await message.reply_text("ᴡʜʏ ᴡᴏᴜʟᴅ ɪ ʀᴇᴘᴏʀᴛ ᴍʏsᴇʟғ?")
    if reply_user_id in admins or reply_user_id == chat_id or (linked_chat and reply_user_id == linked_chat.id):
        return await message.reply_text(
            "**» ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴀᴛ ᴛʜᴇ ᴜsᴇʀ ʏᴏᴜ ᴀʀᴇ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ɪs ᴀɴ ᴀᴅᴍɪɴ?**"
        )

    user_mention = reply.from_user.mention if reply.from_user else "ᴛʜᴇ ᴜsᴇʀ"
    text = f"**» ʀᴇᴘᴏʀᴛᴇᴅ {user_mention} ᴛᴏ ᴀᴅᴍɪɴs!.**"

    for admin in admins:
        admin_member = await client.get_chat_member(chat_id, admin)
        if not admin_member.user.is_bot and not admin_member.user.is_deleted:
            text += f"[\u2063](tg://user?id={admin})"

    await reply.reply_text(text)


@app.on_message(
    filters.command(
        ["stoptag", "astop"],
        prefixes=["/", "@"],
    )
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass
        return await message.reply_text("**» ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ!**")
    else:
        await message.reply_text("**» ɴᴏ ᴘʀᴏᴄᴇss ᴏɴɢᴏɪɴɢ!**")
        return



# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
