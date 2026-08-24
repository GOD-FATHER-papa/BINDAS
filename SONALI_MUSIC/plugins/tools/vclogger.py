import asyncio
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.raw import functions

from SONALI_MUSIC import app
from SONALI_MUSIC.utils.database import get_assistant
from SONALI_MUSIC.core.mongo import mongodb


# ==========================================================
# LOGGER
# ==========================================================

LOGGER = getLogger(__name__)


# ==========================================================
# VC LOGGER CONFIG
# ==========================================================

# None = jis group me VC hai, usi group me log jayega.
#
# Agar separate log group/channel chahiye:
#
# VC_LOGGER_CHAT_ID = -1001234567890

VC_LOGGER_CHAT_ID = None


# ==========================================================
# SETTINGS
# ==========================================================

# VC log 5 seconds baad delete hoga
VC_LOG_DELETE_AFTER = 5

# Same event 5 seconds ke andar repeat nahi hoga
VC_LOG_COOLDOWN = 5

# VC check interval
VC_CHECK_INTERVAL = 5


# ==========================================================
# VC DATA
# ==========================================================

vc_active_users: Dict[int, Set[int]] = {}

active_vc_chats: Set[int] = set()

vc_logging_status: Dict[int, bool] = {}

vcloggerdb = mongodb.vclogger


# ==========================================================
# SPAM PROTECTION DATA
# ==========================================================

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
        mapping.get(
            char,
            char
        )
        for char in text
    )


# ==========================================================
# LOAD LOGGER STATUS
# ==========================================================

async def load_vc_logger_status():

    try:

        cursor = vcloggerdb.find({})

        enabled_chats = []

        async for doc in cursor:

            chat_id = doc.get("chat_id")

            status = doc.get(
                "status",
                False
            )

            if chat_id is None:
                continue

            vc_logging_status[
                chat_id
            ] = status

            if status:
                enabled_chats.append(
                    chat_id
                )

        for chat_id in enabled_chats:

            asyncio.create_task(
                check_and_monitor_vc(
                    chat_id
                )
            )

        LOGGER.info(
            f"Loaded VC logger status "
            f"for {len(vc_logging_status)} chats"
        )

        LOGGER.info(
            f"Started monitoring "
            f"{len(enabled_chats)} enabled chats"
        )

    except Exception as e:

        LOGGER.error(
            f"Error loading VC logger status: {e}"
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
                    "status": status,
                }
            },
            upsert=True,
        )

        LOGGER.info(
            f"Saved VC logger status "
            f"for {chat_id}: {status}"
        )

    except Exception as e:

        LOGGER.error(
            f"Error saving VC logger status: {e}"
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

            status = doc.get(
                "status",
                False
            )

            vc_logging_status[
                chat_id
            ] = status

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

        prefix_ui = ", ".join(
            [
                f"<b>{p}vclogger</b>"
                for p in prefixes
            ]
        )

        current_state_ui = (
            to_small_caps(
                str(status)
            )
        )

        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        if len(args) == 1:

            text = (
                f"📌 <b>Current VC Logging "
                f"State:</b> "
                f"<b>{current_state_ui}</b>\n\n"
                f"Use {prefix_ui} "
                f"<b>[on/enable/yes | "
                f"off/disable/no]</b>"
            )

            await message.reply(
                text,
                disable_web_page_preview=True
            )

            return

        # --------------------------------------------------
        # ARGUMENT
        # --------------------------------------------------

        if len(args) == 2:

            arg = args[1].lower()

            # ==============================================
            # ENABLE
            # ==============================================

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

                await message.reply(
                    "✅ <b>VC logging ENABLED</b>\n"
                    "Current State: <b>True</b>",
                    disable_web_page_preview=True
                )

                asyncio.create_task(
                    check_and_monitor_vc(
                        chat_id
                    )
                )

                return

            # ==============================================
            # DISABLE
            # ==============================================

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

                await message.reply(
                    "🚫 <b>VC logging DISABLED</b>\n"
                    "Current State: <b>False</b>",
                    disable_web_page_preview=True
                )

                return

            # ==============================================
            # INVALID
            # ==============================================

            await message.reply(
                "❌ <b>Invalid argument!</b>\n\n"
                "Use <b>[on/enable/yes | "
                "off/disable/no]</b>",
                disable_web_page_preview=True
            )

    except Exception as e:

        LOGGER.error(
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
                limit=100,
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
                f"Flood wait detected. "
                f"Sleeping {wait_time}s."
            )

            await asyncio.sleep(
                wait_time + 1
            )

            return await get_group_call_participants(
                userbot,
                peer
            )

        # --------------------------------------------------
        # NO GROUP CALL
        # --------------------------------------------------

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
            f"Error fetching VC participants: {e}"
        )

        return []


