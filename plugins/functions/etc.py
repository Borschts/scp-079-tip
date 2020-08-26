# SCP-079-TIP - Here's a tip
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-TIP.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from datetime import datetime
from copy import deepcopy
from html import escape
from json import dumps
from random import choice, uniform
from re import sub
from string import ascii_letters, digits
from threading import Thread, Timer
from time import localtime, sleep, strftime, time
from typing import Any, Callable, Optional, Union
from unicodedata import normalize

from cryptography.fernet import Fernet
from opencc import OpenCC
from pyrogram import Message, User
from pyrogram.errors import FloodWait

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)

# Init Opencc
converter = OpenCC(config="t2s.json")


def bold(text: Any) -> str:
    # Get a bold text
    try:
        text = str(text).strip()

        if text:
            return f"<b>{escape(text)}</b>"
    except Exception as e:
        logger.warning(f"Bold error: {e}", exc_info=True)

    return ""


def button_data(action: str, action_type: str = None, data: Union[int, str] = None) -> Optional[bytes]:
    # Get a button's bytes data
    result = None
    try:
        button = {
            "a": action,
            "t": action_type,
            "d": data
        }
        result = dumps(button).replace(" ", "").encode("utf-8")
    except Exception as e:
        logger.warning(f"Button data error: {e}", exc_info=True)

    return result


def code(text: Any) -> str:
    # Get a code text
    try:
        text = str(text).strip()

        if text:
            return f"<code>{escape(text)}</code>"
    except Exception as e:
        logger.warning(f"Code error: {e}", exc_info=True)

    return ""


def code_block(text: Any) -> str:
    # Get a code block text
    try:
        text = str(text).rstrip()

        if text:
            return f"<pre>{escape(text)}</pre>"
    except Exception as e:
        logger.warning(f"Code block error: {e}", exc_info=True)

    return ""


def crypt_str(operation: str, text: str, key: bytes) -> str:
    # Encrypt or decrypt a string
    result = ""

    try:
        f = Fernet(key)
        text = text.encode("utf-8")

        if operation == "decrypt":
            result = f.decrypt(text)
        else:
            result = f.encrypt(text)

        result = result.decode("utf-8")
    except Exception as e:
        logger.warning(f"Crypt str error: {e}", exc_info=True)

    return result


def delay(secs: int, target: Callable, args: list = None) -> bool:
    # Call a function with delay
    result = False

    try:
        t = Timer(secs, target, args)
        t.daemon = True
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Delay error: {e}", exc_info=True)

    return result


def general_link(text: Union[int, str], link: str) -> str:
    # Get a general link
    result = ""
    try:
        text = str(text).strip()
        link = link.strip()

        if text and link:
            result = f'<a href="{link}">{escape(text)}</a>'
    except Exception as e:
        logger.warning(f"General link error: {e}", exc_info=True)

    return result


def get_channel_link(message: Union[int, Message]) -> str:
    # Get a channel reference link
    text = ""
    try:
        text = "https://t.me/"

        if isinstance(message, int):
            text += f"c/{str(message)[4:]}"
        else:
            if message.chat.username:
                text += f"{message.chat.username}"
            else:
                cid = message.chat.id
                text += f"c/{str(cid)[4:]}"
    except Exception as e:
        logger.warning(f"Get channel link error: {e}", exc_info=True)

    return text


def get_command_context(message: Message) -> (str, str):
    # Get the type "a" and the context "b" in "/command a b"
    command_type = ""
    command_context = ""
    try:
        text = get_text(message)
        command_list = text.split()

        if len(list(filter(None, command_list))) <= 1:
            return "", ""

        i = 1
        command_type = command_list[i]

        while command_type == "" and i < len(command_list):
            i += 1
            command_type = command_list[i]

        command_context = text[1 + len(command_list[0]) + i + len(command_type):].strip()
    except Exception as e:
        logger.warning(f"Get command context error: {e}", exc_info=True)

    return command_type, command_context


def get_command_type(message: Message) -> str:
    # Get the command type "a" in "/command a"
    result = ""
    try:
        text = get_text(message)
        command_list = list(filter(None, text.split()))
        result = text[len(command_list[0]):].strip()
    except Exception as e:
        logger.warning(f"Get command type error: {e}", exc_info=True)

    return result


def get_filename(message: Message, normal: bool = False, printable: bool = False) -> str:
    # Get file's filename
    text = ""
    try:
        if message.document:
            if message.document.file_name:
                text += message.document.file_name
        elif message.audio:
            if message.audio.file_name:
                text += message.audio.file_name

        if text:
            text = t2t(text, normal, printable)
    except Exception as e:
        logger.warning(f"Get filename error: {e}", exc_info=True)

    return text


def get_forward_name(message: Message, normal: bool = False, printable: bool = False) -> str:
    # Get forwarded message's origin sender's name
    text = ""
    try:
        if message.forward_from:
            user = message.forward_from
            text = get_full_name(user, normal, printable)
        elif message.forward_sender_name:
            text = message.forward_sender_name
        elif message.forward_from_chat:
            chat = message.forward_from_chat
            text = chat.title

        if text:
            text = t2t(text, normal, printable)
    except Exception as e:
        logger.warning(f"Get forward name error: {e}", exc_info=True)

    return text


