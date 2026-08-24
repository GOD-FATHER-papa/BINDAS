import asyncio
import random
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram.raw import functions

from SONALI_MUSIC import app
from SONALI_MUSIC.utils.database import get_assistant
from SONALI_MUSIC.core.mongo import mongodb


LOGGER = getLogger(__name__)


# ==========================================================
# VC LOGGER CONFIG
# ==========================================================

# Agar separate log group/channel hai to yahan ID do.
# Example:
# VC_LOGGER_CHAT_ID = -1003979103138
#
# None = jis group me VC hai, usi group me log jayega.

VC_LOGGER_CHAT_ID = None


# ==========================================================
# VC DATA
# ==========================================================

vc_active_users: Dict[int, Set[int]] = {}
active_vc_chats: Set[int] = set()
vc_logging_status: Dict[int, bool] = {}

vcloggerdb = mongodb.vclogger

prefixes = [".", "!", "/", "@", "?", "'"]


# ==========================================================
# LOAD VC LOGGER STATUS
# ==========================================================

async def load_vc_logger_status():
    try:
        cursor = vcloggerdb.find({})

        enabled_chats = []

        async for doc in cursor:
            chat_id = doc.get("chat_id")
            status = doc.get("status", False)

            if chat_id is None:
                continue

            vc_logging_status[chat_id] = status

            if status:
                enabled_chats.append(chat_id)

        for chat_id in enabled_chats:
            asyncio.create_task(
                check_and_monitor_vc(chat_id)
            )

        LOGGER.info(
            f"Loaded VC logger status for "
            f"{len(vc_logging_status)} chats"
        )

        LOGGER.info(
            f"Started monitoring for "
            f"{len(enabled_chats)} enabled chats"
        )

    except Exception as e:
        LOGGER.error(
            f"Error loading VC logger status: {e}"
        )


# ==========================================================
# SAVE VC LOGGER STATUS
# ==========================================================

async def save_vc_logger_status(
    chat_id: int,
    status: bool
):
    try:
        await vcloggerdb.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "chat_id": chat_id,
                    "status": status,
                }
            },
            upsert=True,
        )

        LOGGER.info(
            f"Saved VC logger status for "
            f"{chat_id}: {status}"
        )

    except Exception as e:
        LOGGER.error(
            f"Error saving VC logger status: {e}"
        )


# ==========================================================
# GET VC LOGGER STATUS
# ==========================================================

async def get_vc_logger_status(chat_id: int) -> bool:
    if chat_id in vc_logging_status:
        return vc_logging_status[chat_id]

    try:
        doc = await vcloggerdb.find_one(
            {"chat_id": chat_id}
        )

        if doc:
            status = doc.get("status", False)

            vc_logging_status[chat_id] = status

            return status

    except Exception as e:
        LOGGER.error(
            f"Error getting VC logger status: {e}"
        )

    return False


# ==========================================================
# COMMAND FILTER
# ==========================================================

def generate_vclogger_filters():
    return (
        filters.command(
            "vclogger",
            prefixes=prefixes
        )
        & filters.group
    )


# ==========================================================
# VC LOGGER COMMAND
# ==========================================================

