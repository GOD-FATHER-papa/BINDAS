# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import os 
import random
from datetime import datetime 
from telegraph import upload_file
from PIL import Image , ImageDraw
from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import *

#BOT FILE NAME
from SONALI_MUSIC import app as app
from SONALI_MUSIC.mongo.couples_db import _get_image, get_couple

POLICE = [
    [
        InlineKeyboardButton(
            text="• ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ •",
            url=f"https://t.me/Sonali_Music_bot?startgroup=true",
        ),
    ],
]


def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list
    

def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a

tomorrow = str(dt_tom())
today = str(dt()[0])

@app.on_message(filters.command("couples"))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("✦ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")
    try:
        msg = await message.reply_text("**➻ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴏᴜᴘʟᴇs ɪᴍᴀɢᴇs...**")
        # GET LIST OF USERS
        list_of_users = []

        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo

        N1 = (await app.get_users(c1_id)).mention 
        N2 = (await app.get_users(c2_id)).mention
         
        try:
            p1 = await app.download_media(photo1.big_file_id, file_name="pfp.png")
        except Exception:
            p1 = "SONALI_MUSIC/assets/upic.png"
        try:
            p2 = await app.download_media(photo2.big_file_id, file_name="pfp1.png")
        except Exception:
            p2 = "SONALI_MUSIC/assets/upic.png"
            
        img1 = Image.open(f"{p1}")
        img2 = Image.open(f"{p2}")

        img = Image.open("SONALI_MUSIC/assets/cppic.png")

        img1 = img1.resize((390, 390))
        img2 = img2.resize((390,390))

        mask = Image.new('L', img1.size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + img1.size, fill=255)

        mask1 = Image.new('L', img2.size, 0)
        draw = ImageDraw.Draw(mask1) 
        draw.ellipse((0, 0) + img2.size, fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask1)

        draw = ImageDraw.Draw(img)

        img.paste(img1, (91, 215), img1)
        img.paste(img2, (805, 215), img2)

        img.save(f'test_{cid}.png')
    
        TXT = f"""
**ㅤ◦•●◉✿ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ  ✿◉●•◦
▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬▭

 {N1} + {N2} = ♥︎

❖ ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ sᴇʟᴇᴄᴛᴇᴅ ᴏɴ 
❖ ᴅᴀᴛᴇ -`{tomorrow}`
▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬▭**
"""
    
        await message.reply_photo(
            f"test_{cid}.png",
            caption=TXT,
            reply_markup=InlineKeyboardMarkup(POLICE),
            has_spoiler=True  
        )
        await msg.delete()

        a = upload_file(f"test_{cid}.png")
        for x in a:
            img = "https://graph.org/" + x
            couple = {"c1_id": c1_id, "c2_id": c2_id}
          
    except Exception as e:
        print(str(e))
    try:
        os.remove(f"./downloads/pfp1.png")
        os.remove(f"./downloads/pfp2.png")
        os.remove(f"test_{cid}.png")
    except Exception:
        pass

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
