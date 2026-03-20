# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, BadRequest
import datetime
from SONALI_MUSIC import app


def mention(user, name, mention=True):
    if mention:
        return f"[{name}](tg://openmessage?user_id={user})"
    else:
        return f"[{name}](https://t.me/{user})"


async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
        return [user.id, user.first_name]
    except:
        return None


def format_time(td: datetime.timedelta):
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = []
    if days > 0:
        result.append(f"{days}ᴅ")
    if hours > 0:
        result.append(f"{hours}ʜ")
    if minutes > 0:
        result.append(f"{minutes}ᴍ")
    if seconds > 0:
        result.append(f"{seconds}s")
    return " ".join(result)


# ----- BAN -----
async def ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason=None, time=None):
    try:
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "**⚠ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ʀɪɢʜᴛs 😡**", False
    except UserAdminInvalid:
        return "**❌ ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴀɴ ᴀᴅᴍɪɴ !!**", False
    except Exception as e:
        return f"**⚠ ᴏᴘᴘs !! :-** {e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    text = f"**🔒 {user_mention} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ʙʏ {admin_mention}**"
    if reason:
        text += f"\n\n**📝 ʀᴇᴀsᴏɴ :-** `{reason}`**"
    if time:
        text += f"\n\n**⏱ ᴛɪᴍᴇ :-** `{format_time(time)}`"
    return text, True


# ----- UNBAN -----
async def unban_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "**⚠ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ʀɪɢʜᴛs 😡**"
    except Exception as e:
        return f"**⚠ ᴏᴘᴘs !! -:** {e}"

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    return f"**🔓 {user_mention} ʜᴀs ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ ʙʏ {admin_mention}**"


# ----- MUTE -----
async def mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason=None, time=None):
    try:
        if time:
            mute_end_time = datetime.datetime.now() + time
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), mute_end_time)
        else:
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
    except ChatAdminRequired:
        return "**⚠ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛs 😡**", False
    except UserAdminInvalid:
        return "**❌ ɪ ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ ᴀɴ ᴀᴅᴍɪɴ !!**", False
    except Exception as e:
        return f"**⚠ ᴏᴘᴘs!!\n{e}**", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    text = f"**🔇 {user_mention} ʜᴀs ʙᴇᴇɴ ᴍᴜᴛᴇᴅ ʙʏ {admin_mention}**"
    if reason:
        text += f"\n\n**📝 ʀᴇᴀsᴏɴ :-** `{reason}`"
    if time:
        text += f"\n\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ :-** `{format_time(time)}`"
    return text, True


# ----- UNMUTE -----
async def unmute_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                #can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )
    except ChatAdminRequired:
        return "**⚠ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛs 😡**"
    except Exception as e:
        return f"**⚠ ᴏᴘᴘs !! :-** {e}"

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    return f"**🔊 {user_mention} ʜᴀs ʙᴇᴇɴ ᴜɴᴍᴜᴛᴇᴅ ʙʏ {admin_mention}**"


# ----- COMMAND HANDLERS -----
@app.on_message(filters.command(["ban"]))
async def ban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or not member.privileges.can_restrict_members:
        return await message.reply_text("**❌ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ !!**")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = " ".join(message.command[1:]) if len(message.command) > 1 else None
    else:
        if len(message.command) < 2:
            return await message.reply_text("**❌ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ᴛᴏ ʙᴀɴ !!**")
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if not user_obj:
                return await message.reply_text("**❌ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ !!**")
            user_id = user_obj[0]
            first_name = user_obj[1]
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else None

    text, result = await ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason)
    await message.reply_text(text)


@app.on_message(filters.command(["unban"]))
async def unban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or not member.privileges.can_restrict_members:
        return await message.reply_text("**❌ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴʙᴀɴ !!**")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if not user_obj:
                return await message.reply_text("**❌ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ !!**")
            user_id = user_obj[0]
            first_name = user_obj[1]
    else:
        return await message.reply_text("**❌ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ᴛᴏ ᴜɴʙᴀɴ !!**")

    text = await unban_user(user_id, first_name, admin_id, admin_name, chat_id)
    await message.reply_text(text)


@app.on_message(filters.command(["mute"]))
async def mute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or not member.privileges.can_restrict_members:
        return await message.reply_text("**❌ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ !!**")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = " ".join(message.command[1:]) if len(message.command) > 1 else None
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if not user_obj:
                return await message.reply_text("**❌ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ !!**")
            user_id = user_obj[0]
            first_name = user_obj[1]
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else None
    else:
        return await message.reply_text("**❌ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ᴛᴏ ᴍᴜᴛᴇ !!**")

    text, result = await mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason)
    await message.reply_text(text)


# ----- UNMUTE COMMAND -----
@app.on_message(filters.command(["unmute"]))
async def unmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or not member.privileges.can_restrict_members:
        return await message.reply_text("**❌ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ !!**")

    # Get target user
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if not user_obj:
                return await message.reply_text("**❌ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ !!**")
            user_id = user_obj[0]
            first_name = user_obj[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        return await message.reply_text("**❌ ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ**")

    text = await unmute_user(user_id, first_name, admin_id, admin_name, chat_id)
    await message.reply_text(f"**{text}**")


# ----- TEMPORARY MUTE (TMUTE) -----
@app.on_message(filters.command(["tmute"]))
async def tmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or not member.privileges.can_restrict_members:
        return await message.reply_text("**❌ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ !!**")

    # Get user and time
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        if len(message.command) < 2:
            return await message.reply_text("**❌ ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴛɪᴍᴇ ᴅᴜʀᴀᴛɪᴏɴ !!**\n\n**ᴇx :-** `/tmute 2m`")
        time_text = message.command[1]
    elif len(message.command) >= 3:
        user_text = message.command[1]
        try:
            user_id = int(user_text)
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(user_text)
            if not user_obj:
                return await message.reply_text("**❌ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ !!**")
            user_id = user_obj[0]
            first_name = user_obj[1]
        time_text = message.command[2]
    else:
        return await message.reply_text("**❌ ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴜsᴇʀ ᴀɴᴅ ᴛɪᴍᴇ !!**\n\n**ᴇx :-** `/tmute @user 2m`")

    # Parse time
    try:
        amount = int(time_text[:-1])
        unit = time_text[-1]
        if unit == "m":
            mute_duration = datetime.timedelta(minutes=amount)
        elif unit == "h":
            mute_duration = datetime.timedelta(hours=amount)
        elif unit == "d":
            mute_duration = datetime.timedelta(days=amount)
        else:
            return await message.reply_text("**❌ ᴡʀᴏɴɢ ᴛɪᴍᴇ ᴜɴɪᴛ !!. Use m/h/d**")
    except:
        return await message.reply_text("**❌ ᴡʀᴏɴɢ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ !!. ᴇx :- 2m, 3h, 1d**")

    text, result = await mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason=None, time=mute_duration)
    await message.reply_text(text)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
