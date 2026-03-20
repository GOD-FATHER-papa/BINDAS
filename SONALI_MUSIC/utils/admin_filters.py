# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from SONALI_MUSIC.utils.admin_check import is_admin, is_group_owner
from SONALI_MUSIC.misc import SUDOERS
from config import OWNER_ID


def sudo_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    return bool(
        (
            (msg.from_user and msg.from_user.id in SUDOERS)
            or (msg.sender_chat and msg.sender_chat.id in SUDOERS)
        )
        and not getattr(msg, "edit_date", False)
    )

sudo_filter = filters.create(func=sudo_filter_func, name="SudoUsersFilter")


async def admin_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    if getattr(msg, "edit_date", False):
        return False
    return await is_admin(msg)

admin_filter = filters.create(func=admin_filter_func, name="AdminFilter")


async def group_owner_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    if getattr(msg, "edit_date", False):
        return False
    return await is_group_owner(msg)

owner_filter = filters.create(func=group_owner_filter_func, name="GroupOwnerFilter")


def bot_owner_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    return (
        msg.from_user
        and msg.from_user.id == OWNER_ID
        and not getattr(msg, "edit_date", False)
    )

dev_filter = filters.create(func=bot_owner_filter_func, name="BotOwnerFilter")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
