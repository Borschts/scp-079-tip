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
import pickle
from codecs import getdecoder
from configparser import RawConfigParser
from os import mkdir
from os.path import exists
from shutil import rmtree
from string import ascii_lowercase
from threading import Lock
from typing import Dict, List, Set, Tuple, Union

from emoji import UNICODE_EMOJI
from pyrogram import Chat, ChatMember

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="log",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [bots]
avatar_id: int = 0
captcha_id: int = 0
clean_id: int = 0
lang_id: int = 0
long_id: int = 0
noflood_id: int = 0
noporn_id: int = 0
nospam_id: int = 0
recheck_id: int = 0
tip_id: int = 0
user_id: int = 0
warn_id: int = 0

# [channels]
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

# [custom]
aio: Union[bool, str] = ""
backup: Union[bool, str] = ""
date_reset: str = ""
default_group_link: str = ""
project_link: str = ""
project_name: str = ""
time_channel: int = 0
time_keyword: int = 0
time_ot: int = 0
time_rm: int = 0
time_welcome: int = 0
zh_cn: Union[bool, str] = ""

# [emoji]
emoji_ad_single: int = 0
emoji_ad_total: int = 0
emoji_many: int = 0
emoji_protect: str = ""
emoji_wb_single: int = 0
emoji_wb_total: int = 0

# [encrypt]
key: Union[str, bytes] = ""
password: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")

    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))

    # [bots]
    avatar_id = int(config["bots"].get("avatar_id", avatar_id))
    captcha_id = int(config["bots"].get("captcha_id", captcha_id))
    clean_id = int(config["bots"].get("clean_id", clean_id))
    lang_id = int(config["bots"].get("lang_id", lang_id))
    long_id = int(config["bots"].get("long_id", long_id))
    noflood_id = int(config["bots"].get("noflood_id", noflood_id))
    noporn_id = int(config["bots"].get("noporn_id", noporn_id))
    nospam_id = int(config["bots"].get("nospam_id", nospam_id))
    recheck_id = int(config["bots"].get("recheck_id", recheck_id))
    tip_id = int(config["bots"].get("tip_id", tip_id))
    user_id = int(config["bots"].get("user_id", user_id))
    warn_id = int(config["bots"].get("warn_id", warn_id))

    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))

    # [custom]
    aio = config["custom"].get("aio", aio)
    aio = eval(aio)
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    date_reset = config["custom"].get("date_reset", date_reset)
    default_group_link = config["custom"].get("default_group_link", default_group_link)
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    time_channel = int(config["custom"].get("time_channel", time_channel))
    time_keyword = int(config["custom"].get("time_keyword", time_keyword))
    time_ot = int(config["custom"].get("time_ot", time_ot))
    time_rm = int(config["custom"].get("time_rm", time_rm))
    time_welcome = int(config["custom"].get("time_welcome", time_welcome))
    zh_cn = config["custom"].get("zh_cn", zh_cn)
    zh_cn = eval(zh_cn)

    # [emoji]
    emoji_ad_single = int(config["emoji"].get("emoji_ad_single", emoji_ad_single))
    emoji_ad_total = int(config["emoji"].get("emoji_ad_total", emoji_ad_total))
    emoji_many = int(config["emoji"].get("emoji_many", emoji_many))
    emoji_protect = getdecoder("unicode_escape")(config["emoji"].get("emoji_protect", emoji_protect))[0]
    emoji_wb_single = int(config["emoji"].get("emoji_wb_single", emoji_wb_single))
    emoji_wb_total = int(config["emoji"].get("emoji_wb_total", emoji_wb_total))

    # [encrypt]
    key = config["encrypt"].get("key", key)
    key = key.encode("utf-8")
    password = config["encrypt"].get("password", password)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or avatar_id == 0
        or captcha_id == 0
        or clean_id == 0
        or lang_id == 0
        or long_id == 0
        or noflood_id == 0
        or noporn_id == 0
        or nospam_id == 0
        or recheck_id == 0
        or tip_id == 0
        or user_id == 0
        or warn_id == 0
        or critical_channel_id == 0
        or debug_channel_id == 0
        or exchange_channel_id == 0
        or hide_channel_id == 0
        or test_group_id == 0
        or aio not in {False, True}
        or backup not in {False, True}
        or date_reset in {"", "[DATA EXPUNGED]"}
        or default_group_link in {"", "[DATA EXPUNGED]"}
        or project_link in {"", "[DATA EXPUNGED]"}
        or project_name in {"", "[DATA EXPUNGED]"}
        or time_channel == 0
        or time_keyword == 0
        or time_ot == 0
        or time_rm == 0
        or time_welcome == 0
        or zh_cn not in {False, True}
        or emoji_ad_single == 0
        or emoji_ad_total == 0
        or emoji_many == 0
        or emoji_protect in {"", "[DATA EXPUNGED]"}
        or emoji_wb_single == 0
        or emoji_wb_total == 0
        or key in {b"", b"[DATA EXPUNGED]", "", "[DATA EXPUNGED]"}
        or password in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Languages
