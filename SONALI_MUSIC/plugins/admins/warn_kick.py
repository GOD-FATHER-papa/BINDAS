# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
from contextlib import suppress
from string import ascii_lowercase
from typing import Dict, Union

from pyrogram import filters, enums
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import (
    CallbackQuery,
    Message,
)

from SONALI_MUSIC import app
from SONALI_MUSIC.misc import SUDOERS
from SONALI_MUSIC.core.mongo import mongodb
from SONALI_MUSIC.utils.errors import capture_err
from SONALI_MUSIC.utils.keyboard import ikb
from SONALI_MUSIC.utils.database import save_filter
from SONALI_MUSIC.utils.functions import extract_user, extract_user_and_reason
from SONALI_MUSIC.utils.permissions import adminsOnly, member_permissions
from config import BANNED_USERS
from pyrogram.errors import ChatAdminRequired, UserNotParticipant


warnsdb = mongodb.warns


# ---------------------- HELPERS ---------------------- #

async def int_to_alpha(user_id: int) -> str:
    """Convert integer ID to a-z representation for db keys."""
    alphabet = list(ascii_lowercase)[:10]
    return "".join(alphabet[int(digit)] for digit in str(user_id))


async def get_warns_count() -> dict:
    """Get total warns and chats stored in DB."""
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    """Fetch all warns in a chat."""
    warns = await warnsdb.find_one({"chat_id": chat_id})
    return warns["warns"] if warns else {}


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    """Get single user's warn info."""
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    return warns.get(name)


async def add_warn(chat_id: int, name: str, warn: dict):
    """Add or update a warn for a user."""
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn
    await warnsdb.update_one({"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True)


async def remove_warns(chat_id: int, name: str) -> bool:
    """Remove all warns of a user."""
    name = name.lower().strip()
    warnsd = await get_warns(chat_id)
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one({"chat_id": chat_id}, {"$set": {"warns": warnsd}}, upsert=True)
        return True
    return False


# ---------------------- KICK COMMAND ---------------------- #

@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kick_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)

    if not user_id:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.**")
    if user_id == app.id:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.**")
    if user_id in SUDOERS:
        return await message.reply_text("**ʏᴏᴜ ᴡᴀɴɴᴀ ᴋɪᴄᴋ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ ?**")

    # Admin check
    chat_admins = [member.user.id async for member in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)]
    if user_id in chat_admins:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs.**")

    mention = (await app.get_users(user_id)).mention
    msg = f"""
**» ᴋɪᴄᴋᴇᴅ :-** {mention}

**» ᴋɪᴄᴋ ʙʏ :-** {message.from_user.mention if message.from_user else 'ᴀɴᴏɴᴍᴏᴜs'}
**» ʀᴇᴀsᴏɴ :-** {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ'}
"""

    await message.chat.ban_member(user_id)
    if message.reply_to_message:
        message = message.reply_to_message
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)

    # Silent kick deletes user messages
    if message.command[0].startswith("s") and message.reply_to_message:
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)