def get_full_name(user: User, normal: bool = False, printable: bool = False) -> str:
    # Get user's full name
    text = ""
    try:
        if not user or user.is_deleted:
            return ""

        text = user.first_name

        if user.last_name:
            text += f" {user.last_name}"

        if text and normal:
            text = t2t(text, normal, printable)
    except Exception as e:
        logger.warning(f"Get full name error: {e}", exc_info=True)

    return text


def get_int(text: str) -> Optional[int]:
    # Get a int from a string
    result = None
    try:
        result = int(text)
    except Exception as e:
        logger.info(f"Get int error: {e}", exc_info=True)

    return result


def get_length(text: str) -> int:
    # Get the length of the string
    result = 0
    try:
        if not text:
            return 0

        emoji_dict = {}
        emoji_set = {emoji for emoji in glovar.emoji_set if emoji in text and emoji not in glovar.emoji_protect}
        emoji_old_set = deepcopy(emoji_set)

        for emoji in emoji_old_set:
            if any(emoji in emoji_old and emoji != emoji_old for emoji_old in emoji_old_set):
                emoji_set.discard(emoji)

        for emoji in emoji_set:
            emoji_dict[emoji] = text.count(emoji)

        length_add = 0

        for emoji in emoji_dict:
            length_add += 3 * emoji_dict[emoji]

        length_remove = 0

        for emoji in emoji_dict:
            length_remove += len(emoji.encode()) * emoji_dict[emoji]

        result = len(text.encode()) + length_add - length_remove
    except Exception as e:
        logger.warning(f"Get length error: {e}", exc_info=True)

    return result


def get_now() -> int:
    # Get time for now
    result = 0
    try:
        result = int(time())
    except Exception as e:
        logger.warning(f"Get now error: {e}", exc_info=True)

    return result


def get_readable_time(secs: int = 0, the_format: str = "%Y%m%d%H%M%S") -> str:
    # Get a readable time string
    result = ""

    try:
        if secs:
            result = datetime.utcfromtimestamp(secs).strftime(the_format)
        else:
            result = strftime(the_format, localtime())
    except Exception as e:
        logger.warning(f"Get readable time error: {e}", exc_info=True)

    return result


def get_text(message: Message, normal: bool = False, printable: bool = False) -> str:
    # Get message's text
    text = ""
    try:
        if not message:
            return ""

        the_text = message.text or message.caption

        if the_text:
            text += the_text

        if text:
            text = t2t(text, normal, printable)
    except Exception as e:
        logger.warning(f"Get text error: {e}", exc_info=True)

    return text


def lang(text: str) -> str:
    # Get the text
    result = ""

    try:
        result = glovar.lang_dict.get(text, text)
    except Exception as e:
        logger.warning(f"Lang error: {e}", exc_info=True)

    return result


def mention_id(uid: int) -> str:
    # Get a ID mention string
    result = ""
    try:
        result = general_link(f"{uid}", f"tg://user?id={uid}")
    except Exception as e:
        logger.warning(f"Mention id error: {e}", exc_info=True)

    return result


def mention_name(user: User) -> str:
    # Get a name mention string
    result = ""
    try:
        name = get_full_name(user)
        uid = user.id
        result = general_link(f"{name}", f"tg://user?id={uid}")
    except Exception as e:
        logger.warning(f"Mention name error: {e}", exc_info=True)

    return result


def mention_text(text: str, uid: int) -> str:
    # Get a text mention string
    result = ""
    try:
        result = general_link(f"{text}", f"tg://user?id={uid}")
    except Exception as e:
        logger.warning(f"Mention text error: {e}", exc_info=True)

    return result


def random_str(i: int) -> str:
    # Get a random string
    text = ""
    try:
        text = "".join(choice(ascii_letters + digits) for _ in range(i))
    except Exception as e:
        logger.warning(f"Random str error: {e}", exc_info=True)

    return text


def t2t(text: str, normal: bool, printable: bool, pure: bool = False) -> str:
    # Convert the string, text to text
    result = text

    try:
        if not result:
            return ""

        if glovar.normalize and normal:
            for special in ["spc", "spe"]:
                result = "".join(eval(f"glovar.{special}_dict").get(t, t) for t in result)

            result = normalize("NFKC", result)

        if glovar.normalize and normal and "Hans" in glovar.lang:
            result = converter.convert(result)

        if printable:
            result = "".join(t for t in result if t.isprintable() or t in {"\n", "\r", "\t"})

        if pure:
            result = sub(r"""[^\da-zA-Z一-龥.,:'"?!~;()。，？！～@“”]""", "", result)
    except Exception as e:
        logger.warning(f"T2T error: {e}", exc_info=True)

    return result


def thread(target: Callable, args: tuple, kwargs: dict = None, daemon: bool = True) -> bool:
    # Call a function using thread
    result = False

    try:
        t = Thread(target=target, args=args, kwargs=kwargs, daemon=daemon)
        t.daemon = daemon
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Thread error: {e}", exc_info=True)

    return result


def wait_flood(e: FloodWait) -> bool:
    # Wait flood secs
    result = False

    try:
        result = sleep(e.x + uniform(0.5, 1.0)) or True
    except Exception as e:
        logger.warning(f"Wait flood error: {e}", exc_info=True)

    return result
