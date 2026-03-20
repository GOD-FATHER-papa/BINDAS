# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import Client, filters, enums
from pyrogram.types import ChatPrivileges
from pyrogram.errors import ChatAdminRequired
from functools import wraps
from SONALI_MUSIC import app

def mention(user_id, name):
    return f"[{name}](tg://user?id={user_id})"

def admin_required(*privileges):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message):
            if not message.from_user:
                await message.reply_text("**⋟ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ. ᴘʟᴇᴀsᴇ ᴜɴʜɪᴅᴇ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")
                return

            member = await message.chat.get_member(message.from_user.id)
            if member.status == enums.ChatMemberStatus.OWNER:
                return await func(client, message)
            elif member.status == enums.ChatMemberStatus.ADMINISTRATOR:
                if not member.privileges:
                    await message.reply_text("**⋟ ᴄᴀɴɴᴏᴛ ʀᴇᴛʀɪᴇᴠᴇ ʏᴏᴜʀ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇs**")
                    return
                missing_privileges = [priv for priv in privileges if not getattr(member.privileges, priv, False)]
                if missing_privileges:
                    await message.reply_text(f"**⋟ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴs :-** {', '.join(missing_privileges)}")
                    return
                return await func(client, message)
            else:
                await message.reply_text("**⋟ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.**")
                return
        return wrapper
    return decorator

async def extract_user_and_title(message, client):
    user = None
    title = None

    cmd = message.text.strip().split()[0]
    text = message.text[len(cmd):].strip()

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            await message.reply_text("**⋟ ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴇ ᴜsᴇʀ ɪɴ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.**")
            return None, None, None
        title = text if text else None
    else:
        args = text.strip().split(maxsplit=1)
        if not args:
            await message.reply_text("**⋟ ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.**")
            return None, None, None
        user_arg = args[0]
        try:
            user = await client.get_users(user_arg)
            if not user:
                await message.reply_text("**⋟ ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.**")
                return None, None, None
        except Exception:
            await message.reply_text("**⋟ ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.**")
            return None, None, None
        title = args[1] if len(args) > 1 else None

    return user.id, user.first_name, title

def format_promotion_message(chat_name, user_mention, admin_mention, action):
    action_text = "ᴩʀᴏᴍᴏᴛɪɴɢ" if action == "promote" else "ᴅᴇᴍᴏᴛɪɴɢ"
    return (
        f"**⋟ {action_text} ᴀ ᴜsᴇʀ ɪɴ {chat_name}\n"
        f"ᴜsᴇʀ :- {user_mention}\n"
        f"ᴀᴅᴍɪɴ :- {admin_mention}**"
    )

@app.on_message(filters.command("promote"))
@admin_required("can_promote_members")
async def promote_command_handler(client, message):
    user_id, first_name, title = await extract_user_and_title(message, client)
    if not user_id:
        return
    try:
        member = await client.get_chat_member(message.chat.id, user_id)
        if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text("**⋟ ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ.**")
            return

        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_delete_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_restrict_members=False,
                can_promote_members=False,
                can_manage_chat=True,
                can_manage_video_chats=True,
                is_anonymous=False,
            )
        )

        if title:
            try:
                await client.set_administrator_title(message.chat.id, user_id, title)
            except Exception as e:
                await message.reply_text(f"**⋟ ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴛ ᴛɪᴛʟᴇ :-** {e}")

        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        chat_name = message.chat.title
        msg = format_promotion_message(chat_name, user_mention, admin_mention, action="promote")
        await message.reply_text(msg)
    except ChatAdminRequired:
        await message.reply_text("**⋟ ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴘʀᴏᴍᴏᴛᴇ ᴘᴇʀᴍɪssɪᴏɴs.**")
    except Exception as e:
        await message.reply_text(f"**⋟ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :-** {e}")

@app.on_message(filters.command("fullpromote"))
@admin_required("can_promote_members")
async def fullpromote_command_handler(client, message):
    user_id, first_name, title = await extract_user_and_title(message, client)
    if not user_id:
        return
    try:
        member = await client.get_chat_member(message.chat.id, user_id)
        if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text("**⋟ ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ.**")
            return

        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_change_info=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                is_anonymous=False,
                can_manage_video_chats=True,
            )
        )

        if title:
            try:
                await client.set_administrator_title(message.chat.id, user_id, title)
            except Exception as e:
                await message.reply_text(f"**⋟ ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴛ ᴛɪᴛʟᴇ :-** {e}")

        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        chat_name = message.chat.title
        msg = format_promotion_message(chat_name, user_mention, admin_mention, action="promote")
        await message.reply_text(msg)
    except ChatAdminRequired:
        await message.reply_text("**⋟ ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴘʀᴏᴍᴏᴛᴇ ᴘᴇʀᴍɪssɪᴏɴs.**")
    except Exception as e:
        await message.reply_text(f"**⋟ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :-** {e}")

@app.on_message(filters.command("demote"))
@admin_required("can_promote_members")
async def demote_command_handler(client, message):
    user_id, first_name, _ = await extract_user_and_title(message, client)
    if not user_id:
        return
    try:
        member = await client.get_chat_member(message.chat.id, user_id)
        if member.status != enums.ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text("**⋟ ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.**")
            return

        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                is_anonymous=False
            )
        )

        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        chat_name = message.chat.title
        msg = format_promotion_message(chat_name, user_mention, admin_mention, action="demote")
        await message.reply_text(msg)
    except ChatAdminRequired:
        await message.reply_text("**⋟ ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴘʀᴏᴍᴏᴛᴇ ᴘᴇʀᴍɪssɪᴏɴs.**")
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            await message.reply_text("**⋟ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪs ᴜsᴇʀ.**")
        else:
            await message.reply_text(f"**⋟ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :-** {e}")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
