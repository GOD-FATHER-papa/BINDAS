import asyncio
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.raw import functions
from pyrogram.types import Message

from SONALI_MUSIC import app
from SONALI_MUSIC.utils.database import get_assistant
from SONALI_MUSIC.core.mongo import mongodb


LOGGER = getLogger(__name__)

# ==========================================================
# SETTINGS
# ==========================================================

VC_LOGGER_CHAT_ID = None

# Log 10 seconds baad delete hoga
VC_LOG_DELETE_AFTER = 10

# Duplicate event protection
VC_LOG_COOLDOWN = 5

# Participant check
VC_CHECK_INTERVAL = 3


# ==========================================================
# DATABASE
# ==========================================================

vcloggerdb = mongodb.vclogger


# ==========================================================
# MEMORY
# ==========================================================

vc_logging_status: Dict[int, bool] = {}

vc_active_users: Dict[int, Set[int]] = {}

vc_monitor_tasks: Dict[int, asyncio.Task] = {}

vc_log_cooldown = {}


# ==========================================================
# SMALL FONT
# ==========================================================

def sc(text):

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
    }

    return "".join(
        mapping.get(
            x.lower(),
            x
        )
        for x in str(text)
    )


# ==========================================================
# COMMAND FILTER
# ==========================================================

def vclogger_filter():

    return (
        filters.command(
            "vclogger",
            prefixes=[
                ".",
                "!",
                "/",
                "@",
                "?",
                "'",
            ]
        )
        & filters.group
    )


# ==========================================================
# DATABASE STATUS
# ==========================================================