@app.on_message(filters.command("kickme"))
async def kickme_cmd(client, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘs.** 😅")

    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀᴅᴍɪɴs ᴏʀ ᴄʀᴇᴀᴛᴏʀs.** 😎")

        # Kick user
        await client.ban_chat_member(message.chat.id, message.from_user.id)
        await asyncio.sleep(3)
        await client.unban_chat_member(message.chat.id, message.from_user.id)

        # Goodbye message in smallcaps
        goodbye_msg = f"**👋 ʙʏᴇ ʙʏᴇ {message.from_user.mention}! ʜᴀᴠᴇ ᴀ ɴɪᴄᴇ ᴅᴀʏ!** 🌸"
        await message.reply_text(goodbye_msg)

    except ChatAdminRequired:
        await message.reply_text("**ɪ ɴᴇᴇᴅ ʙᴀɴ ᴘᴇʀᴍɪssɪᴏɴs.** ❌")
    except UserNotParticipant:
        await message.reply_text("**ʜᴍᴍ, ɪᴛ sᴇᴇᴍs ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.** 🤔")
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ :-** {e}")



# ---------------------- WARN COMMAND ---------------------- #

@app.on_message(filters.command(["warn", "swarn"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id

    if not user_id:
        return await message.reply_text("**ɪ ᴄᴀɴᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.**")
    if user_id == app.id:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏsᴇʟғ.**")
    if user_id in SUDOERS:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏ ᴍᴀɴᴀɢᴇʀ !!**")

    chat_admins = [member.user.id async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]
    if user_id in chat_admins:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴀɴ ᴀᴅᴍɪɴ.**")

    user, warns = await asyncio.gather(app.get_users(user_id), get_warn(chat_id, await int_to_alpha(user_id)))
    mention = user.mention
    keyboard = ikb({"🚨 ʀᴇᴍᴏᴠᴇ ᴡᴀʀɴ 🚨": f"unwarn_{user_id}"})
    warns = warns["warns"] if warns else 0

    # Delete replied message for silent warn
    if message.command[0].startswith("s") and message.reply_to_message:
        await message.reply_to_message.delete()
        await app.delete_user_history(chat_id, user_id)

    # Ban user if 3 warns reached
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"**ɴᴜᴍʙᴇʀ ᴏғ ᴡᴀʀɴs ᴏғ {mention} ᴇxᴄᴇᴇᴅᴇᴅ, ʙᴀɴɴᴇᴅ !!**")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**ᴡᴀʀɴᴇᴅ :-** {mention}
**ᴡᴀʀɴᴇᴅ ʙʏ :-** {message.from_user.mention if message.from_user else 'ᴀɴᴏɴᴍᴏᴜs'}
**ʀᴇᴀsᴏɴ :-** {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ'}
**ᴡᴀʀɴs :-** {warns + 1}/3
"""
        if message.reply_to_message:
            message = message.reply_to_message
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


# ---------------------- CALLBACK QUERY ---------------------- #

@app.on_callback_query(filters.regex("unwarn_") & ~BANNED_USERS)
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id

    permissions = await member_permissions(chat_id, from_user.id)
    if "can_restrict_members" not in permissions:
        return await cq.answer(
            f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs\n\nᴘᴇʀᴍɪssɪᴏɴ ɴᴇᴇᴅᴇᴅ - can_restrict_members",
            show_alert=True,
        )

    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    warns = warns["warns"] if warns else 0

    if warns == 0:
        return await cq.answer("ᴜsᴇʀ ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.")

    await add_warn(chat_id, await int_to_alpha(user_id), {"warns": warns - 1})
    text = cq.message.text.markdown
    await cq.message.edit(f"~~{text}~~\n\n__ᴡᴀʀɴ ʀᴇᴍᴏᴠᴇᴅ ʙʏ :- {from_user.mention}__")


# ---------------------- REMOVE ALL WARNS ---------------------- #

@app.on_message(filters.command("rmwarns") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")

    mention = (await app.get_users(user_id)).mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    warns = warns["warns"] if warns else 0

    if warns == 0:
        return await message.reply_text(f"{mention} ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.")
    await remove_warns(chat_id, await int_to_alpha(user_id))
    await message.reply_text(f"**ʀᴇᴍᴏᴠᴇᴅ ᴡᴀʀɴɪɴɢs ᴏғ :- {mention}.**")


# ---------------------- CHECK WARNS ---------------------- #

@app.on_message(filters.command("warns") & ~filters.private & ~BANNED_USERS)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("**ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.**")

    mention = (await app.get_users(user_id)).mention
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    warns = warns["warns"] if warns else 0

    if warns == 0:
        return await message.reply_text(f"**{mention} ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.**")
    await message.reply_text(f"**{mention} ʜᴀs** `{warns}/3` **ᴡᴀʀɴɪɴɢs**")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