@app.on_message(generate_vclogger_filters())
async def vclogger_command(_, message: Message):

    chat_id = message.chat.id
    args = message.text.split()

    status = await get_vc_logger_status(chat_id)

    prefix_ui = ", ".join(
        f"<b>{p}vclogger</b>"
        for p in prefixes
    )

    current_state_ui = to_small_caps(
        str(status)
    )

    if len(args) == 1:

        text = (
            f"📌 <b>Current VC Logging State:</b> "
            f"<b>{current_state_ui}</b>\n\n"
            f"Use {prefix_ui} "
            f"<b>[on/enable/yes | off/disable/no]</b>"
        )

        await message.reply(
            text,
            disable_web_page_preview=True
        )

        return

    if len(args) == 2:

        arg = args[1].lower()

        # --------------------------------------------------
        # ENABLE
        # --------------------------------------------------

        if arg in [
            "on",
            "enable",
            "yes",
        ]:

            vc_logging_status[chat_id] = True

            await save_vc_logger_status(
                chat_id,
                True
            )

            await message.reply(
                "✅ <b>VC logging ENABLED</b>\n"
                f"Current State: "
                f"<b>{to_small_caps('True')}</b>",
                disable_web_page_preview=True
            )

            asyncio.create_task(
                check_and_monitor_vc(chat_id)
            )

            return

        # --------------------------------------------------
        # DISABLE
        # --------------------------------------------------

        if arg in [
            "off",
            "disable",
            "no",
        ]:

            vc_logging_status[chat_id] = False

            await save_vc_logger_status(
                chat_id,
                False
            )

            active_vc_chats.discard(chat_id)

            vc_active_users.pop(
                chat_id,
                None
            )

            await message.reply(
                "🚫 <b>VC logging DISABLED</b>\n"
                f"Current State: "
                f"<b>{to_small_caps('False')}</b>",
                disable_web_page_preview=True
            )

            return

        await message.reply(
            "❌ <b>Invalid argument!</b>\n\n"
            "Use <b>[on/enable/yes | "
            "off/disable/no]</b>",
            disable_web_page_preview=True
        )


# ==========================================================
# GET VC PARTICIPANTS
# ==========================================================

async def get_group_call_participants(
    userbot,
    peer
):

    try:

        full_chat = await userbot.invoke(
            functions.channels.GetFullChannel(
                channel=peer
            )
        )

        if not hasattr(
            full_chat.full_chat,
            "call"
        ):
            return []

        if not full_chat.full_chat.call:
            return []

        call = full_chat.full_chat.call

        participants = await userbot.invoke(
            functions.phone.GetGroupParticipants(
                call=call,
                ids=[],
                sources=[],
                offset="",
                limit=100
            )
        )

        return participants.participants

    except Exception as e:

        error_msg = str(e).upper()

        # --------------------------------------------------
        # FLOOD WAIT
        # --------------------------------------------------

        if "FLOOD_WAIT_" in error_msg:

            try:
                wait_time = int(
                    error_msg.split(
                        "FLOOD_WAIT_"
                    )[1].split("]")[0]
                )
            except Exception:
                wait_time = 10

            LOGGER.warning(
                f"Flood wait detected, "
                f"sleeping {wait_time}s"
            )

            await asyncio.sleep(
                wait_time + 1
            )

            return await get_group_call_participants(
                userbot,
                peer
            )

        # --------------------------------------------------
        # NO ACTIVE CALL
        # --------------------------------------------------

        if any(
            x in error_msg
            for x in (
                "GROUPCALL_NOT_FOUND",
                "CALL_NOT_FOUND",
                "NO_GROUPCALL",
            )
        ):
            return []

        LOGGER.error(
            f"Error fetching participants: {e}"
        )

        return []


# ==========================================================
# USER INFO
# ==========================================================

def get_user_full_name(user):

    try:

        first_name = user.first_name or ""
        last_name = user.last_name or ""

        name = f"{first_name} {last_name}".strip()

        return name or "ㅤ-"

    except Exception:

        return "ㅤ-"


def get_user_username(user):

    try:

        if user.username:
            return f"@{user.username}"

    except Exception:
        pass

    return ""


# ==========================================================
# USER ROLE
# ==========================================================

async def get_user_role(
    chat_id: int,
    user_id: int
):

    try:

        member = await app.get_chat_member(
            chat_id,
            user_id
        )

        if member.status == ChatMemberStatus.OWNER:
            return "Owner"

        if member.status == ChatMemberStatus.ADMINISTRATOR:
            return "Admin"

        if member.status == ChatMemberStatus.RESTRICTED:
            return "Restricted"

    except Exception as e:

        LOGGER.warning(
            f"Could not get role for "
            f"{user_id}: {e}"
        )

    return "Member"


