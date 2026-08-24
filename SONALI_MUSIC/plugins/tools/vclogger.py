# ==========================================================
# ©️ VC LOGGER SYSTEM
# ==========================================================

import asyncio
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram.raw import functions

from SONALI_MUSIC import app
from SONALI_MUSIC.utils.database import get_assistant
from SONALI_MUSIC.core.mongo import mongodb


# ==========================================================
# LOGGER
# ==========================================================

LOGGER = getLogger(__name__)


# ==========================================================
# CONFIG
# ==========================================================

# None = same group me log send hoga.
# Separate logger group ke liye:
#
# VC_LOGGER_CHAT_ID = -1001234567890

VC_LOGGER_CHAT_ID = None

# Log message kitne seconds baad delete hoga
VC_LOG_DELETE_AFTER = 10

# Same event ka duplicate log block
VC_LOG_COOLDOWN = 5

# VC participants check interval
VC_CHECK_INTERVAL = 5


# ==========================================================
# DATABASE
# ==========================================================

vcloggerdb = mongodb.vclogger


# ==========================================================
# MEMORY
# ==========================================================

vc_active_users: Dict[int, Set[int]] = {}

active_vc_chats: Set[int] = set()

vc_logging_status: Dict[int, bool] = {}

vc_monitor_tasks: Dict[int, asyncio.Task] = {}

vc_log_cooldown = {}


# ==========================================================
# COMMAND PREFIXES
# ==========================================================

prefixes = [
    ".",
    "!",
    "/",
    "@",
    "?",
    "'",
]


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
        mapping.get(char, char)
        for char in str(text)
    )


# ==========================================================
# LOAD LOGGER STATUS
# ==========================================================

async def load_vc_logger_status():

    try:

        cursor = vcloggerdb.find({})

        enabled_count = 0

        async for doc in cursor:

            chat_id = doc.get("chat_id")

            if chat_id is None:
                continue

            status = bool(
                doc.get(
                    "status",
                    False
                )
            )

            vc_logging_status[
                chat_id
            ] = status

            if status:

                enabled_count += 1

                start_vc_monitor(
                    chat_id
                )

        LOGGER.info(
            "Loaded VC logger status for "
            f"{len(vc_logging_status)} chats"
        )

        LOGGER.info(
            f"Started {enabled_count} VC monitors"
        )

    except Exception as e:

        LOGGER.exception(
            "Error loading VC logger status: "
            f"{e}"
        )


# ==========================================================
# SAVE LOGGER STATUS
# ==========================================================

async def save_vc_logger_status(
    chat_id: int,
    status: bool
):

    try:

        await vcloggerdb.update_one(
            {
                "chat_id": chat_id
            },
            {
                "$set": {
                    "chat_id": chat_id,
                    "status": bool(status),
                }
            },
            upsert=True,
        )

    except Exception as e:

        LOGGER.exception(
            "Error saving VC logger status: "
            f"{e}"
        )


# ==========================================================
# GET LOGGER STATUS
# ==========================================================

