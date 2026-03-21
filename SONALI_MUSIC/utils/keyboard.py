# =======================================================
# ©️ 2025-26 All Rights Reserved by kuruvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @KURUVI_TELE
# =======================================================

from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton as Ikb

from .functions import get_urls_from_text as is_url


def keyboard(buttons_list, row_width: int = 2):
    buttons = InlineKeyboard(row_width=row_width)
    data = [
        (
            Ikb(text=str(i[0]), callback_data=str(i[1]))
            if not is_url(i[1])
            else Ikb(text=str(i[0]), url=str(i[1]))
        )
        for i in buttons_list
    ]
    buttons.add(*data)
    return buttons


def ikb(data: dict, row_width: int = 2):
    return keyboard(data.items(), row_width=row_width)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/itzmekuruvi
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/kuruvibotz
# =======================================================
