# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import imghdr
import os
from asyncio import gather
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from SONALI_MUSIC import app
from SONALI_MUSIC.utils.errors import capture_err

from SONALI_MUSIC.utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)

from SONALI_MUSIC.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

# -----------

MAX_STICKERS = 120  # would be better if we could fetch this limit directly from telegram
SUPPORTED_TYPES = ["jpeg", "png", "webp"]

# ------------------------------------------
@app.on_message(filters.command("dlsticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("**✦ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ**")

    if not r.sticker:
        return await message.reply("**✦ ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ.**")

    m = await message.reply("✦ sᴇɴᴅɪɴɢ..")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)


#----------------
@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("**✦ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ/ɪᴍᴀɢᴇ ᴛᴏ ᴋᴀɴɢ ɪᴛ.**")
    if not message.from_user:
        return await message.reply_text(
            "**✦ ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴ ᴀᴅᴍɪɴ, ᴋᴀɴɢ sᴛɪᴄᴋᴇʀs ɪɴ ᴍʏ ᴅᴍ.**"
        )
    msg = await message.reply_text("**✦ ᴋᴀɴɢɪɴɢ sᴛɪᴄᴋᴇʀ...**")

    # Find the proper emoji
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif (
        message.reply_to_message.sticker
        and message.reply_to_message.sticker.emoji
    ):
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🙈"

    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    message.reply_to_message.sticker.file_id
                ),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("**✦ ғɪʟᴇ sɪᴢᴇ ᴛᴏᴏ ʟᴀʀɢᴇ.**")

            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit(
                    "Format not supported! ({})".format(image_type)
                )
            try:
                temp_file_path = await resize_file_to_sticker_size(
                    temp_file_path
                )
            except OSError as e:
                await msg.edit_text("**✦ sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.**")
                raise Exception(
                    f"✦ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ʀᴇsɪᴢɪɴɢ ᴛʜᴇ sᴛɪᴄᴋᴇʀ (at {temp_file_path}); {e}"
                )
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("**✦ ɴᴏᴘᴇ, ᴄᴀɴ'ᴛ  ᴋᴀɴɢ ᴛʜᴀᴛ.**")
    except ShortnameOccupyFailed:
        await message.reply_text("**✦ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ɴᴀᴍᴇ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ.**")
        return

    except Exception as e:
        await message.reply_text(str(e))
        e = format_exc()
        return print(e)

    #-------
    packnum = 0
    packname = "f" + str(message.from_user.id) + "_by_" + app.username
    limit = 0
    try:
        while True:
            # Prevent infinite rules
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s ᴘᴀᴄᴋ ʙʏ @{app.username}",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = (
                    "f"
                    + str(packnum)
                    + "_"
                    + str(message.from_user.id)
                    + "_by_"
                    + app.username
                )
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            break

        await msg.edit(
            f"**✦ sᴛɪᴄᴋᴇʀ ᴋᴀɴɢᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/{packname})**\n**✦ ᴇᴍᴏᴊɪ :-** {sticker_emoji}"
        )
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="⌯ sᴛᴀʀᴛ ɪɴ ᴘᴍ ⌯", url=f"t.me/{app.username}")]]
        )
        await msg.edit(
            "**✦ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ sᴛᴀʀᴛ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ.**",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await message.reply_text(
            "**✦ sᴛɪᴄᴋᴇʀs ᴍᴜsᴛ ʙᴇ ᴘɴɢ ғɪʟᴇs ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ɪᴍᴀɢᴇ ᴡᴀs ɴᴏᴛ ᴀ ᴘɴɢ.**"
        )
    except StickerPngDimensions:
        await message.reply_text("**✦ ᴛʜᴇ sᴛɪᴄᴋᴇʀ ᴘɴɢ ᴅɪᴍᴇɴsɪᴏɴs ᴀʀᴇ ɪɴᴠᴀʟɪᴅ.**")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
