# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import filters
from pyrogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserAdminInvalid, UserNotParticipant
from pyrogram.enums import ChatMemberStatus
from datetime import datetime, timedelta

from SONALI_MUSIC.utils.permissions import adminsOnly, member_permissions
from SONALI_MUSIC import app
from SONALI_MUSIC.core.mongo import mongodb

antiflood_collection = mongodb.antiflood_settings
DEFAULT_FLOOD_ACTION = "tmute"

async def get_chat_flood_settings(chat_id):
    settings = await antiflood_collection.find_one({"chat_id": chat_id})
    if not settings:
        return {
            "flood_limit": 0,
            "flood_timer": 0,
            "flood_action": DEFAULT_FLOOD_ACTION,
            "delete_flood": False
        }
    return {
        "flood_limit": settings.get("flood_limit", 0),
        "flood_timer": settings.get("flood_timer", 0),
        "flood_action": settings.get("flood_action", DEFAULT_FLOOD_ACTION),
        "delete_flood": settings.get("delete_flood", False)
    }

def update_chat_flood_settings(chat_id, update_data):
    antiflood_collection.update_one({"chat_id": chat_id}, {"$set": update_data}, upsert=True)

async def check_admin_rights(client, message: Message):
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
        if participant.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return True
    except UserNotParticipant:
        pass
    await message.reply("**⋟ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !!**")
    return False

@app.on_message(filters.command(["flood", "lood"], prefixes=["/", "!", ".", "F", "f"]))
async def get_flood_settings(client, message: Message):
    if not await check_admin_rights(client, message):
        return
    chat_id = message.chat.id
    settings = await get_chat_flood_settings(chat_id)

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙",
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ]]
    )

    await message.reply(
        f"**⋟ ᴄᴜʀʀᴇɴᴛ ғʟᴏᴏᴅ sᴇᴛᴛɪɴɢs :-**\n\n"
        f"**➤ ʟɪᴍɪᴛ :-** {settings['flood_limit']} messages\n"
        f"**➤ ᴛɪᴍᴇʀ :-** {settings['flood_timer']} sec\n"
        f"**➤ ᴀᴄᴛɪᴏɴ :-** {settings['flood_action']}\n"
        f"**➤ ᴅᴇʟᴇᴛᴇ ғʟᴏᴏᴅ ᴍᴇssᴀɢᴇs :-** {settings['delete_flood']}\n\n"
        f"**⋟ ʙʏ :- {app.mention}**",
        reply_markup=buttons
    )

@app.on_message(filters.command(["setflood", "etfood", "f"], prefixes=["/", "!", ".", "S", "s"]))
async def set_flood_limit(client, message: Message):
    if not await check_admin_rights(client, message):
        return
    chat_id = message.chat.id
    args = message.command[1:]
    
    if not args:
        return await message.reply("**⋟ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴏʀ 'off'.**\n\n**ᴛʀʏ :-** `setflood 10`")
    
    limit = args[0].lower()
    if limit in ["off", "no", "0"]:
        update_chat_flood_settings(chat_id, {"flood_limit": 0})
        return await message.reply("**⋟ ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ !!**")
    
    try:
        limit = int(limit)
        update_chat_flood_settings(chat_id, {"flood_limit": limit})
        await message.reply(f"**⋟ ғʟᴏᴏᴅ ʟɪᴍɪᴛ sᴇᴛ ᴛᴏ** `{limit}` **ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ᴍᴇssᴀɢᴇs.**")
    except ValueError:
        await message.reply("**⋟ ɪɴᴠᴀʟɪᴅ ғʟᴏᴏᴅ ʟɪᴍɪᴛ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ.**")

