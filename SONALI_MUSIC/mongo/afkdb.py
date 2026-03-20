# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from SONALI_MUSIC.utils.mongo import db

afkdb = db.afk


async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    if not user:
        return False, {}
    return True, user["reason"]


async def add_afk(user_id: int, mode):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )


async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})


async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