lang: Dict[str, str] = {
    # Admin
    "admin": (zh_cn and "管理员") or "Admin",
    "admin_group": (zh_cn and "群管理") or "Group Admin",
    "admin_project": (zh_cn and "项目管理员") or "Project Admin",
    # Basic
    "action": (zh_cn and "执行操作") or "Action",
    "clear": (zh_cn and "清空数据") or "Clear Data",
    "colon": (zh_cn and "：") or ": ",
    "description": (zh_cn and "说明") or "Description",
    "disabled": (zh_cn and "禁用") or "Disabled",
    "enabled": (zh_cn and "启用") or "Enabled",
    "name": (zh_cn and "名称") or "Name",
    "reason": (zh_cn and "原因") or "Reason",
    "reset": (zh_cn and "重置数据") or "Reset Data",
    "result": (zh_cn and "结果") or "Result",
    "rollback": (zh_cn and "数据回滚") or "Rollback",
    "score": (zh_cn and "评分") or "Score",
    "status_failed": (zh_cn and "未执行") or "Failed",
    "status_succeeded": (zh_cn and "成功执行") or "Succeeded",
    "version": (zh_cn and "版本") or "Version",
    # Command
    "command_lack": (zh_cn and "命令参数缺失") or "Lack of Parameter",
    "command_para": (zh_cn and "命令参数有误") or "Incorrect Command Parameter",
    "command_type": (zh_cn and "命令类别有误") or "Incorrect Command Type",
    "command_usage": (zh_cn and "用法有误") or "Incorrect Usage",
    # Config
    "config": (zh_cn and "设置") or "Settings",
    "config_button": (zh_cn and "请点击下方按钮进行设置") or "Press the Button to Config",
    "config_change": (zh_cn and "更改设置") or "Change Config",
    "config_create": (zh_cn and "创建设置会话") or "Create Config Session",
    "config_go": (zh_cn and "前往设置") or "Go to Config",
    "config_locked": (zh_cn and "设置当前被锁定") or "Config is Locked",
    "config_show": (zh_cn and "查看设置") or "Show Config",
    "config_updated": (zh_cn and "已更新") or "Updated",
    "custom": (zh_cn and "自定义") or "Custom",
    "default": (zh_cn and "默认") or "Default",
    "captcha": (zh_cn and "过审欢迎") or "Welcome After CAPTCHA",
    "alone": (zh_cn and "非回复欢迎") or "Alone Mode",
    "clean": (zh_cn and "无痕模式") or "Clean Mode",
    "resend": (zh_cn and "每日重发入群链接") or "Resend Invite Link Everyday",
    "channel": (zh_cn and "入群频道") or "Entry Channel",
    "hold": (zh_cn and "保持置顶") or "Hold the Pinned Message",
    "keyword": (zh_cn and "关键词提示") or "Custom Keywords",
    "ot": (zh_cn and "OT 警告") or "OT Warning by Members",
    "rm": (zh_cn and "RM 警告") or "RM Jokes Warning",
    "welcome": (zh_cn and "欢迎信息") or "Welcome Message",
    # Debug
    "triggered_by": (zh_cn and "触发消息") or "Triggered By",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Group
    "group_id": (zh_cn and "群组 ID") or "Group ID",
    "group_name": (zh_cn and "群组名称") or "Group Name",
    "inviter": (zh_cn and "邀请人") or "Inviter",
    "leave_auto": (zh_cn and "自动退出并清空数据") or "Leave automatically",
    "leave_approve": (zh_cn and "已批准退出群组") or "Approve to Leave the Group",
    "reason_admin": (zh_cn and "获取管理员列表失败") or "Failed to Fetch Admin List",
    "reason_leave": (zh_cn and "非管理员或已不在群组中") or "Not Admin in Group",
    "reason_none": (zh_cn and "无数据") or "No Data",
    "reason_permissions": (zh_cn and "权限缺失") or "Missing Permissions",
    "reason_unauthorized": (zh_cn and "未授权使用") or "Unauthorized",
    "reason_user": (zh_cn and "缺失 USER") or "Missing USER",
    "refresh": (zh_cn and "刷新群管列表") or "Refresh Admin Lists",
    "status_joined": (zh_cn and "已加入群组") or "Joined the Group",
    "status_left": (zh_cn and "已退出群组") or "Left the Group",
    # More
    "privacy": (zh_cn and "可能涉及隐私而未转发") or "Not Forwarded Due to Privacy Reason",
    "cannot_forward": (zh_cn and "此类消息无法转发至频道") or "The Message Cannot be Forwarded to Channel",
    # Message Types
    "gam": (zh_cn and "游戏") or "Game",
    "ser": (zh_cn and "服务消息") or "Service",
    # Record
    "project": (zh_cn and "项目编号") or "Project",
    "project_origin": (zh_cn and "原始项目") or "Original Project",
    "status": (zh_cn and "状态") or "Status",
    "user_id": (zh_cn and "用户 ID") or "User ID",
    "level": (zh_cn and "操作等级") or "Level",
    "rule": (zh_cn and "规则") or "Rule",
    "message_type": (zh_cn and "消息类别") or "Message Type",
    "message_game": (zh_cn and "游戏标识") or "Game Short Name",
    "message_lang": (zh_cn and "消息语言") or "Message Language",
    "message_len": (zh_cn and "消息长度") or "Message Length",
    "message_freq": (zh_cn and "消息频率") or "Message Frequency",
    "user_score": (zh_cn and "用户得分") or "User Score",
    "user_bio": (zh_cn and "用户简介") or "User Bio",
    "user_name": (zh_cn and "用户昵称") or "User Name",
    "from_name": (zh_cn and "来源名称") or "Forward Name",
    "contact": (zh_cn and "联系方式") or "Contact Info",
    "more": (zh_cn and "附加信息") or "Extra Info",
    # Special
    "action_bind": (zh_cn and "绑定频道") or "Bind Channel",
    "action_channel": (zh_cn and "调整邀请提示") or "Adjust Invite Text",
    "action_close": (zh_cn and "关闭入群通道") or "Close Group Channel",
    "action_hold": (zh_cn and "设置保持置顶") or "Hold the Pinned Message",
    "action_keyword": (zh_cn and "调整关键词") or "Adjust Keywords",
    "action_open": (zh_cn and "开启入群通道") or "Open Group Channel",
    "action_ot": (zh_cn and "调整 OT 提示") or "Adjust OT Tip",
    "action_rm": (zh_cn and "调整 RM 警告") or "Adjust RM Tip",
    "action_resend": (zh_cn and "重新发送入群链接") or "Resend Group Link Message",
    "action_show": (zh_cn and "查看设置内容") or "Show the Config Text",
    "action_welcome": (zh_cn and "调整欢迎消息") or "Adjust Welcome Tip",
    "button_channel": (zh_cn and "点击加入") or "Click to Join",
    "description_channel": ((zh_cn and "请点击下方按钮加入讨论群组")
                            or "Please click the button below to join the chat group"),
    "description_close": ((zh_cn and "根据群组的设置，暂时不会提供群组链接，请稍后再试")
                          or ("According to the group's settings, the group link will not be provided at this time. "
                              "Please try again later")),
    "description_ot": (zh_cn and "离题内容请适度") or "OT Warning",
    "description_rm": (zh_cn and "请勿开 rm 命令类玩笑") or "Please do not joke about the rm command",
    "description_welcome": (zh_cn and "你好，$mention_name") or "Hello $mention_name",
    "pinned_message": (zh_cn and "置顶消息") or "Pinned Message",
    "type": (zh_cn and "类别") or "Type",
    # Terminate
    "auto_ban": (zh_cn and "自动封禁") or "Auto Ban",
    "auto_delete": (zh_cn and "自动删除") or "Auto Delete",
    "global_delete": (zh_cn and "全局删除") or "Global Delete",
    "name_ban": (zh_cn and "名称封禁") or "Ban by Name",
    "name_examine": (zh_cn and "名称检查") or "Name Examination",
    "name_recheck": (zh_cn and "名称复查") or "Name Recheck",
    "op_downgrade": (zh_cn and "操作降级") or "Operation Downgrade",
    "op_upgrade": (zh_cn and "操作升级") or "Operation Upgrade",
    "rule_custom": (zh_cn and "群组自定义") or "Custom Rule",
    "rule_global": (zh_cn and "全局规则") or "Global Rule",
    "score_ban": (zh_cn and "评分封禁") or "Ban by Score",
    "score_user": (zh_cn and "用户评分") or "High Score",
    "watch_ban": (zh_cn and "追踪封禁") or "Watch Ban",
    "watch_delete": (zh_cn and "追踪删除") or "Watch Delete",
    "watch_user": (zh_cn and "敏感追踪") or "Watched User"
}