async def get_vc_logger_status(chat_id):

    if chat_id in vc_logging_status:

        return vc_logging_status[
            chat_id
        ]

    try:

        data = await vcloggerdb.find_one(
            {
                "chat_id": chat_id
            }
        )

        if data:

            status = bool(
                data.get(
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
            f"VC status read error: {e}"
        )

    return False


async def save_vc_logger_status(
    chat_id,
    status
):

    try:

        await vcloggerdb.update_one(
            {
                "chat_id": chat_id
            },
            {
                "$set": {
                    "chat_id": chat_id,
                    "status": bool(status)
                }
            },
            upsert=True
        )

    except Exception as e:

        LOGGER.error(
            f"VC status save error: {e}"
        )


# ==========================================================
# COMMAND
# ==========================================================

@app.on_message(
    vclogger_filter()
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

        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        if len(args) == 1:

            status = await get_vc_logger_status(
                chat_id
            )

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
                "➜ <b>/vclogger on</b>\n"
                "➜ <b>/vclogger off</b>"
                "</blockquote>"
            )

            return

        arg = args[1].lower()

        # --------------------------------------------------
        # ON
        # --------------------------------------------------

        if arg in (
            "on",
            "enable",
            "yes"
        ):

            vc_logging_status[
                chat_id
            ] = True

            await save_vc_logger_status(
                chat_id,
                True
            )

            old_task = vc_monitor_tasks.get(
                chat_id
            )

            if (
                old_task is None
                or old_task.done()
            ):

                vc_monitor_tasks[
                    chat_id
                ] = asyncio.create_task(
                    vc_monitor_supervisor(
                        chat_id
                    )
                )

            await message.reply(
                "<blockquote>"
                "❖ <b>ᴠᴄ ʟᴏɢɢᴇʀ</b>\n\n"
                "╭───────────────\n"
                "├ <b>sᴛᴀᴛᴜs</b> ➛ ᴇɴᴀʙʟᴇᴅ\n"
                "╰───────────────\n\n"
                "✦ ᴠᴄ ᴊᴏɪɴ/ʟᴇᴀᴠᴇ "
                "ʟᴏɢɢɪɴɢ ᴀᴄᴛɪᴠᴇ."
                "</blockquote>"
            )

            return

        # --------------------------------------------------
        # OFF
        # --------------------------------------------------

        if arg in (
            "off",
            "disable",
            "no"
        ):

            vc_logging_status[
                chat_id
            ] = False

            await save_vc_logger_status(
                chat_id,
                False
            )

            task = vc_monitor_tasks.pop(
                chat_id,
                None
            )

            if task and not task.done():

                task.cancel()

            vc_active_users.pop(
                chat_id,
                None
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

        await message.reply(
            "<blockquote>"
            "❌ <b>ɪɴᴠᴀʟɪᴅ</b>\n\n"
            "ᴜsᴇ <b>on</b> ᴏʀ <b>off</b>."
            "</blockquote>"
        )

    except Exception as e:

        LOGGER.exception(
            f"VC command error: {e}"
        )


# ==========================================================
# GET ACTIVE CALL
# ==========================================================

async def get_active_call(
    userbot,
    peer
):

    try:

        full = await userbot.invoke(
            functions.channels.GetFullChannel(
                channel=peer
            )
        )

        return getattr(
            full.full_chat,
            "call",
            None
        )

    except Exception as e:

        error = str(e).upper()

        if any(
            x in error
            for x in (
                "GROUPCALL_NOT_FOUND",
                "CALL_NOT_FOUND",
                "NO_GROUPCALL"
            )
        ):

            return None

        LOGGER.error(
            f"Active call error: {e}"
        )

        return None


# ==========================================================
# PARTICIPANT PEER → ID
# ==========================================================

def peer_to_id(peer):

    if not peer:
        return None

    try:

        user_id = getattr(
            peer,
            "user_id",
            None
        )

        if user_id:
            return int(user_id)

        channel_id = getattr(
            peer,
            "channel_id",
            None
        )

        if channel_id:

            return int(
                "-100"
                + str(channel_id)
            )

        chat_id = getattr(
            peer,
            "chat_id",
            None
        )

        if chat_id:

            return -int(chat_id)

    except Exception:

        pass

    return None


# ==========================================================
# GET PARTICIPANTS
# ==========================================================

async def get_vc_users(
    userbot,
    peer
):

    try:

        call = await get_active_call(
            userbot,
            peer
        )

        if not call:

            return set()

        try:

            result = await userbot.invoke(
                functions.phone.GetGroupCall(
                    call=call,
                    limit=100
                )
            )

            participants = getattr(
                result,
                "participants",
                []
            )

            users = set()

            for participant in participants:

                if getattr(
                    participant,
                    "left",
                    False
                ):
                    continue

                p = getattr(
                    participant,
                    "peer",
                    None
                )

                user_id = peer_to_id(
                    p
                )

                if user_id:

                    users.add(
                        user_id
                    )

            return users

        except Exception as e:

            LOGGER.warning(
                f"GetGroupCall failed: {e}"
            )

            return set()

    except Exception as e:

        error = str(e).upper()

        if "FLOOD_WAIT_" in error:

            try:

                wait = int(
                    error.split(
                        "FLOOD_WAIT_"
                    )[1].split("]")[0]
                )

            except Exception:

                wait = 10

            await asyncio.sleep(
                wait + 1
            )

            return await get_vc_users(
                userbot,
                peer
            )

        return set()


# ==========================================================
# USER INFO
# ==========================================================

async def get_user_info(
    userbot,
    user_id
):

    try:

        return await userbot.get_users(
            user_id
        )

    except Exception:

        try:

            return await app.get_users(
                user_id
            )

        except Exception:

            return None


# ==========================================================
# ROLE
# ==========================================================

async def get_role(
    chat_id,
    user_id
):

    try:

        member = await app.get_chat_member(
            chat_id,
            user_id
        )

        if member.status == ChatMemberStatus.OWNER:

            return "ᴏᴡɴᴇʀ"

        if (
            member.status
            == ChatMemberStatus.ADMINISTRATOR
        ):

            return "ᴀᴅᴍɪɴ"

        if (
            member.status
            == ChatMemberStatus.RESTRICTED
        ):

            return "ʀᴇsᴛʀɪᴄᴛᴇᴅ"

    except Exception:

        pass

    return "ᴍᴇᴍʙᴇʀ"


# ==========================================================
# SEND LOG
# ==========================================================

async def send_vc_log(
    chat_id,
    user_id,
    action,
    count,
    userbot
):

    key = (
        chat_id,
        user_id,
        action
    )

    now = (
        asyncio.get_running_loop()
        .time()
    )

    if (
        now
        - vc_log_cooldown.get(
            key,
            0
        )
        < VC_LOG_COOLDOWN
    ):

        return

    vc_log_cooldown[
        key
    ] = now

    try:

        # --------------------------------------------------
        # GROUP
        # --------------------------------------------------

        try:

            chat = await app.get_chat(
                chat_id
            )

            group = (
                chat.title
                or "ᴜɴᴋɴᴏᴡɴ"
            )

        except Exception:

            group = "ᴜɴᴋɴᴏᴡɴ"

        # --------------------------------------------------
        # USER
        # --------------------------------------------------

        user = await get_user_info(
            userbot,
            user_id
        )

        if user:

            name = (
                f"{user.first_name or ''} "
                f"{user.last_name or ''}"
            ).strip()

            name = name or "ㅤ-"

            username = (
                f"@{user.username}"
                if user.username
                else "ㅤ-"
            )

        else:

            name = "ㅤ-"
            username = "ㅤ-"

        # --------------------------------------------------
        # ROLE
        # --------------------------------------------------

        role = await get_role(
            chat_id,
            user_id
        )

        # --------------------------------------------------
        # ACTION
        # --------------------------------------------------

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

        # --------------------------------------------------
        # MESSAGE
        # --------------------------------------------------

        text = (
            "<blockquote>"
            f"<b>{tag}</b>\n"
            "╭───────────────\n"
            f"├ <b>ɢʀᴏᴜᴘ</b> ➛ {group}\n"
            f"├ <b>ɴᴀᴍᴇ</b> ➛ {name}\n"
            f"├ <b>ɪᴅ</b> ➛ "
            f"<code>{user_id}</code>\n"
            f"├ <b>ᴜsᴇʀɴᴀᴍᴇ</b> ➛ "
            f"{username}\n"
            f"├ <b>ᴀᴄᴛɪᴏɴ</b> ➛ "
            f"{action_text}\n"
            f"├ <b>ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛs</b> ➛ "
            f"{count}\n"
            "╰───────────────"
            "</blockquote>"
        )

        destination = (
            VC_LOGGER_CHAT_ID
            if VC_LOGGER_CHAT_ID
            else chat_id
        )

        # --------------------------------------------------
        # NO BUTTON
        # --------------------------------------------------

        sent = await app.send_message(
            destination,
            text,
            disable_web_page_preview=True
        )

        # --------------------------------------------------
        # DELETE AFTER 10 SEC
        # --------------------------------------------------

        await asyncio.sleep(
            VC_LOG_DELETE_AFTER
        )

        try:

            await sent.delete()

        except Exception:

            pass

    except Exception as e:

        LOGGER.exception(
            f"Send VC log failed: {e}"
        )


# ==========================================================
# ACTUAL MONITOR
# ==========================================================

async def monitor_vc(
    chat_id
):

    userbot = await get_assistant(
        chat_id
    )

    if not userbot:

        LOGGER.warning(
            f"Assistant unavailable: "
            f"{chat_id}"
        )

        return

    peer = await userbot.resolve_peer(
        chat_id
    )

    old_users = await get_vc_users(
        userbot,
        peer
    )

    vc_active_users[
        chat_id
    ] = set(old_users)

    LOGGER.info(
        f"VC monitor active: "
        f"{chat_id}"
    )

    while await get_vc_logger_status(
        chat_id
    ):

        current = await get_vc_users(
            userbot,
            peer
        )

        # --------------------------------------------------
        # JOIN
        # --------------------------------------------------

        for user_id in (
            current - old_users
        ):

            await send_vc_log(
                chat_id,
                user_id,
                "Joined",
                len(current),
                userbot
            )

        # --------------------------------------------------
        # LEAVE
        # --------------------------------------------------

        for user_id in (
            old_users - current
        ):

            await send_vc_log(
                chat_id,
                user_id,
                "Left",
                len(current),
                userbot
            )

        old_users = set(
            current
        )

        vc_active_users[
            chat_id
        ] = set(current)

        await asyncio.sleep(
            VC_CHECK_INTERVAL
        )


# ==========================================================
# SUPERVISOR
# ==========================================================

async def vc_monitor_supervisor(
    chat_id
):

    try:

        while await get_vc_logger_status(
            chat_id
        ):

            try:

                await monitor_vc(
                    chat_id
                )

            except asyncio.CancelledError:

                raise

            except Exception as e:

                LOGGER.error(
                    f"VC monitor stopped "
                    f"temporarily for "
                    f"{chat_id}: {e}"
                )

            # Reconnect/restart monitor
            # instead of permanently dying.
            if await get_vc_logger_status(
                chat_id
            ):

                await asyncio.sleep(3)

    except asyncio.CancelledError:

        LOGGER.info(
            f"VC supervisor cancelled: "
            f"{chat_id}"
        )

    finally:

        vc_active_users.pop(
            chat_id,
            None
        )

        vc_monitor_tasks.pop(
            chat_id,
            None
        )


# ==========================================================
# LOAD ENABLED GROUPS
# ==========================================================

async def load_vc_logger_status():

    try:

        cursor = vcloggerdb.find({})

        async for doc in cursor:

            chat_id = doc.get(
                "chat_id"
            )

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

                task = vc_monitor_tasks.get(
                    chat_id
                )

                if (
                    task is None
                    or task.done()
                ):

                    vc_monitor_tasks[
                        chat_id
                    ] = asyncio.create_task(
                        vc_monitor_supervisor(
                            chat_id
                        )
                    )

        LOGGER.info(
            "VC logger status loaded."
        )

    except Exception as e:

        LOGGER.exception(
            f"VC logger load error: {e}"
        )


# ==========================================================
# END
# ==========================================================