async def get_vc_logger_status(
    chat_id: int
) -> bool:

    if chat_id in vc_logging_status:

        return vc_logging_status[
            chat_id
        ]

    try:

        doc = await vcloggerdb.find_one(
            {
                "chat_id": chat_id
            }
        )

        if doc:

            status = bool(
                doc.get(
                    "status",
                    False
                )
            )

            vc_logging_status[
                chat_id
            ] = status

            return status

    except Exception as e:

        LOGGER.error(
            "Error getting VC logger status "
            f"for {chat_id}: {e}"
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
# START MONITOR
# ==========================================================

def start_vc_monitor(
    chat_id: int
):

    task = vc_monitor_tasks.get(
        chat_id
    )

    if task and not task.done():

        return

    task = asyncio.create_task(
        check_and_monitor_vc(
            chat_id
        )
    )

    vc_monitor_tasks[
        chat_id
    ] = task


# ==========================================================
# STOP MONITOR
# ==========================================================

def stop_vc_monitor(
    chat_id: int
):

    task = vc_monitor_tasks.pop(
        chat_id,
        None
    )

    if task and not task.done():

        task.cancel()


# ==========================================================
# VC LOGGER COMMAND
# ==========================================================

@app.on_message(
    generate_vclogger_filters()
)
async def vclogger_command(
    _,
    message: Message
):

    try:

        chat_id = message.chat.id

        args = (
            message.text or ""
        ).split()

        status = await get_vc_logger_status(
            chat_id
        )

        # ==================================================
        # STATUS
        # ==================================================

        if len(args) == 1:

            state = (
                "ᴇɴᴀʙʟᴇᴅ"
                if status
                else
                "ᴅɪsᴀʙʟᴇᴅ"
            )

            await message.reply(
                "<blockquote>"
                "❖ <b>ᴠᴄ ʟᴏɢɢᴇʀ</b>\n\n"
                "╭───────────────\n"
                f"├ <b>sᴛᴀᴛᴜs</b> ➛ {state}\n"
                "╰───────────────\n\n"
                "ᴜsᴇ:\n"
                f"➜ <b>{prefixes[0]}vclogger on</b>\n"
                f"➜ <b>{prefixes[0]}vclogger off</b>"
                "</blockquote>"
            )

            return

        # ==================================================
        # ENABLE
        # ==================================================

        arg = args[1].lower()

        if arg in (
            "on",
            "enable",
            "yes",
        ):

            vc_logging_status[
                chat_id
            ] = True

            await save_vc_logger_status(
                chat_id,
                True
            )

            start_vc_monitor(
                chat_id
            )

            await message.reply(
                "<blockquote>"
                "❖ <b>ᴠᴄ ʟᴏɢɢᴇʀ</b>\n\n"
                "╭───────────────\n"
                "├ <b>sᴛᴀᴛᴜs</b> ➛ ᴇɴᴀʙʟᴇᴅ\n"
                "╰───────────────\n\n"
                "✦ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴊᴏɪɴ/ʟᴇᴀᴠᴇ "
                "ʟᴏɢɢɪɴɢ ᴀᴄᴛɪᴠᴇ."
                "</blockquote>"
            )

            return

        # ==================================================
        # DISABLE
        # ==================================================

        if arg in (
            "off",
            "disable",
            "no",
        ):

            vc_logging_status[
                chat_id
            ] = False

            await save_vc_logger_status(
                chat_id,
                False
            )

            active_vc_chats.discard(
                chat_id
            )

            vc_active_users.pop(
                chat_id,
                None
            )

            stop_vc_monitor(
                chat_id
            )

            await message.reply(
                "<blockquote>"
                "❖ <b>ᴠᴄ ʟᴏɢɢᴇʀ</b>\n\n"
                "╭───────────────\n"
                "├ <b>sᴛᴀᴛᴜs</b> ➛ ᴅɪsᴀʙʟᴇᴅ\n"
                "╰───────────────"
                "</blockquote>"
            )

            return

        # ==================================================
        # INVALID
        # ==================================================

        await message.reply(
            "<blockquote>"
            "❌ <b>ɪɴᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛ</b>\n\n"
            "ᴜsᴇ <b>on</b> ᴏʀ <b>off</b>."
            "</blockquote>"
        )

    except Exception as e:

        LOGGER.exception(
            f"Error in vclogger command: {e}"
        )


# ==========================================================
# GET GROUP CALL PARTICIPANTS
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

        call = getattr(
            full_chat.full_chat,
            "call",
            None
        )

        if not call:

            return []

        participants = await userbot.invoke(
            functions.phone.GetGroupParticipants(
                call=call,
                ids=[],
                sources=[],
                offset="",
                limit=100,
            )
        )

        return (
            participants.participants
            or []
        )

    except Exception as e:

        error_msg = str(e).upper()

        # ==================================================
        # FLOOD WAIT
        # ==================================================

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
                f"Flood wait detected: "
                f"{wait_time}s"
            )

            await asyncio.sleep(
                wait_time + 1
            )

            return await get_group_call_participants(
                userbot,
                peer
            )

        # ==================================================
        # NO CALL
        # ==================================================

        if any(
            error_name in error_msg
            for error_name in (
                "GROUPCALL_NOT_FOUND",
                "CALL_NOT_FOUND",
                "NO_GROUPCALL",
            )
        ):

            return []

        LOGGER.error(
            "Error fetching VC participants: "
            f"{e}"
        )

        return []


# ==========================================================
# USER FULL NAME
# ==========================================================

