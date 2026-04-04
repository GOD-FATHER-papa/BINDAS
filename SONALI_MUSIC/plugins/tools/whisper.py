# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from SONALI_MUSIC import app as app
from config import BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 sᴛᴀʀᴛ ᴡʜɪsᴘᴇʀ 💒", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="💒 ᴡʜɪsᴘᴇʀ 💒",
                description=f"@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]",
                input_message_content=InputTextMessageContent(f"💒 ᴜsᴀɢᴇ :\n\n@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]"),
                thumb_url="https://files.catbox.moe/ynsu0c.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = data.split()[0]
            msg = data.split(None, 1)[1]
        except IndexError as e:
            pass
        
        try:
            user = await _.get_users(user_id)
        except:
            mm = [
                InlineQueryResultArticle(
                    title="💒 ᴡʜɪsᴘᴇʀ 💒",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://files.catbox.moe/ynsu0c.jpg",
                    reply_markup=switch_btn
                )
            ]
        
        try:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 sʜᴏᴡ ᴡʜɪsᴘᴇʀ ᴍᴇssᴀɢᴇ 💒", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔩 sᴇᴇ ᴏɴᴇ-ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💒 ᴡʜɪsᴘᴇʀ 💒",
                    description=f"sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ ᴛᴏ{user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💒 ʏᴏᴜ ᴀʀᴇ sᴇɴᴅɪɴɢ ᴀ ᴡʜɪsᴘᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ {user.first_name}. 🏩\n\n➻ ᴏɴʟʏ {user.first_name} sᴇᴇ ᴛʜɪs ʏᴏᴜʀ ᴍᴇssᴀɢᴇ.😆"),
                    thumb_url="https://files.catbox.moe/ynsu0c.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="🔩 ᴏɴᴇ-ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ",
                    description=f"sᴇɴᴅ ᴀ ᴏɴᴇ-ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ ᴛᴏ {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"🔩 ʏᴏᴜ ᴀʀᴇ sᴇɴᴅɪɴɢ ᴀ ᴏɴᴇ ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ {user.first_name}. 🏩\n\n➻ ᴏɴʟʏ {user.first_name} sᴇᴇ ᴛʜɪs ʏᴏᴜʀ ᴍᴇssᴀɢᴇ.😆"),
                    thumb_url="https://files.catbox.moe/ynsu0c.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
        except:
            pass
        
        try:
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except:
            pass
    
    results.append(mm)
    return results


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id
    
    if user_id not in [from_user, to_user, 7473021518]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} ɪs ᴛʀʏɪɴɢ ᴛᴏ ᴏᴘᴇɴ ʏᴏᴜʀ ᴡʜɪsᴘᴇʀ. 🚧")
        except Unauthorized:
            pass
        
        return await query.answer("⚠️ ᴛʜɪs ᴡʜɪsᴘᴇʀ ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ ʙᴀʙʏ 🚨", show_alert=True)
    
    search_msg = f"{from_user}_{to_user}"
    
    try:
        msg = whisper_db[search_msg]
    except:
        msg = "🚫 ᴇʀʀᴏʀ !!\n\nᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ !!"
    
    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("🗼ɢᴏ ɪɴʟɪɴᴇ 🗼", switch_inline_query_current_chat="")]])
    
    await query.answer(msg, show_alert=True)
    
    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("📬 ᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ ʀᴇᴀᴅ !!\n\nᴘʀᴇss ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ !!", reply_markup=SWITCH)


async def in_help():
    answers = [
        InlineQueryResultArticle(
            title="💒 ᴡʜɪsᴘᴇʀ 💒",
            description=f"@Aaru_Musics_bot [USERNAME / ID] [ YOUR TEXT]",
            input_message_content=InputTextMessageContent(f"**📍ᴜsᴀɢᴇ :-**\n\n@Aaru_Musics_bot (Target Username or ID) (Your Message).\n\n**Example :-**\n@Aaru_Musics_bot @kuruvi_tele I love You 😘"),
            thumb_url="https://files.catbox.moe/ynsu0c.jpg",
            reply_markup=switch_btn
        )
    ]
    return answers


@app.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    else:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
                                               

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