# Init

all_commands: List[str] = [
    "channel",
    "config",
    "config_tip",
    "hold",
    "keyword",
    "ot",
    "resend",
    "rm",
    "show",
    "welcome",
    "version"
]

bot_ids: Set[int] = {avatar_id, captcha_id, clean_id, lang_id, long_id, noflood_id,
                     noporn_id, nospam_id, recheck_id, tip_id, user_id, warn_id}

chats: Dict[int, Chat] = {}
# chats = {
#     -10012345678: Chat
# }

declared_message_ids: Dict[int, Set[int]] = {}
# declared_message_ids = {
#     -10012345678: {123}
# }

default_config: Dict[str, Union[bool, int, str]] = {
    "default": True,
    "lock": 0,
    "captcha": True,
    "alone": False,
    "clean": True,
    "resend": False,
    "channel": 0,
    "channel_text": lang["description_channel"],
    "channel_button": lang["button_channel"],
    "channel_link": "",
    "hold": 0,
    "keyword": True,
    "keyword_text": "",
    "keyword_button": "",
    "keyword_link": "",
    "ot": False,
    "ot_text": lang["description_ot"],
    "ot_button": "",
    "ot_link": "",
    "rm": False,
    "rm_text": lang["description_rm"],
    "rm_button": "",
    "rm_link": "",
    "welcome": False,
    "welcome_text": lang["description_welcome"],
    "welcome_button": "",
    "welcome_link": "",
}

