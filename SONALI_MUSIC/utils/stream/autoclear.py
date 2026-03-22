# =======================================================
# ©️ 2025-26 All Rights Reserved by kuruvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @KURUVI_TELE
# =======================================================

import os

from config import autoclean


async def auto_clean(popped):
    try:
        rem = popped["file"]
        autoclean.remove(rem)
        count = autoclean.count(rem)
        if count == 0:
            if "vid_" not in rem or "live_" not in rem or "index_" not in rem:
                try:
                    os.remove(rem)
                except:
                    pass
    except:
        pass

# ======================================================
# ©️ 2025-26 All Rights Reserved by kuruvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/itzmekuruvi
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/kuruvibotz
# =======================================================
