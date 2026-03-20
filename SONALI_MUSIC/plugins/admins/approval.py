# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC import app

active_buttons = {}


@app.on_chat_join_request()
async def join_request_handler(client, join_req):
    chat = join_req.chat
    user = join_req.from_user
    
    request_key = f"{chat.id}_{user.id}"
    if request_key in active_buttons:
        return  
    
    active_buttons[request_key] = True

    text = (
        "**🚨 ᴀ ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ғᴏᴜɴᴅ !!**\n\n"
        f"**👤 ᴜsᴇʀ :-** {user.mention}\n"
        f"**🆔 ɪᴅ :-** `{user.id}`\n"
        f"**🔗 ᴜsᴇʀɴᴀᴍᴇ :-** @{user.username if user.username else 'ɴᴏɴᴇ'}\n\n"
        f"**📝 ɴᴏᴛᴇ :-** <i>ᴍᴇssᴀɢᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ɪɴ 10 ᴍɪɴᴜᴛᴇs.</i>"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"approve:{chat.id}:{user.id}"),
                InlineKeyboardButton("❌ ᴅɪsᴍɪss", callback_data=f"dismiss:{chat.id}:{user.id}")
            ]
        ]
    )

    sent = await client.send_message(chat.id, text, reply_markup=buttons)

    async def delete_and_cleanup():
        await asyncio.sleep(600)
        try:
            await client.delete_messages(chat.id, sent.id)
        except:
            pass
        finally:
            if request_key in active_buttons:
                del active_buttons[request_key]

    asyncio.create_task(delete_and_cleanup())


@app.on_callback_query(filters.regex("^(approve|dismiss):"))
async def callback_handler(client: Client, query: CallbackQuery):
    action, chat_id, user_id = query.data.split(":")
    chat_id = int(chat_id)
    user_id = int(user_id)

    try:
        member = await client.get_chat_member(chat_id, query.from_user.id)
        if member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return await query.answer("⚠️ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ 😜", show_alert=True)
    except:
        return await query.answer("⚠️ ᴀᴅᴍɪɴ ᴄʜᴇᴄᴋ ғᴀɪʟᴇᴅ", show_alert=True)

    if action == "approve":
        try:
            await client.approve_chat_join_request(chat_id, user_id)

            user_obj = await client.get_users(user_id)
            chat_obj = await client.get_chat(chat_id)

            await query.edit_message_text(
                f"**🎉 ᴅᴇᴀʀ {user_obj.mention}, ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ :-** `{chat_obj.title}`"
            )

        except Exception as e:
            error_msg = str(e)
            if "already handled" in error_msg.lower():
                await query.edit_message_text("**✅ ʀᴇǫᴜᴇsᴛ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ**")
            else:
                await query.answer(f"⚠️ ᴇʀʀᴏʀ :- {error_msg}", show_alert=True)

    elif action == "dismiss":
        try:
            await client.decline_chat_join_request(chat_id, user_id)

            user_obj = await client.get_users(user_id)
            chat_obj = await client.get_chat(chat_id)

            await query.edit_message_text(
                f"**❌ ᴅᴇᴀʀ {user_obj.mention}, ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴡᴀs ᴅɪsᴍɪssᴇᴅ ғʀᴏᴍ :-** `{chat_obj.title}`"
            )

        except Exception as e:
            error_msg = str(e)
            if "already handled" in error_msg.lower():
                await query.edit_message_text("**❌ ʀᴇǫᴜᴇsᴛ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ**")
            else:
                await query.answer(f"⚠️ ᴇʀʀᴏʀ :- {error_msg}", show_alert=True)

    request_key = f"{chat_id}_{user_id}"
    if request_key in active_buttons:
        del active_buttons[request_key]

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
