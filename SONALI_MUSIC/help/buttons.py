# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

import config
from SONALI_MUSIC import app

class BUTTONS(object):
    BBUTTON = [
    [
        InlineKeyboardButton("• ᴀᴄᴛɪᴏɴ •", callback_data="TOOL_BACK HELP_06"),
        InlineKeyboardButton("• ᴀɴᴛɪ-ғʟᴏᴏᴅ •", callback_data="TOOL_BACK HELP_11"),
        InlineKeyboardButton("• ᴀᴘᴘʀᴏᴠᴀʟ •", callback_data="TOOL_BACK HELP_12"),
    ],
    [
        InlineKeyboardButton("• ᴄʜᴀᴛ-ɢᴘᴛ •", callback_data="TOOL_BACK HELP_01"),
        InlineKeyboardButton("• ɢɪᴛʜᴜʙ •", callback_data="TOOL_BACK HELP_09"),
        InlineKeyboardButton("• ɢʀᴏᴜᴘ •", callback_data="TOOL_BACK HELP_07"),
    ],
    [
        InlineKeyboardButton("• ʜɪsᴛᴏʀʏ •", callback_data="TOOL_BACK HELP_08"),
        InlineKeyboardButton("• ɪɴғᴏ •", callback_data="TOOL_BACK HELP_03"),
        InlineKeyboardButton("• ᴘᴜʀɢᴇ •", callback_data="TOOL_BACK HELP_13"),
    ],
    [
        InlineKeyboardButton("• sᴛɪᴄᴋᴇʀ•", callback_data="TOOL_BACK HELP_05"),
        InlineKeyboardButton("• ᴛᴀɢ-ᴀʟʟ •", callback_data="TOOL_BACK HELP_04"),
        InlineKeyboardButton("• ᴛᴏᴏʟs •", callback_data="TOOL_BACK HELP_10"),
    ],
    [
        InlineKeyboardButton("• ᴠᴄ-ᴛᴏᴏʟs •", callback_data="TOOL_BACK HELP_14"),
        InlineKeyboardButton("• ᴡᴇʟᴄᴏᴍᴇ •", callback_data="TOOL_BACK HELP_15"),
        InlineKeyboardButton("• ᴡʜɪsᴘᴇʀ•", callback_data="TOOL_BACK HELP_02"),
    ],
    [
        InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="MAIN_CP"),
    ]
]
    
    
    
    
    PBUTTON = [
        [
            InlineKeyboardButton("˹ ᴄσηᴛᴧᴄᴛ ˼", url="https://t.me/About_Kuruvi"),
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="MAIN_CP"),
        ]
        ]
    
    ABUTTON = [
        [
            InlineKeyboardButton("˹ sυᴘᴘσʀᴛ ˼", url="https://t.me/About_Kuruvi"),
            InlineKeyboardButton("˹ υᴘᴅᴧᴛєs ˼", url="https://t.me/kuruvi_botz"),
        ],
        [  
            InlineKeyboardButton("˹ ᴘʀɪᴠᴧᴄʏ ˼", url="https://telegra.ph/PRIVACY-POLICY--KURUVI-BOTS-04-08-3"),
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="settingsback_helper"),
        ]
        ]
    
    SBUTTON = [
        [
            InlineKeyboardButton("ϻᴜѕɪᴄ", callback_data="settings_back_helper"),
            InlineKeyboardButton("ϻᴧηᴧɢєϻєηᴛ", callback_data="TOOL_CP"),
        ],
        
        [
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ᴛσ ʜσϻє ⌯", callback_data="settingsback_helper"),
            
        ]
        ]




# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
