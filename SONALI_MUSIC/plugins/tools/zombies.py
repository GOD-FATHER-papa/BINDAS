# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
from typing import List

from pyrogram import Client, enums, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SONALI_MUSIC import app
from SONALI_MUSIC.utils.admin_check import is_admin

chatQueue: set[int] = set()
stopProcess: bool = False

async def scan_deleted_members(chat_id: int) -> List:
    return [member.user async for member in app.get_chat_members(chat_id) if member.user and member.user.is_deleted]

async def safe_edit(msg: Message, text: str):
    try:
        await msg.edit(text)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await msg.edit(text)
    except Exception:
        pass

@app.on_message(filters.command(["zombies"]))
async def prompt_zombie_cleanup(_: Client, message: Message):
    if not await is_admin(message):
        return await message.reply("**👮🏻 | ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")

    deleted_list = await scan_deleted_members(message.chat.id)
    if not deleted_list:
        return await message.reply("**⟳ | ɴᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")

    total = len(deleted_list)
    est_time = max(1, total // 5)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ ʏᴇs, ᴄʟᴇᴀɴ", callback_data=f"confirm_zombies:{message.chat.id}"),
                InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel_zombies"),
            ]
        ]
    )

    await message.reply(
        (
            f"**⚠️ | ғᴏᴜɴᴅ** `{total}` **ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.**\n"
            f"**⏳ | ᴇsᴛɪᴍᴀᴛᴇᴅ ᴄʟᴇᴀɴᴜᴘ ᴛɪᴍᴇ :-** `{est_time}s`\n\n"
            "ᴅ**ᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʟᴇᴀɴ ᴛʜᴇᴍ ??**"
        ),
        reply_markup=keyboard,
    )

@app.on_callback_query(filters.regex(r"^confirm_zombies"))
async def execute_zombie_cleanup(_: Client, cq: CallbackQuery):
    global stopProcess
    chat_id = int(cq.data.split(":")[1])

    if not await is_admin(cq):
        return await cq.answer("👮🏻 | ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄᴏɴғɪʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.", show_alert=True)

    if chat_id in chatQueue:
        return await cq.answer("⚠️ | ᴄʟᴇᴀɴᴜᴘ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴘʀᴏɢʀᴇss.", show_alert=True)

    bot_me = await app.get_chat_member(chat_id, "self")
    if bot_me.status != ChatMemberStatus.ADMINISTRATOR:
        return await cq.edit_message_text("**➠ | ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.**")

    chatQueue.add(chat_id)
    deleted_list = await scan_deleted_members(chat_id)
    total = len(deleted_list)

    status = await cq.edit_message_text(
        f"**🧭 | ғᴏᴜɴᴅ** `{total}` **ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.**\n**🥀 | sᴛᴀʀᴛɪɴɢ ᴄʟᴇᴀɴᴜᴘ...**"
    )

    removed = 0

    async def ban_member(user_id):
        try:
            await app.ban_chat_member(chat_id, user_id)
            return True
        except FloodWait as e:
            await asyncio.sleep(e.value)
            return await ban_member(user_id)
        except Exception:
            return False

    tasks = []
    for user in deleted_list:
        if stopProcess:
            break
        tasks.append(ban_member(user.id))

    batch_size = 20
    for i in range(0, len(tasks), batch_size):
        results = await asyncio.gather(*tasks[i:i + batch_size], return_exceptions=True)
        removed += sum(1 for r in results if r is True)
        await safe_edit(status, f"**♻️ | ʀᴇᴍᴏᴠᴇᴅ** `{removed}/{total}` **ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs...**")
        await asyncio.sleep(2)

    chatQueue.discard(chat_id)
    await safe_edit(status, f"**✅ | sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ** `{removed}` **ᴏᴜᴛ ᴏғ** `{total}` **ᴢᴏᴍʙɪᴇs.**")

@app.on_callback_query(filters.regex(r"^cancel_zombies$"))
async def cancel_zombie_cleanup(_: Client, cq: CallbackQuery):
    await cq.edit_message_text("**❌ | ᴄʟᴇᴀɴᴜᴘ ᴄᴀɴᴄᴇʟʟᴇᴅ.**")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
