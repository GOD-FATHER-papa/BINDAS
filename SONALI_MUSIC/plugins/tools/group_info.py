# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from SONALI_MUSIC import app
import os
import time
from asyncio import sleep

@app.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply("**ᴘʀᴏᴠɪᴅᴇ ᴀ ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ. ᴇxᴀᴍᴘʟᴇ :-** `/groupinfo @Isha_updates`")
        return
    
    group_username = message.command[1]
    
    try:
        group = await app.get_chat(group_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return
    
    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description
    premium_acc = banned = deleted_acc = bot = 0  

    response_text = (
        f"**➖➖➖➖➖➖➖➖➖**\n"
        f"**➲ GROUP NAME :-** {group.title}\n\n"
        f"**➲ GROUP ID :-** {group.id}\n"
        f"**➲ TOTAL MEMBERS :-** {total_members}\n"
        f"**➲ DESCRIPTION :-** {group_description or 'N/A'}\n"
        f"**➲ USERNAME :-** {group_username}\n\n"
        f"**➲ CHECK BY :- {app.mention}**\n"      
        f"**➖➖➖➖➖➖➖➖➖**"
    )
    
    await message.reply(response_text)


@app.on_message(~filters.private & filters.command(["groupdata"]), group=2)
async def instatus(app, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("**ɢᴇᴛᴛɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ...**")
        deleted_acc = 0
        premium_acc = 0
        banned = 0
        bot = 0
        uncached = 0
        async for ban in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for member in app.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(f"""
**➖➖➖➖➖➖➖➖➖
➲ NAME :- {message.chat.title} ✅
➲ MEMBERS :- [ {count} ]🫂
➖➖➖➖➖➖➖
➲ BOTS :- {bot}💡
➲ ZOMBIES :- {deleted_acc}🧟
➲ BANNED :- {banned}🚫
➲ PREMIUM USERS :- {premium_acc}🎁
➖➖➖➖➖➖➖➖➖
TIME TAKEN :- {timelog} S**""")
    else:
        sent_message = await message.reply_text("**ᴏɴʟʏ ᴀᴅᴍɪɴs ᴜsᴇ ᴛʜɪs !**")
        await sleep(5)
        await sent_message.delete()


@app.on_message(filters.command("gcstats") & filters.group)
async def group_status(client, message):
    chat = message.chat 
    status_text = (
        f"**ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ**\n\n"
        f"**ɢʀᴏᴜᴘ ɪᴅ :-** `{chat.id}`\n"
        f"**ᴛɪᴛʟᴇ :-** **{chat.title}**\n"
        f"**ᴛʏᴘᴇ :-** `{chat.type}`\n"
    )

   
    if chat.username:
        status_text += f"**ᴜsᴇʀɴᴀᴍᴇ :-** @{chat.username}\n"
    else:
        status_text += "**ᴜsᴇʀɴᴀᴍᴇ :-** None\n"

    await message.reply_text(status_text)
    

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