@app.on_message(filters.command(["setfloodtimer", "etfloodtime", "ft"], prefixes=["/", "!", ".", "S", "s"]))
async def set_flood_timer(client, message: Message):
    if not await check_admin_rights(client, message):
        return
    chat_id = message.chat.id
    args = message.command[1:]
    
    if not args or args[0].lower() in ["off", "no"]:
        update_chat_flood_settings(chat_id, {"flood_timer": 0})
        return await message.reply("**⋟ ᴛɪᴍᴇᴅ ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ.**")
    
    if len(args) != 2:
        return await message.reply("**⋟ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ʙᴏᴛʜ ᴍᴇssᴀɢᴇ** `ᴄᴏᴜɴᴛ` **ᴀɴᴅ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ** `sᴇᴄᴏɴᴅs`.\n\n**ᴛʀʏ :-** `setfloodtimer 10 30s`")
    
    try:
        count = int(args[0])
        duration = int(args[1].replace("s", ""))
        update_chat_flood_settings(chat_id, {"flood_timer": duration, "flood_limit": count})
        await message.reply(f"**⋟ ғʟᴏᴏᴅ ᴛɪᴍᴇʀ sᴇᴛ ᴛᴏ {count} ᴍᴇssᴀɢᴇs ɪɴ {duration} sᴇᴄ.**")
    except ValueError:
        await message.reply("**⋟ ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇʀ sᴇᴛᴛɪɴɢs.**")

@app.on_message(filters.command(["floodmode", "loodmode", "m"], prefixes=["/", "!", ".", "F", "f"]))
async def set_flood_mode(client, message: Message):
    if not await check_admin_rights(client, message):
        return
    chat_id = message.chat.id
    args = message.command[1:]
    
    if not args:
        return await message.reply("**⋟ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴀᴄᴛɪᴏɴ (ban/mute/kick/tban/tmute).**")
    
    action = args[0].lower()
    if action not in ["ban", "mute", "kick", "tban", "tmute"]:
        return await message.reply("**⋟ ɪɴᴠᴀʟɪᴅ ᴀᴄᴛɪᴏɴ !!, ᴄʜᴏᴏsᴇ ᴏɴᴇ :- ban/mute/kick/tban/tmute.**")
    
    update_chat_flood_settings(chat_id, {"flood_action": action})
    await message.reply(f"**⋟ ғʟᴏᴏᴅ ᴀᴄᴛɪᴏɴ sᴇᴛ ᴛᴏ :-** `{action}`")

@app.on_message(filters.command(["delflood", "clearflood", "learflood", "f"], prefixes=["/", "!", ".", "C", "c"]))
async def set_flood_clear(client, message: Message):
    if not await check_admin_rights(client, message):
        return
    chat_id = message.chat.id
    args = message.command[1:]
    
    if not args or args[0].lower() not in ["yes", "no", "on", "off"]:
        return await message.reply("**⋟ ᴘʟᴇᴀsᴇ ᴄʜᴏᴏsᴇ ᴇɪᴛʜᴇʀ** `yes` **ᴏʀ** `no`")
    
    delete_flood = args[0].lower() in ["yes", "on"]
    update_chat_flood_settings(chat_id, {"delete_flood": delete_flood})
    await message.reply(f"**⋟ ᴅᴇʟᴇᴛᴇ ғʟᴏᴏᴅ ᴍᴇssᴀɢᴇs sᴇᴛ ᴛᴏ :-** `{delete_flood}`")


flood_count = {}