# ==========================================================
# SEND VC LOG
# ==========================================================

async def send_vc_log(
    chat_id: int,
    user_id: int,
    action: str,
    participants_count: int,
    userbot
):

    try:

        # --------------------------------------------------
        # LOG CHAT
        # --------------------------------------------------

        log_chat_id = (
            VC_LOGGER_CHAT_ID
            if VC_LOGGER_CHAT_ID
            else chat_id
        )

        # --------------------------------------------------
        # GROUP
        # --------------------------------------------------

        try:

            chat = await app.get_chat(
                chat_id
            )

            group_name = (
                chat.title
                or "Unknown Group"
            )

        except Exception:

            group_name = "Unknown Group"

        # --------------------------------------------------
        # USER
        # --------------------------------------------------

        try:

            user = await userbot.get_users(
                user_id
            )

        except Exception:

            try:

                user = await app.get_users(
                    user_id
                )

            except Exception:

                user = None

        if user:

            name = get_user_full_name(
                user
            )

            username = get_user_username(
                user
            )

        else:

            name = "ㅤ-"
            username = ""

        # --------------------------------------------------
        # ROLE
        # --------------------------------------------------

        role = await get_user_role(
            chat_id,
            user_id
        )

        # --------------------------------------------------
        # ACTION
        # --------------------------------------------------

        if action == "Joined":

            action_text = (
                f"Joined [{role}]"
            )

            tag = "#JoinVideoChat"

        else:

            action_text = (
                f"Left [{role}]"
            )

            tag = "#LeaveVideoChat"

        # --------------------------------------------------
        # FINAL LOG
        # --------------------------------------------------

        log_text = (
            f"<b>{tag}</b>\n"
            f"<b>Group ➛</b> "
            f"{group_name}\n"
            f"<b>Name ➛</b> "
            f"{name}\n"
            f"<b>Id ➛</b> "
            f"{user_id}\n"
            f"<b>Username ➛</b> "
            f"{username}\n"
            f"<b>Action ➛</b> "
            f"{action_text}\n"
            f"<b>Participants ➛</b> "
            f"{participants_count}"
        )

        await app.send_message(
            log_chat_id,
            log_text,
            disable_web_page_preview=True
        )

        LOGGER.info(
            f"{tag} sent for {user_id} "
            f"in {chat_id}"
        )

    except Exception as e:

        LOGGER.error(
            f"Error sending VC log: {e}"
        )


# ==========================================================
# MONITOR VC
# ==========================================================

async def monitor_vc_chat(chat_id):

    userbot = await get_assistant(
        chat_id
    )

    if not userbot:

        LOGGER.warning(
            f"No assistant found "
            f"for {chat_id}"
        )

        active_vc_chats.discard(
            chat_id
        )

        return

    while (
        chat_id in active_vc_chats
        and await get_vc_logger_status(
            chat_id
        )
    ):

        try:

            peer = await userbot.resolve_peer(
                chat_id
            )

            participants_list = (
                await get_group_call_participants(
                    userbot,
                    peer
                )
            )

            new_users = set()

            for participant in participants_list:

                if (
                    hasattr(
                        participant,
                        "peer"
                    )
                    and hasattr(
                        participant.peer,
                        "user_id"
                    )
                ):

                    new_users.add(
                        participant.peer.user_id
                    )

            current_users = (
                vc_active_users.get(
                    chat_id,
                    set()
                )
            )

            joined = (
                new_users
                - current_users
            )

            left = (
                current_users
                - new_users
            )

            # --------------------------------------------------
            # JOIN USERS
            # --------------------------------------------------

            if joined:

                tasks = []

                for user_id in joined:

                    tasks.append(
                        handle_user_join(
                            chat_id,
                            user_id,
                            userbot,
                            len(new_users)
                        )
                    )

                await asyncio.gather(
                    *tasks,
                    return_exceptions=True
                )

            # --------------------------------------------------
            # LEAVE USERS
            # --------------------------------------------------

            if left:

                tasks = []

                for user_id in left:

                    tasks.append(
                        handle_user_leave(
                            chat_id,
                            user_id,
                            userbot,
                            len(new_users)
                        )
                    )

                await asyncio.gather(
                    *tasks,
                    return_exceptions=True
                )

            # --------------------------------------------------
            # UPDATE STATE
            # --------------------------------------------------

            vc_active_users[
                chat_id
            ] = new_users

        except Exception as e:

            LOGGER.error(
                f"Error monitoring VC "
                f"for {chat_id}: {e}"
            )

        await asyncio.sleep(5)


