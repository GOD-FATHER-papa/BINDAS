# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC import app
import config
from SONALI_MUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """**<u>❃ ɪsʜᴀ ʙᴏᴛs ʀєᴘσs ❃</u>

✼ ʀєᴘᴏ ɪs ηᴏᴡ ᴘʀɪᴠᴧᴛє ᴅᴜᴅє 😌
 
❉  ʏᴏᴜ ᴄᴧη мʏ ᴜsє ᴘᴜʙʟɪᴄ ʀєᴘσs !! 

✼ || ɢɪᴛ :-  [ᴋᴜʀᴜᴠɪ-ʙᴧʙʏ](https://github.com/kuruvinetwork-maker/) ||
 
❊ ʀᴜη 24x7 ʟᴧɢ ϝʀєє ᴡɪᴛʜσᴜᴛ sᴛσᴘ**
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
    [
        InlineKeyboardButton("• ɪsʜᴀ ᴍᴜsɪᴄ •", url="https://github.com/kuruvinetwork-maker/"),
        InlineKeyboardButton("• sᴏɴᴀʟɪ ᴍᴜsɪᴄ •", url="https://github.com/kuruvinetwork-maker/")
    ],
    [
        InlineKeyboardButton("• sɪᴍᴘʟᴇ ᴍᴜsɪᴄ •", url="https://github.com/kuruvinetwork-maker/"),
        InlineKeyboardButton("• ᴄʜᴀᴛ ʙᴏᴛ •", url="https://github.com/kuruvinetwork-maker/")
    ],
    [
        InlineKeyboardButton("• ᴜsᴇʀ ʙᴏᴛ •", url="https://github.com/kuruvinetwork-maker/"),
        InlineKeyboardButton("• sᴘᴀᴍ ʙᴏᴛ •", url="https://github.com/kuruvinetwork-maker/")
    ],
    [
        InlineKeyboardButton("• sᴇssɪᴏɴ ʙᴏᴛ •", url="https://github.com/kuruvinetwork-maker/"),
        InlineKeyboardButton("• sᴇssɪᴏɴ ʜᴀᴄᴋ •", url="https://github.com/kuruvinetwork-maker/")
    ],
    [
        InlineKeyboardButton("• ʙᴀɴᴀʟʟ ʙᴏᴛ •", url="https://github.com/kuruvinetwork-maker/"),
        InlineKeyboardButton("• ᴀɴʏ ɪssᴜᴇ •", user_id=config.@KURUVI_TELE)
    ],
    [
        InlineKeyboardButton("✙ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✙", url=f"https://t.me/{app.username}?startgroup=true")
    ]
]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/kbi6t5.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
