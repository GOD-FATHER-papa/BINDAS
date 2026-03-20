# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from SONALI_MUSIC import app


def help_pannel(_, START: Union[bool, int] = None):
    first = [
                 InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close")
    ]
    second = [
                 InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"MAIN_CP",),
    ]
    mark = second if START else first
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1",),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2",),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3",),
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4",),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5",),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6",),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7",),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8",),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9",),
            ],
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10",),
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11",),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12",),
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13",),
               # InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="MAIN_CP",),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15",),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"settings_back_helper",),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help",)
        ],
    ]
    return buttons




# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