# ==========================================================
# START MONITOR
# ==========================================================

async def check_and_monitor_vc(
    chat_id
):

    if not await get_vc_logger_status(
        chat_id
    ):
        return

    userbot = await get_assistant(
        chat_id
    )

    if not userbot:

        LOGGER.warning(
            f"No assistant available "
            f"for {chat_id}"
        )

        return

    try:

        if chat_id in active_vc_chats:
            return

        active_vc_chats.add(
            chat_id
        )

        # --------------------------------------------------
        # INITIAL VC STATE
        # --------------------------------------------------

        try:

            peer = await userbot.resolve_peer(
                chat_id
            )

            participants = (
                await get_group_call_participants(
                    userbot,
                    peer
                )
            )

            current_users = set()

            for participant in participants:

                if (
                    hasattr(
                        participant,
                        "peer"
                    )
                    and hasattr(
                        participant.peer,
                        "user_id"
                    )
                ):

                    current_users.add(
                        participant.peer.user_id
                    )

            vc_active_users[
                chat_id
            ] = current_users

        except Exception as e:

            LOGGER.warning(
                f"Could not initialize VC "
                f"state for {chat_id}: {e}"
            )

            vc_active_users[
                chat_id
            ] = set()

        asyncio.create_task(
            monitor_vc_chat(
                chat_id
            )
        )

        LOGGER.info(
            f"Started VC monitoring "
            f"for {chat_id}"
        )

    except Exception as e:

        LOGGER.error(
            f"Error in check_and_monitor_vc: {e}"
        )


# ==========================================================
# HANDLE JOIN
# ==========================================================

async def handle_user_join(
    chat_id,
    user_id,
    userbot,
    participants_count=0
):

    try:

        user = await userbot.get_users(
            user_id
        )

        name = (
            user.first_name
            or "Someone"
        )

        mention = (
            f'<a href="tg://user?id={user_id}">'
            f'<b>{to_small_caps(name)}</b>'
            f'</a>'
        )

        messages = [

            f"🎤 {mention} "
            f"<b>ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴄ – "
            f"ʟᴇᴛ's ᴍᴀᴋᴇ ɪᴛ ʟɪᴠᴇʟʏ! 🎶</b>",

            f"✨ {mention} "
            f"<b>ɪs ɴᴏᴡ ɪɴ ᴛʜᴇ ᴠᴄ – "
            f"ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ! 💫</b>",

            f"🎵 {mention} "
            f"<b>ʜᴀs ᴊᴏɪɴᴇᴅ – "
            f"ʟᴇᴛ's ʀᴏᴄᴋ ᴛʜɪs ᴠɪʙᴇ! 🔥</b>",
        ]

        msg = random.choice(
            messages
        )

        sent_msg = await app.send_message(
            chat_id,
            msg
        )

        # --------------------------------------------------
        # JOIN LOG
        # --------------------------------------------------

        await send_vc_log(
            chat_id=chat_id,
            user_id=user_id,
            action="Joined",
            participants_count=participants_count,
            userbot=userbot
        )

        asyncio.create_task(
            delete_after_delay(
                sent_msg,
                10
            )
        )

    except Exception as e:

        LOGGER.error(
            f"Error sending join message "
            f"for {user_id}: {e}"
        )


# ==========================================================
# HANDLE LEAVE
# ==========================================================