# ==========================================================
# USER NAME
# ==========================================================

def get_user_full_name(
    user
):

    try:

        first_name = (
            user.first_name
            or ""
        )

        last_name = (
            user.last_name
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

        if user.username:

            return (
                f"@{user.username}"
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

        last_time = (
            vc_log_cooldown.get(
                key,
                0
            )
        )

        # --------------------------------------------------
        # SAME EVENT WITHIN 5 SECONDS
        # --------------------------------------------------

        if (
            now - last_time
            < VC_LOG_COOLDOWN
        ):

            return False

        vc_log_cooldown[
            key
        ] = now

        # --------------------------------------------------
        # CLEAN OLD CACHE
        # --------------------------------------------------

        if len(vc_log_cooldown) > 1000:

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
# GET GROUP LINK
# ==========================================================

async def get_group_link(
    chat
):

    try:

        # --------------------------------------------------
        # PUBLIC GROUP
        # --------------------------------------------------

        if chat.username:

            return (
                f"https://t.me/"
                f"{chat.username}"
            )

        # --------------------------------------------------
        # PRIVATE GROUP
        # --------------------------------------------------

        try:

            return await app.export_chat_invite_link(
                chat.id
            )

        except Exception as e:

            LOGGER.warning(
                f"Could not export invite link: "
                f"{e}"
            )

    except Exception as e:

        LOGGER.warning(
            f"Could not get group link: {e}"
        )

    return None


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
        # SPAM PROTECTION
        # --------------------------------------------------

        allowed = await is_vc_log_allowed(
            chat_id,
            user_id,
            action
        )

        if not allowed:

            LOGGER.info(
                f"Duplicate VC log ignored: "
                f"{user_id} -> {action}"
            )

            return

        # --------------------------------------------------
        # LOG DESTINATION
        # --------------------------------------------------

        if VC_LOGGER_CHAT_ID:

            log_chat_id = (
                VC_LOGGER_CHAT_ID
            )

        else:

            log_chat_id = chat_id

        # --------------------------------------------------
        # GROUP INFO
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

            chat = None

            group_name = (
                "Unknown Group"
            )

        # --------------------------------------------------
        # USER INFO
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

            tag = (
                "#ᴊᴏɪɴᴠɪᴅᴇᴏᴄʜᴀᴛ"
            )

            action_text = (
                f"Joined [{role}]"
            )

        else:

            tag = (
                "#ʟᴇᴀᴠᴇᴠɪᴅᴇᴏᴄʜᴀᴛ"
            )

            action_text = (
                f"Left [{role}]"
            )

        # --------------------------------------------------
        # LOG TEXT
        # --------------------------------------------------

        log_text = (
            "<blockquote>"
            f"<b>{tag}</b>\n"
            f"<b>ɢʀᴏᴜᴘ ➛</b> "
            f"{group_name}\n"
            f"<b>ɴᴀᴍᴇ ➛</b> "
            f"{name}\n"
            f"<b>ɪᴅ ➛</b> "
            f"{user_id}\n"
            f"<b>ᴜsᴇʀɴᴀᴍᴇ ➛</b> "
            f"{username}\n"
            f"<b>ᴀᴄᴛɪᴏɴ ➛</b> "
            f"{action_text}\n"
            f"<b>ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛs ➛</b> "
            f"{participants_count}"
            "</blockquote>"
        )

        # --------------------------------------------------
        # GROUP LINK
        # --------------------------------------------------

        group_link = None

        if chat:

            group_link = await get_group_link(
                chat
            )

        # --------------------------------------------------
        # JOIN VC BUTTON
        # --------------------------------------------------

        keyboard = None

        if group_link:

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ᴊᴏɪɴᴇᴅ_ᴠᴄ",
                            url=group_link
                        )
                    ]
                ]
            )

        # --------------------------------------------------
        # SEND LOG
        # --------------------------------------------------

        sent_log = await app.send_message(
            log_chat_id,
            log_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

        # --------------------------------------------------
        # DELETE AFTER 5 SECONDS
        # --------------------------------------------------

        asyncio.create_task(
            delete_after_delay(
                sent_log,
                VC_LOG_DELETE_AFTER
            )
        )

        LOGGER.info(
            f"{tag} sent: "
            f"user={user_id}, "
            f"chat={chat_id}, "
            f"participants={participants_count}"
        )

    except Exception as e:

        LOGGER.error(
            f"Error sending VC log "
            f"for user {user_id}: {e}"
        )


# ==========================================================
# DELETE MESSAGE
# ==========================================================

async def delete_after_delay(
    message,
    delay=5
):

    try:

        await asyncio.sleep(
            delay
        )

        await message.delete()

    except Exception as e:

        LOGGER.warning(
            f"Could not delete VC log: {e}"
        )


# ==========================================================
# MONITOR VC
# ==========================================================

async def monitor_vc_chat(
    chat_id: int
):

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

            # --------------------------------------------------
            # CURRENT PARTICIPANTS
            # --------------------------------------------------

            for participant in participants_list:

                if not hasattr(
                    participant,
                    "peer"
                ):

                    continue

                if not hasattr(
                    participant.peer,
                    "user_id"
                ):

                    continue

                new_users.add(
                    participant.peer.user_id
                )

            # --------------------------------------------------
            # PREVIOUS PARTICIPANTS
            # --------------------------------------------------

            current_users = (
                vc_active_users.get(
                    chat_id,
                    set()
                )
            )

            # --------------------------------------------------
            # JOINED
            # --------------------------------------------------

            joined = (
                new_users
                - current_users
            )

            # --------------------------------------------------
            # LEFT
            # --------------------------------------------------

            left = (
                current_users
                - new_users
            )

            # --------------------------------------------------
            # JOIN HANDLER
            # --------------------------------------------------

            if joined:

                join_tasks = []

                for user_id in joined:

                    join_tasks.append(
                        handle_user_join(
                            chat_id,
                            user_id,
                            userbot,
                            len(new_users)
                        )
                    )

                if join_tasks:

                    await asyncio.gather(
                        *join_tasks,
                        return_exceptions=True
                    )

            # --------------------------------------------------
            # LEAVE HANDLER
            # --------------------------------------------------

            if left:

                leave_tasks = []

                for user_id in left:

                    leave_tasks.append(
                        handle_user_leave(
                            chat_id,
                            user_id,
                            userbot,
                            len(new_users)
                        )
                    )

                if leave_tasks:

                    await asyncio.gather(
                        *leave_tasks,
                        return_exceptions=True
                    )

            # --------------------------------------------------
            # UPDATE STATE
            # --------------------------------------------------

            vc_active_users[
                chat_id
            ] = new_users

        except asyncio.CancelledError:

            raise

        except Exception as e:

            LOGGER.error(
                f"Error monitoring VC "
                f"for {chat_id}: {e}"
            )

        await asyncio.sleep(
            VC_CHECK_INTERVAL
        )


# ==========================================================
# CHECK / START MONITOR
# ==========================================================

async def check_and_monitor_vc(
    chat_id: int
):

    try:

        # --------------------------------------------------
        # CHECK STATUS
        # --------------------------------------------------

        if not await get_vc_logger_status(
            chat_id
        ):

            return

        # --------------------------------------------------
        # ALREADY ACTIVE
        # --------------------------------------------------

        if chat_id in active_vc_chats:

            return

        # --------------------------------------------------
        # GET ASSISTANT
        # --------------------------------------------------

        userbot = await get_assistant(
            chat_id
        )

        if not userbot:

            LOGGER.warning(
                f"No assistant available "
                f"for {chat_id}"
            )

            return

        # --------------------------------------------------
        # MARK ACTIVE
        # --------------------------------------------------

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

                if not hasattr(
                    participant,
                    "peer"
                ):

                    continue

                if not hasattr(
                    participant.peer,
                    "user_id"
                ):

                    continue

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

        # --------------------------------------------------
        # START MONITOR TASK
        # --------------------------------------------------

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
            f"Error in check_and_monitor_vc: "
            f"{e}"
        )


# ==========================================================
# HANDLE JOIN
# ==========================================================

async def handle_user_join(
    chat_id: int,
    user_id: int,
    userbot,
    participants_count: int = 0
):

    try:

        # कोई पुराना join message नहीं.
        # केवल detailed VC log.

        await send_vc_log(
            chat_id=chat_id,
            user_id=user_id,
            action="Joined",
            participants_count=participants_count,
            userbot=userbot
        )

    except Exception as e:

        LOGGER.error(
            f"Error sending join log "
            f"for {user_id}: {e}"
        )


# ==========================================================
# HANDLE LEAVE
# ==========================================================

async def handle_user_leave(
    chat_id: int,
    user_id: int,
    userbot,
    participants_count: int = 0
):

    try:

        # कोई पुराना leave message नहीं.
        # केवल detailed VC log.

        await send_vc_log(
            chat_id=chat_id,
            user_id=user_id,
            action="Left",
            participants_count=participants_count,
            userbot=userbot
        )

    except Exception as e:

        LOGGER.error(
            f"Error sending leave log "
            f"for {user_id}: {e}"
        )


# ==========================================================
# INITIALIZE VC LOGGER
# ==========================================================

async def initialize_vc_logger():

    await load_vc_logger_status()