def get_user_full_name(
    user
):

    try:

        first_name = (
            getattr(
                user,
                "first_name",
                None
            )
            or ""
        )

        last_name = (
            getattr(
                user,
                "last_name",
                None
            )
            or ""
        )

        name = (
            f"{first_name} {last_name}"
            .strip()
        )

        return name or "ㅤ-"

    except Exception:

        return "ㅤ-"


# ==========================================================
# USERNAME
# ==========================================================

def get_user_username(
    user
):

    try:

        username = getattr(
            user,
            "username",
            None
        )

        if username:

            return (
                f"@{username}"
            )

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

        status = member.status

        if (
            status
            == ChatMemberStatus.OWNER
        ):

            return "ᴏᴡɴᴇʀ"

        if (
            status
            == ChatMemberStatus.ADMINISTRATOR
        ):

            return "ᴀᴅᴍɪɴ"

        if (
            status
            == ChatMemberStatus.RESTRICTED
        ):

            return "ʀᴇsᴛʀɪᴄᴛᴇᴅ"

    except Exception as e:

        LOGGER.warning(
            f"Could not get role "
            f"for {user_id}: {e}"
        )

    return "ᴍᴇᴍʙᴇʀ"


# ==========================================================
# SPAM PROTECTION
# ==========================================================

async def is_vc_log_allowed(
    chat_id: int,
    user_id: int,
    action: str
):

    try:

        key = (
            chat_id,
            user_id,
            action
        )

        now = (
            asyncio.get_running_loop()
            .time()
        )

        last_time = vc_log_cooldown.get(
            key,
            0
        )

        if (
            now - last_time
            < VC_LOG_COOLDOWN
        ):

            return False

        vc_log_cooldown[
            key
        ] = now

        if len(
            vc_log_cooldown
        ) > 1000:

            expired = [
                key
                for key, timestamp
                in vc_log_cooldown.items()
                if now - timestamp > 30
            ]

            for key in expired:

                vc_log_cooldown.pop(
                    key,
                    None
                )

        return True

    except Exception:

        return True


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

        allowed = await is_vc_log_allowed(
            chat_id,
            user_id,
            action
        )

        if not allowed:

            return

        # ==================================================
        # LOG DESTINATION
        # ==================================================

        log_chat_id = (
            VC_LOGGER_CHAT_ID
            if VC_LOGGER_CHAT_ID
            else chat_id
        )

        # ==================================================
        # GROUP INFO
        # ==================================================

        try:

            chat = await app.get_chat(
                chat_id
            )

            group_name = (
                getattr(
                    chat,
                    "title",
                    None
                )
                or
                "ᴜɴᴋɴᴏᴡɴ ɢʀᴏᴜᴘ"
            )

        except Exception:

            group_name = (
                "ᴜɴᴋɴᴏᴡɴ ɢʀᴏᴜᴘ"
            )

        # ==================================================
        # USER INFO
        # ==================================================

        user = None

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

        # ==================================================
        # ROLE
        # ==================================================

        role = await get_user_role(
            chat_id,
            user_id
        )

        # ==================================================
        # ACTION
        # ==================================================

        if action == "Joined":

            tag = (
                "❖ #ᴊᴏɪɴᴠɪᴅᴇᴏᴄʜᴀᴛ"
            )

            action_text = (
                f"ᴊᴏɪɴᴇᴅ [{role}]"
            )

        else:

            tag = (
                "❖ #ʟᴇᴀᴠᴇᴠɪᴅᴇᴏᴄʜᴀᴛ"
            )

            action_text = (
                f"ʟᴇꜰᴛ [{role}]"
            )

        # ==================================================
        # FINAL LOG
        # ==================================================

        log_text = (
            "<blockquote>"
            f"<b>{tag}</b>\n"
            "╭───────────────\n"
            f"├ <b>ɢʀᴏᴜᴘ</b> ➛ "
            f"{group_name}\n"
            f"├ <b>ɴᴀᴍᴇ</b> ➛ "
            f"{name}\n"
            f"├ <b>ɪᴅ</b> ➛ "
            f"<code>{user_id}</code>\n"
            f"├ <b>ᴜsᴇʀɴᴀᴍᴇ</b> ➛ "
            f"{username or 'ㅤ-'}\n"
            f"├ <b>ᴀᴄᴛɪᴏɴ</b> ➛ "
            f"{action_text}\n"
            f"├ <b>ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛs</b> ➛ "
            f"{participants_count}\n"
            "╰───────────────"
            "</blockquote>"
        )

        # ==================================================
        # SEND
        # ==================================================

        sent = await app.send_message(
            log_chat_id,
            log_text,
            disable_web_page_preview=True
        )

        # ==================================================
        # DELETE
        # ==================================================

        if VC_LOG_DELETE_AFTER > 0:

            await asyncio.sleep(
                VC_LOG_DELETE_AFTER
            )

            try:

                await sent.delete()

            except Exception:

                pass

    except Exception as e:

        LOGGER.exception(
            "Error sending VC log: "
            f"{e}"
        )