@app.on_message(filters.group, group=31)
async def flood_detector(client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        settings = await get_chat_flood_settings(chat_id)
        participant = await client.get_chat_member(chat_id, user_id)
        
        if participant.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return
        if settings['flood_limit'] == 0:
            return

        if chat_id not in flood_count:
            flood_count[chat_id] = {}
        
        user_data = flood_count[chat_id].get(user_id, {"count": 0, "first_message_time": datetime.now()})
        flood_timer = settings.get("flood_timer", 0)
        
        if (datetime.now() - user_data["first_message_time"]).seconds > flood_timer:
            user_data = {"count": 1, "first_message_time": datetime.now()}
        else:
            user_data["count"] += 1
        
        flood_count[chat_id][user_id] = user_data
        
        if user_data["count"] > settings["flood_limit"]:
            action = settings["flood_action"]
            await take_flood_action(client, message, action)
            if settings["delete_flood"]:
                await message.delete()
    except Exception as e:
        print(f"**ᴇʀʀᴏʀ ɪɴ ғʟᴏᴏᴅ ᴅᴇᴛᴇᴄᴛᴏʀ :-** {e}")


@app.on_callback_query(filters.regex(r"^unban:(\d+)$"))
async def handle_unban(client: app, query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    chat_id = query.message.chat.id
    try:
        perms = await member_permissions(chat_id, query.from_user.id)
        if "can_restrict_members" not in perms:
            return await query.answer("⋟ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs.", show_alert=True)
    except UserNotParticipant:
        return await query.answer("⋟ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ.", show_alert=True)

    try:
        await client.unban_chat_member(chat_id, user_id)
        await query.message.edit_text(f"**⋟ ᴜsᴇʀ ᴜɴʙᴀɴɴᴇᴅ !!**")
    except UserAdminInvalid:
        await query.message.edit_text("**⋟ ғᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ, ᴍᴀʏʙᴇ ᴛʜᴇʏ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ.**")


@app.on_callback_query(filters.regex(r"^unmute:(\d+)$"))
async def handle_unmute(client: app, query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    chat_id = query.message.chat.id
    try:
        perms = await member_permissions(chat_id, query.from_user.id)
        if "can_restrict_members" not in perms:
            return await query.answer("⋟ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs.", show_alert=True)
    except UserNotParticipant:
        return await query.answer("⋟ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ.", show_alert=True)

    try:
        await client.restrict_chat_member(chat_id, user_id, permissions=ChatPermissions(can_send_messages=True))
        await query.message.edit_text(f"**⋟ ᴜsᴇʀ ᴜɴᴍᴜᴛᴇᴅ !!**")
    except UserAdminInvalid:
        await query.message.edit_text("**⋟ ғᴀɪʟᴇᴅ ᴛᴏ ᴜɴᴍᴜᴛᴇ, ᴍᴀʏʙᴇ ᴛʜᴇʏ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ.**")


    
async def take_flood_action(client, message, action):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_first_name = message.from_user.first_name

    buttons = None

    if action == "ban":
        try:
            await client.ban_chat_member(chat_id, user_id)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴜɴʙᴀɴ", callback_data=f"unban:{user_id}")]]
            )
        except UserAdminInvalid:
            return
    elif action == "mute":
        try:
            await client.restrict_chat_member(
                chat_id, user_id, permissions=ChatPermissions(can_send_messages=False)
            )
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴜɴᴍᴜᴛᴇ", callback_data=f"unmute:{user_id}")]]
            )
        except UserAdminInvalid:
            return
    elif action == "kick":
        try:
            await client.kick_chat_member(chat_id, user_id)
            await client.unban_chat_member(chat_id, user_id)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", url=f"tg://user?id={user_id}")]]
            )
        except UserAdminInvalid:
            return
    elif action == "tban":
        try:
            until_date = datetime.now() + timedelta(minutes=1)
            await client.ban_chat_member(chat_id, user_id, until_date=until_date)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴜɴʙᴀɴ", callback_data=f"unban:{user_id}")]]
            )
        except UserAdminInvalid:
            return
    elif action == "tmute":
        try:
            until_date = datetime.now() + timedelta(minutes=1)
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until_date
            )
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴜɴᴍᴜᴛᴇ", callback_data=f"unmute:{user_id}")]]
            )
        except UserAdminInvalid:
            return

    await message.reply(
        f"**⋟ ᴜsᴇʀ {user_first_name} ᴡᴀs {action}ed ғᴏʀ ғʟᴏᴏᴅɪɴɢ.**",
        reply_markup=buttons
    )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