default_message_data: Dict[str, Tuple[int, int]] = {
    "channel": (0, 0),
    "hold": (0, 0),
    "keyword": (0, 0),
    "ot": (0, 0),
    "rm": (0, 0),
    "welcome": (0, 0)
}

default_user_status: Dict[str, Dict[str, float]] = {
    "score": {
        "captcha": 0.0,
        "clean": 0.0,
        "lang": 0.0,
        "long": 0.0,
        "noflood": 0.0,
        "noporn": 0.0,
        "nospam": 0.0,
        "recheck": 0.0,
        "warn": 0.0
    }
}

emoji_set: Set[str] = set(UNICODE_EMOJI)

locks: Dict[str, Lock] = {
    "admin": Lock(),
    "channel": Lock(),
    "message": Lock(),
    "receive": Lock(),
    "regex": Lock()
}

members: Dict[int, Dict[int, ChatMember]] = {}
# members = {
#     -10012345678: {
#         12345678: ChatMember
#     }
# }

regex: Dict[str, bool] = {
    "ad": False,
    "ban": False,
    "bio": False,
    "con": False,
    "del": False,
    "fil": False,
    "iml": False,
    "pho": False,
    "nm": False,
    "rm": True,
    "sho": False,
    "spc": False,
    "spe": False,
    "tgl": False,
    "wb": False
}