async def handle_user_leave(
    chat_id,
    user_id,
    userbot,
    participants_count=0
):

    try:

        user = await userbot.get_users(
            user_id
        )

        name = (
            user.first_name
            or "Someone"
        )

        mention = (
            f'<a href="tg://user?id={user_id}">'
            f'<b>{to_small_caps(name)}</b>'
            f'</a>'
        )

        messages = [

            f"👋 {mention} "
            f"<b>ʟᴇғᴛ ᴛʜᴇ ᴠᴄ – "
            f"ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ʙᴀᴄᴋ sᴏᴏɴ! 🌟</b>",

            f"🚪 {mention} "
            f"<b>sᴛᴇᴘᴘᴇᴅ ᴏᴜᴛ – "
            f"ᴅᴏɴ'ᴛ ᴛᴀᴋᴇ ᴛᴏᴏ ʟᴏɴɢ, "
            f"ᴡᴇ'ʟʟ ᴍɪss ʏᴏᴜ! 💖</b>",

            f"✌️ {mention} "
            f"<b>sᴀɪᴅ ɢᴏᴏᴅʙʏᴇ – "
            f"ᴄᴏᴍᴇ ʙᴀᴄᴋ "
            f"ᴀɴᴅ ᴊᴏɪɴ "
            f"ᴛʜᴇ ғᴜɴ ᴀɢᴀɪɴ! 🎶</b>",
        ]

        msg = random.choice(
            messages
        )

        sent_msg = await app.send_message(
            chat_id,
            msg
        )

        # --------------------------------------------------
        # LEAVE LOG
        # --------------------------------------------------

        await send_vc_log(
            chat_id=chat_id,
            user_id=user_id,
            action="Left",
            participants_count=participants_count,
            userbot=userbot
        )

        asyncio.create_task(
            delete_after_delay(
                sent_msg,
                10
            )
        )

    except Exception as e:

        LOGGER.error(
            f"Error sending leave message "
            f"for {user_id}: {e}"
        )


# ==========================================================
# DELETE MESSAGE
# ==========================================================

async def delete_after_delay(
    message,
    delay
):

    try:

        await asyncio.sleep(
            delay
        )

        await message.delete()

    except Exception:
        pass


# ==========================================================
# SMALL CAPS
# ==========================================================

def to_small_caps(text):

    mapping = {

        "a": "ᴀ",
        "b": "ʙ",
        "c": "ᴄ",
        "d": "ᴅ",
        "e": "ᴇ",
        "f": "ꜰ",
        "g": "ɢ",
        "h": "ʜ",
        "i": "ɪ",
        "j": "ᴊ",
        "k": "ᴋ",
        "l": "ʟ",
        "m": "ᴍ",
        "n": "ɴ",
        "o": "ᴏ",
        "p": "ᴘ",
        "q": "ǫ",
        "r": "ʀ",
        "s": "s",
        "t": "ᴛ",
        "u": "ᴜ",
        "v": "ᴠ",
        "w": "ᴡ",
        "x": "x",
        "y": "ʏ",
        "z": "ᴢ",

        "A": "ᴀ",
        "B": "ʙ",
        "C": "ᴄ",
        "D": "ᴅ",
        "E": "ᴇ",
        "F": "ꜰ",
        "G": "ɢ",
        "H": "ʜ",
        "I": "ɪ",
        "J": "ᴊ",
        "K": "ᴋ",
        "L": "ʟ",
        "M": "ᴍ",
        "N": "ɴ",
        "O": "ᴏ",
        "P": "ᴘ",
        "Q": "ǫ",
        "R": "ʀ",
        "S": "s",
        "T": "ᴛ",
        "U": "ᴜ",
        "V": "ᴠ",
        "W": "ᴡ",
        "X": "x",
        "Y": "ʏ",
        "Z": "ᴢ",
    }

    return "".join(
        mapping.get(c, c)
        for c in text
    )


# ==========================================================
# INITIALIZE
# ==========================================================

async def initialize_vc_logger():

    await load_vc_logger_status()