# ==========================================================
# GET CURRENT VC USERS
# ==========================================================

async def get_current_vc_users(
    userbot,
    peer
):

    participants = (
        await get_group_call_participants(
            userbot,
            peer
        )
    )

    users = set()

    for participant in participants:

        user_id = getattr(
            participant,
            "user_id",
            None
        )

        if user_id:

            users.add(
                user_id
            )

    return users


# ==========================================================
# MONITOR VC
# ==========================================================

async def check_and_monitor_vc(
    chat_id: int
):

    if chat_id in active_vc_chats:

        return

    active_vc_chats.add(
        chat_id
    )

    try:

        # ==================================================
        # STATUS CHECK
        # ==================================================

        if not await get_vc_logger_status(
            chat_id
        ):

            return

        # ==================================================
        # ASSISTANT
        # ==================================================

        userbot = await get_assistant(
            chat_id
        )

        if not userbot:

            LOGGER.warning(
                f"Assistant not found "
                f"for {chat_id}"
            )

            return

        # ==================================================
        # PEER
        # ==================================================

        peer = await userbot.resolve_peer(
            chat_id
        )

        old_users = set()

        # ==================================================
        # INITIAL PARTICIPANTS
        # ==================================================

        try:

            old_users = (
                await get_current_vc_users(
                    userbot,
                    peer
                )
            )

        except Exception as e:

            LOGGER.warning(
                f"Initial VC fetch failed "
                f"for {chat_id}: {e}"
            )

            old_users = set()

        vc_active_users[
            chat_id
        ] = old_users

        # ==================================================
        # LOOP
        # ==================================================

        while await get_vc_logger_status(
            chat_id
        ):

            try:

                current_users = (
                    await get_current_vc_users(
                        userbot,
                        peer
                    )
                )

                # ==================================================
                # JOINED USERS
                # ==================================================

                joined_users = (
                    current_users - old_users
                )

                for user_id in joined_users:

                    await send_vc_log(
                        chat_id=chat_id,
                        user_id=user_id,
                        action="Joined",
                        participants_count=len(
                            current_users
                        ),
                        userbot=userbot,
                    )

                # ==================================================
                # LEFT USERS
                # ==================================================

                left_users = (
                    old_users - current_users
                )

                for user_id in left_users:

                    await send_vc_log(
                        chat_id=chat_id,
                        user_id=user_id,
                        action="Left",
                        participants_count=len(
                            current_users
                        ),
                        userbot=userbot,
                    )

                old_users = current_users

                vc_active_users[
                    chat_id
                ] = current_users

                await asyncio.sleep(
                    VC_CHECK_INTERVAL
                )

            except asyncio.CancelledError:

                raise

            except Exception as e:

                LOGGER.error(
                    f"VC monitor error "
                    f"for {chat_id}: {e}"
                )

                await asyncio.sleep(
                    VC_CHECK_INTERVAL
                )

    except asyncio.CancelledError:

        LOGGER.info(
            f"VC monitor cancelled: "
            f"{chat_id}"
        )

    except Exception as e:

        LOGGER.exception(
            f"VC monitor crashed "
            f"for {chat_id}: {e}"
        )

    finally:

        active_vc_chats.discard(
            chat_id
        )

        vc_active_users.pop(
            chat_id,
            None
        )

        vc_monitor_tasks.pop(
            chat_id,
            None
        )


# ==========================================================
# STARTUP INITIALIZER
# ==========================================================

async def init_vc_logger():

    await load_vc_logger_status()


# ==========================================================
# END
# ==========================================================