for c in ascii_lowercase:
    regex[f"ad{c}"] = False

sender: str = "TIP"

should_hide: bool = False

version: str = "0.1.8"

welcomed_ids: Dict[int, Set[int]] = {}
# welcomed_ids = {
#     -10012345678: {12345678}
# }

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)

# Init ids variables

admin_ids: Dict[int, Set[int]] = {}
# admin_ids = {
#     -10012345678: {12345678}
# }

bad_ids: Dict[str, Set[int]] = {
    "channels": set(),
    "users": set()
}
# bad_ids = {
#     "channels": {-10012345678},
#     "users": {12345678}
# }

flooded_ids: Set[int] = set()
# flooded_ids = {-10012345678}

lack_group_ids: Set[int] = set()
# lack_group_ids = {-10012345678}

left_group_ids: Set[int] = set()
# left_group_ids = {-10012345678}

message_ids: Dict[int, Dict[str, Tuple[int, int]]] = {}
# message_ids = {
#     -10012345678: {
#         "channel": (123, 1512345678),
#         "hold": (123, 1512345678),
#         "keyword": (124, 1512345678),
#         "ot": (125, 1512345678),
#         "rm": (126, 1512345678),
#         "welcome": (127, 1512345678)
#     }
# }

trust_ids: Dict[int, Set[int]] = {}
# trust_ids = {
#     -10012345678: {12345678}
# }

user_ids: Dict[int, Dict[str, Dict[str, float]]] = {}
# user_ids = {
#     12345678: {
#         "score": {
#             "captcha": 0.0,
#             "clean": 0.0,
#             "lang": 0.0,
#             "long": 0.0,
#             "noflood": 0.0,
#             "noporn": 0.0,
#             "nospam": 0.0,
#             "recheck": 0.0,
#             "warn": 0.0
#         }
#     }
# }

watch_ids: Dict[str, Dict[int, int]] = {
    "ban": {},
    "delete": {}
}
# watch_ids = {
#     "ban": {
#         12345678: 0
#     },
#     "delete": {
#         12345678: 0
#     }
# }

# Init data variables

configs: Dict[int, Dict[str, Union[bool, int, str]]] = {}
# configs = {
#     -10012345678: {
#         "default": True,
#         "lock": 0,
#         "captcha": True,
#         "alone": False,
#         "clean": True,
#         "resend": False,
#         "channel": 0,
#         "channel_text": "text",
#         "channel_button": "text",
#         "channel_link": "",
#         "hold": 0,
#         "keyword": True,
#         "keyword_text": "string",
#         "keyword_button": "",
#         "keyword_link": "",
#         "ot": False,
#         "ot_text": "string",
#         "ot_button": "",
#         "ot_link": "",
#         "rm": False,
#         "rm_text": "string",
#         "rm_button": "",
#         "rm_link": "",
#         "welcome": False,
#         "welcome_text": "string",
#         "welcome_button": "",
#         "welcome_link": ""
#     }
# }

# Init word variables

for word_type in regex:
    locals()[f"{word_type}_words"]: Dict[str, Dict[str, Union[float, int]]] = {}

# type_words = {
#     "regex": 0
# }

# Load data
file_list: List[str] = ["admin_ids", "bad_ids", "flooded_ids", "lack_group_ids", "left_group_ids", "message_ids",
                        "trust_ids", "user_ids", "watch_ids",
                        "configs"]
file_list += [f"{f}_words" for f in regex]

for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"data/.{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Generate special characters dictionary
for special in ["spc", "spe"]:
    locals()[f"{special}_dict"]: Dict[str, str] = {}

    for rule in locals()[f"{special}_words"]:
        # Check keys
        if "[" not in rule:
            continue

        # Check value
        if "?#" not in rule:
            continue

        keys = rule.split("]")[0][1:]
        value = rule.split("?#")[1][1]

        for k in keys:
            locals()[f"{special}_dict"][k] = value

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
