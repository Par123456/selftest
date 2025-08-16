#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Self-Bot Platinum Edition v3.5 (2025)
Enhanced security, performance, and features
Created for educational purposes only
"""

import os
import sys
import re
import json
import time
import logging
import random
import hashlib
import asyncio
import traceback
import datetime
import string
import platform
import signal
import threading
import socket
import base64
from typing import Dict, List, Set, Tuple, Union, Optional, Any, Callable
from io import BytesIO
from datetime import datetime, timedelta
from collections import Counter, defaultdict, deque

# Import third-party libraries
try:
    # Core libraries
    from telethon import TelegramClient, events, functions, types, utils
    from telethon.tl.functions.channels import GetFullChannelRequest
    from telethon.tl.types import MessageEntityTextUrl, MessageEntityUrl, PeerUser, PeerChannel, PeerChat, Channel
    import pytz
    import colorama
    from colorama import Fore, Back, Style
    import jdatetime
    from googletrans import Translator
    import qrcode
    import pyfiglet
    
    # Media handling
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
    import textwrap
    import requests
    from gtts import gTTS

    # Optional libraries
    try:
        import numpy as np
        NUMPY_AVAILABLE = True
    except ImportError:
        NUMPY_AVAILABLE = False

    try:
        import emoji
        EMOJI_AVAILABLE = True
    except ImportError:
        EMOJI_AVAILABLE = False

    try:
        import psutil
        PSUTIL_AVAILABLE = True
    except ImportError:
        PSUTIL_AVAILABLE = False

    try:
        from cryptography.fernet import Fernet
        ENCRYPTION_AVAILABLE = True
    except ImportError:
        ENCRYPTION_AVAILABLE = False

    # Initialize colorama
    colorama.init(autoreset=True)
    ALL_DEPENDENCIES_LOADED = True

except ImportError as e:
    ALL_DEPENDENCIES_LOADED = False
    MISSING_DEPENDENCY = str(e).split("'")[1]

# ====================================
# Configuration and Global Variables
# ====================================

# App information
APP_VERSION = "3.5"
APP_NAME = "Telegram Self-Bot Platinum+"
APP_YEAR = "2025"
APP_AUTHOR = "Anonymous"
APP_DESCRIPTION = "Advanced Telegram self-bot with enhanced security and features"

# Configuration files
CONFIG_FILE = "config.json"
LOG_FILE = "selfbot.log"
DATA_FILE = "selfbot_data.json"
BACKUP_FILE = "selfbot_backup.json"
STATS_FILE = "selfbot_stats.json"
SESSION_FILE_EXTENSION = ".session"

# File paths
MEDIA_DIR = "media"
VOICE_DIR = os.path.join(MEDIA_DIR, "voice")
IMAGE_DIR = os.path.join(MEDIA_DIR, "image")
GIF_DIR = os.path.join(MEDIA_DIR, "gif")
QR_DIR = os.path.join(MEDIA_DIR, "qr")

# Create necessary directories
for directory in [MEDIA_DIR, VOICE_DIR, IMAGE_DIR, GIF_DIR, QR_DIR]:
    os.makedirs(directory, exist_ok=True)

# Default configuration
default_config = {
    "api_id": 29042268,
    "api_hash": "54a7b377dd4a04a58108639febe2f443",
    "session_name": "anon",
    "log_level": "INFO",
    "timezone": "Asia/Tehran",
    "auto_backup": True,
    "backup_interval": 60,  # minutes
    "encrypted_backup": False,
    "encryption_key": "",
    "enemy_reply_chance": 100,  # percentage
    "enemy_auto_reply": True,
    "auto_read_messages": False,
    "allowed_users": [],
    "cloud_backup": False,
    "auto_translate": False,
    "default_translate_lang": "fa",
    "weather_api_key": "",
    "auto_weather": False,
    "stats_tracking": True,
    "max_spam_count": 50,
    "bot_prefix": "!",
    "user_agent": f"TelegramSelfBot/{APP_VERSION} ({platform.system()}; {platform.release()})",
    "ai_filter_level": "low",
    "proxy": {
        "enabled": False,
        "type": "socks5",
        "host": "",
        "port": 0,
        "username": "",
        "password": ""
    },
    "advanced": {
        "connection_retries": 5,
        "auto_reconnect": True,
        "connection_timeout": 30,
        "request_timeout": 60,
        "flood_sleep_threshold": 60,
        "takeout": False,
        "device_model": f"SelfBot {APP_VERSION}",
        "system_version": platform.system() + " " + platform.release(),
        "app_version": APP_VERSION
    }
}

# Global data structures
enemies: Set[str] = set()
current_font: str = 'normal'
actions: Dict[str, bool] = {
    'typing': False,
    'online': False,
    'reaction': False,
    'read': False,
    'auto_reply': False,
    'stats': False,
    'translate': False,
    'bot_mode': False,
    'silent': False,
    'invisible': False,
    'privacy': False,
    'security': False
}
spam_words: List[str] = []
saved_messages: List[str] = []
reminders: List[Tuple[str, str, int]] = []
time_enabled: bool = True
saved_pics: List[str] = []
custom_replies: Dict[str, str] = {}
blocked_words: List[str] = []
last_backup_time: Optional[datetime] = None
running: bool = True
start_time: float = 0.0  # Initialize start_time
status_rotation: List[str] = []
status_rotation_active: bool = False
periodic_messages: List[Dict[str, Any]] = []
filters: Dict[str, Any] = {}
message_stats: Dict[str, Dict[str, Any]] = {}
welcome_messages: Dict[str, str] = {}
theme: str = "default"
chat_themes: Dict[str, str] = {}
chat_nicknames: Dict[str, str] = {}
custom_commands: Dict[str, str] = {}
auto_reactions: Dict[str, List[str]] = {}
message_cache: Dict[int, Dict[str, Any]] = {}
active_tasks: Dict[str, asyncio.Task] = {}
command_queue: List[Tuple[str, List[str]]] = []
user_notes: Dict[str, str] = {}
private_emoji_mapping: Dict[str, str] = {}

# Command history for undo functionality
command_history: List[Tuple[str, Any]] = []
MAX_HISTORY: int = 50

# Security and protection settings
locked_chats: Dict[str, Set[str]] = {
    'screenshot': set(),  # Screenshot protection
    'forward': set(),     # Forward protection
    'copy': set(),        # Copy protection
    'delete': set(),      # Auto-delete messages
    'edit': set(),        # Prevent editing
    'spam': set(),        # Anti-spam protection
    'link': set(),        # Block links
    'mention': set(),     # Block mentions
    'ai_filter': set(),   # AI content filtering
    'raid': set(),        # Anti-raid protection
    'privacy': set(),     # Enhanced privacy mode
    'log': set(),         # Log all messages
    'join': set(),        # Restrict new joins
    'media': set()        # Block media
}

# Enhanced font styles
font_styles: Dict[str, Callable[[str], str]] = {
    'normal': lambda text: text,
    'bold': lambda text: f"**{text}**",
    'italic': lambda text: f"__{text}__",
    'script': lambda text: f"`{text}`",
    'double': lambda text: f"```{text}```",
    'bubble': lambda text: f"||{text}||",
    'square': lambda text: f"```{text}```",
    'strikethrough': lambda text: f"~~{text}~~",
    'underline': lambda text: f"___{text}___",
    'caps': lambda text: text.upper(),
    'lowercase': lambda text: text.lower(),
    'title': lambda text: text.title(),
    'space': lambda text: " ".join(text),
    'reverse': lambda text: text[::-1],
    'rainbow': lambda text: "".join([f"<span style='color:#{color}'>{c}</span>" for c, color in zip(text, ['ff0000', 'ff7700', 'ffff00', '00ff00', '0000ff', '8a2be2', 'ff00ff'])]),
    'fancy': lambda text: "".join([c + "̲" for c in text]),
    'small_caps': lambda text: text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ")),
    'bubble_text': lambda text: text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ⓪①②③④⑤⑥⑦⑧⑨")),
    'medieval': lambda text: text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ")),
    'cursive': lambda text: text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩")),
    # New font styles
    'double_struck': lambda text: text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡")),
    'monospace': lambda text: text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿")),
    'fullwidth': lambda text: text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９")),
    'crypt': lambda text: text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "ₐBCDₑFGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥWₓYZₐbcdₑfgₕᵢⱼₖₗₘₙₒₚqᵣₛₜᵤᵥwₓyz")),
    'circled': lambda text: text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨")),
    'inverted': lambda text: text.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄Zɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz0ƖᄅƐㄣϛ9ㄥ86")),
    'box': lambda text: "┏" + "━" * (len(text) + 2) + "┓\n┃ " + text + " ┃\n┗" + "━" * (len(text) + 2) + "┛",
    'dotted': lambda text: "╭" + "─" * (len(text) + 2) + "╮\n│ " + text + " │\n╰" + "─" * (len(text) + 2) + "╯",
    'invisible': lambda text: "".join([c + "\u200B" for c in text]),  # Zero-width space after each character
    'zalgo': lambda text: "".join([c + "".join(random.choices(["\u0300", "\u0301", "\u0302", "\u0303"], k=random.randint(1, 3))) for c in text]),
}

# Enhanced insults list
insults = [
    "کیرم تو کص ننت", "مادرجنده", "کص ننت", "کونی", "جنده", "کیری", "بی ناموس", "حرومزاده", "مادر قحبه", "جاکش",
    "کص ننه", "ننه جنده", "مادر کصده", "خارکصه", "کون گشاد", "ننه کیردزد", "مادر به خطا", "توله سگ", "پدر سگ", "حروم لقمه",
    "ننه الکسیس", "کص ننت میجوشه", "کیرم تو کص مادرت", "مادر جنده ی حرومی", "زنا زاده", "مادر خراب", "کصکش", "ننه سگ پرست",
    "مادرتو گاییدم", "خواهرتو گاییدم", "کیر سگ تو کص ننت", "کص مادرت", "کیر خر تو کص ننت", "کص خواهرت", "کون گشاد",
    "سیکتیر کص ننه", "ننه کیر خور", "خارکصده", "مادر جنده", "ننه خیابونی", "کیرم تو دهنت", "کص لیس", "ساک زن",
    "کیرم تو قبر ننت", "بی غیرت", "کص ننه پولی", "کیرم تو کص زنده و مردت", "مادر به خطا", "لاشی", "عوضی", "آشغال",
    "ننه کص طلا", "کیرم تو کص ننت بالا پایین", "کیر قاطر تو کص ننت", "کص ننت خونه خالی", "کیرم تو کص ننت یه دور", 
    "مادر خراب گشاد", "کیرم تو نسل اولت", "کیرم تو کص ننت محکم", "کیر خر تو کص مادرت", "کیرم تو روح مادر جندت",
    "کص ننت سفید برفی", "کیرم تو کص خارت", "کیر سگ تو کص مادرت", "کص ننه کیر خور", "کیرم تو کص زیر خواب",
    "مادر جنده ولگرد", "کیرم تو دهن مادرت", "کص مادرت گشاد", "کیرم تو لای پای مادرت", "کص ننت خیس",
    "کیرم تو کص مادرت بگردش", "کص ننه پاره", "مادر جنده حرفه ای", "کیرم تو کص و کون ننت", "کص ننه تنگ",
    "کیرم تو حلق مادرت", "ننه جنده مفت خور", "کیرم از پهنا تو کص ننت", "کص مادرت بد بو", "کیرم تو همه کس و کارت",
    "مادر کصده سیاه", "کیرم تو کص گشاد مادرت", "کص ننه ساک زن", "کیرم تو کص خاندانت", "مادر جنده خیابونی",
    "کیرم تو کص ننت یه عمر", "ننه جنده کص خور", "کیرم تو نسل و نژادت", "کص مادرت پاره", "کیرم تو شرف مادرت",
    "مادر جنده فراری", "کیرم تو روح مادرت", "کص ننه جندت", "کیرم تو غیرتت", "کص مادر بدکاره",
    "کیرم تو ننه جندت", "مادر کصده لاشی", "کیرم تو وجود مادرت", "کص ننه بی آبرو", "کیرم تو شعور ننت"
]

# Enhanced color themes
themes = {
    "default": {
        "primary": Fore.BLUE,
        "secondary": Fore.CYAN,
        "accent": Fore.YELLOW,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.WHITE,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTCYAN_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    },
    "dark": {
        "primary": Fore.BLUE,
        "secondary": Fore.MAGENTA,
        "accent": Fore.CYAN,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.WHITE,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTBLUE_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    },
    "light": {
        "primary": Fore.BLUE,
        "secondary": Fore.CYAN,
        "accent": Fore.MAGENTA,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.BLACK,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTMAGENTA_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.WHITE
    },
    "hacker": {
        "primary": Fore.GREEN,
        "secondary": Fore.GREEN,
        "accent": Fore.GREEN,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.GREEN,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTGREEN_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    },
    "colorful": {
        "primary": Fore.BLUE,
        "secondary": Fore.MAGENTA,
        "accent": Fore.CYAN,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.WHITE,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTCYAN_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    },
    "cyberpunk": {
        "primary": Fore.MAGENTA,
        "secondary": Fore.CYAN,
        "accent": Fore.YELLOW,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.LIGHTBLUE_EX,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTMAGENTA_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    },
    "neon": {
        "primary": Fore.LIGHTMAGENTA_EX,
        "secondary": Fore.LIGHTCYAN_EX,
        "accent": Fore.LIGHTYELLOW_EX,
        "success": Fore.LIGHTGREEN_EX,
        "error": Fore.LIGHTRED_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "info": Fore.LIGHTWHITE_EX,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTCYAN_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    },
    "pastel": {
        "primary": Fore.LIGHTBLUE_EX,
        "secondary": Fore.LIGHTCYAN_EX,
        "accent": Fore.LIGHTMAGENTA_EX,
        "success": Fore.LIGHTGREEN_EX,
        "error": Fore.LIGHTRED_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "info": Fore.LIGHTWHITE_EX,
        "muted": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTBLUE_EX,
        "critical": Fore.LIGHTRED_EX,
        "background": Back.BLACK
    }
}

# ASCII Art Logo
LOGO = f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.BLUE}████████╗███████╗██╗     ███████╗██████╗  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}╚══██╔══╝██╔════╝██║     ██╔════╝██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ██║   █████╗  ██║     █████╗  ██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ██║   ██╔══╝  ██║     ██╔══╝  ██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ██║   ███████╗███████╗███████╗██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████╗███████╗██╗     ███████╗██████╗  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}██╔════╝██╔════╝██║     ██╔════╝██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████╗█████╗  ██║     █████╗  ██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████║███████╗███████╗███████╗██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}╚══════╝╚══════╝╚══════╝╚══════╝╚═════╝  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██████╗  ██████╗ ████████╗               {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██╔══██╗██╔═══██╗╚══██╔══╝               {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██████╔╝██║   ██║   ██║                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██╔══██╗██║   ██║   ██║                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██████╔╝╚██████╔╝   ██║                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}╚═════╝  ╚═════╝    ╚═╝                  {Fore.CYAN}║
{Fore.CYAN}╚════════════════════════════════════════════╝
{Fore.GREEN}        Enhanced Platinum+ Edition v{APP_VERSION} ({APP_YEAR})
"""

MINI_LOGO = f"""
{Fore.CYAN}╔═══════════════════════════════╗
{Fore.CYAN}║ {Fore.BLUE}████████╗███████╗██╗     ███████╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████╗███████╗██╗     ███████╗ {Fore.CYAN}║ 
{Fore.CYAN}║ {Fore.YELLOW}██████╗  ██████╗ ████████╗     {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════╝
{Fore.GREEN}     Telegram SelfBot v{APP_VERSION}
"""

# Setup logging
def setup_logging(level=logging.INFO):
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root_logger = logging.getLogger()
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(log_formatter)
    
    # Stream handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.WARNING)  # Console shows only warnings and errors
    
    # Configure root logger
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Create logger for this app
    logger = logging.getLogger("TelegramSelfBot")
    return logger

# Initialize logger
logger = setup_logging()

# Initialize translator
translator = Translator()

# ====================================
# Utility Functions
# ====================================

def to_superscript(num):
    """Convert numbers to superscript notation"""
    superscripts = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '-': '⁻', '+': '⁺', '=': '⁼', '(': '⁽', ')': '⁾'
    }
    return ''.join(superscripts.get(n, n) for n in str(num))

def to_subscript(num):
    """Convert numbers to subscript notation"""
    subscripts = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '-': '₋', '+': '₊', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ', 'h': 'ₕ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'p': 'ₚ',
        's': 'ₛ', 't': 'ₜ'
    }
    return ''.join(subscripts.get(n, n) for n in str(num).lower())

def get_theme_color(color_name):
    """Get color value from current theme"""
    return themes.get(theme, themes["default"]).get(color_name, Fore.WHITE)

def colored_text(text, color_name):
    """Return colored text using current theme"""
    return f"{get_theme_color(color_name)}{text}{Style.RESET_ALL}"

def print_header(text, width=None):
    """Print a header with decoration"""
    if width is None:
        width = len(text) + 4
    
    print(f"\n{get_theme_color('secondary')}{'═' * width}")
    print(f"{get_theme_color('secondary')}║ {get_theme_color('info')}{text}{' ' * (width - len(text) - 3)}{get_theme_color('secondary')}║")
    print(f"{get_theme_color('secondary')}{'═' * width}\n")

def print_success(text):
    """Print success message"""
    print(f"{get_theme_color('success')}✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"{get_theme_color('error')}❌ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{get_theme_color('warning')}⚠️ {text}")

def print_info(text):
    """Print info message"""
    print(f"{get_theme_color('info')}ℹ️ {text}")

def print_status(label, status, active=True):
    """Print a status item with colored indicator"""
    status_color = get_theme_color('success') if active else get_theme_color('error')
    status_icon = "✅" if active else "❌"
    print(f"{get_theme_color('info')}{label}: {status_color}{status_icon} {status}")

def print_loading(text="Loading", cycles=3):
    """Display a loading animation"""
    animations = [".  ", ".. ", "..."]
    for _ in range(cycles):
        for animation in animations:
            sys.stdout.write(f"\r{get_theme_color('warning')}{text} {animation}")
            sys.stdout.flush()
            time.sleep(0.3)
    sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")
    sys.stdout.flush()

def print_progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    """Call in a loop to create terminal progress bar"""
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    sys.stdout.write(f'\r{get_theme_color("primary")}{prefix} |{get_theme_color("secondary")}{bar}{get_theme_color("primary")}| {percent}% {suffix}')
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def print_figlet(text, font="slant"):
    """Print stylized ASCII text using figlet"""
    try:
        fig_text = pyfiglet.figlet_format(text, font=font)
        print(f"{get_theme_color('accent')}{fig_text}")
    except Exception as e:
        logger.error(f"Error in figlet: {e}")
        print(text)

def secure_hash(text, algorithm='sha256'):
    """Create a secure hash of text"""
    if algorithm == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(text.encode()).hexdigest()
    else:
        return hashlib.sha256(text.encode()).hexdigest()

def generate_random_string(length=10):
    """Generate a random string of specified length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def format_time_difference(seconds):
    """Format a time difference in seconds to a human-readable string"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days != 1 else ''}"

def sanitize_text(text):
    """Clean text to prevent injection or other issues"""
    if text is None:
        return ""
    # Remove control characters except newlines and tabs
    return re.sub(r'[\x00-\x09\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', str(text))

def truncate_text(text, max_length=100, suffix="..."):
    """Truncate text to specified length with suffix"""
    if text is None:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-len(suffix)] + suffix

# ====================================
# Configuration and Data Management
# ====================================

def load_config():
    """Load configuration from file or create default"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Update with any missing keys from default config
                updated = False
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                        updated = True
                    elif isinstance(value, dict) and isinstance(config[key], dict):
                        # Handle nested dictionaries
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                                updated = True
                
                if updated:
                    save_config(config)
                    
                return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return default_config
    else:
        save_config(default_config)
        return default_config

def save_config(config):
    """Save configuration to file with error handling"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return False

def backup_data():
    """Backup all user data to file with optional encryption"""
    global last_backup_time
    backup_data = {
        "enemies": list(enemies),
        "current_font": current_font,
        "actions": actions,
        "spam_words": spam_words,
        "saved_messages": saved_messages,
        "reminders": reminders,
        "time_enabled": time_enabled,
        "saved_pics": saved_pics,
        "custom_replies": custom_replies,
        "blocked_words": blocked_words,
        "locked_chats": {k: list(v) for k, v in locked_chats.items()},
        "status_rotation": status_rotation,
        "status_rotation_active": status_rotation_active,
        "periodic_messages": periodic_messages,
        "filters": filters,
        "message_stats": message_stats,
        "welcome_messages": welcome_messages,
        "theme": theme,
        "chat_themes": chat_themes,
        "chat_nicknames": chat_nicknames,
        "custom_commands": custom_commands,
        "auto_reactions": auto_reactions,
        "user_notes": user_notes,
        "private_emoji_mapping": private_emoji_mapping,
        "backup_timestamp": datetime.now().isoformat(),
        "version": APP_VERSION
    }
    
    try:
        config = load_config()
        
        # Encrypt backup if enabled
        if config.get('encrypted_backup', False) and ENCRYPTION_AVAILABLE:
            key = config.get('encryption_key')
            if not key:
                key = Fernet.generate_key().decode()
                config['encryption_key'] = key
                save_config(config)
            
            cipher = Fernet(key.encode())
            encrypted_data = cipher.encrypt(json.dumps(backup_data).encode())
            
            with open(BACKUP_FILE, 'wb') as f:
                f.write(encrypted_data)
        else:
            # Standard JSON backup
            with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=4)
                
        last_backup_time = datetime.now()
        return True
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False

def restore_data():
    """Restore user data from backup file with support for encryption"""
    global enemies, current_font, actions, spam_words, saved_messages, reminders
    global time_enabled, saved_pics, custom_replies, blocked_words, locked_chats
    global status_rotation, status_rotation_active, periodic_messages, filters 
    global message_stats, welcome_messages, theme, chat_themes, chat_nicknames
    global custom_commands, auto_reactions, user_notes, private_emoji_mapping
    
    if not os.path.exists(BACKUP_FILE):
        return False
    
    try:
        config = load_config()
        data = None
        
        # Check if backup is encrypted
        if config.get('encrypted_backup', False) and ENCRYPTION_AVAILABLE:
            key = config.get('encryption_key')
            if not key:
                logger.error("Encryption key not found")
                return False
            
            cipher = Fernet(key.encode())
            with open(BACKUP_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            data = json.loads(decrypted_data)
        else:
            # Standard JSON backup
            with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        if not data:
            return False
            
        # Restore data with type checking
        enemies = set(data.get("enemies", []))
        current_font = data.get("current_font", "normal")
        
        # Safely update actions dictionary
        for key, value in data.get("actions", {}).items():
            if key in actions:
                actions[key] = bool(value)
        
        spam_words = list(data.get("spam_words", []))
        saved_messages = list(data.get("saved_messages", []))
        
        # Process reminders with error handling
        raw_reminders = data.get("reminders", [])
        reminders = []
        for reminder in raw_reminders:
            try:
                if isinstance(reminder, list) and len(reminder) == 3:
                    time_str, message, chat_id = reminder
                    reminders.append((str(time_str), str(message), int(chat_id)))
            except (ValueError, TypeError):
                logger.warning(f"Skipped invalid reminder: {reminder}")
        
        time_enabled = bool(data.get("time_enabled", True))
        saved_pics = list(data.get("saved_pics", []))
        custom_replies = data.get("custom_replies", {})
        blocked_words = list(data.get("blocked_words", []))
        
        # Restore locked_chats as sets
        locked_chats_data = data.get("locked_chats", {})
        for key in locked_chats.keys():
            if key in locked_chats_data:
                locked_chats[key] = set(locked_chats_data[key])
        
        status_rotation = list(data.get("status_rotation", []))
        status_rotation_active = bool(data.get("status_rotation_active", False))
        periodic_messages = list(data.get("periodic_messages", []))
        filters = data.get("filters", {})
        message_stats = data.get("message_stats", {})
        welcome_messages = data.get("welcome_messages", {})
        theme = data.get("theme", "default")
        chat_themes = data.get("chat_themes", {})
        chat_nicknames = data.get("chat_nicknames", {})
        custom_commands = data.get("custom_commands", {})
        auto_reactions = data.get("auto_reactions", {})
        user_notes = data.get("user_notes", {})
        private_emoji_mapping = data.get("private_emoji_mapping", {})
        
        return True
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False

async def cloud_backup(client):
    """Backup data to Telegram saved messages with encryption support"""
    try:
        if os.path.exists(BACKUP_FILE):
            config = load_config()
            me = await client.get_me()
            
            # Create caption with encryption status
            encryption_status = "🔒 Encrypted" if config.get('encrypted_backup', False) else "🔓 Unencrypted"
            caption = f"📂 Automatic cloud backup\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n🔐 {encryption_status}"
            
            # Send the backup file
            await client.send_file(
                me.id, 
                BACKUP_FILE,
                caption=caption
            )
            
            # Check if we should also backup the config
            if config.get('backup_config', True):
                await client.send_file(
                    me.id,
                    CONFIG_FILE,
                    caption=f"⚙️ Configuration backup\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
            
            return True
        return False
    except Exception as e:
        logger.error(f"Cloud backup failed: {e}")
        return False

# ====================================
# Media and Conversion Utilities
# ====================================

async def text_to_voice(text, lang='fa', slow=False):
    """Convert text to voice file with progress indicators and enhanced quality"""
    print_info("Converting text to voice...")
    try:
        # Create a random filename
        filename = os.path.join(VOICE_DIR, f"voice_{int(time.time())}_{generate_random_string(5)}.mp3")
        
        # Check if directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Create tts instance with options
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(filename)
        
        print_success("Voice file created successfully")
        return filename
    except Exception as e:
        logger.error(f"Error in text to voice: {e}")
        print_error(f"Failed to convert text to voice: {e}")
        return None

async def text_to_image(text, bg_color='white', text_color='black', font_name=None, font_size=40, 
                        effect=None, gradient=False, border=False, shadow=False, rotate=0):
    """Convert text to image with enhanced customization and effects"""
    print_info("Creating image from text...")
    try:
        # Calculate dimensions based on text length
        width = 800
        height = max(400, len(text) // 20 * 50)  # Dynamic height based on text length
        
        # Create base image
        if gradient and NUMPY_AVAILABLE:
            # Create gradient background
            import numpy as np
            from PIL import Image
            
            # Parse bg_color to get start color
            if isinstance(bg_color, str):
                # Simple gradient from color to white or black
                if bg_color.lower() in ['red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'magenta']:
                    color_map = {
                        'red': (255, 0, 0),
                        'green': (0, 255, 0),
                        'blue': (0, 0, 255),
                        'yellow': (255, 255, 0),
                        'purple': (128, 0, 128),
                        'cyan': (0, 255, 255),
                        'magenta': (255, 0, 255)
                    }
                    start_color = color_map.get(bg_color.lower(), (0, 0, 0))
                    end_color = (255, 255, 255)  # White
                else:
                    # Default gradient
                    start_color = (30, 30, 30)  # Dark gray
                    end_color = (200, 200, 200)  # Light gray
            else:
                start_color = (30, 30, 30)
                end_color = (200, 200, 200)
                
            # Create gradient array
            arr = np.zeros((height, width, 3), dtype=np.uint8)
            for i in range(width):
                r = start_color[0] + (end_color[0] - start_color[0]) * i // width
                g = start_color[1] + (end_color[1] - start_color[1]) * i // width
                b = start_color[2] + (end_color[2] - start_color[2]) * i // width
                arr[:, i] = [r, g, b]
                
            img = Image.fromarray(arr)
        else:
            # Solid color background
            img = Image.new('RGB', (width, height), color=bg_color)
        
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            if font_name and os.path.exists(font_name):
                font = ImageFont.truetype(font_name, font_size)
            else:
                # Try some common fonts
                common_fonts = [
                    "arial.ttf", "Arial.ttf",
                    "times.ttf", "Times.ttf",
                    "cour.ttf", "Courier.ttf",
                    "verdana.ttf", "Verdana.ttf",
                    "DejaVuSans.ttf"
                ]
                
                font = None
                for font_file in common_fonts:
                    try:
                        font = ImageFont.truetype(font_file, font_size)
                        break
                    except IOError:
                        continue
                
                if font is None:
                    font = ImageFont.load_default()
        except IOError:
            # Fallback to default
            font = ImageFont.load_default()
        
        # Wrap and render text
        lines = textwrap.wrap(text, width=30)
        y = 50
        for i, line in enumerate(lines):
            print_progress_bar(i + 1, len(lines), 'Progress:', 'Complete', 20)
            
            # Get text width for centering
            text_width, text_height = draw.textsize(line, font=font) if hasattr(draw, 'textsize') else (font.getlength(line), font.size)
            position = ((width - text_width) // 2, y)
            
            # Add shadow if requested
            if shadow:
                shadow_offset = 3
                draw.text((position[0] + shadow_offset, position[1] + shadow_offset), line, font=font, fill=(50, 50, 50))
            
            # Draw the text
            draw.text(position, line, font=font, fill=text_color)
            y += font_size + 10
        
        # Apply effects if requested
        if effect:
            if effect == 'blur':
                img = img.filter(ImageFilter.BLUR)
            elif effect == 'contour':
                img = img.filter(ImageFilter.CONTOUR)
            elif effect == 'emboss':
                img = img.filter(ImageFilter.EMBOSS)
            elif effect == 'sharpen':
                img = img.filter(ImageFilter.SHARPEN)
            elif effect == 'smooth':
                img = img.filter(ImageFilter.SMOOTH)
            elif effect == 'bw':
                img = img.convert('L').convert('RGB')
            elif effect == 'sepia':
                # Sepia effect
                sepia = img.convert('L')
                sepia = ImageEnhance.Contrast(sepia).enhance(1.5)
                sepia = ImageEnhance.Brightness(sepia).enhance(1.1)
                img = ImageOps.colorize(sepia, (112, 66, 20), (255, 255, 230))
        
        # Add border if requested
        if border:
            border_color = 'black' if bg_color.lower() in ['white', '#ffffff', 'lightyellow', 'lightblue'] else 'white'
            bordered_img = Image.new('RGB', (width + 20, height + 20), color=border_color)
            bordered_img.paste(img, (10, 10))
            img = bordered_img
        
        # Rotate if requested
        if rotate != 0:
            img = img.rotate(rotate, expand=True)
        
        # Save image
        filename = os.path.join(IMAGE_DIR, f"text_{int(time.time())}_{generate_random_string(5)}.png")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img.save(filename)
        
        print_success("Image created successfully")
        return filename
    except Exception as e:
        logger.error(f"Error in text to image: {e}")
        print_error(f"Failed to convert text to image: {e}")
        return None

async def text_to_gif(text, duration=500, bg_color='white', effects='color', font_size=40, width=800, height=400):
    """Convert text to animated GIF with customization"""
    print_info("Creating GIF from text...")
    try:
        frames = []
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            try:
                common_fonts = ["times.ttf", "cour.ttf", "verdana.ttf", "DejaVuSans.ttf"]
                for font_file in common_fonts:
                    try:
                        font = ImageFont.truetype(font_file, font_size)
                        break
                    except IOError:
                        continue
                if 'font' not in locals():
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
        
        if effects == 'color':
            # Color changing effect
            for i, color in enumerate(colors):
                print_progress_bar(i + 1, len(colors), 'Creating frames:', 'Complete', 20)
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Center text
                text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font.getlength(text), font.size)
                position = ((width - text_width) // 2, (height - text_height) // 2)
                
                draw.text(position, text, font=font, fill=color)
                frames.append(img)
        elif effects == 'zoom':
            # Zoom effect
            for i in range(5):
                print_progress_bar(i + 1, 5, 'Creating frames:', 'Complete', 20)
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                size = 30 + i * 10
                try:
                    curr_font = ImageFont.truetype("arial.ttf", size) if font is None else font
                except:
                    curr_font = ImageFont.load_default()
                
                # Center text
                text_width, text_height = draw.textsize(text, font=curr_font) if hasattr(draw, 'textsize') else (curr_font.getlength(text), curr_font.size)
                position = ((width - text_width) // 2, (height - text_height) // 2)
                
                draw.text(position, text, font=curr_font, fill='black')
                frames.append(img)
        elif effects == 'fade':
            # Fade effect (simulate opacity)
            opacity_steps = [0.2, 0.4, 0.6, 0.8, 1.0]
            for i, opacity in enumerate(opacity_steps):
                print_progress_bar(i + 1, len(opacity_steps), 'Creating frames:', 'Complete', 20)
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Simulate opacity by blending with background
                r, g, b = (0, 0, 0)  # Text color black
                if isinstance(bg_color, str) and bg_color.startswith('#'):
                    # Parse hex color
                    bg_r, bg_g, bg_b = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
                else:
                    bg_r, bg_g, bg_b = (255, 255, 255)  # Default white
                
                # Blend colors to simulate opacity
                blend_r = int(bg_r * (1 - opacity) + r * opacity)
                blend_g = int(bg_g * (1 - opacity) + g * opacity)
                blend_b = int(bg_b * (1 - opacity) + b * opacity)
                blend_color = (blend_r, blend_g, blend_b)
                
                # Center text
                text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font.getlength(text), font.size)
                position = ((width - text_width) // 2, (height - text_height) // 2)
                
                draw.text(position, text, font=font, fill=blend_color)
                frames.append(img)
        elif effects == 'rotate':
            # Rotation effect
            angles = [0, 10, 20, 30, 20, 10, 0, -10, -20, -30, -20, -10]
            for i, angle in enumerate(angles):
                print_progress_bar(i + 1, len(angles), 'Creating frames:', 'Complete', 20)
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Create a separate image for rotation to avoid quality loss
                txt_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
                txt_draw = ImageDraw.Draw(txt_img)
                
                # Center text
                text_width, text_height = txt_draw.textsize(text, font=font) if hasattr(txt_draw, 'textsize') else (font.getlength(text), font.size)
                position = ((width - text_width) // 2, (height - text_height) // 2)
                
                txt_draw.text(position, text, font=font, fill="black")
                rotated = txt_img.rotate(angle, resample=Image.BICUBIC, expand=False, center=(width//2, height//2))
                
                # Paste rotated text onto base image
                img.paste(rotated, (0, 0), rotated)
                frames.append(img)
        elif effects == 'rainbow':
            # Rainbow wave effect
            rainbow_colors = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
            for i in range(7):
                print_progress_bar(i + 1, 7, 'Creating frames:', 'Complete', 20)
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Center and draw text
                text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font.getlength(text), font.size)
                position = ((width - text_width) // 2, (height - text_height) // 2)
                
                # Shift rainbow colors
                shifted_colors = rainbow_colors[i:] + rainbow_colors[:i]
                
                # Draw each character with a different color
                char_width = text_width / len(text) if len(text) > 0 else 0
                for j, char in enumerate(text):
                    color_idx = j % len(shifted_colors)
                    draw.text((position[0] + j * char_width, position[1]), char, font=font, fill=shifted_colors[color_idx])
                
                frames.append(img)
        else:
            # Default animation
            for i, color in enumerate(colors):
                print_progress_bar(i + 1, len(colors), 'Creating frames:', 'Complete', 20)
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Center text
                text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font.getlength(text), font.size)
                position = ((width - text_width) // 2, (height - text_height) // 2)
                
                draw.text(position, text, font=font, fill=color)
                frames.append(img)
        
        filename = os.path.join(GIF_DIR, f"text_{int(time.time())}_{generate_random_string(5)}.gif")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
        print_success("GIF created successfully")
        return filename
    except Exception as e:
        logger.error(f"Error in text to gif: {e}")
        print_error(f"Failed to convert text to GIF: {e}")
        return None

async def create_qr_code(text, file_path=None, box_size=10, border=4, fill_color="black", back_color="white"):
    """Create a QR code from text with customization"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        if not file_path:
            file_path = os.path.join(QR_DIR, f"qrcode_{int(time.time())}_{generate_random_string(5)}.png")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
        img.save(file_path)
        return file_path
    except Exception as e:
        logger.error(f"Error creating QR code: {e}")
        return None

async def compress_image(image_path, quality=85, optimize=True):
    """Compress an image to reduce file size"""
    try:
        img = Image.open(image_path)
        
        # Generate output filename
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_compressed{ext}"
        
        # Save with compression
        img.save(output_path, quality=quality, optimize=optimize)
        return output_path
    except Exception as e:
        logger.error(f"Error compressing image: {e}")
        return None

async def translate_text(text, dest='fa', src='auto'):
    """Translate text to specified language with fallback mechanisms"""
    try:
        # Try with googletrans library
        result = translator.translate(text, dest=dest, src=src)
        return result.text
    except Exception as primary_error:
        logger.warning(f"Primary translation error: {primary_error}")
        
        try:
            # Fallback to HTTP request to Google Translate API
            base_url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": src,
                "tl": dest,
                "dt": "t",
                "q": text
            }
            
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                result = response.json()
                translated_text = ''.join([sentence[0] for sentence in result[0] if sentence[0]])
                return translated_text
            else:
                logger.error(f"HTTP translation error: {response.status_code}")
                return text
        except Exception as fallback_error:
            logger.error(f"Fallback translation error: {fallback_error}")
            return text

async def get_weather(city, api_key):
    """Get weather information for a city with enhanced formatting"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != 200:
            return f"Error: {data['message']}"
            
        # Extract data
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        wind_direction = data["wind"].get("deg", 0)
        country = data["sys"]["country"]
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M')
        
        # Get direction name from degrees
        directions = ["North", "NE", "East", "SE", "South", "SW", "West", "NW"]
        direction_idx = round(wind_direction / 45) % 8
        wind_dir_name = directions[direction_idx]
        
        # Create emojis based on weather
        weather_main = data["weather"][0]["main"].lower()
        if "clear" in weather_main:
            emoji = "☀️"
        elif "cloud" in weather_main:
            emoji = "☁️"
        elif "rain" in weather_main:
            emoji = "🌧️"
        elif "snow" in weather_main:
            emoji = "❄️"
        elif "thunder" in weather_main:
            emoji = "⛈️"
        elif "fog" in weather_main or "mist" in weather_main:
            emoji = "🌫️"
        else:
            emoji = "🌤️"
        
        return f"{emoji} **Weather in {city}, {country}**\n\n" \
               f"🌡️ **Temperature**: {temp}°C (feels like {feels_like}°C)\n" \
               f"🔍 **Range**: {temp_min}°C to {temp_max}°C\n" \
               f"🌤️ **Condition**: {weather_desc.capitalize()}\n" \
               f"💧 **Humidity**: {humidity}%\n" \
               f"💨 **Wind**: {wind_speed} m/s from {wind_dir_name} ({wind_direction}°)\n" \
               f"🌅 **Sunrise**: {sunrise}\n" \
               f"🌇 **Sunset**: {sunset}"
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return f"Error getting weather data: {e}"

# ====================================
# Telegram Utility Functions
# ====================================

async def update_time(client):
    """Update the last name with current time"""
    while running:
        try:
            if time_enabled:
                config = load_config()
                now = datetime.now(pytz.timezone(config['timezone']))
                hours = to_superscript(now.strftime('%H'))
                minutes = to_superscript(now.strftime('%M'))
                time_string = f"{hours}:{minutes}"
                
                # Avoid unnecessary updates if the time is the same
                me = await client.get_me()
                if me.last_name != time_string:
                    await client(functions.account.UpdateProfileRequest(last_name=time_string))
        except Exception as e:
            logger.error(f'Error updating time: {e}')
        await asyncio.sleep(60)

async def update_status_rotation(client):
    """Rotate through status messages in bio"""
    global status_rotation, status_rotation_active
    
    current_index = 0
    
    while running and status_rotation_active and status_rotation:
        try:
            status = status_rotation[current_index]
            
            # Avoid unnecessary updates if the status is the same
            me = await client.get_me()
            if me.about != status:
                await client(functions.account.UpdateProfileRequest(about=status))
            
            # Move to next status
            current_index = (current_index + 1) % len(status_rotation)
            
            # Wait for next rotation
            await asyncio.sleep(300)  # Change every 5 minutes
        except Exception as e:
            logger.error(f'Error updating status rotation: {e}')
            await asyncio.sleep(60)

async def auto_online(client):
    """Keep user online automatically"""
    while running and actions['online']:
        try:
            await client(functions.account.UpdateStatusRequest(offline=False))
        except Exception as e:
            logger.error(f'Error updating online status: {e}')
        await asyncio.sleep(30)

async def auto_typing(client, chat):
    """Maintain typing status in chat"""
    while running and actions['typing']:
        try:
            async with client.action(chat, 'typing'):
                await asyncio.sleep(3)
        except Exception as e:
            logger.error(f'Error in typing action: {e}')
            break

async def auto_reaction(event):
    """Add automatic reaction to messages"""
    if actions['reaction']:
        try:
            # Check for custom reactions for this chat
            chat_id = str(event.chat_id)
            sender_id = str(event.sender_id) if event.sender_id else None
            
            # Logic: First check for user-specific reaction, then chat-specific, then default
            reaction = None
            
            # User-specific reaction
            if sender_id and sender_id in auto_reactions:
                reaction_options = auto_reactions[sender_id]
                if reaction_options:
                    reaction = random.choice(reaction_options)
            
            # Chat-specific reaction
            if not reaction and chat_id in auto_reactions:
                reaction_options = auto_reactions[chat_id]
                if reaction_options:
                    reaction = random.choice(reaction_options)
            
            # Default reaction
            if not reaction:
                reaction = '👍'
            
            await event.message.react(reaction)
        except Exception as e:
            logger.error(f'Error adding reaction: {e}')

async def auto_read_messages(event, client):
    """Mark messages as read automatically"""
    if actions['read']:
        try:
            await client.send_read_acknowledge(event.chat_id, event.message)
        except Exception as e:
            logger.error(f'Error marking message as read: {e}')

async def auto_translate_message(event, client):
    """Automatically translate incoming messages"""
    if actions['translate'] and event.text:
        try:
            config = load_config()
            translated = await translate_text(event.text, dest=config['default_translate_lang'])
            
            if translated != event.text:
                sender = await event.get_sender()
                sender_name = utils.get_display_name(sender) if sender else "Unknown"
                
                translation_text = f"🔄 {sender_name}: {translated}"
                await client.send_message(event.chat_id, translation_text, reply_to=event.id)
        except Exception as e:
            logger.error(f'Error in auto translation: {e}')

async def schedule_message(client, chat_id, delay, message, recurring=False, interval=0):
    """Schedule message sending with countdown"""
    print_info(f"Message scheduled to send in {delay} minutes")
    
    # For one-time messages
    if not recurring:
        try:
            # Convert delay to seconds
            delay_seconds = delay * 60
            
            # Show a notification at the start
            logger.info(f"Message scheduled to send in {delay} minutes")
            
            # Wait with periodic updates
            start_time = time.time()
            end_time = start_time + delay_seconds
            
            while time.time() < end_time and running:
                remaining_seconds = end_time - time.time()
                remaining_minutes = int(remaining_seconds / 60)
                
                if (remaining_minutes % 5 == 0 and remaining_minutes > 0) or remaining_minutes <= 5:
                    if int(remaining_seconds) % 60 == 0:  # Only log once per minute
                        logger.info(f"Scheduled message will send in {remaining_minutes} minutes")
                
                await asyncio.sleep(1)
            
            if running:
                await client.send_message(chat_id, message)
                print_success(f"Scheduled message sent: {truncate_text(message, 30)}...")
                return True
            else:
                print_warning("Message scheduling cancelled: bot is no longer running")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send scheduled message: {e}")
            print_error(f"Failed to send scheduled message: {e}")
            return False
    
    # For recurring messages
    else:
        message_id = f"recurring_{chat_id}_{generate_random_string(5)}"
        
        async def recurring_task():
            while running:
                try:
                    # Wait for the interval
                    for i in range(interval):
                        if not running:
                            return
                        await asyncio.sleep(60)
                    
                    if running:  # Double-check running state
                        await client.send_message(chat_id, message)
                        logger.info(f"Recurring message sent: {truncate_text(message, 30)}...")
                except Exception as e:
                    logger.error(f"Failed to send recurring message: {e}")
                    # Wait a bit and continue trying
                    await asyncio.sleep(60)
        
        # Create and store the task for later cancellation if needed
        task = asyncio.create_task(recurring_task())
        active_tasks[message_id] = task
        
        return True

async def spam_messages(client, chat_id, count, message, delay=0.5):
    """Send multiple messages in sequence with progress indicators"""
    print_info(f"Sending {count} messages...")
    success_count = 0
    
    for i in range(count):
        try:
            await client.send_message(chat_id, message)
            success_count += 1
            print_progress_bar(i + 1, count, 'Sending:', 'Complete', 20)
            await asyncio.sleep(delay)
        except Exception as e:
            logger.error(f"Error in spam message {i+1}: {e}")
    
    print_success(f"Successfully sent {success_count}/{count} messages")
    return success_count

async def check_reminders(client):
    """Check and send reminders"""
    while running:
        try:
            current_time = datetime.now().strftime('%H:%M')
            to_remove = []
            
            for i, (reminder_time, message, chat_id) in enumerate(reminders):
                if reminder_time == current_time:
                    try:
                        await client.send_message(chat_id, f"🔔 یادآوری: {message}")
                        to_remove.append(i)
                    except Exception as e:
                        logger.error(f"Failed to send reminder: {e}")
            
            # Remove sent reminders
            for i in sorted(to_remove, reverse=True):
                try:
                    del reminders[i]
                except IndexError:
                    pass
                    
            # Backup if reminders were sent and removed
            if to_remove:
                backup_data()
                
        except Exception as e:
            logger.error(f"Error in check_reminders: {e}")
            
        await asyncio.sleep(30)  # Check every 30 seconds

async def auto_backup(client):
    """Automatically backup data at intervals"""
    try:
        config = load_config()
        if not config['auto_backup']:
            return
            
        interval = config['backup_interval'] * 60  # Convert to seconds
        
        while running:
            await asyncio.sleep(interval)
            
            if running:  # Double-check we're still running
                if backup_data():
                    logger.info("Auto-backup completed successfully")
                    
                    # If cloud backup is enabled
                    if config['cloud_backup']:
                        if await cloud_backup(client):
                            logger.info("Cloud backup completed successfully")
                        else:
                            logger.error("Cloud backup failed")
                else:
                    logger.error("Auto-backup failed")
    except Exception as e:
        logger.error(f"Error in auto_backup: {e}")

async def handle_anti_delete(event):
    """Save deleted messages for anti-delete feature"""
    try:
        chat_id = str(event.chat_id)
        if chat_id in locked_chats['delete'] and event.message:
            # Save message info before it's deleted
            msg = event.message
            sender = await event.get_sender()
            sender_name = utils.get_display_name(sender) if sender else "Unknown"
            
            content = ""
            if msg.text:
                content = msg.text
            elif msg.media:
                content = "[Media content]"
            elif msg.file:
                content = f"[File: {msg.file.name if hasattr(msg.file, 'name') else 'unknown'}]"
            else:
                content = "[Content unavailable]"
            
            saved_text = f"🔴 Deleted message from {sender_name}:\n{content}"
            await event.reply(saved_text)
            return True
    except Exception as e:
        logger.error(f"Error in anti-delete: {e}")
    return False

async def track_message_stats(event):
    """Track message statistics for analytics"""
    if actions['stats']:
        try:
            chat_id = str(event.chat_id)
            sender_id = str(event.sender_id) if event.sender_id else "unknown"
            
            # Initialize chat stats if not exist
            if chat_id not in message_stats:
                message_stats[chat_id] = {
                    "total_messages": 0,
                    "users": {},
                    "hourly": [0] * 24,
                    "daily": [0] * 7,
                    "keywords": {},
                    "first_message": datetime.now().isoformat(),
                    "last_message": datetime.now().isoformat(),
                    "media_count": 0,
                    "reaction_count": 0,
                    "reply_count": 0,
                    "forward_count": 0,
                    "top_words": {},
                    "emoji_count": 0
                }
            
            # Update total messages
            message_stats[chat_id]["total_messages"] += 1
            
            # Update timestamp of last message
            message_stats[chat_id]["last_message"] = datetime.now().isoformat()
            
            # Update user stats
            if sender_id not in message_stats[chat_id]["users"]:
                message_stats[chat_id]["users"][sender_id] = 0
            message_stats[chat_id]["users"][sender_id] += 1
            
            # Update hourly stats
            hour = datetime.now().hour
            message_stats[chat_id]["hourly"][hour] += 1
            
            # Update daily stats
            day = datetime.now().weekday()
            message_stats[chat_id]["daily"][day] += 1
            
            # Update media count
            if event.media:
                message_stats[chat_id]["media_count"] += 1
                
            # Update reply count
            if event.is_reply:
                message_stats[chat_id]["reply_count"] += 1
                
            # Update forward count
            if event.forward:
                message_stats[chat_id]["forward_count"] += 1
                
            # Track keywords and words
            if event.text:
                words = event.text.lower().split()
                
                # Update word stats
                for word in words:
                    if len(word) > 3:  # Only track words longer than 3 chars
                        if word not in message_stats[chat_id]["top_words"]:
                            message_stats[chat_id]["top_words"][word] = 0
                        message_stats[chat_id]["top_words"][word] += 1
                    
                # Track any specified keywords
                for word in words:
                    if word in message_stats[chat_id].get("keywords", {}):
                        message_stats[chat_id]["keywords"][word] += 1
                    elif len(word) > 3:  # Only auto-add longer words
                        if len(message_stats[chat_id]["keywords"]) < 100:  # Limit to prevent excessive memory usage
                            message_stats[chat_id]["keywords"][word] = 1
            
            # Save stats periodically
            if message_stats[chat_id]["total_messages"] % 100 == 0:
                backup_data()
                
        except Exception as e:
            logger.error(f"Error tracking message stats: {e}")

# ====================================
# Help and Information Functions
# ====================================

async def show_help_menu(client, event):
    """Show enhanced help menu with categories"""
    help_text = """
📱 **راهنمای ربات سلف بات پلاتینیوم+ نسخه 3.5**

🔰 **بخش‌های اصلی**:

🔹 **تنظیمات اولیه**:
• `پنل` - نمایش منوی راهنما
• `وضعیت` - نمایش وضعیت کلی ربات
• `theme [نام تم]` - تغییر تم ربات (default, dark, light, hacker, colorful, cyberpunk, neon, pastel)
• `exit` - خروج از برنامه
• `backup` - پشتیبان‌گیری دستی از داده‌ها
• `restore` - بازیابی داده‌ها از پشتیبان
• `secure backup on/off` - فعال/غیرفعال کردن رمزنگاری پشتیبان
• `cloud backup on/off` - پشتیبان‌گیری خودکار در پیام‌های ذخیره شده
• `undo` - برگرداندن آخرین عملیات

🔹 **مدیریت دشمن**:
• `تنظیم دشمن` (ریپلای) - اضافه کردن به لیست دشمن
• `حذف دشمن` (ریپلای) - حذف از لیست دشمن  
• `لیست دشمن` - نمایش لیست دشمنان
• `insult [on/off]` - فعال/غیرفعال کردن پاسخ خودکار به دشمن
• `blacklist [username]` - افزودن کاربر به لیست سیاه

🔹 **سبک متن**:
• `bold on/off` - فونت ضخیم
• `italic on/off` - فونت کج
• `script on/off` - فونت دست‌نویس 
• `double on/off` - فونت دوتایی
• `bubble on/off` - فونت حبابی
• `square on/off` - فونت مربعی
• `strikethrough on/off` - فونت خط خورده
• `underline on/off` - فونت زیر خط دار
• `caps on/off` - فونت بزرگ
• `lowercase on/off` - فونت کوچک
• `title on/off` - فونت عنوان
• `space on/off` - فونت فاصله‌دار
• `reverse on/off` - فونت معکوس
• `rainbow on/off` - فونت رنگین‌کمانی
• `fancy on/off` - فونت فانتزی
• `small_caps on/off` - فونت کوچک کپس
• `bubble_text on/off` - فونت حبابی متن
• `medieval on/off` - فونت قرون وسطایی
• `cursive on/off` - فونت دست‌خط
• `monospace on/off` - فونت تک‌فاصله
• `fullwidth on/off` - فونت عریض
• `double_struck on/off` - فونت دوخطی
• `circled on/off` - فونت دایره‌ای
• `inverted on/off` - فونت وارونه
• `box on/off` - متن درون کادر
• `dotted on/off` - متن با حاشیه نقطه‌ای
• `zalgo on/off` - متن با جلوه زالگو

🔹 **اکشن‌های خودکار**:
• `typing on/off` - تایپینگ دائم
• `online on/off` - آنلاین دائم 
• `reaction on/off` - ری‌اکشن خودکار
• `time on/off` - نمایش ساعت در نام
• `read on/off` - خواندن خودکار پیام‌ها
• `reply on/off` - پاسخ خودکار به پیام‌ها
• `stats on/off` - ثبت آمار پیام‌ها
• `translate on/off` - ترجمه خودکار پیام‌ها
• `silent on/off` - حالت بی‌صدا
• `invisible on/off` - حالت مخفی
• `privacy on/off` - حالت حریم خصوصی
• `set translate [زبان]` - تنظیم زبان پیش‌فرض ترجمه

🔹 **قفل‌های امنیتی پیشرفته**:
• `screenshot on/off` - قفل اسکرین‌شات
• `forward on/off` - قفل فوروارد
• `copy on/off` - قفل کپی
• `delete on/off` - ضد حذف پیام
• `edit on/off` - ضد ویرایش پیام
• `spam on/off` - ضد اسپم
• `link on/off` - فیلتر لینک
• `mention on/off` - فیلتر منشن
• `ai_filter on/off` - فیلتر محتوای هوشمند
• `raid on/off` - محافظت ضد حمله گروهی
• `privacy on/off` - حالت حریم خصوصی پیشرفته
• `log on/off` - ثبت تمام پیام‌ها
• `join on/off` - محدودیت عضویت جدید
• `media on/off` - مسدود کردن رسانه

🔹 **تبدیل فرمت پیشرفته**:
• `متن به ویس بگو [متن]` - تبدیل متن به ویس
• `متن به ویس بگو [متن] [زبان] [سرعت]` - تبدیل با تنظیمات سفارشی
• `متن به عکس [متن]` - تبدیل متن به عکس
• `متن به عکس [متن] [رنگ‌پس‌زمینه] [رنگ‌متن]` - تبدیل متن به عکس با رنگ سفارشی
• `متن به گیف [متن]` - تبدیل متن به گیف
• `متن به گیف [متن] [افکت]` - تبدیل متن به گیف با افکت‌های متنوع (color/zoom/fade/rotate/rainbow)
• `qrcode [متن]` - ساخت کیو‌آر‌کد از متن
• `qrcode [متن] [رنگ] [رنگ‌پس‌زمینه]` - ساخت کیو‌آر‌کد سفارشی
• `compress [ریپلای عکس]` - فشرده‌سازی عکس
• `ترجمه [متن] [زبان مقصد]` - ترجمه متن به زبان مورد نظر

🔹 **مدیریت محتوا**:
• `save pic` - ذخیره عکس (ریپلای)
• `show pics` - نمایش عکس‌های ذخیره شده
• `delete pic [شماره]` - حذف عکس ذخیره شده
• `save` - ذخیره پیام (ریپلای)
• `saved` - نمایش پیام های ذخیره شده
• `delete saved [شماره]` - حذف پیام ذخیره شده
• `tag [نام]` - ایجاد تگ برای کاربر
• `tags` - نمایش لیست تگ‌ها
• `note [کلید] [متن]` - ذخیره یادداشت
• `notes` - نمایش لیست یادداشت‌ها
• `get note [کلید]` - نمایش یادداشت

🔹 **مدیریت کلمات و فیلترها**:
• `block word [کلمه]` - مسدود کردن کلمه
• `unblock word [کلمه]` - رفع مسدودیت کلمه
• `block list` - نمایش لیست کلمات مسدود شده
• `filter [کلمه/عبارت] [جایگزین]` - تنظیم فیلتر جایگزینی
• `filters` - نمایش لیست فیلترها
• `remove filter [کلمه/عبارت]` - حذف فیلتر

🔹 **پیام‌رسانی هوشمند**:
• `schedule [زمان به دقیقه] [متن پیام]` - ارسال پیام زمان‌دار
• `schedule recurring [فاصله به دقیقه] [متن پیام]` - ارسال پیام تکراری
• `cancel schedule [شناسه]` - لغو پیام زمان‌بندی شده
• `schedulelist` - نمایش لیست پیام‌های زمان‌بندی شده
• `remind [ساعت:دقیقه] [متن پیام]` - تنظیم یادآور
• `remindlist` - نمایش لیست یادآورها
• `spam [تعداد] [متن پیام]` - ارسال پیام تکراری
• `smartspam [تعداد] [تاخیر] [متن پیام]` - اسپم هوشمند با تأخیر
• `multispam [تعداد] [متن۱] | [متن۲] | ...` - اسپم متن‌های مختلف

🔹 **پاسخ خودکار پیشرفته**:
• `auto reply [کلمه کلیدی] [پاسخ]` - تنظیم پاسخ خودکار ساده
• `smart reply [کلمه کلیدی] [پاسخ] [احتمال]` - پاسخ خودکار با احتمال مشخص
• `pattern reply [الگو] [پاسخ]` - پاسخ خودکار براساس الگو
• `delete reply [کلمه کلیدی]` - حذف پاسخ خودکار
• `replies` - نمایش لیست پاسخ‌های خودکار
• `welcome [متن]` - تنظیم پیام خوش‌آمدگویی
• `show welcome` - نمایش پیام خوش‌آمدگویی
• `auto react [ایموجی]` - تنظیم ری‌اکشن خودکار
• `auto react [چت/کاربر] [ایموجی]` - تنظیم ری‌اکشن برای چت/کاربر مشخص

🔹 **ابزارهای سودمند**:
• `status [متن]` - تنظیم متن وضعیت (بیو)
• `add status [متن]` - اضافه کردن به وضعیت‌های چرخشی
• `status rotation on/off` - فعال/غیرفعال کردن چرخش خودکار وضعیت
• `show status` - نمایش وضعیت‌های چرخشی
• `clear status` - پاک کردن وضعیت‌های چرخشی
• `search [متن]` - جستجو در پیام ها
• `weather [شهر]` - نمایش آب و هوا
• `set weather [کلید API]` - تنظیم کلید API آب و هوا
• `nick [نام]` - تنظیم لقب برای چت فعلی
• `date` - نمایش تاریخ شمسی و میلادی
• `ping` - بررسی زمان پاسخ‌دهی ربات
• `id` - نمایش شناسه کاربر یا چت
• `stats [نام چت/آیدی]` - نمایش آمار پیام‌ها
• `calc [عبارت]` - ماشین حساب
• `logo [متن] [فونت]` - ساخت لوگو متنی
• `custom command [نام] [پاسخ]` - ایجاد دستور سفارشی
• `commands` - نمایش لیست دستورات سفارشی

🔹 **ابزارهای امنیتی پیشرفته**:
• `encrypt [متن]` - رمزنگاری متن
• `decrypt [متن]` - رمزگشایی متن
• `password [طول]` - تولید رمز عبور تصادفی و قوی
• `hash [متن]` - ساخت هش از متن
• `clear chat` - پاکسازی تاریخچه چت خصوصی
• `wipe [تعداد]` - پاکسازی آخرین N پیام شما
• `lock chat` - قفل کردن چت با تمام محافظت‌ها
• `unlock chat` - باز کردن قفل چت

🔹 **تنظیمات پیشرفته**:
• `set prefix [پیشوند]` - تغییر پیشوند دستورات بات
• `set spam limit [عدد]` - تنظیم محدودیت تعداد اسپم
• `set backup interval [دقیقه]` - تنظیم فاصله زمانی پشتیبان‌گیری خودکار
• `set log level [سطح]` - تنظیم سطح ثبت رویدادها
• `set timezone [منطقه]` - تنظیم منطقه زمانی
• `set auto read [on/off]` - فعال/غیرفعال کردن خواندن خودکار پیام‌ها
• `set auto backup [on/off]` - فعال/غیرفعال کردن پشتیبان‌گیری خودکار
• `disable command [نام]` - غیرفعال کردن دستور
• `enable command [نام]` - فعال کردن دستور غیرفعال شده

---
📝 برای اطلاعات بیشتر و آموزش‌های پیشرفته، دستور `help [نام بخش]` را اجرا کنید.
برای مثال: `help security`، `help messages`، `help filters`، یا `help autoresponder`
"""
    try:
        await event.edit(help_text)
    except Exception as e:
        print_error(f"Error displaying help menu: {e}")
        print(help_text.replace("**", "").replace("`", ""))

async def show_section_help(client, event, section):
    """Show detailed help for a specific section"""
    section = section.lower()
    
    help_sections = {
        "security": """
📛 **راهنمای بخش امنیت** 📛

🔐 **محافظت از چت**:
• `screenshot on/off` - جلوگیری از اسکرین‌شات (فقط در بعضی کلاینت‌ها موثر است)
• `forward on/off` - مسدود کردن فوروارد پیام‌ها
• `copy on/off` - مسدود کردن کپی پیام‌ها
• `delete on/off` - ذخیره و بازیابی پیام‌های حذف شده
• `edit on/off` - ذخیره نسخه‌های قبلی پیام‌های ویرایش شده
• `spam on/off` - مسدود کردن اسپم
• `link on/off` - مسدود کردن ارسال لینک
• `mention on/off` - مسدود کردن منشن
• `ai_filter on/off` - فیلتر محتوا با هوش مصنوعی (تشخیص محتوای نامناسب)
• `raid on/off` - جلوگیری از حملات گروهی (حذف پیام‌های مشکوک)
• `log on/off` - ثبت تمام پیام‌ها برای بررسی بعدی
• `join on/off` - محدود کردن عضویت افراد جدید
• `media on/off` - مسدود کردن ارسال مدیا (عکس، ویدیو، و...)
• `lock chat` - فعال کردن تمام محافظت‌ها برای چت فعلی
• `unlock chat` - غیرفعال کردن تمام محافظت‌ها برای چت فعلی

🔒 **حریم خصوصی و امنیت شخصی**:
• `privacy on/off` - حالت حریم خصوصی پیشرفته (مخفی کردن آخرین زمان آنلاین، وضعیت تایپینگ و...)
• `invisible on/off` - حالت مخفی (عدم نمایش در لیست کاربران آنلاین)
• `silent on/off` - حالت بی‌صدا (غیرفعال کردن تمام اعلان‌ها)
• `encrypt [متن]` - رمزنگاری متن با کلید خصوصی
• `decrypt [متن]` - رمزگشایی متن رمزنگاری شده
• `password [طول]` - تولید رمز عبور تصادفی و قوی
• `hash [متن]` - ساخت هش SHA-256 از متن
• `secure backup on/off` - فعال/غیرفعال کردن رمزنگاری پشتیبان
• `clear chat` - پاکسازی تاریخچه چت خصوصی
• `wipe [تعداد]` - پاکسازی آخرین N پیام شما

👥 **مدیریت کاربران**:
• `تنظیم دشمن` (ریپلای) - اضافه کردن کاربر به لیست دشمن
• `حذف دشمن` (ریپلای) - حذف کاربر از لیست دشمن
• `لیست دشمن` - نمایش لیست دشمنان
• `blacklist [username]` - افزودن کاربر به لیست سیاه (مسدود کردن تمام پیام‌ها)
• `whitelist [username]` - افزودن کاربر به لیست سفید (اجازه ارتباط در حالت حریم خصوصی)
• `blocklist` - نمایش لیست کاربران مسدود شده

🔍 **نظارت و پایش**:
• `watch [username]` - نظارت بر فعالیت کاربر (ثبت تمام پیام‌ها)
• `watchlist` - نمایش لیست کاربران تحت نظارت
• `stop watch [username]` - توقف نظارت بر کاربر
• `alert [keyword]` - دریافت هشدار هنگام استفاده از کلمه کلیدی
• `alerts` - نمایش لیست هشدارها

💡 **نکات امنیتی**:
• برای حداکثر امنیت، ترکیبی از قفل‌ها را برای چت‌های مهم فعال کنید
• از رمزنگاری برای پیام‌های حساس استفاده کنید
• پشتیبان‌های رمزنگاری شده را در مکان امن نگهداری کنید
• کلید رمزنگاری را با هیچکس به اشتراک نگذارید
• از گزینه‌های `watch` و `alert` برای شناسایی تهدیدات احتمالی استفاده کنید
""",

        "messages": """
📨 **راهنمای بخش پیام‌رسانی** 📨

⏱️ **پیام‌های زمان‌بندی شده**:
• `schedule [زمان به دقیقه] [متن پیام]` - ارسال پیام بعد از زمان مشخص
• `schedule recurring [فاصله به دقیقه] [متن پیام]` - ارسال پیام تکراری با فاصله زمانی مشخص
• `cancel schedule [شناسه]` - لغو پیام زمان‌بندی شده
• `schedulelist` - نمایش لیست پیام‌های زمان‌بندی شده
• `schedule at [ساعت:دقیقه] [متن پیام]` - ارسال پیام در زمان مشخص
• `schedule daily [ساعت:دقیقه] [متن پیام]` - ارسال پیام روزانه در زمان مشخص
• `schedule weekly [روز هفته] [ساعت:دقیقه] [متن پیام]` - ارسال پیام هفتگی

🔔 **یادآوری**:
• `remind [ساعت:دقیقه] [متن پیام]` - تنظیم یادآور
• `remind after [دقیقه] [متن پیام]` - یادآوری بعد از مدت مشخص
• `remind every [دقیقه] [متن پیام]` - یادآوری دوره‌ای با فاصله زمانی مشخص
• `remindlist` - نمایش لیست یادآورها
• `delete remind [شماره]` - حذف یادآور

📝 **مدیریت پیام‌ها**:
• `save` - ذخیره پیام (ریپلای)
• `saved` - نمایش پیام های ذخیره شده
• `delete saved [شماره]` - حذف پیام ذخیره شده
• `save pic` - ذخیره عکس (ریپلای)
• `show pics` - نمایش عکس‌های ذخیره شده
• `delete pic [شماره]` - حذف عکس ذخیره شده
• `forward to [username]` - فوروارد به کاربر مشخص (ریپلای)
• `copy to [username]` - کپی به کاربر مشخص (ریپلای)

🔁 **تکرار پیام‌ها**:
• `spam [تعداد] [متن پیام]` - ارسال پیام تکراری
• `smartspam [تعداد] [تاخیر] [متن پیام]` - اسپم هوشمند با تأخیر
• `multispam [تعداد] [متن۱] | [متن۲] | ...` - اسپم متن‌های مختلف به صورت تصادفی
• `charspam [تعداد] [کاراکتر]` - ارسال یک کاراکتر به تعداد مشخص
• `groupspam [تعداد چت] [تعداد پیام] [متن]` - ارسال اسپم به چندین چت همزمان

📋 **الگوهای پیام**:
• `template [نام] [متن الگو]` - ذخیره الگوی پیام
• `templates` - نمایش لیست الگوها
• `send template [نام]` - ارسال پیام با استفاده از الگو
• `edit template [نام] [متن جدید]` - ویرایش الگو
• `delete template [نام]` - حذف الگو

💬 **قالب‌های پیام**:
• در الگوها می‌توانید از متغیرهای زیر استفاده کنید:
  - `{name}` - نام کاربر مخاطب
  - `{username}` - نام کاربری مخاطب
  - `{chat}` - نام چت
  - `{date}` - تاریخ فعلی
  - `{time}` - زمان فعلی

💡 **نکات کاربردی**:
• از `smartspam` برای جلوگیری از محدودیت فلود استفاده کنید
• برای ارسال پیام‌های طولانی، آنها را در الگوها ذخیره کنید
• از یادآورها برای قرارها و فعالیت‌های مهم استفاده کنید
• پیام‌های حساس را با `encrypt` رمزنگاری کنید قبل از ارسال
• از `multispam` برای تنوع در پیام‌های تکراری استفاده کنید
""",

        "filters": """
🔍 **راهنمای بخش فیلترها و کلمات** 🔍

⛔ **مدیریت کلمات مسدود**:
• `block word [کلمه]` - مسدود کردن کلمه
• `unblock word [کلمه]` - رفع مسدودیت کلمه
• `block list` - نمایش لیست کلمات مسدود شده
• `block words [کلمه1] [کلمه2] ...` - مسدود کردن چندین کلمه همزمان
• `clear blocked` - پاک کردن لیست کلمات مسدود شده

🔄 **فیلترهای جایگزینی**:
• `filter [کلمه/عبارت] [جایگزین]` - تنظیم فیلتر جایگزینی
• `filters` - نمایش لیست فیلترها
• `remove filter [کلمه/عبارت]` - حذف فیلتر
• `import filters [نام فایل]` - وارد کردن فیلترها از فایل JSON
• `export filters` - استخراج فیلترها به فایل JSON

🎯 **فیلترهای پیشرفته**:
• `regex filter [الگو] [جایگزین]` - ایجاد فیلتر براساس الگوی regex
• `animated filter [کلمه] [انیمیشن]` - جایگزینی کلمه با متن انیمیشنی
• `random filter [کلمه] [گزینه1|گزینه2|...]` - جایگزینی تصادفی
• `sticker filter [کلمه] [آیدی استیکر]` - پاسخ با استیکر به کلمه خاص
• `media filter [کلمه] [آدرس فایل]` - پاسخ با مدیا به کلمه خاص

🧠 **فیلترهای هوشمند**:
• `ai_filter on/off` - فعال/غیرفعال کردن فیلتر محتوا با هوش مصنوعی
• `set ai_filter level [low/medium/high]` - تنظیم سطح حساسیت فیلتر هوشمند
• `add sensitive [کلمه/عبارت]` - افزودن به لیست کلمات حساس
• `sensitive list` - نمایش لیست کلمات حساس
• `remove sensitive [کلمه/عبارت]` - حذف از لیست کلمات حساس

📊 **تنظیمات فیلتر**:
• `set filter mode [delete/replace/alert]` - تنظیم نحوه عملکرد فیلتر
• `set filter scope [all/group/private]` - تنظیم محدوده عملکرد فیلتر
• `set filter users [all/blacklist/whitelist]` - تنظیم کاربران مشمول فیلتر
• `filter stats` - آمار عملکرد فیلترها

🔠 **مدیریت ایموجی‌ها**:
• `emoji map [ایموجی عادی] [ایموجی سفارشی]` - تعیین نگاشت ایموجی
• `emoji maps` - نمایش لیست نگاشت‌های ایموجی
• `clear emoji maps` - پاک کردن تمام نگاشت‌های ایموجی
• `auto emoji on/off` - تبدیل خودکار ایموجی‌ها

💡 **نکات کاربردی**:
• از `regex filter` برای الگوهای پیچیده استفاده کنید
• فیلترهای `random` برای تنوع در پاسخ‌ها مفید هستند
• برای حفاظت از حریم خصوصی، از فیلترهای `ai_filter` استفاده کنید
• نگاشت‌های ایموجی برای سفارشی‌سازی ظاهر پیام‌ها مفید است
• ترکیب فیلترها را می‌توان برای سطوح مختلف مدیریت محتوا استفاده کرد
""",

        "autoresponder": """
🤖 **راهنمای سیستم پاسخ خودکار** 🤖

🔄 **پاسخ‌های ساده**:
• `auto reply [کلمه کلیدی] [پاسخ]` - تنظیم پاسخ خودکار ساده
• `delete reply [کلمه کلیدی]` - حذف پاسخ خودکار
• `replies` - نمایش لیست پاسخ‌های خودکار
• `clear replies` - پاک کردن تمام پاسخ‌های خودکار
• `reply on/off` - فعال/غیرفعال کردن سیستم پاسخ خودکار

🎲 **پاسخ‌های پیشرفته**:
• `smart reply [کلمه کلیدی] [پاسخ] [احتمال]` - پاسخ خودکار با احتمال مشخص (0-100)
• `pattern reply [الگو] [پاسخ]` - پاسخ خودکار براساس الگوی regex
• `multi reply [کلمه کلیدی] [پاسخ1|پاسخ2|...]` - پاسخ تصادفی از بین گزینه‌ها
• `delayed reply [کلمه کلیدی] [تاخیر] [پاسخ]` - پاسخ با تاخیر (به ثانیه)
• `chain reply [کلمه کلیدی] [پاسخ1] [تاخیر1] [پاسخ2] [تاخیر2] ...` - زنجیره پاسخ‌ها

👋 **پیام‌های خوش‌آمدگویی**:
• `welcome [متن]` - تنظیم پیام خوش‌آمدگویی برای چت فعلی
• `show welcome` - نمایش پیام خوش‌آمدگویی چت فعلی
• `welcome list` - نمایش تمام پیام‌های خوش‌آمدگویی
• `delete welcome` - حذف پیام خوش‌آمدگویی چت فعلی
• `welcome media [آدرس فایل]` - تنظیم رسانه برای خوش‌آمدگویی

😊 **ری‌اکشن‌های خودکار**:
• `auto react [ایموجی]` - تنظیم ری‌اکشن خودکار برای همه پیام‌ها
• `auto react [چت/کاربر] [ایموجی]` - تنظیم ری‌اکشن برای چت/کاربر مشخص
• `random react on/off` - ری‌اکشن تصادفی به پیام‌ها
• `react list` - نمایش لیست ری‌اکشن‌های خودکار
• `remove react [چت/کاربر]` - حذف ری‌اکشن خودکار

🔍 **پاسخ‌های هوشمند**:
• `context reply [کلمه کلیدی] [پاسخ با متغیر]` - پاسخ با در نظر گرفتن زمینه
• `auto poll [کلمه کلیدی] [سوال] [گزینه1|گزینه2|...]` - ایجاد نظرسنجی خودکار
• `media reply [کلمه کلیدی] [آدرس فایل]` - پاسخ با مدیا
• `forward reply [کلمه کلیدی] [آیدی پیام]` - فوروارد پیام به عنوان پاسخ

📊 **تنظیمات پاسخ‌دهنده**:
• `set reply mode [all/mention/private]` - تنظیم حالت پاسخ‌دهی
• `set reply delay [ثانیه]` - تنظیم تاخیر پیش‌فرض برای پاسخ‌ها
• `reply stats` - آمار عملکرد پاسخ‌های خودکار
• `export replies` - استخراج پاسخ‌های خودکار به فایل
• `import replies [نام فایل]` - وارد کردن پاسخ‌های خودکار از فایل

💡 **نکات پیشرفته**:
• در پاسخ‌ها می‌توانید از متغیرهای زیر استفاده کنید:
  - `{name}` - نام فرستنده پیام
  - `{username}` - نام کاربری فرستنده
  - `{chat}` - نام چت
  - `{message}` - متن پیام اصلی
  - `{date}` - تاریخ فعلی
  - `{time}` - زمان فعلی
  - `{count}` - تعداد دفعات پاسخ به این کلمه کلیدی

• از `pattern reply` برای پاسخ‌های پیچیده‌تر استفاده کنید
• برای کاربران VIP، پاسخ‌های شخصی تنظیم کنید
• از پاسخ‌های زنجیره‌ای برای مکالمات طبیعی‌تر استفاده کنید
""",

        "fonts": """
🔤 **راهنمای سبک‌های متنی و فونت‌ها** 🔤

✏️ **فونت‌های پایه**:
• `bold on/off` - فونت ضخیم **مثال**
• `italic on/off` - فونت کج __مثال__
• `script on/off` - فونت دست‌نویس `مثال`
• `double on/off` - فونت دوتایی ```مثال```
• `bubble on/off` - فونت حبابی ||مثال||
• `square on/off` - فونت مربعی ```مثال```
• `strikethrough on/off` - فونت خط خورده ~~مثال~~
• `underline on/off` - فونت زیر خط دار ___مثال___

🔠 **تغییر حروف**:
• `caps on/off` - حروف بزرگ مثال
• `lowercase on/off` - حروف کوچک مثال
• `title on/off` - حروف عنوان مثال
• `space on/off` - فاصله‌دار م ث ا ل
• `reverse on/off` - معکوس لاثم

🎨 **سبک‌های ویژه**:
• `rainbow on/off` - رنگین‌کمانی
• `fancy on/off` - فانتزی م̲ث̲ا̲ل̲
• `small_caps on/off` - حروف کوچک بزرگنما ᴍᴜᴛʜᴀʟ
• `bubble_text on/off` - حباب‌دار ⓜⓤⓣⓗⓐⓛ
• `medieval on/off` - قرون وسطایی 𝔪𝔲𝔱𝔥𝔞𝔩
• `cursive on/off` - دست‌خط 𝓶𝓾𝓽𝓱𝓪𝓵

✨ **سبک‌های جدید**:
• `monospace on/off` - تک‌فاصله 𝚖𝚞𝚝𝚑𝚊𝚕
• `fullwidth on/off` - عریض ｍｕｔｈａｌ
• `double_struck on/off` - دوخطی 𝕞𝕦𝕥𝕙𝕒𝕝
• `circled on/off` - دایره‌ای ⓜⓤⓣⓗⓐⓛ
• `inverted on/off` - وارونه ɯnʇɥɐl
• `crypt on/off` - رمزی ₘᵤₜₕₐₗ
• `zalgo on/off` - زالگو (متن با جلوه‌های آشوبناک)

📦 **سبک‌های بلوکی**:
• `box on/off` - متن در کادر
  ┏━━━━━━┓
  ┃ مثال ┃
  ┗━━━━━━┛
• `dotted on/off` - متن با حاشیه نقطه‌ای
  ╭─────╮
  │ مثال │
  ╰─────╯

🔢 **اعداد ویژه**:
• `superscript` - اعداد بالانویس ⁰¹²³⁴⁵⁶⁷⁸⁹
• `subscript` - اعداد زیرنویس ₀₁₂₃₄₅₆₇₈₉

⚙️ **دستورات ترکیبی و مدیریت**:
• `font [نام فونت]` - تغییر فونت فعال به فونت مشخص شده
• `fontlist` - نمایش لیست تمام فونت‌های در دسترس
• `resetfont` - بازگشت به فونت پیش‌فرض
• `combine [فونت1] [فونت2]` - ترکیب دو سبک فونت
• `fontmode [پیش‌فرض/خودکار/دستی]` - تنظیم حالت استفاده از فونت

💡 **ترکیب‌های سبکی پیشنهادی**:
• `bold` + `italic` = __**متن پررنگ کج**__
• `bubble_text` + `rainbow` = رنگین کمان حبابی
• `medieval` + `caps` = قرون وسطایی بزرگ 𝔐𝔘𝔗ℌ𝔄𝔏
• `box` + `monospace` = کادر با فونت تک‌فاصله

📝 **نکات کاربردی**:
• فونت‌های خاص ممکن است در همه کلاینت‌ها درست نمایش داده نشوند
• از `zalgo` با احتیاط استفاده کنید، ممکن است باعث مشکلات نمایشی شود
• ترکیب بیش از 2-3 سبک توصیه نمی‌شود
• فونت‌های عددی مثل `superscript` فقط روی اعداد تأثیر می‌گذارند
""",

        "utils": """
🔧 **راهنمای ابزارهای کاربردی** 🔧

⏰ **زمان و تاریخ**:
• `time on/off` - نمایش ساعت در نام کاربری
• `date` - نمایش تاریخ شمسی و میلادی
• `time now` - نمایش زمان دقیق فعلی در چندین منطقه زمانی
• `set timezone [منطقه]` - تنظیم منطقه زمانی
• `calendar` - نمایش تقویم ماه جاری
• `countdown [رویداد] [تاریخ]` - شمارش معکوس تا رویداد مشخص

🌐 **جستجو و ترجمه**:
• `search [متن]` - جستجو در پیام‌های چت
• `wiki [موضوع]` - جستجو در ویکی‌پدیا
• `ترجمه [متن] [زبان مقصد]` - ترجمه متن به زبان مورد نظر
• `translate [متن] [زبان مبدا] [زبان مقصد]` - ترجمه با زبان‌های مشخص
• `ocr [ریپلای به عکس]` - استخراج متن از تصویر
• `detect lang [متن]` - تشخیص زبان متن

🧮 **ابزارهای محاسباتی**:
• `calc [عبارت]` - ماشین حساب
• `convert [مقدار] [واحد1] to [واحد2]` - تبدیل واحدها
• `currency [مقدار] [ارز1] to [ارز2]` - تبدیل ارز
• `morse [متن]` - تبدیل متن به کد مورس
• `unmorse [کد]` - تبدیل کد مورس به متن
• `binary [متن]` - تبدیل متن به کد باینری
• `hexcode [متن]` - تبدیل متن به کد هگز

🌦️ **آب و هوا و اطلاعات**:
• `weather [شهر]` - نمایش آب و هوا
• `forecast [شهر] [روز]` - پیش‌بینی آب و هوا
• `set weather [کلید API]` - تنظیم کلید API آب و هوا
• `news [موضوع]` - آخرین اخبار در موضوع مشخص
• `corona [کشور]` - آمار کرونا

🎮 **سرگرمی**:
• `dice [تعداد]` - پرتاب تاس
• `flip` - پرتاب سکه
• `random [حداقل] [حداکثر]` - تولید عدد تصادفی
• `poll [سوال] [گزینه1|گزینه2|...]` - ایجاد نظرسنجی
• `joke` - جوک تصادفی
• `quote` - نقل قول تصادفی
• `fact` - حقیقت جالب تصادفی
• `8ball [سوال]` - پاسخ تصادفی به سوال بله/خیر

🎨 **ابزارهای رسانه**:
• `logo [متن] [فونت]` - ساخت لوگو متنی
• `banner [متن] [سبک]` - ساخت بنر تبلیغاتی
• `sticker [ایموجی/متن]` - تبدیل به استیکر
• `color [کد رنگ]` - نمایش اطلاعات رنگ
• `qrcode [متن]` - ساخت کیو‌آر‌کد
• `barcode [متن]` - ساخت بارکد
• `styletext [متن] [سبک]` - متن با سبک‌های زیبا

💡 **نکات مدیریتی**:
• `ping` - بررسی زمان پاسخ‌دهی ربات
• `id` - نمایش شناسه کاربر یا چت
• `info [username]` - اطلاعات کاربر
• `chatinfo` - اطلاعات چت فعلی
• `stats [نام چت/آیدی]` - نمایش آمار پیام‌ها
• `uptime` - نمایش زمان کارکرد ربات
• `system` - اطلاعات سیستم
• `usage` - آمار استفاده از دستورات
• `speedtest` - تست سرعت اینترنت

⚙️ **دستورات سفارشی**:
• `custom command [نام] [پاسخ]` - ایجاد دستور سفارشی
• `commands` - نمایش لیست دستورات سفارشی
• `edit command [نام] [پاسخ جدید]` - ویرایش دستور سفارشی
• `delete command [نام]` - حذف دستور سفارشی
""",

        "admin": """
👑 **راهنمای مدیریت و تنظیمات پیشرفته** 👑

⚙️ **تنظیمات کلی**:
• `set prefix [پیشوند]` - تغییر پیشوند دستورات بات
• `set spam limit [عدد]` - تنظیم محدودیت تعداد اسپم
• `set backup interval [دقیقه]` - تنظیم فاصله زمانی پشتیبان‌گیری خودکار
• `set log level [سطح]` - تنظیم سطح ثبت رویدادها (DEBUG, INFO, WARNING, ERROR)
• `set timezone [منطقه]` - تنظیم منطقه زمانی
• `set auto read [on/off]` - فعال/غیرفعال کردن خواندن خودکار پیام‌ها
• `set auto backup [on/off]` - فعال/غیرفعال کردن پشتیبان‌گیری خودکار

💾 **مدیریت پشتیبان**:
• `backup` - پشتیبان‌گیری دستی از داده‌ها
• `restore` - بازیابی داده‌ها از پشتیبان
• `secure backup on/off` - فعال/غیرفعال کردن رمزنگاری پشتیبان
• `cloud backup on/off` - پشتیبان‌گیری خودکار در پیام‌های ذخیره شده
• `export settings` - استخراج تنظیمات به فایل JSON
• `import settings [فایل]` - وارد کردن تنظیمات از فایل JSON
• `reset settings` - بازنشانی تمام تنظیمات به حالت پیش‌فرض

👥 **مدیریت کاربران**:
• `allow user [آیدی/یوزرنیم]` - اجازه دسترسی به کاربر
• `disallow user [آیدی/یوزرنیم]` - لغو دسترسی کاربر
• `allowed users` - لیست کاربران مجاز
• `set user level [آیدی/یوزرنیم] [سطح]` - تنظیم سطح دسترسی کاربر
• `promote [آیدی/یوزرنیم]` - ارتقای سطح دسترسی کاربر
• `demote [آیدی/یوزرنیم]` - کاهش سطح دسترسی کاربر

🔧 **مدیریت دستورات**:
• `disable command [نام]` - غیرفعال کردن دستور
• `enable command [نام]` - فعال کردن دستور غیرفعال شده
• `disabled commands` - نمایش لیست دستورات غیرفعال
• `limit command [نام] [محدودیت]` - تنظیم محدودیت استفاده از دستور
• `command cooldown [نام] [ثانیه]` - تنظیم زمان انتظار بین اجرای دستور
• `override command [نام] [عملکرد جدید]` - بازنویسی عملکرد دستور

📊 **نظارت و گزارش‌گیری**:
• `logs [تعداد]` - نمایش آخرین رویدادهای ثبت شده
• `stats` - آمار کلی ربات
• `command stats` - آمار استفاده از دستورات
• `chat stats [آیدی/نام]` - آمار چت
• `user stats [آیدی/یوزرنیم]` - آمار کاربر
• `error logs` - نمایش خطاهای ثبت شده
• `performance` - بررسی عملکرد و منابع مصرفی
• `report [پیام]` - ارسال گزارش از مشکل یا پیشنهاد

🌐 **اتصال و شبکه**:
• `proxy on/off` - فعال/غیرفعال کردن پروکسی
• `set proxy [نوع] [آدرس] [پورت]` - تنظیم مشخصات پروکسی
• `ping` - تست وضعیت اتصال
• `speedtest` - تست سرعت اینترنت
• `reconnect` - اتصال مجدد به تلگرام
• `session info` - نمایش اطلاعات نشست فعلی
• `api info` - اطلاعات API تلگرام

⚡ **بهینه‌سازی و عملکرد**:
• `optimize` - بهینه‌سازی عملکرد ربات
• `clean` - پاکسازی حافظه موقت و فایل‌های زائد
• `clear cache` - پاکسازی کش ربات
• `limit memory [مگابایت]` - محدود کردن مصرف حافظه
• `flood mode [حالت]` - تنظیم رفتار در شرایط محدودیت فلود
• `debug on/off` - فعال/غیرفعال کردن حالت اشکال‌زدایی

💡 **نکات مدیریتی**:
• دستورات مدیریتی فقط توسط خود کاربر قابل اجرا هستند
• سطح لاگ DEBUG اطلاعات بیشتری ثبت می‌کند اما حجم لاگ را افزایش می‌دهد
• برای امنیت بیشتر، پشتیبان‌گیری رمزنگاری شده را فعال کنید
• در صورت بروز مشکل عملکرد، حافظه کش را پاک کنید
• پس از تغییر تنظیمات مهم، یک پشتیبان دستی تهیه کنید
"""
    }
    
    if section in help_sections:
        try:
            await event.edit(help_sections[section])
        except Exception as e:
            print_error(f"Error displaying section help: {e}")
            print(help_sections[section].replace("**", "").replace("`", ""))
    else:
        # Show available sections
        sections_text = """
📚 **بخش‌های راهنما**

لطفاً یکی از بخش‌های زیر را برای نمایش راهنمای تخصصی انتخاب کنید:

• `help security` - راهنمای بخش امنیت و محافظت
• `help messages` - راهنمای بخش پیام‌رسانی و مدیریت پیام
• `help filters` - راهنمای بخش فیلترها و مدیریت کلمات
• `help autoresponder` - راهنمای سیستم پاسخ خودکار
• `help fonts` - راهنمای سبک‌های متنی و فونت‌ها
• `help utils` - راهنمای ابزارهای کاربردی
• `help admin` - راهنمای مدیریت و تنظیمات پیشرفته

برای راهنمای کلی، دستور `پنل` را اجرا کنید.
"""
        try:
            await event.edit(sections_text)
        except Exception as e:
            print_error(f"Error displaying sections help: {e}")
            print(sections_text.replace("**", "").replace("`", ""))

async def show_status(client, event):
    """Show enhanced bot status with detailed information"""
    try:
        global start_time # <--- این خط رو به اینجا منتقل کردیم (خط اول داخل try)

        # Measure ping - نام متغیرها رو تغییر دادیم تا با start_time سراسری اشتباه نشه
        start_ping_time = time.time() # <--- تغییر نام
        await client(functions.PingRequest(ping_id=0))
        end_ping_time = time.time() # <--- تغییر نام
        ping = round((end_ping_time - start_ping_time) * 1000, 2) # <--- تغییر نام

        # Get time information
        config = load_config()
        tz = pytz.timezone(config['timezone'])
        now = datetime.now(tz)
        
        # Jalali date for Iran
        j_date = jdatetime.datetime.fromgregorian(datetime=now)
        jalali_date = j_date.strftime('%Y/%m/%d')
        local_time = now.strftime('%H:%M:%S')

        # Calculate uptime - دیگه نیازی به global نیست چون قبلاً تعریف شده
        # global start_time # <--- این خط رو کامنت یا حذف کن
        uptime_seconds = int(time.time() - start_time)
        uptime = str(timedelta(seconds=uptime_seconds))
        
        # Memory usage
        if PSUTIL_AVAILABLE:
            process = psutil.Process(os.getpid())
            memory_usage = f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
            cpu_usage = f"{process.cpu_percent()}%"
            thread_count = process.num_threads()
            disk_usage = f"{psutil.disk_usage('/').percent}%"
        else:
            memory_usage = "N/A"
            cpu_usage = "N/A"
            thread_count = "N/A"
            disk_usage = "N/A"

        # Build status text
        status_text = f"""🤖 **وضعیت ربات**:

⏱️ **پینگ**: `{ping} ms`
⏳ **آپتایم**: `{uptime}`
🕒 **زمان محلی**: `{local_time}`
📅 **تاریخ شمسی**: `{jalali_date}`

🧠 **مصرف منابع**:
💾 حافظه: `{memory_usage}`
⚡ CPU: `{cpu_usage}`
🧵 ترد‌ها: `{thread_count}`
💿 دیسک: `{disk_usage}`

🔧 **تنظیمات**:
🔐 رمزنگاری پشتیبان: {'✅' if config.get('encrypted_backup', False) else '❌'}
💾 پشتیبان‌گیری خودکار: {'✅' if config['auto_backup'] else '❌'}
☁️ پشتیبان‌گیری ابری: {'✅' if config['cloud_backup'] else '❌'}
⏱️ فاصله پشتیبان‌گیری: `{config['backup_interval']} دقیقه`
📌 پیشوند دستورات: `{config.get('bot_prefix', '!')}`
🛡️ سطح فیلتر هوشمند: `{config.get('ai_filter_level', 'low')}`
🌐 پروکسی: {'✅' if config['proxy']['enabled'] else '❌'}
"""
        await event.edit(status_text)
        
    except Exception as e:
        logger.error(f"Error in show_status: {e}")
        await event.edit(f"❌ خطا: {str(e)}")

async def show_chat_stats(client, event, chat_id=None):
    """Display chat statistics with visualizations"""
    try:
        if not chat_id:
            chat_id = str(event.chat_id)
            
        if chat_id not in message_stats:
            await event.edit("❌ آماری برای این چت ثبت نشده است")
            return
            
        stats = message_stats[chat_id]
        
        # Get chat info
        try:
            chat = await client.get_entity(int(chat_id))
            chat_name = chat.title if hasattr(chat, 'title') else f"چت خصوصی {chat_id}"
        except:
            chat_name = f"چت {chat_id}"
            
        # Get top 5 users
        top_users = sorted(stats["users"].items(), key=lambda x: x[1], reverse=True)[:5]
        top_users_text = ""
        for i, (user_id, count) in enumerate(top_users, 1):
            try:
                user = await client.get_entity(int(user_id))
                user_name = utils.get_display_name(user)
            except:
                user_name = f"کاربر {user_id}"
            top_users_text += f"{i}. {user_name}: {count} پیام\n"
            
        # Get top 5 keywords/words
        top_words_dict = stats.get("top_words", {}) or stats.get("keywords", {})
        top_keywords = sorted(top_words_dict.items(), key=lambda x: x[1], reverse=True)[:5]
        keywords_text = "\n".join([f"{i+1}. {word}: {count} بار" for i, (word, count) in enumerate(top_keywords)])
        
        # Most active hours
        hourly_data = stats["hourly"]
        max_hour = hourly_data.index(max(hourly_data))
        
        # Create ASCII chart for hourly activity
        max_hourly = max(hourly_data) if max(hourly_data) > 0 else 1  # Avoid division by zero
        hourly_chart = "\n"
        for h in range(0, 24, 3):  # Group by 3 hours for a more compact chart
            group_sum = sum(hourly_data[h:h+3])
            bar_length = int((group_sum / max_hourly) * 15)
            hourly_chart += f"{h:02d}-{h+2:02d}: {'█' * bar_length} {group_sum}\n"
        
        # Most active day
        days = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
        daily_data = stats["daily"]
        max_day = days[daily_data.index(max(daily_data))]
        
        # Create ASCII chart for daily activity
        max_daily = max(daily_data) if max(daily_data) > 0 else 1  # Avoid division by zero
        daily_chart = "\n"
        for d in range(7):
            bar_length = int((daily_data[d] / max_daily) * 15)
            daily_chart += f"{days[d]}: {'█' * bar_length} {daily_data[d]}\n"
        
        # Calculate additional statistics
        first_message = datetime.fromisoformat(stats.get("first_message", datetime.now().isoformat()))
        last_message = datetime.fromisoformat(stats.get("last_message", datetime.now().isoformat()))
        days_tracked = (last_message - first_message).days or 1  # Avoid division by zero
        
        messages_per_day = stats["total_messages"] / days_tracked
        media_percentage = (stats.get("media_count", 0) / stats["total_messages"]) * 100 if stats["total_messages"] > 0 else 0
        reply_percentage = (stats.get("reply_count", 0) / stats["total_messages"]) * 100 if stats["total_messages"] > 0 else 0
        
        stats_text = f"""
📊 **آمار چت: {chat_name}**

📈 **آمار کلی**:
• تعداد کل پیام‌ها: `{stats['total_messages']}`
• تعداد کاربران فعال: `{len(stats['users'])}`
• میانگین پیام روزانه: `{messages_per_day:.1f}`
• مدیا: `{stats.get('media_count', 0)} ({media_percentage:.1f}%)`
• پاسخ‌ها: `{stats.get('reply_count', 0)} ({reply_percentage:.1f}%)`
• فوروارد‌ها: `{stats.get('forward_count', 0)}`
• ساعت پرتراکم: `{max_hour}:00`
• روز پرتراکم: `{max_day}`

⏱️ **نمودار فعالیت ساعتی**:{hourly_chart}

📅 **نمودار فعالیت روزانه**:{daily_chart}

👥 **کاربران فعال**:
{top_users_text}

🔤 **کلمات پرتکرار**:
{keywords_text}

⏳ **آمار زمانی**:
• اولین پیام ثبت شده: `{first_message.strftime('%Y/%m/%d %H:%M')}`
• آخرین پیام ثبت شده: `{last_message.strftime('%Y/%m/%d %H:%M')}`
• مدت زمان ثبت آمار: `{days_tracked} روز`
"""
        await event.edit(stats_text)
    except Exception as e:
        logger.error(f"Error in show_chat_stats: {e}")
        await event.edit(f"❌ خطا در نمایش آمار: {str(e)}")

# ====================================
# Main Functions
# ====================================

async def main():
    """Main function with enhanced UI and error handling"""
    global start_time
    start_time = time.time()  # Set start_time at the beginning of main
    
    # Check if dependencies are loaded
    if not ALL_DEPENDENCIES_LOADED:
        print_error(f"نصب کتابخانه ضروری {MISSING_DEPENDENCY} ناموفق بود. لطفا آن را با استفاده از دستور زیر نصب کنید:")
        print(f"pip install {MISSING_DEPENDENCY}")
        return
    
    # Print logo and initialize
    print(LOGO)
    print_header("Initializing Telegram Self-Bot")
    
    # Load configuration
    config = load_config()
    print_info(f"Configuration loaded from {CONFIG_FILE}")
    
    # Setup logging
    log_level = getattr(logging, config['log_level'])
    logger = setup_logging(log_level)
    
    # Restore data if available
    if os.path.exists(BACKUP_FILE):
        print_loading("Restoring data from backup")
        if restore_data():
            print_success("Data restored from backup")
        else:
            print_warning("Failed to restore data from backup")
    
    # Initialize client with animated progress
    print_loading("Connecting to Telegram")
    
    # Configure proxy if enabled
    proxy = None
    if config['proxy']['enabled'] and config['proxy']['host'] and config['proxy']['port'] > 0:
        proxy = {
            'proxy_type': config['proxy']['type'],
            'addr': config['proxy']['host'],
            'port': config['proxy']['port'],
            'username': config['proxy']['username'],
            'password': config['proxy']['password'],
        }
        print_info(f"Using {config['proxy']['type']} proxy at {config['proxy']['host']}:{config['proxy']['port']}")
    
    # Configure connection parameters
    connection_retries = config['advanced']['connection_retries']
    auto_reconnect = config['advanced']['auto_reconnect']
    
    # Initialize client with options
    client = TelegramClient(
        config['session_name'], 
        config['api_id'], 
        config['api_hash'],
        proxy=proxy,
        connection_retries=connection_retries,
        auto_reconnect=auto_reconnect,
        retry_delay=1,
        flood_sleep_threshold=config['advanced']['flood_sleep_threshold'],
        device_model=config['advanced']['device_model'],
        system_version=config['advanced']['system_version'],
        app_version=config['advanced']['app_version']
    )
    
    try:
        # Connect to Telegram
        await client.connect()
        print_success("Connected to Telegram")
        
        # Check authorization
        if not await client.is_user_authorized():
            print_header("Authentication Required")
            print("Please enter your phone number (e.g., +989123456789):")
            phone = input(f"{get_theme_color('accent')}> ")
            
            try:
                print_loading("Sending verification code")
                await client.send_code_request(phone)
                print_success("Verification code sent")
                
                print("\nPlease enter the verification code:")
                code = input(f"{get_theme_color('accent')}> ")
                
                print_loading("Verifying code")
                await client.sign_in(phone, code)
                print_success("Verification successful")
                
            except Exception as e:
                if "two-steps verification" in str(e).lower():
                    print_warning("Two-step verification is enabled")
                    print("Please enter your password:")
                    password = input(f"{get_theme_color('accent')}> ")
                    
                    print_loading("Verifying password")
                    await client.sign_in(password=password)
                    print_success("Password verification successful")
                else:
                    print_error(f"Login error: {str(e)}")
                    return
        
        # Successfully logged in
        me = await client.get_me()
        print_success(f"Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or 'No username'})")
        print_info("Self-bot is now active! Type 'پنل' in any chat to see commands.")
        
        # Start background tasks
        asyncio.create_task(update_time(client))
        asyncio.create_task(check_reminders(client))
        asyncio.create_task(auto_backup(client))
        
        if status_rotation_active and status_rotation:
            asyncio.create_task(update_status_rotation(client))
            
        if actions['online']:
            asyncio.create_task(auto_online(client))
        
        # Register signal handlers for clean exit
        def signal_handler(sig, frame):
            global running
            print_warning("\nReceived termination signal, shutting down gracefully...")
            running = False
            # Use asyncio to safely disconnect in the event loop
            future = asyncio.run_coroutine_threadsafe(client.disconnect(), client.loop)
            future.result(5)  # Wait up to 5 seconds for disconnect
            
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, signal_handler)
        
        # ====================================
        # Event Handlers
        # ====================================
        
        # Time-related command handler
        @client.on(events.NewMessage(pattern=r'^time (on|off|now)$'))
        async def time_handler(event):
            global time_enabled
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                action = event.pattern_match.group(1)
                
                if action in ['on', 'off']:
                    # Previous state for undo
                    prev_state = time_enabled
                    
                    time_enabled = (action == 'on')
                    if not time_enabled:
                        await client(functions.account.UpdateProfileRequest(last_name=''))
                    
                    # Add to command history
                    command_history.append(('time', prev_state))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                        
                    await event.edit(f"✅ نمایش ساعت {'فعال' if time_enabled else 'غیرفعال'} شد")
                
                elif action == 'now':
                    # Show current time in multiple time zones
                    config = load_config()
                    local_tz = pytz.timezone(config['timezone'])
                    now = datetime.now(local_tz)
                    
                    # Create time info for multiple timezones
                    time_info = f"⏰ **زمان فعلی**:\n\n"
                    time_info += f"🕒 **{config['timezone']}**: `{now.strftime('%H:%M:%S')}`\n"
                    
                    # Add other common timezones
                    common_timezones = ['UTC', 'Europe/London', 'Europe/Paris', 'America/New_York', 'America/Los_Angeles']
                    for tz_name in common_timezones:
                        tz = pytz.timezone(tz_name)
                        tz_time = now.astimezone(tz)
                        time_info += f"🕒 **{tz_name}**: `{tz_time.strftime('%H:%M:%S')}`\n"
                    
                    # Add Jalali date for Iran
                    j_date = jdatetime.datetime.fromgregorian(datetime=now)
                    jalali_date = j_date.strftime('%Y/%m/%d')
                    time_info += f"\n📅 **تاریخ شمسی**: `{jalali_date}`\n"
                    time_info += f"📅 **تاریخ میلادی**: `{now.strftime('%Y/%m/%d')}`"
                    
                    await event.edit(time_info)
                    
            except Exception as e:
                logger.error(f"Error in time handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # Date command
        @client.on(events.NewMessage(pattern='^date$'))
        async def date_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                config = load_config()
                local_tz = pytz.timezone(config['timezone'])
                now = datetime.now(local_tz)
                
                # Jalali date for Iran
                j_date = jdatetime.datetime.fromgregorian(datetime=now)
                jalali_date = j_date.strftime('%Y/%m/%d')
                jalali_weekday = j_date.strftime('%A')
                
                # Gregorian date
                gregorian_date = now.strftime('%Y/%m/%d')
                gregorian_weekday = now.strftime('%A')
                
                date_info = f"📅 **اطلاعات تاریخ**:\n\n"
                date_info += f"📆 **تاریخ شمسی**: `{jalali_date}`\n"
                date_info += f"📆 **روز هفته (شمسی)**: `{jalali_weekday}`\n\n"
                date_info += f"📆 **تاریخ میلادی**: `{gregorian_date}`\n"
                date_info += f"📆 **روز هفته (میلادی)**: `{gregorian_weekday}`\n\n"
                date_info += f"⏰ **ساعت محلی**: `{now.strftime('%H:%M:%S')}`\n"
                date_info += f"🌐 **منطقه زمانی**: `{config['timezone']}`"
                
                await event.edit(date_info)
                
            except Exception as e:
                logger.error(f"Error in date handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # Enemy-related command handler
        @client.on(events.NewMessage(pattern=r'^insult (on|off)$'))
        async def insult_toggle_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                config = load_config()
                config['enemy_auto_reply'] = (status == 'on')
                save_config(config)
                
                await event.edit(f"✅ پاسخ خودکار به دشمن {'فعال' if config['enemy_auto_reply'] else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in insult toggle handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # Blacklist command
        @client.on(events.NewMessage(pattern=r'^blacklist (.+)$'))
        async def blacklist_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                username_or_id = event.pattern_match.group(1)
                
                try:
                    # Try to get user entity
                    user = await client.get_entity(username_or_id)
                    user_id = str(user.id)
                    user_name = user.first_name
                    
                    # Check if already in enemies list
                    if user_id in enemies:
                        await event.edit(f"❌ کاربر {user_name} از قبل در لیست سیاه قرار دارد")
                        return
                    
                    # Add to enemies set
                    enemies.add(user_id)
                    
                    # Add to command history
                    command_history.append(('enemy_add', user_id))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    # Backup after significant change
                    backup_data()
                    
                    await event.edit(f"✅ کاربر {user_name} به لیست سیاه اضافه شد")
                    
                except ValueError:
                    await event.edit("❌ کاربر یافت نشد. لطفاً آیدی یا یوزرنیم صحیح را وارد کنید")
                except Exception as e:
                    await event.edit(f"❌ خطا در افزودن کاربر به لیست سیاه: {str(e)}")
                    
            except Exception as e:
                logger.error(f"Error in blacklist handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # Text-to-media conversion handlers
        @client.on(events.NewMessage(pattern='^متن به ویس بگو (.+)$'))
        async def voice_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Parse command parts
                parts = event.raw_text.split(maxsplit=4)
                
                # Default parameters
                text = event.pattern_match.group(1)
                lang = 'fa'
                slow = False
                
                # Check for additional parameters
                if len(parts) > 4:
                    text = parts[3]
                    lang = parts[4]
                elif len(parts) > 5:
                    text = parts[3]
                    lang = parts[4]
                    slow = parts[5].lower() == 'slow'
                
                await event.edit("⏳ در حال تبدیل متن به ویس...")
                
                voice_file = await text_to_voice(text, lang, slow)
                if voice_file:
                    await event.delete()
                    await client.send_file(event.chat_id, voice_file)
                    # Don't remove file immediately to avoid issues with sending
                    # Schedule deletion after a short delay
                    asyncio.get_event_loop().call_later(5, lambda: os.remove(voice_file) if os.path.exists(voice_file) else None)
                else:
                    await event.edit("❌ خطا در تبدیل متن به ویس")
            except Exception as e:
                logger.error(f"Error in voice handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^save pic$'))
        async def save_pic_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not event.is_reply:
                    await event.edit("❌ لطفا روی یک عکس ریپلای کنید")
                    return
                    
                replied = await event.get_reply_message()
                
                # Check for any media, not just photo
                if not replied.media:
                    await event.edit("❌ پیام ریپلای شده رسانه ندارد")
                    return
                    
                await event.edit("⏳ در حال ذخیره رسانه...")
                path = await client.download_media(replied.media, file=os.path.join(MEDIA_DIR, f"saved_{int(time.time())}"))
                saved_pics.append(path)
                
                # Add to command history
                command_history.append(('save_pic', path))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after significant change
                backup_data()
                
                # Show more detailed success message
                media_type = "عکس"
                if hasattr(replied.media, 'document'):
                    if replied.document.mime_type:
                        if 'image' in replied.document.mime_type:
                            media_type = "عکس"
                        elif 'video' in replied.document.mime_type:
                            media_type = "ویدیو"
                        elif 'audio' in replied.document.mime_type:
                            media_type = "فایل صوتی"
                        else:
                            media_type = "فایل"
                
                await event.edit(f"✅ {media_type} ذخیره شد (شماره {len(saved_pics)})")
            except Exception as e:
                logger.error(f"Error in save pic handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^show pics$'))
        async def show_pics_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not saved_pics:
                    await event.edit("❌ هیچ رسانه‌ای ذخیره نشده است")
                    return
                
                await event.edit(f"⏳ در حال بارگذاری {len(saved_pics)} رسانه ذخیره شده...")
                
                # Send saved pictures one by one
                success_count = 0
                not_found_count = 0
                
                for i, pic_path in enumerate(saved_pics):
                    if os.path.exists(pic_path):
                        try:
                            await client.send_file(event.chat_id, pic_path, caption=f"رسانه {i+1}/{len(saved_pics)}")
                            success_count += 1
                        except Exception as e:
                            await client.send_message(event.chat_id, f"❌ خطا در ارسال رسانه {i+1}: {str(e)}")
                            not_found_count += 1
                    else:
                        await client.send_message(event.chat_id, f"❌ فایل رسانه {i+1} یافت نشد")
                        not_found_count += 1
                
                status_message = f"✅ {success_count} رسانه نمایش داده شد"
                if not_found_count > 0:
                    status_message += f" ({not_found_count} مورد یافت نشد)"
                    
                await event.edit(status_message)
            except Exception as e:
                logger.error(f"Error in show pics handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^delete pic (\d+)$'))
        async def delete_pic_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                pic_num = int(event.pattern_match.group(1))
                
                if not saved_pics or pic_num <= 0 or pic_num > len(saved_pics):
                    await event.edit("❌ شماره رسانه نامعتبر است")
                    return
                
                # Get path and remove from list
                pic_path = saved_pics[pic_num - 1]
                saved_pics.pop(pic_num - 1)
                
                # Delete file if exists
                if os.path.exists(pic_path):
                    os.remove(pic_path)
                    
                # Backup changes
                backup_data()
                
                await event.edit(f"✅ رسانه شماره {pic_num} حذف شد")
            except Exception as e:
                logger.error(f"Error in delete pic handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^متن به عکس (.+)$'))
        async def img_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Parse command with advanced parameters
                parts = event.raw_text.split(maxsplit=7)
                
                # Default parameters
                text = event.pattern_match.group(1)
                bg_color = 'white'
                text_color = 'black'
                effect = None
                rotate = 0
                
                # Handle multiple parameters if provided
                if len(parts) > 3:
                    text = parts[3]
                if len(parts) > 4:
                    bg_color = parts[4]
                if len(parts) > 5:
                    text_color = parts[5]
                if len(parts) > 6:
                    effect = parts[6]
                if len(parts) > 7:
                    try:
                        rotate = int(parts[7])
                    except ValueError:
                        rotate = 0
                
                await event.edit("⏳ در حال تبدیل متن به عکس...")
                
                img_file = await text_to_image(
                    text, 
                    bg_color=bg_color, 
                    text_color=text_color,
                    effect=effect,
                    rotate=rotate,
                    gradient=(bg_color.lower() == 'gradient'),
                    border=(effect == 'border')
                )
                
                if img_file:
                    await event.delete()
                    await client.send_file(event.chat_id, img_file)
                    # Schedule deletion after a short delay
                    asyncio.get_event_loop().call_later(5, lambda: os.remove(img_file) if os.path.exists(img_file) else None)
                else:
                    await event.edit("❌ خطا در تبدیل متن به عکس")
            except Exception as e:
                logger.error(f"Error in image handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^متن به گیف (.+)$'))
        async def gif_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Parse command with advanced parameters
                parts = event.raw_text.split(maxsplit=6)
                
                # Default parameters
                text = event.pattern_match.group(1)
                effect = 'color'
                bg_color = 'white'
                duration = 500
                
                # Handle multiple parameters if provided
                if len(parts) > 3:
                    text = parts[3]
                if len(parts) > 4:
                    effect = parts[4]
                if len(parts) > 5:
                    bg_color = parts[5]
                if len(parts) > 6:
                    try:
                        duration = int(parts[6])
                    except ValueError:
                        duration = 500
                
                await event.edit("⏳ در حال تبدیل متن به گیف...")
                
                gif_file = await text_to_gif(
                    text, 
                    effects=effect,
                    bg_color=bg_color,
                    duration=duration
                )
                
                if gif_file:
                    await event.delete()
                    await client.send_file(event.chat_id, gif_file)
                    # Schedule deletion after a short delay
                    asyncio.get_event_loop().call_later(5, lambda: os.remove(gif_file) if os.path.exists(gif_file) else None)
                else:
                    await event.edit("❌ خطا در تبدیل متن به گیف")
            except Exception as e:
                logger.error(f"Error in gif handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^qrcode (.+)$'))
        async def qrcode_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Parse command with advanced parameters
                parts = event.raw_text.split(maxsplit=4)
                
                # Default parameters
                text = event.pattern_match.group(1)
                fill_color = "black"
                back_color = "white"
                
                # Handle multiple parameters if provided
                if len(parts) > 2:
                    text = parts[1]
                if len(parts) > 3:
                    fill_color = parts[2]
                if len(parts) > 4:
                    back_color = parts[3]
                
                await event.edit("⏳ در حال ساخت کیو آر کد...")
                
                qr_file = await create_qr_code(
                    text,
                    fill_color=fill_color,
                    back_color=back_color
                )
                
                if qr_file:
                    await event.delete()
                    await client.send_file(event.chat_id, qr_file, caption=f"QR Code for: {truncate_text(text, 50)}")
                    # Schedule deletion after a short delay
                    asyncio.get_event_loop().call_later(5, lambda: os.remove(qr_file) if os.path.exists(qr_file) else None)
                else:
                    await event.edit("❌ خطا در ساخت کیو آر کد")
            except Exception as e:
                logger.error(f"Error in qrcode handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^compress$'))
        async def compress_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not event.is_reply:
                    await event.edit("❌ لطفا روی یک عکس ریپلای کنید")
                    return
                
                replied = await event.get_reply_message()
                
                if not replied.photo and not (replied.document and 'image' in replied.document.mime_type):
                    await event.edit("❌ پیام ریپلای شده عکس نیست")
                    return
                
                await event.edit("⏳ در حال دانلود و فشرده‌سازی عکس...")
                
                # Download the image
                path = await client.download_media(replied.media, file=os.path.join(MEDIA_DIR, f"compress_{int(time.time())}.jpg"))
                
                # Compress the image
                compressed_path = await compress_image(path)
                
                if compressed_path:
                    # Get original and compressed file sizes
                    original_size = os.path.getsize(path)
                    compressed_size = os.path.getsize(compressed_path)
                    
                    # Calculate compression ratio
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    
                    await event.delete()
                    await client.send_file(
                        event.chat_id, 
                        compressed_path,
                        caption=f"🗜️ **فشرده‌سازی تصویر**\n\n• اندازه اصلی: `{original_size / 1024:.1f} KB`\n• اندازه فشرده: `{compressed_size / 1024:.1f} KB`\n• نسبت فشرده‌سازی: `{compression_ratio:.1f}%`"
                    )
                    
                    # Clean up files
                    for file in [path, compressed_path]:
                        if os.path.exists(file):
                            os.remove(file)
                else:
                    await event.edit("❌ خطا در فشرده‌سازی عکس")
                    
                    # Clean up original file
                    if os.path.exists(path):
                        os.remove(path)
            except Exception as e:
                logger.error(f"Error in compress handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^ترجمه (.+?) (.+?)$'))
        async def translate_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Parse command parts
                raw_text = event.raw_text
                if raw_text.count(' ') >= 2:
                    _, text, dest = raw_text.split(maxsplit=2)
                else:
                    text = event.pattern_match.group(1)
                    dest = event.pattern_match.group(2)
                
                await event.edit("⏳ در حال ترجمه متن...")
                
                translated = await translate_text(text, dest)
                
                # Emojis for common languages
                lang_emojis = {
                    'fa': '🇮🇷',
                    'en': '🇬🇧',
                    'ar': '🇸🇦',
                    'fr': '🇫🇷',
                    'de': '🇩🇪',
                    'es': '🇪🇸',
                    'ru': '🇷🇺',
                    'it': '🇮🇹',
                    'zh-cn': '🇨🇳',
                    'ja': '🇯🇵',
                    'ko': '🇰🇷',
                    'tr': '🇹🇷'
                }
                
                # Get emoji for destination language
                lang_emoji = lang_emojis.get(dest.lower(), '🌐')
                
                await event.edit(f"{lang_emoji} **ترجمه به {dest}**:\n\n**اصل متن**:\n{text}\n\n**ترجمه شده**:\n{translated}")
            except Exception as e:
                logger.error(f"Error in translate handler: {e}")
                await event.edit(f"❌ خطا در ترجمه: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^weather (.+)$'))
        async def weather_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                city = event.pattern_match.group(1)
                config = load_config()
                
                if not config.get('weather_api_key'):
                    await event.edit("❌ کلید API آب و هوا تنظیم نشده است. با دستور `set weather [کلید API]` آن را تنظیم کنید")
                    return
                    
                await event.edit(f"⏳ در حال دریافت اطلاعات آب و هوای {city}...")
                
                weather_info = await get_weather(city, config['weather_api_key'])
                await event.edit(weather_info)
            except Exception as e:
                logger.error(f"Error in weather handler: {e}")
                await event.edit(f"❌ خطا در دریافت آب و هوا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set weather (.+)$'))
        async def set_weather_api_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                api_key = event.pattern_match.group(1)
                config = load_config()
                config['weather_api_key'] = api_key
                save_config(config)
                
                await event.edit("✅ کلید API آب و هوا با موفقیت تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set weather api handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^(screenshot|forward|copy|delete|edit|spam|link|mention|ai_filter|raid|privacy|log|join|media) (on|off)$'))
        async def lock_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                command, status = event.raw_text.lower().split()
                chat_id = str(event.chat_id)
                
                # Previous state for undo
                prev_state = chat_id in locked_chats[command]
                
                if status == 'on':
                    locked_chats[command].add(chat_id)
                    
                    # Special handling for raid protection
                    if command == 'raid':
                        # Automatically enable anti-spam, link filtering, and mention filtering for comprehensive protection
                        locked_chats['spam'].add(chat_id)
                        locked_chats['link'].add(chat_id)
                        locked_chats['mention'].add(chat_id)
                        await event.edit(f"✅ محافظت ضد حمله فعال شد (شامل ضد اسپم، فیلتر لینک و منشن)")
                    elif command == 'privacy':
                        # Enable comprehensive privacy protection
                        locked_chats['screenshot'].add(chat_id)
                        locked_chats['forward'].add(chat_id)
                        locked_chats['copy'].add(chat_id)
                        await event.edit(f"✅ حالت حریم خصوصی فعال شد (شامل محافظت اسکرین‌شات، فوروارد و کپی)")
                    else:
                        await event.edit(f"✅ قفل {command} فعال شد")
                else:
                    locked_chats[command].discard(chat_id)
                    
                    # Special handling for raid protection and privacy
                    if command == 'raid':
                        # Ask if user wants to disable all related protections
                        await event.edit(f"✅ محافظت ضد حمله غیرفعال شد. آیا می‌خواهید ضد اسپم، فیلتر لینک و منشن هم غیرفعال شوند؟ (بله/خیر)")
                        
                        # Wait for response
                        response = await client.wait_for_message(
                            message=lambda msg: 
                                msg.chat_id == event.chat_id and 
                                msg.from_id and msg.from_id.user_id == (await client.get_me()).id and
                                msg.text and msg.text.lower() in ['بله', 'آره', 'yes', 'y', 'خیر', 'نه', 'no', 'n'],
                            timeout=30
                        )
                        
                        if response and response.text.lower() in ['بله', 'آره', 'yes', 'y']:
                            locked_chats['spam'].discard(chat_id)
                            locked_chats['link'].discard(chat_id)
                            locked_chats['mention'].discard(chat_id)
                            await event.edit("✅ تمام محافظت‌های مرتبط با ضد حمله غیرفعال شدند")
                        else:
                            await event.edit("✅ فقط محافظت ضد حمله غیرفعال شد. سایر محافظت‌ها همچنان فعال هستند")
                    elif command == 'privacy':
                        # Ask if user wants to disable all related protections
                        await event.edit(f"✅ حالت حریم خصوصی غیرفعال شد. آیا می‌خواهید محافظت اسکرین‌شات، فوروارد و کپی هم غیرفعال شوند؟ (بله/خیر)")
                        
                        # Wait for response
                        response = await client.wait_for_message(
                            message=lambda msg: 
                                msg.chat_id == event.chat_id and 
                                msg.from_id and msg.from_id.user_id == (await client.get_me()).id and
                                msg.text and msg.text.lower() in ['بله', 'آره', 'yes', 'y', 'خیر', 'نه', 'no', 'n'],
                            timeout=30
                        )
                        
                        if response and response.text.lower() in ['بله', 'آره', 'yes', 'y']:
                            locked_chats['screenshot'].discard(chat_id)
                            locked_chats['forward'].discard(chat_id)
                            locked_chats['copy'].discard(chat_id)
                            await event.edit("✅ تمام محافظت‌های مرتبط با حریم خصوصی غیرفعال شدند")
                        else:
                            await event.edit("✅ فقط حالت حریم خصوصی غیرفعال شد. سایر محافظت‌ها همچنان فعال هستند")
                    else:
                        await event.edit(f"✅ قفل {command} غیرفعال شد")
                
                # Add to command history
                command_history.append(('lock', (command, chat_id, prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Backup after significant change
                backup_data()
                    
            except Exception as e:
                logger.error(f"Error in lock handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^lock chat$'))
        async def lock_chat_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                chat_id = str(event.chat_id)
                
                # Enable all protections for this chat
                for protection in locked_chats:
                    locked_chats[protection].add(chat_id)
                
                # Backup after significant change
                backup_data()
                
                await event.edit("🔒 تمام محافظت‌ها برای این چت فعال شدند")
            except Exception as e:
                logger.error(f"Error in lock chat handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^unlock chat$'))
        async def unlock_chat_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                chat_id = str(event.chat_id)
                
                # Disable all protections for this chat
                for protection in locked_chats:
                    locked_chats[protection].discard(chat_id)
                
                # Backup after significant change
                backup_data()
                
                await event.edit("🔓 تمام محافظت‌ها برای این چت غیرفعال شدند")
            except Exception as e:
                logger.error(f"Error in unlock chat handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^theme (.+)$'))
        async def theme_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                global theme
                new_theme = event.pattern_match.group(1).lower()
                
                if new_theme not in themes:
                    await event.edit(f"❌ تم '{new_theme}' یافت نشد. تم‌های موجود: {', '.join(themes.keys())}")
                    return
                    
                # Store previous state for undo
                prev_theme = theme
                
                # Update theme
                theme = new_theme
                
                # Add to command history
                command_history.append(('theme', prev_theme))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ تم به '{new_theme}' تغییر یافت")
            except Exception as e:
                logger.error(f"Error in theme handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^secure backup (on|off)$'))
        async def secure_backup_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                status = event.pattern_match.group(1)
                config = load_config()
                
                if status == 'on' and not ENCRYPTION_AVAILABLE:
                    await event.edit("❌ کتابخانه cryptography برای رمزنگاری پشتیبان نصب نشده است. لطفا با دستور `pip install cryptography` آن را نصب کنید")
                    return
                
                # Previous state for undo
                prev_state = config.get('encrypted_backup', False)
                
                # Update config
                config['encrypted_backup'] = (status == 'on')
                
                if status == 'on' and not config.get('encryption_key'):
                    # Generate new encryption key
                    key = Fernet.generate_key().decode()
                    config['encryption_key'] = key
                    save_config(config)
                    
                    # Show warning to save the key
                    await event.edit(f"✅ پشتیبان‌گیری رمزنگاری شده فعال شد\n\n⚠️ **هشدار**: کلید رمزنگاری زیر را در جای امنی ذخیره کنید. بدون این کلید بازیابی پشتیبان ممکن نخواهد بود!\n\n`{key}`")
                else:
                    save_config(config)
                    await event.edit(f"✅ پشتیبان‌گیری رمزنگاری شده {'فعال' if config['encrypted_backup'] else 'غیرفعال'} شد")
                
                # Add to command history
                command_history.append(('secure_backup', prev_state))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Create a new backup with the updated settings
                if backup_data():
                    logger.info(f"Created new {'encrypted' if config['encrypted_backup'] else 'unencrypted'} backup")
                
            except Exception as e:
                logger.error(f"Error in secure backup handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^status (.+)$'))
        async def status_set_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                await client(functions.account.UpdateProfileRequest(about=status))
                await event.edit("✅ وضعیت (بیو) با موفقیت تنظیم شد")
            except Exception as e:
                logger.error(f"Error in status set handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^add status (.+)$'))
        async def add_status_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                global status_rotation
                status = event.pattern_match.group(1)
                
                if status in status_rotation:
                    await event.edit("❌ این وضعیت قبلاً در لیست چرخشی وجود دارد")
                    return
                    
                status_rotation.append(status)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ وضعیت به لیست چرخشی اضافه شد (تعداد: {len(status_rotation)})")
            except Exception as e:
                logger.error(f"Error in add status handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

@client.on(events.NewMessage(pattern=r'^status rotation (on|off)$'))
async def status_rotation_handler(event):
    try:
        if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
            return
            
        global status_rotation, status_rotation_active # <--- این خط رو اصلاح کن
        status = event.pattern_match.group(1)
        
        if status == 'on' and not status_rotation: # <--- حالا مشکلی نداره
            await event.edit("❌ لیست وضعیت‌های چرخشی خالی است. ابتدا با دستور `add status` وضعیت اضافه کنید")
            return
                    
                # Previous state for undo
                prev_state = status_rotation_active
                
                status_rotation_active = (status == 'on')
                
                # Add to command history
                command_history.append(('status_rotation', prev_state))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Start or stop the rotation task
                if status_rotation_active:
                    asyncio.create_task(update_status_rotation(client))
                    
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ چرخش خودکار وضعیت {'فعال' if status_rotation_active else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in status rotation handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^show status$'))
        async def show_status_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not status_rotation:
                    await event.edit("❌ لیست وضعیت‌های چرخشی خالی است")
                    return
                    
                statuses = "\n".join([f"{i+1}. {status}" for i, status in enumerate(status_rotation)])
                await event.edit(f"📋 **لیست وضعیت‌های چرخشی**:\n\n{statuses}\n\n🔄 وضعیت چرخش: {'✅ فعال' if status_rotation_active else '❌ غیرفعال'}")
            except Exception as e:
                logger.error(f"Error in show status handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^clear status$'))
        async def clear_status_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                global status_rotation, status_rotation_active
                
                # Store for undo
                prev_statuses = status_rotation.copy()
                prev_active = status_rotation_active
                
                # Clear the statuses
                status_rotation = []
                status_rotation_active = False
                
                # Add to command history
                command_history.append(('clear_status', (prev_statuses, prev_active)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Backup after change
                backup_data()
                
                await event.edit("✅ لیست وضعیت‌های چرخشی پاک شد")
            except Exception as e:
                logger.error(f"Error in clear status handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^cloud backup (on|off)$'))
        async def cloud_backup_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                config = load_config()
                
                # Previous state for undo
                prev_state = config['cloud_backup']
                
                config['cloud_backup'] = (status == 'on')
                save_config(config)
                
                # Add to command history
                command_history.append(('cloud_backup', prev_state))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                if status == 'on':
                    # Perform an immediate backup to test
                    await event.edit("⏳ در حال آزمایش پشتیبان‌گیری ابری...")
                    if await cloud_backup(client):
                        await event.edit("✅ پشتیبان‌گیری ابری فعال شد و با موفقیت آزمایش شد")
                    else:
                        config['cloud_backup'] = False
                        save_config(config)
                        await event.edit("❌ خطا در پشتیبان‌گیری ابری. این قابلیت غیرفعال شد")
                else:
                    await event.edit("✅ پشتیبان‌گیری ابری غیرفعال شد")
            except Exception as e:
                logger.error(f"Error in cloud backup handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^translate (on|off)$'))
        async def translate_toggle_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                
                # Store previous state for undo
                prev_state = actions['translate']
                
                # Update state
                actions['translate'] = (status == 'on')
                
                # Add to command history
                command_history.append(('action', ('translate', prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ ترجمه خودکار {'فعال' if actions['translate'] else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in translate toggle handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set translate (.+)$'))
        async def set_translate_lang_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                lang = event.pattern_match.group(1)
                config = load_config()
                
                # Store previous state for undo
                prev_lang = config['default_translate_lang']
                
                # Update config
                config['default_translate_lang'] = lang
                save_config(config)
                
                # Add to command history
                command_history.append(('translate_lang', prev_lang))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ زبان پیش‌فرض ترجمه به '{lang}' تغییر یافت")
            except Exception as e:
                logger.error(f"Error in set translate language handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^stats (on|off)$'))
        async def stats_toggle_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                
                # Store previous state for undo
                prev_state = actions['stats']
                
                # Update state
                actions['stats'] = (status == 'on')
                
                # Add to command history
                command_history.append(('action', ('stats', prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ ثبت آمار پیام‌ها {'فعال' if actions['stats'] else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in stats toggle handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^stats$'))
        async def show_chat_stats_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await show_chat_stats(client, event)
            except Exception as e:
                logger.error(f"Error in show chat stats handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^stats (.+)$'))
        async def show_specific_chat_stats_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                chat_id = event.pattern_match.group(1)
                try:
                    # Try to convert to integer ID
                    chat_id = str(int(chat_id))
                except:
                    # It might be a username or chat name
                    try:
                        chat = await client.get_entity(chat_id)
                        chat_id = str(chat.id)
                    except:
                        await event.edit(f"❌ چت '{chat_id}' یافت نشد")
                        return
                
                await show_chat_stats(client, event, chat_id)
            except Exception as e:
                logger.error(f"Error in show specific chat stats handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^welcome (.+)$'))
        async def set_welcome_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                message = event.pattern_match.group(1)
                chat_id = str(event.chat_id)
                
                # Store previous welcome message for undo
                prev_welcome = welcome_messages.get(chat_id, None)
                
                # Update welcome message
                welcome_messages[chat_id] = message
                
                # Add to command history
                command_history.append(('welcome', (chat_id, prev_welcome)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                # Backup after change
                backup_data()
                
                await event.edit("✅ پیام خوش‌آمدگویی با موفقیت تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set welcome handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^show welcome$'))
        async def show_welcome_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                chat_id = str(event.chat_id)
                
                if chat_id not in welcome_messages:
                    await event.edit("❌ پیام خوش‌آمدگویی برای این چت تنظیم نشده است")
                    return
                    
                welcome = welcome_messages[chat_id]
                await event.edit(f"📝 **پیام خوش‌آمدگویی چت فعلی**:\n\n{welcome}")
            except Exception as e:
                logger.error(f"Error in show welcome handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^welcome list$'))
        async def welcome_list_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not welcome_messages:
                    await event.edit("❌ هیچ پیام خوش‌آمدگویی تنظیم نشده است")
                    return
                
                welcome_list = "📋 **لیست پیام‌های خوش‌آمدگویی**:\n\n"
                
                for i, (chat_id, message) in enumerate(welcome_messages.items(), 1):
                    try:
                        # Try to get chat info
                        chat = await client.get_entity(int(chat_id))
                        chat_name = chat.title if hasattr(chat, 'title') else f"چت خصوصی {chat_id}"
                    except:
                        chat_name = f"چت {chat_id}"
                    
                    # Truncate message if too long
                    short_message = truncate_text(message, 50)
                    
                    welcome_list += f"{i}. **{chat_name}**: {short_message}\n\n"
                
                await event.edit(welcome_list)
            except Exception as e:
                logger.error(f"Error in welcome list handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^delete welcome$'))
        async def delete_welcome_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                chat_id = str(event.chat_id)
                
                if chat_id not in welcome_messages:
                    await event.edit("❌ پیام خوش‌آمدگویی برای این چت تنظیم نشده است")
                    return
                
                # Store for undo
                prev_welcome = welcome_messages[chat_id]
                
                # Delete welcome message
                del welcome_messages[chat_id]
                
                # Add to command history
                command_history.append(('welcome', (chat_id, prev_welcome)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit("✅ پیام خوش‌آمدگویی با موفقیت حذف شد")
            except Exception as e:
                logger.error(f"Error in delete welcome handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^help$'))
        async def help_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Show available help sections
                sections_text = """
📚 **بخش‌های راهنما**

لطفاً یکی از بخش‌های زیر را برای نمایش راهنمای تخصصی انتخاب کنید:

• `help security` - راهنمای بخش امنیت و محافظت
• `help messages` - راهنمای بخش پیام‌رسانی و مدیریت پیام
• `help filters` - راهنمای بخش فیلترها و مدیریت کلمات
• `help autoresponder` - راهنمای سیستم پاسخ خودکار
• `help fonts` - راهنمای سبک‌های متنی و فونت‌ها
• `help utils` - راهنمای ابزارهای کاربردی
• `help admin` - راهنمای مدیریت و تنظیمات پیشرفته

برای راهنمای کلی، دستور `پنل` را اجرا کنید.
"""
                await event.edit(sections_text)
            except Exception as e:
                logger.error(f"Error in help handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^help (.+)$'))
        async def section_help_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                section = event.pattern_match.group(1)
                await show_section_help(client, event, section)
            except Exception as e:
                logger.error(f"Error in section help handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='پنل'))
        async def panel_handler(event):
            try:
                if not event.from_id:
                    return
                    
                if event.from_id.user_id == (await client.get_me()).id:
                    await show_help_menu(client, event)
            except Exception as e:
                logger.error(f"Error in panel handler: {e}")
                pass

        @client.on(events.NewMessage(pattern='^ping$'))
        async def ping_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Measure ping
                start = time.time()
                message = await event.edit("⏱️ Pinging...")
                end = time.time()
                
                # Calculate round-trip time
                ping_ms = round((end - start) * 1000, 2)
                
                # Get server ping
                server_start = time.time()
                await client(functions.PingRequest(ping_id=0))
                server_end = time.time()
                server_ping_ms = round((server_end - server_start) * 1000, 2)
                
                # Create ping information
                ping_info = f"🏓 **Pong!**\n\n"
                ping_info += f"• **Round-trip**: `{ping_ms} ms`\n"
                ping_info += f"• **Server ping**: `{server_ping_ms} ms`\n"
                
                # Add latency indicator
                if ping_ms < 150:
                    quality = "Excellent"
                    indicator = "🟢"
                elif ping_ms < 300:
                    quality = "Good"
                    indicator = "🟡"
                elif ping_ms < 500:
                    quality = "Fair"
                    indicator = "🟠"
                else:
                    quality = "Poor"
                    indicator = "🔴"
                
                ping_info += f"• **Quality**: `{quality}` {indicator}"
                
                await message.edit(ping_info)
            except Exception as e:
                logger.error(f"Error in ping handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^id$'))
        async def id_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Get chat information
                chat = await event.get_chat()
                
                if event.is_reply:
                    # Get replied message info
                    replied_msg = await event.get_reply_message()
                    sender = await replied_msg.get_sender()
                    
                    if sender:
                        sender_id = sender.id
                        sender_name = utils.get_display_name(sender)
                        sender_username = f"@{sender.username}" if hasattr(sender, 'username') and sender.username else "No username"
                        
                        # Build the response for replied message
                        id_info = f"👤 **User Information**:\n\n"
                        id_info += f"• **Name**: `{sender_name}`\n"
                        id_info += f"• **User ID**: `{sender_id}`\n"
                        id_info += f"• **Username**: `{sender_username}`\n"
                        
                        # Add user type information
                        if hasattr(sender, 'bot') and sender.bot:
                            id_info += f"• **Type**: `Bot`\n"
                        elif hasattr(sender, 'scam') and sender.scam:
                            id_info += f"• **Type**: `Scam Account` ⚠️\n"
                        elif hasattr(sender, 'verified') and sender.verified:
                            id_info += f"• **Type**: `Verified Account` ✓\n"
                        else:
                            id_info += f"• **Type**: `Regular User`\n"
                    else:
                        id_info = "❌ Couldn't get information about the sender"
                        
                    # Add chat information
                    id_info += f"\n💬 **Chat Information**:\n\n"
                    id_info += f"• **Chat ID**: `{chat.id}`\n"
                    
                    if hasattr(chat, 'title'):
                        id_info += f"• **Chat Title**: `{chat.title}`\n"
                    
                    # Add chat type information
                    if isinstance(chat, types.Channel):
                        if chat.broadcast:
                            id_info += f"• **Chat Type**: `Channel`\n"
                        else:
                            id_info += f"• **Chat Type**: `Supergroup`\n"
                    elif isinstance(chat, types.Chat):
                        id_info += f"• **Chat Type**: `Group`\n"
                    else:
                        id_info += f"• **Chat Type**: `Private Chat`\n"
                else:
                    # No reply, just show chat information
                    id_info = f"💬 **Chat Information**:\n\n"
                    id_info += f"• **Chat ID**: `{chat.id}`\n"
                    
                    if hasattr(chat, 'title'):
                        id_info += f"• **Chat Title**: `{chat.title}`\n"
                    
                    # Add chat type and additional info
                    if isinstance(chat, types.Channel):
                        if chat.broadcast:
                            id_info += f"• **Chat Type**: `Channel`\n"
                            
                            # Get subscribers count if available
                            try:
                                full_chat = await client(GetFullChannelRequest(chat))
                                if hasattr(full_chat.full_chat, 'participants_count'):
                                    id_info += f"• **Subscribers**: `{full_chat.full_chat.participants_count}`\n"
                            except:
                                pass
                        else:
                            id_info += f"• **Chat Type**: `Supergroup`\n"
                            
                            # Get members count if available
                            try:
                                full_chat = await client(GetFullChannelRequest(chat))
                                if hasattr(full_chat.full_chat, 'participants_count'):
                                    id_info += f"• **Members**: `{full_chat.full_chat.participants_count}`\n"
                            except:
                                pass
                    elif isinstance(chat, types.Chat):
                        id_info += f"• **Chat Type**: `Group`\n"
                        id_info += f"• **Members**: `{chat.participants_count}`\n"
                    else:
                        id_info += f"• **Chat Type**: `Private Chat`\n"
                        
                        # Get user information for private chat
                        user = await event.get_chat()
                        if user:
                            id_info += f"• **User ID**: `{user.id}`\n"
                            id_info += f"• **Name**: `{utils.get_display_name(user)}`\n"
                            id_info += f"• **Username**: `{f'@{user.username}' if hasattr(user, 'username') and user.username else 'No username'}`\n"
                
                # Add your own user ID for reference
                me = await client.get_me()
                id_info += f"\n👤 **Your ID**: `{me.id}`"
                
                await event.edit(id_info)
            except Exception as e:
                logger.error(f"Error in id handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^calc (.+)$'))
        async def calc_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                expression = event.pattern_match.group(1)
                
                # Sanitize expression to prevent code execution
                if any(keyword in expression.lower() for keyword in ['import', 'eval', 'exec', 'compile', 'open', 'os', 'sys', 'subprocess']):
                    await event.edit("❌ عبارت غیرمجاز. از عملگرهای ریاضی ساده استفاده کنید")
                    return
                
                # Only allow basic math operators and functions
                allowed_chars = set('0123456789.+-*/()% ^<>=!,abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                if not all(c in allowed_chars for c in expression):
                    await event.edit("❌ کاراکترهای غیرمجاز. از عملگرهای ریاضی ساده استفاده کنید")
                    return
                
                # Replace common operations with Python equivalents
                expression = expression.replace('^', '**')  # exponentiation
                
                # Define allowed math functions
                math_funcs = {
                    'sin': 'math.sin',
                    'cos': 'math.cos', 
                    'tan': 'math.tan',
                    'sqrt': 'math.sqrt',
                    'abs': 'abs',
                    'log': 'math.log',
                    'log10': 'math.log10',
                    'exp': 'math.exp',
                    'pi': 'math.pi',
                    'e': 'math.e',
                    'ceil': 'math.ceil',
                    'floor': 'math.floor',
                    'round': 'round'
                }
                
                # Apply substitutions for math functions
                for func, replacement in math_funcs.items():
                    if func in expression:
                        expression = expression.replace(func, replacement)
                
                try:
                    # Import math but in a controlled way
                    import math
                    
                    # Use eval but with limited scope
                    result = eval(expression, {"__builtins__": None}, {"math": math, "abs": abs, "round": round})
                    
                    # Format the result with good precision
                    if isinstance(result, float):
                        formatted_result = f"{result:.6f}".rstrip('0').rstrip('.') if '.' in f"{result:.6f}" else f"{result}"
                    else:
                        formatted_result = str(result)
                    
                    await event.edit(f"🧮 **محاسبه**:\n\n• **ورودی**: `{expression.replace('**', '^')}`\n• **نتیجه**: `{formatted_result}`")
                except Exception as e:
                    await event.edit(f"❌ خطا در محاسبه: {str(e)}")
            except Exception as e:
                logger.error(f"Error in calc handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^logo (.+)$'))
        async def logo_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Parse command with parameters
                parts = event.raw_text.split(maxsplit=2)
                
                # Default parameters
                text = event.pattern_match.group(1)
                font = "slant"
                
                # Check for font specification
                if len(parts) > 2:
                    text = parts[1]
                    font = parts[2]
                
                await event.edit("⏳ در حال ایجاد لوگو...")
                
                # Create ASCII art
                try:
                    fig = pyfiglet.Figlet(font=font)
                    ascii_art = fig.renderText(text)
                    
                    # Format the logo
                    logo_text = f"```\n{ascii_art}\n```"
                    
                    await event.edit(logo_text)
                except Exception as e:
                    # Try with default font if specified font fails
                    try:
                        fig = pyfiglet.Figlet(font="slant")
                        ascii_art = fig.renderText(text)
                        logo_text = f"```\n{ascii_art}\n```"
                        await event.edit(logo_text + f"\n\n❌ فونت '{font}' یافت نشد. از فونت پیش‌فرض استفاده شد.")
                    except:
                        await event.edit(f"❌ خطا در ایجاد لوگو: {str(e)}")
            except Exception as e:
                logger.error(f"Error in logo handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^custom command (.+?) (.+)$'))
        async def custom_command_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                command_name = event.pattern_match.group(1)
                command_response = event.pattern_match.group(2)
                
                # Check if command already exists
                if command_name in custom_commands:
                    await event.edit(f"❌ دستور '{command_name}' از قبل وجود دارد. برای ویرایش آن از 'edit command' استفاده کنید")
                    return
                
                # Add to custom commands
                custom_commands[command_name] = command_response
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ دستور سفارشی '{command_name}' با موفقیت اضافه شد")
            except Exception as e:
                logger.error(f"Error in custom command handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^commands$'))
        async def commands_list_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not custom_commands:
                    await event.edit("❌ هیچ دستور سفارشی تعریف نشده است")
                    return
                
                commands_text = "📋 **لیست دستورات سفارشی**:\n\n"
                
                for i, (command, response) in enumerate(custom_commands.items(), 1):
                    # Truncate long responses
                    short_response = truncate_text(response, 50)
                    commands_text += f"{i}. `{command}`: {short_response}\n\n"
                
                await event.edit(commands_text)
            except Exception as e:
                logger.error(f"Error in commands list handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^edit command (.+?) (.+)$'))
        async def edit_command_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                command_name = event.pattern_match.group(1)
                new_response = event.pattern_match.group(2)
                
                if command_name not in custom_commands:
                    await event.edit(f"❌ دستور '{command_name}' وجود ندارد")
                    return
                
                # Store previous response for undo
                prev_response = custom_commands[command_name]
                
                # Update command
                custom_commands[command_name] = new_response
                
                # Add to command history
                command_history.append(('edit_command', (command_name, prev_response)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ دستور '{command_name}' با موفقیت ویرایش شد")
            except Exception as e:
                logger.error(f"Error in edit command handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^delete command (.+)$'))
        async def delete_command_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                command_name = event.pattern_match.group(1)
                
                if command_name not in custom_commands:
                    await event.edit(f"❌ دستور '{command_name}' وجود ندارد")
                    return
                
                # Store for undo
                prev_response = custom_commands[command_name]
                
                # Delete command
                del custom_commands[command_name]
                
                # Add to command history
                command_history.append(('delete_command', (command_name, prev_response)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ دستور '{command_name}' با موفقیت حذف شد")
            except Exception as e:
                logger.error(f"Error in delete command handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^encrypt (.+)$'))
        async def encrypt_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not ENCRYPTION_AVAILABLE:
                    await event.edit("❌ کتابخانه cryptography برای رمزنگاری نصب نشده است. لطفا با دستور `pip install cryptography` آن را نصب کنید")
                    return
                
                text = event.pattern_match.group(1)
                
                # Generate a key or use existing one
                config = load_config()
                if not config.get('encryption_key'):
                    key = Fernet.generate_key().decode()
                    config['encryption_key'] = key
                    save_config(config)
                else:
                    key = config['encryption_key']
                
                # Encrypt the text
                cipher = Fernet(key.encode())
                encrypted_text = cipher.encrypt(text.encode()).decode()
                
                await event.edit(f"🔒 **متن رمزنگاری شده**:\n\n`{encrypted_text}`")
            except Exception as e:
                logger.error(f"Error in encrypt handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^decrypt (.+)$'))
        async def decrypt_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not ENCRYPTION_AVAILABLE:
                    await event.edit("❌ کتابخانه cryptography برای رمزگشایی نصب نشده است. لط فا با دستور `pip install cryptography` آن را نصب کنید")
                    return
                
                encrypted_text = event.pattern_match.group(1)
                
                # Get the key
                config = load_config()
                if not config.get('encryption_key'):
                    await event.edit("❌ کلید رمزنگاری یافت نشد. ابتدا با دستور `encrypt` یک متن را رمزنگاری کنید")
                    return
                
                key = config['encryption_key']
                
                # Decrypt the text
                try:
                    cipher = Fernet(key.encode())
                    decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
                    
                    await event.edit(f"🔓 **متن رمزگشایی شده**:\n\n`{decrypted_text}`")
                except Exception as e:
                    await event.edit(f"❌ خطا در رمزگشایی: متن نامعتبر یا کلید نادرست")
            except Exception as e:
                logger.error(f"Error in decrypt handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^password(?: (\d+))?$'))
        async def password_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Get length parameter with default value
                length_str = event.pattern_match.group(1)
                length = int(length_str) if length_str else 16
                
                # Set reasonable limits
                if length < 8:
                    length = 8
                elif length > 64:
                    length = 64
                
                # Define character sets
                lowercase = string.ascii_lowercase
                uppercase = string.ascii_uppercase
                digits = string.digits
                symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
                
                # Ensure at least one character from each set
                password = [
                    random.choice(lowercase),
                    random.choice(uppercase),
                    random.choice(digits),
                    random.choice(symbols)
                ]
                
                # Fill the rest of the password
                all_chars = lowercase + uppercase + digits + symbols
                password.extend(random.choice(all_chars) for _ in range(length - 4))
                
                # Shuffle the password characters
                random.shuffle(password)
                
                # Convert list to string
                password_str = ''.join(password)
                
                # Calculate password strength
                strength = 0
                has_lower = any(c in lowercase for c in password_str)
                has_upper = any(c in uppercase for c in password_str)
                has_digit = any(c in digits for c in password_str)
                has_symbol = any(c in symbols for c in password_str)
                
                if has_lower:
                    strength += 1
                if has_upper:
                    strength += 1
                if has_digit:
                    strength += 1
                if has_symbol:
                    strength += 1
                
                if length >= 12:
                    strength += 1
                
                # Determine strength description
                if strength == 5:
                    strength_desc = "بسیار قوی"
                    strength_emoji = "🟢🟢🟢🟢🟢"
                elif strength == 4:
                    strength_desc = "قوی"
                    strength_emoji = "🟢🟢🟢🟢⚪"
                elif strength == 3:
                    strength_desc = "متوسط"
                    strength_emoji = "🟢🟢🟢⚪⚪"
                elif strength == 2:
                    strength_desc = "ضعیف"
                    strength_emoji = "🟢🟢⚪⚪⚪"
                else:
                    strength_desc = "بسیار ضعیف"
                    strength_emoji = "🟢⚪⚪⚪⚪"
                
                await event.edit(f"🔑 **رمز عبور تصادفی ایجاد شد**:\n\n`{password_str}`\n\n" +
                                 f"📏 **طول**: `{length}`\n" +
                                 f"💪 **قدرت**: `{strength_desc}` {strength_emoji}\n\n" +
                                 f"⚠️ این پیام پس از 30 ثانیه حذف خواهد شد برای حفظ امنیت")
                
                # Delete the message after 30 seconds for security
                await asyncio.sleep(30)
                await event.delete()
            except Exception as e:
                logger.error(f"Error in password handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^hash (.+)$'))
        async def hash_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                text = event.pattern_match.group(1)
                
                # Generate different types of hashes
                md5_hash = hashlib.md5(text.encode()).hexdigest()
                sha1_hash = hashlib.sha1(text.encode()).hexdigest()
                sha256_hash = hashlib.sha256(text.encode()).hexdigest()
                sha512_hash = hashlib.sha512(text.encode()).hexdigest()
                
                # Format the output
                hash_output = f"🔐 **Hash values for**: `{text}`\n\n"
                hash_output += f"• **MD5**: `{md5_hash}`\n"
                hash_output += f"• **SHA1**: `{sha1_hash}`\n"
                hash_output += f"• **SHA256**: `{sha256_hash}`\n"
                hash_output += f"• **SHA512**: `{sha512_hash}`"
                
                await event.edit(hash_output)
            except Exception as e:
                logger.error(f"Error in hash handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^(typing|online|reaction|read|reply|stats|translate|silent|invisible|privacy|security) (on|off)$'))
        async def toggle_actions_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                action, status = event.raw_text.lower().split()
                
                if action not in actions:
                    await event.edit(f"❌ عملکرد '{action}' یافت نشد")
                    return
                
                # Previous state for undo
                prev_state = actions[action]
                
                # Update action state
                actions[action] = (status == 'on')
                
                # Add to command history
                command_history.append(('action', (action, prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Special handling for certain actions
                if action == 'online' and actions[action]:
                    asyncio.create_task(auto_online(client))
                elif action == 'privacy' and actions[action]:
                    # Enable privacy settings
                    await client(functions.account.SetPrivacyRequest(
                        key=types.InputPrivacyKeyStatusTimestamp(),
                        rules=[types.InputPrivacyValueDisallowAll()]
                    ))
                    await client(functions.account.SetPrivacyRequest(
                        key=types.InputPrivacyKeyLastSeen(),
                        rules=[types.InputPrivacyValueDisallowAll()]
                    ))
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ عملکرد {action} {'فعال' if actions[action] else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in toggle actions handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^block word (.+)$'))
        async def block_word_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                word = event.pattern_match.group(1).lower()
                
                if word in blocked_words:
                    await event.edit(f"❌ کلمه '{word}' قبلاً مسدود شده است")
                    return
                
                # Add to blocked words
                blocked_words.append(word)
                
                # Add to command history
                command_history.append(('block_word', word))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ کلمه '{word}' مسدود شد")
            except Exception as e:
                logger.error(f"Error in block word handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^unblock word (.+)$'))
        async def unblock_word_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                word = event.pattern_match.group(1).lower()
                
                if word not in blocked_words:
                    await event.edit(f"❌ کلمه '{word}' در لیست مسدود شده‌ها نیست")
                    return
                
                # Remove from blocked words
                blocked_words.remove(word)
                
                # Add to command history
                command_history.append(('unblock_word', word))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ کلمه '{word}' از لیست مسدود شده‌ها حذف شد")
            except Exception as e:
                logger.error(f"Error in unblock word handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^block list$'))
        async def block_list_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not blocked_words:
                    await event.edit("❌ لیست کلمات مسدود شده خالی است")
                    return
                
                block_list = "📋 **لیست کلمات مسدود شده**:\n\n"
                
                for i, word in enumerate(blocked_words, 1):
                    block_list += f"{i}. `{word}`\n"
                
                await event.edit(block_list)
            except Exception as e:
                logger.error(f"Error in block list handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^save$'))
        async def save_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not event.is_reply:
                    await event.edit("❌ لطفا روی یک پیام ریپلای کنید")
                    return
                
                replied = await event.get_reply_message()
                
                if not replied.text and not replied.caption:
                    await event.edit("❌ پیام ریپلای شده متن ندارد")
                    return
                
                # Get message text or caption
                message_text = replied.text or replied.caption
                
                # Add to saved messages
                saved_messages.append(message_text)
                
                # Add to command history
                command_history.append(('save_msg', None))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ پیام ذخیره شد (شماره {len(saved_messages)})")
            except Exception as e:
                logger.error(f"Error in save handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^saved$'))
        async def saved_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not saved_messages:
                    await event.edit("❌ هیچ پیامی ذخیره نشده است")
                    return
                
                saved_text = "📋 **لیست پیام‌های ذخیره شده**:\n\n"
                
                for i, msg in enumerate(saved_messages, 1):
                    # Truncate long messages
                    short_msg = truncate_text(msg, 100)
                    saved_text += f"{i}. {short_msg}\n\n"
                
                # Split long messages if needed
                if len(saved_text) > 4000:
                    chunks = [saved_text[i:i+4000] for i in range(0, len(saved_text), 4000)]
                    for i, chunk in enumerate(chunks):
                        if i == 0:
                            await event.edit(f"{chunk}\n\n(بخش {i+1}/{len(chunks)})")
                        else:
                            await client.send_message(event.chat_id, f"{chunk}\n\n(بخش {i+1}/{len(chunks)})")
                else:
                    await event.edit(saved_text)
            except Exception as e:
                logger.error(f"Error in saved handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^delete saved (\d+)$'))
        async def delete_saved_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                index = int(event.pattern_match.group(1))
                
                if not saved_messages or index <= 0 or index > len(saved_messages):
                    await event.edit("❌ شماره پیام نامعتبر است")
                    return
                
                # Store for undo
                deleted_msg = saved_messages[index - 1]
                
                # Remove from saved messages
                del saved_messages[index - 1]
                
                # Add to command history
                command_history.append(('delete_saved', (index - 1, deleted_msg)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ پیام شماره {index} حذف شد")
            except Exception as e:
                logger.error(f"Error in delete saved handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^auto react(?: (.+))?$'))
        async def auto_react_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Get emoji parameter
                param = event.pattern_match.group(1)
                
                if not param:
                    # Show current auto reactions
                    if not auto_reactions:
                        await event.edit("❌ هیچ ری‌اکشن خودکاری تنظیم نشده است")
                    else:
                        react_text = "📋 **لیست ری‌اکشن‌های خودکار**:\n\n"
                        
                        for target, emojis in auto_reactions.items():
                            try:
                                if target.isdigit():
                                    try:
                                        entity = await client.get_entity(int(target))
                                        target_name = utils.get_display_name(entity)
                                    except:
                                        target_name = f"چت/کاربر {target}"
                                else:
                                    target_name = "همه پیام‌ها"
                                
                                emoji_list = " ".join(emojis)
                                react_text += f"• **{target_name}**: {emoji_list}\n"
                            except Exception as e:
                                react_text += f"• **{target}**: {' '.join(emojis)} (خطا: {str(e)})\n"
                        
                        await event.edit(react_text)
                    return
                
                parts = param.split()
                
                # Check if first part could be a target (chat/user)
                if len(parts) >= 2:
                    # Try to get target entity
                    target = parts[0]
                    emoji = parts[1]
                    
                    try:
                        entity = await client.get_entity(target)
                        target_id = str(entity.id)
                        target_name = utils.get_display_name(entity)
                        
                        # Store reaction for this target
                        if target_id not in auto_reactions:
                            auto_reactions[target_id] = []
                        
                        auto_reactions[target_id].append(emoji)
                        
                        # Backup after change
                        backup_data()
                        
                        await event.edit(f"✅ ری‌اکشن خودکار {emoji} برای {target_name} تنظیم شد")
                    except:
                        # If target is not found, assume it's just an emoji for global auto-reaction
                        if "all" not in auto_reactions:
                            auto_reactions["all"] = []
                        
                        auto_reactions["all"].append(param)
                        
                        # Backup after change
                        backup_data()
                        
                        await event.edit(f"✅ ری‌اکشن خودکار {param} برای همه پیام‌ها تنظیم شد")
                else:
                    # Set global auto-reaction
                    if "all" not in auto_reactions:
                        auto_reactions["all"] = []
                    
                    auto_reactions["all"].append(param)
                    
                    # Backup after change
                    backup_data()
                    
                    await event.edit(f"✅ ری‌اکشن خودکار {param} برای همه پیام‌ها تنظیم شد")
            except Exception as e:
                logger.error(f"Error in auto react handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^remove react(?: (.+))?$'))
        async def remove_react_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                # Get target parameter
                target = event.pattern_match.group(1)
                
                if not target:
                    # Remove all auto reactions
                    prev_reactions = auto_reactions.copy()
                    auto_reactions.clear()
                    
                    # Add to command history
                    command_history.append(('clear_reactions', prev_reactions))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    # Backup after change
                    backup_data()
                    
                    await event.edit("✅ تمام ری‌اکشن‌های خودکار حذف شدند")
                    return
                
                # Try to get target as entity ID
                try:
                    entity = await client.get_entity(target)
                    target_id = str(entity.id)
                    target_name = utils.get_display_name(entity)
                    
                    if target_id in auto_reactions:
                        prev_reactions = auto_reactions[target_id].copy()
                        del auto_reactions[target_id]
                        
                        # Add to command history
                        command_history.append(('remove_reaction', (target_id, prev_reactions)))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                        
                        # Backup after change
                        backup_data()
                        
                        await event.edit(f"✅ ری‌اکشن‌های خودکار برای {target_name} حذف شدند")
                    else:
                        await event.edit(f"❌ هیچ ری‌اکشن خودکاری برای {target_name} تنظیم نشده است")
                except:
                    # Check if target is "all"
                    if target.lower() == "all" and "all" in auto_reactions:
                        prev_reactions = auto_reactions["all"].copy()
                        del auto_reactions["all"]
                        
                        # Add to command history
                        command_history.append(('remove_reaction', ("all", prev_reactions)))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                        
                        # Backup after change
                        backup_data()
                        
                        await event.edit("✅ ری‌اکشن‌های خودکار برای همه پیام‌ها حذف شدند")
                    else:
                        await event.edit("❌ هدف مشخص شده یافت نشد")
            except Exception as e:
                logger.error(f"Error in remove react handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^note (.+?) (.+)$'))
        async def note_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                key = event.pattern_match.group(1)
                value = event.pattern_match.group(2)
                
                # Store previous value for undo
                prev_value = user_notes.get(key)
                
                # Save note
                user_notes[key] = value
                
                # Add to command history
                command_history.append(('note', (key, prev_value)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ یادداشت با کلید '{key}' ذخیره شد")
            except Exception as e:
                logger.error(f"Error in note handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^notes$'))
        async def notes_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not user_notes:
                    await event.edit("❌ هیچ یادداشتی ذخیره نشده است")
                    return
                
                notes_text = "📋 **لیست یادداشت‌ها**:\n\n"
                
                for i, (key, value) in enumerate(user_notes.items(), 1):
                    # Truncate long notes
                    short_value = truncate_text(value, 100)
                    notes_text += f"{i}. **{key}**: {short_value}\n\n"
                
                await event.edit(notes_text)
            except Exception as e:
                logger.error(f"Error in notes handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^get note (.+)$'))
        async def get_note_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                key = event.pattern_match.group(1)
                
                if key not in user_notes:
                    await event.edit(f"❌ یادداشتی با کلید '{key}' یافت نشد")
                    return
                
                note_text = f"📝 **یادداشت**: {key}\n\n{user_notes[key]}"
                
                await event.edit(note_text)
            except Exception as e:
                logger.error(f"Error in get note handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^remind (.+?) (.+)$'))
        async def remind_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                time_str = event.pattern_match.group(1)
                message = event.pattern_match.group(2)
                
                # Validate time format (HH:MM)
                if not re.match(r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$', time_str):
                    await event.edit("❌ فرمت زمان اشتباه است. از فرمت HH:MM استفاده کنید")
                    return
                
                # Add to reminders
                reminders.append((time_str, message, event.chat_id))
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ یادآور برای ساعت {time_str} تنظیم شد")
            except Exception as e:
                logger.error(f"Error in remind handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^remindlist$'))
        async def remindlist_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not reminders:
                    await event.edit("❌ هیچ یادآوری تنظیم نشده است")
                    return
                
                remind_text = "📋 **لیست یادآورها**:\n\n"
                
                for i, (time_str, message, chat_id) in enumerate(reminders, 1):
                    try:
                        # Try to get chat info
                        chat = await client.get_entity(int(chat_id))
                        chat_name = chat.title if hasattr(chat, 'title') else f"چت خصوصی {chat_id}"
                    except:
                        chat_name = f"چت {chat_id}"
                    
                    remind_text += f"{i}. ⏰ **{time_str}** | 💬 **{chat_name}**\n{message}\n\n"
                
                await event.edit(remind_text)
            except Exception as e:
                logger.error(f"Error in remindlist handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^spam (\d+) (.+)$'))
        async def spam_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                count = int(event.pattern_match.group(1))
                message = event.pattern_match.group(2)
                
                # Check spam limit
                config = load_config()
                max_spam = config.get('max_spam_count', 50)
                
                if count > max_spam:
                    await event.edit(f"❌ حداکثر تعداد پیام برای اسپم {max_spam} است. برای تغییر این محدودیت از دستور `set spam limit` استفاده کنید")
                    return
                
                await event.delete()
                await spam_messages(client, event.chat_id, count, message)
            except Exception as e:
                logger.error(f"Error in spam handler: {e}")
                try:
                    await event.edit(f"❌ خطا: {str(e)}")
                except:
                    await client.send_message(event.chat_id, f"❌ خطا در اسپم: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^smartspam (\d+) (\d+(?:\.\d+)?) (.+)$'))
        async def smartspam_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                count = int(event.pattern_match.group(1))
                delay = float(event.pattern_match.group(2))
                message = event.pattern_match.group(3)
                
                # Check spam limit
                config = load_config()
                max_spam = config.get('max_spam_count', 50)
                
                if count > max_spam:
                    await event.edit(f"❌ حداکثر تعداد پیام برای اسپم {max_spam} است. برای تغییر این محدودیت از دستور `set spam limit` استفاده کنید")
                    return
                
                if delay < 0.5:
                    delay = 0.5  # Minimum delay to avoid flood wait
                
                await event.delete()
                await spam_messages(client, event.chat_id, count, message, delay)
            except Exception as e:
                logger.error(f"Error in smartspam handler: {e}")
                try:
                    await event.edit(f"❌ خطا: {str(e)}")
                except:
                    await client.send_message(event.chat_id, f"❌ خطا در اسپم هوشمند: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^multispam (\d+) (.+)$'))
        async def multispam_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                count = int(event.pattern_match.group(1))
                message_text = event.pattern_match.group(2)
                
                # Check spam limit
                config = load_config()
                max_spam = config.get('max_spam_count', 50)
                
                if count > max_spam:
                    await event.edit(f"❌ حداکثر تعداد پیام برای اسپم {max_spam} است. برای تغییر این محدودیت از دستور `set spam limit` استفاده کنید")
                    return
                
                # Split messages by |
                messages = message_text.split("|")
                if not messages:
                    await event.edit("❌ هیچ پیامی برای اسپم مشخص نشده است")
                    return
                
                await event.delete()
                
                print_info(f"Sending {count} messages with {len(messages)} different contents...")
                success_count = 0
                
                for i in range(count):
                    try:
                        # Choose a random message
                        message = random.choice(messages).strip()
                        await client.send_message(event.chat_id, message)
                        success_count += 1
                        print_progress_bar(i + 1, count, 'Sending:', 'Complete', 20)
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        logger.error(f"Error in multispam message {i+1}: {e}")
                
                print_success(f"Successfully sent {success_count}/{count} messages")
            except Exception as e:
                logger.error(f"Error in multispam handler: {e}")
                try:
                    await event.edit(f"❌ خطا: {str(e)}")
                except:
                    await client.send_message(event.chat_id, f"❌ خطا در اسپم چندگانه: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^auto reply (.+?) (.+)$'))
        async def auto_reply_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                trigger = event.pattern_match.group(1)
                response = event.pattern_match.group(2)
                
                # Store previous response for undo
                prev_response = custom_replies.get(trigger)
                
                # Update custom replies
                custom_replies[trigger] = response
                
                # Add to command history
                command_history.append(('add_reply', trigger))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ پاسخ خودکار برای '{trigger}' تنظیم شد")
            except Exception as e:
                logger.error(f"Error in auto reply handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^delete reply (.+)$'))
        async def delete_reply_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                trigger = event.pattern_match.group(1)
                
                if trigger not in custom_replies:
                    await event.edit(f"❌ هیچ پاسخ خودکاری برای '{trigger}' وجود ندارد")
                    return
                
                # Store for undo
                prev_response = custom_replies[trigger]
                
                # Delete from custom replies
                del custom_replies[trigger]
                
                # Add to command history
                command_history.append(('del_reply', (trigger, prev_response)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ پاسخ خودکار برای '{trigger}' حذف شد")
            except Exception as e:
                logger.error(f"Error in delete reply handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^replies$'))
        async def replies_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                if not custom_replies:
                    await event.edit("❌ هیچ پاسخ خودکاری تنظیم نشده است")
                    return
                
                replies_text = "📋 **لیست پاسخ‌های خودکار**:\n\n"
                
                for trigger, response in custom_replies.items():
                    # Truncate long responses
                    short_response = truncate_text(response, 100)
                    replies_text += f"🔸 **{trigger}**:\n{short_response}\n\n"
                
                await event.edit(replies_text)
            except Exception as e:
                logger.error(f"Error in replies handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^nick (.+)$'))
        async def nick_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                nickname = event.pattern_match.group(1)
                chat_id = str(event.chat_id)
                
                # Store previous nickname for undo
                prev_nick = chat_nicknames.get(chat_id)
                
                # Update chat nicknames
                chat_nicknames[chat_id] = nickname
                
                # Add to command history
                command_history.append(('nick', (chat_id, prev_nick)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Backup after change
                backup_data()
                
                await event.edit(f"✅ نام مستعار '{nickname}' برای این چت تنظیم شد")
            except Exception as e:
                logger.error(f"Error in nick handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^search (.+)$'))
        async def search_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                query = event.pattern_match.group(1)
                
                await event.edit(f"🔍 در حال جستجوی '{query}'...")
                
                try:
                    messages = await client.get_messages(event.chat_id, search=query, limit=10)
                    
                    if not messages:
                        await event.edit("❌ پیامی یافت نشد")
                        return
                    
                    result = f"🔍 **نتایج جستجو برای** `{query}`:\n\n"
                    
                    for i, msg in enumerate(messages, 1):
                        sender = await msg.get_sender()
                        sender_name = utils.get_display_name(sender) if sender else "Unknown"
                        message_date = msg.date.strftime("%Y/%m/%d %H:%M")
                        
                        # Get message text or caption
                        message_text = msg.text or msg.caption or "[No text]"
                        message_preview = truncate_text(message_text, 100)
                        
                        result += f"{i}. **از** {sender_name} **در** {message_date}:\n{message_preview}\n\n"
                    
                    await event.edit(result)
                except Exception as e:
                    await event.edit(f"❌ خطا در جستجو: {str(e)}")
            except Exception as e:
                logger.error(f"Error in search handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set spam limit (\d+)$'))
        async def set_spam_limit_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                limit = int(event.pattern_match.group(1))
                
                if limit <= 0:
                    await event.edit("❌ محدودیت باید بزرگتر از صفر باشد")
                    return
                
                if limit > 1000:
                    await event.edit("⚠️ محدودیت بسیار بالاست! این ممکن است منجر به محدودیت حساب شما شود. آیا مطمئن هستید؟ (بله/خیر)")
                    
                    # Wait for confirmation
                    response = await client.wait_for_message(
                        message=lambda msg: 
                            msg.chat_id == event.chat_id and 
                            msg.from_id and msg.from_id.user_id == (await client.get_me()).id and
                            msg.text and msg.text.lower() in ['بله', 'آره', 'yes', 'y', 'خیر', 'نه', 'no', 'n'],
                        timeout=30
                    )
                    
                    if not response or response.text.lower() in ['خیر', 'نه', 'no', 'n']:
                        await event.edit("❌ تنظیم محدودیت اسپم لغو شد")
                        return
                
                # Update config
                config = load_config()
                
                # Store previous limit for undo
                prev_limit = config['max_spam_count']
                
                config['max_spam_count'] = limit
                save_config(config)
                
                # Add to command history
                command_history.append(('spam_limit', prev_limit))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ محدودیت اسپم به {limit} تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set spam limit handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set backup interval (\d+)$'))
        async def set_backup_interval_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                interval = int(event.pattern_match.group(1))
                
                if interval < 5:
                    await event.edit("❌ حداقل فاصله زمانی پشتیبان‌گیری 5 دقیقه است")
                    return
                
                # Update config
                config = load_config()
                
                # Store previous interval for undo
                prev_interval = config['backup_interval']
                
                config['backup_interval'] = interval
                save_config(config)
                
                # Add to command history
                command_history.append(('backup_interval', prev_interval))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ فاصله زمانی پشتیبان‌گیری به {interval} دقیقه تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set backup interval handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set log level (DEBUG|INFO|WARNING|ERROR|CRITICAL)$'))
        async def set_log_level_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                level = event.pattern_match.group(1)
                
                # Update config
                config = load_config()
                
                # Store previous level for undo
                prev_level = config['log_level']
                
                config['log_level'] = level
                save_config(config)
                
                # Update logger level
                logger.setLevel(getattr(logging, level))
                
                # Add to command history
                command_history.append(('log_level', prev_level))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ سطح لاگ به {level} تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set log level handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set timezone (.+)$'))
        async def set_timezone_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                timezone = event.pattern_match.group(1)
                
                # Validate timezone
                try:
                    pytz.timezone(timezone)
                except:
                    await event.edit("❌ منطقه زمانی نامعتبر است")
                    return
                
                # Update config
                config = load_config()
                
                # Store previous timezone for undo
                prev_timezone = config['timezone']
                
                config['timezone'] = timezone
                save_config(config)
                
                # Add to command history
                command_history.append(('timezone', prev_timezone))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ منطقه زمانی به {timezone} تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set timezone handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set prefix (.+)$'))
        async def set_prefix_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                prefix = event.pattern_match.group(1)
                
                if len(prefix) > 5:
                    await event.edit("❌ پیشوند نباید بیشتر از 5 کاراکتر باشد")
                    return
                
                # Update config
                config = load_config()
                
                # Store previous prefix for undo
                prev_prefix = config.get('bot_prefix', '!')
                
                config['bot_prefix'] = prefix
                save_config(config)
                
                # Add to command history
                command_history.append(('prefix', prev_prefix))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ پیشوند به '{prefix}' تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set prefix handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set auto (read|backup) (on|off)$'))
        async def set_auto_setting_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                setting = event.pattern_match.group(1)
                status = event.pattern_match.group(2)
                
                # Update config
                config = load_config()
                
                if setting == 'read':
                    # Store previous state for undo
                    prev_state = config.get('auto_read_messages', False)
                    
                    config['auto_read_messages'] = (status == 'on')
                    
                    # Update actions
                    actions['read'] = (status == 'on')
                    
                    setting_name = "خواندن خودکار پیام‌ها"
                elif setting == 'backup':
                    # Store previous state for undo
                    prev_state = config.get('auto_backup', True)
                    
                    config['auto_backup'] = (status == 'on')
                    setting_name = "پشتیبان‌گیری خودکار"
                else:
                    await event.edit("❌ تنظیمات نامعتبر")
                    return
                
                save_config(config)
                
                # Add to command history
                command_history.append(('auto_setting', (setting, prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ {setting_name} {'فعال' if status == 'on' else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in set auto setting handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^set ai_filter level (low|medium|high)$'))
        async def set_ai_filter_level_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                level = event.pattern_match.group(1)
                
                # Update config
                config = load_config()
                
                # Store previous level for undo
                prev_level = config.get('ai_filter_level', 'low')
                
                config['ai_filter_level'] = level
                save_config(config)
                
                # Add to command history
                command_history.append(('ai_filter_level', prev_level))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ سطح فیلتر هوشمند به '{level}' تنظیم شد")
            except Exception as e:
                logger.error(f"Error in set ai filter level handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^backup$'))
        async def backup_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                await event.edit("⏳ در حال پشتیبان‌گیری...")
                
                if backup_data():
                    # Check if cloud backup is enabled
                    config = load_config()
                    if config['cloud_backup']:
                        await event.edit("⏳ در حال پشتیبان‌گیری در ابر...")
                        if await cloud_backup(client):
                            await event.edit("✅ پشتیبان‌گیری معمولی و ابری با موفقیت انجام شد")
                        else:
                            await event.edit("✅ پشتیبان‌گیری معمولی با موفقیت انجام شد، اما پشتیبان‌گیری ابری ناموفق بود")
                    else:
                        await event.edit("✅ پشتیبان‌گیری با موفقیت انجام شد")
                else:
                    await event.edit("❌ خطا در پشتیبان‌گیری")
            except Exception as e:
                logger.error(f"Error in backup handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^restore$'))
        async def restore_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                
                await event.edit("⏳ در حال بازیابی داده‌ها...")
                
                if restore_data():
                    await event.edit("✅ بازیابی داده‌ها با موفقیت انجام شد")
                else:
                    await event.edit("❌ فایل پشتیبان یافت نشد یا مشکلی در بازیابی وجود دارد")
            except Exception as e:
                logger.error(f"Error in restore handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^undo$'))
        async def undo_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not command_history:
                    await event.edit("❌ تاریخچه دستورات خالی است")
                    return
                
                last_command = command_history.pop()
                command_type, data = last_command
                
                if command_type == 'time':
                    global time_enabled
                    time_enabled = data
                    if not time_enabled:
                        await client(functions.account.UpdateProfileRequest(last_name=''))
                    await event.edit(f"✅ وضعیت نمایش ساعت به {'فعال' if time_enabled else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'lock':
                    lock_type, chat_id, prev_state = data
                    if prev_state:
                        locked_chats[lock_type].add(chat_id)
                    else:
                        locked_chats[lock_type].discard(chat_id)
                    await event.edit(f"✅ وضعیت قفل {lock_type} به {'فعال' if prev_state else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'font':
                    global current_font
                    current_font = data
                    await event.edit(f"✅ فونت به {current_font} برگردانده شد")
                
                elif command_type == 'enemy_add':
                    enemies.discard(data)
                    await event.edit("✅ کاربر از لیست دشمن حذف شد")
                
                elif command_type == 'enemy_remove':
                    enemies.add(data)
                    await event.edit("✅ کاربر به لیست دشمن اضافه شد")
                
                elif command_type == 'action':
                    action_type, prev_state = data
                    actions[action_type] = prev_state
                    await event.edit(f"✅ وضعیت {action_type} به {'فعال' if prev_state else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'save_msg':
                    saved_messages.pop()
                    await event.edit("✅ آخرین پیام ذخیره شده حذف شد")
                
                elif command_type == 'save_pic':
                    path = data
                    if path in saved_pics:
                        saved_pics.remove(path)
                    if os.path.exists(path):
                        os.remove(path)
                    await event.edit("✅ آخرین عکس ذخیره شده حذف شد")
                
                elif command_type == 'block_word':
                    blocked_words.remove(data)
                    await event.edit(f"✅ کلمه '{data}' از لیست کلمات مسدود شده حذف شد")
                
                elif command_type == 'unblock_word':
                    blocked_words.append(data)
                    await event.edit(f"✅ کلمه '{data}' به لیست کلمات مسدود شده اضافه شد")
                
                elif command_type == 'add_reply':
                    trigger = data
                    if trigger in custom_replies:
                        del custom_replies[trigger]
                    await event.edit(f"✅ پاسخ خودکار برای '{trigger}' حذف شد")
                
                elif command_type == 'del_reply':
                    trigger, response = data
                    custom_replies[trigger] = response
                    await event.edit(f"✅ پاسخ خودکار برای '{trigger}' بازگردانده شد")
                
                elif command_type == 'theme':
                    global theme
                    theme = data
                    await event.edit(f"✅ تم به '{theme}' برگردانده شد")
                
                elif command_type == 'translate_lang':
                    config = load_config()
                    config['default_translate_lang'] = data
                    save_config(config)
                    await event.edit(f"✅ زبان پیش‌فرض ترجمه به '{data}' برگردانده شد")
                
                elif command_type == 'cloud_backup':
                    config = load_config()
                    config['cloud_backup'] = data
                    save_config(config)
                    await event.edit(f"✅ وضعیت پشتیبان‌گیری ابری به {'فعال' if data else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'status_rotation':
                    global status_rotation_active
                    status_rotation_active = data
                    if status_rotation_active and status_rotation:
                        asyncio.create_task(update_status_rotation(client))
                    await event.edit(f"✅ وضعیت چرخش خودکار وضعیت به {'فعال' if data else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'clear_status':
                    global status_rotation
                    statuses, active = data
                    status_rotation = statuses
                    status_rotation_active = active
                    if active:
                        asyncio.create_task(update_status_rotation(client))
                    await event.edit("✅ لیست وضعیت‌های چرخشی بازگردانده شد")
                
                elif command_type == 'welcome':
                    chat_id, prev_welcome = data
                    if prev_welcome:
                        welcome_messages[chat_id] = prev_welcome
                    else:
                        if chat_id in welcome_messages:
                            del welcome_messages[chat_id]
                    await event.edit("✅ پیام خوش‌آمدگویی به وضعیت قبلی برگردانده شد")
                
                elif command_type == 'secure_backup':
                    config = load_config()
                    config['encrypted_backup'] = data
                    save_config(config)
                    await event.edit(f"✅ وضعیت پشتیبان‌گیری رمزنگاری شده به {'فعال' if data else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'spam_limit':
                    config = load_config()
                    config['max_spam_count'] = data
                    save_config(config)
                    await event.edit(f"✅ محدودیت اسپم به {data} برگردانده شد")
                
                elif command_type == 'backup_interval':
                    config = load_config()
                    config['backup_interval'] = data
                    save_config(config)
                    await event.edit(f"✅ فاصله زمانی پشتیبان‌گیری به {data} دقیقه برگردانده شد")
                
                elif command_type == 'log_level':
                    config = load_config()
                    config['log_level'] = data
                    save_config(config)
                    logger.setLevel(getattr(logging, data))
                    await event.edit(f"✅ سطح لاگ به {data} برگردانده شد")
                
                elif command_type == 'timezone':
                    config = load_config()
                    config['timezone'] = data
                    save_config(config)
                    await event.edit(f"✅ منطقه زمانی به {data} برگردانده شد")
                
                elif command_type == 'prefix':
                    config = load_config()
                    config['bot_prefix'] = data
                    save_config(config)
                    await event.edit(f"✅ پیشوند به '{data}' برگردانده شد")
                
                elif command_type == 'auto_setting':
                    setting, prev_state = data
                    config = load_config()
                    
                    if setting == 'read':
                        config['auto_read_messages'] = prev_state
                        actions['read'] = prev_state
                        setting_name = "خواندن خودکار پیام‌ها"
                    elif setting == 'backup':
                        config['auto_backup'] = prev_state
                        setting_name = "پشتیبان‌گیری خودکار"
                    
                    save_config(config)
                    await event.edit(f"✅ {setting_name} به {'فعال' if prev_state else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'ai_filter_level':
                    config = load_config()
                    config['ai_filter_level'] = data
                    save_config(config)
                    await event.edit(f"✅ سطح فیلتر هوشمند به '{data}' برگردانده شد")
                
                elif command_type == 'nick':
                    chat_id, prev_nick = data
                    if prev_nick:
                        chat_nicknames[chat_id] = prev_nick
                    else:
                        if chat_id in chat_nicknames:
                            del chat_nicknames[chat_id]
                    await event.edit("✅ نام مستعار چت به وضعیت قبلی برگردانده شد")
                
                elif command_type == 'note':
                    key, prev_value = data
                    if prev_value:
                        user_notes[key] = prev_value
                    else:
                        if key in user_notes:
                            del user_notes[key]
                    await event.edit(f"✅ یادداشت '{key}' به وضعیت قبلی برگردانده شد")
                
                elif command_type == 'edit_command':
                    command_name, prev_response = data
                    custom_commands[command_name] = prev_response
                    await event.edit(f"✅ دستور '{command_name}' به وضعیت قبلی برگردانده شد")
                
                elif command_type == 'delete_command':
                    command_name, prev_response = data
                    custom_commands[command_name] = prev_response
                    await event.edit(f"✅ دستور '{command_name}' بازگردانده شد")
                
                elif command_type == 'clear_reactions':
                    global auto_reactions
                    auto_reactions = data
                    await event.edit("✅ ری‌اکشن‌های خودکار بازگردانده شدند")
                
                elif command_type == 'remove_reaction':
                    target, reactions = data
                    auto_reactions[target] = reactions
                    await event.edit(f"✅ ری‌اکشن‌های خودکار برای '{target}' بازگردانده شدند")
                
                elif command_type == 'delete_saved':
                    index, msg = data
                    saved_messages.insert(index, msg)
                    await event.edit(f"✅ پیام ذخیره شده بازگردانده شد")
                
                # Backup after undo
                backup_data()
                
            except Exception as e:
                logger.error(f"Error in undo handler: {e}")
                await event.edit(f"❌ خطا در برگرداندن عملیات: {str(e)}")

        @client.on(events.NewMessage)
        async def enemy_handler(event):
            try:
                if not event.from_id:
                    return
                
                config = load_config()
                if event.from_id.user_id == (await client.get_me()).id:
                    if event.raw_text == 'تنظیم دشمن' and event.is_reply:
                        # Fix for enemy reply bug
                        replied = await event.get_reply_message()
                        if replied and replied.from_id and hasattr(replied.from_id, 'user_id'):
                            user_id = str(replied.from_id.user_id)
                            # Previous state for undo
                            prev_state = user_id in enemies
                            
                            # Add to enemies set
                            enemies.add(user_id)
                            
                            # Add to command history
                            command_history.append(('enemy_add', user_id))
                            if len(command_history) > MAX_HISTORY:
                                command_history.pop(0)
                                
                            # Backup after significant change
                            backup_data()
                            
                            await event.reply('✅ کاربر به لیست دشمن اضافه شد')
                        else:
                            await event.reply('❌ نمی‌توان این کاربر را به لیست دشمن اضافه کرد')

                    elif event.raw_text == 'حذف دشمن' and event.is_reply:
                        replied = await event.get_reply_message()
                        if replied and replied.from_id and hasattr(replied.from_id, 'user_id'):
                            user_id = str(replied.from_id.user_id)
                            # Previous state for undo
                            prev_state = user_id in enemies
                            
                            # Remove from enemies set
                            enemies.discard(user_id)
                            
                            # Add to command history
                            command_history.append(('enemy_remove', user_id))
                            if len(command_history) > MAX_HISTORY:
                                command_history.pop(0)
                                
                            # Backup after significant change
                            backup_data()
                            
                            await event.reply('✅ کاربر از لیست دشمن حذف شد')
                        else:
                            await event.reply('❌ نمی‌توان این کاربر را از لیست دشمن حذف کرد')

                    elif event.raw_text == 'لیست دشمن':
                        enemy_list = ''
                        for i, enemy in enumerate(enemies, 1):
                            try:
                                user = await client.get_entity(int(enemy))
                                enemy_list += f'{i}. {user.first_name} {user.last_name or ""} (@{user.username or "بدون یوزرنیم"})\n'
                            except:
                                enemy_list += f'{i}. ID: {enemy}\n'
                        await event.reply(enemy_list or '❌ لیست دشمن خالی است')

                # Auto-reply to enemy messages
                elif config['enemy_auto_reply'] and str(event.from_id.user_id) in enemies:
                    # Fix: Only reply to enemies if auto-reply is enabled
                    # Enhanced enemy reply with random insult selection
                    reply_chance = config.get('enemy_reply_chance', 100)
                    
                    if random.randint(1, 100) <= reply_chance:
                        # Use more sophisticated selection to avoid repeating the same insult
                        # Get list of recent insults (up to 5) from message_cache
                        recent_insults = []
                        for msg_id, cache_data in list(message_cache.items())[-10:]:
                            if cache_data.get('type') == 'enemy_reply':
                                recent_insults.append(cache_data.get('text', ''))
                        
                        # Select insults that haven't been used recently
                        available_insults = [i for i in insults if i not in recent_insults]
                        if not available_insults:  # If all have been used recently
                            available_insults = insults
                        
                        # Choose random insults
                        insult1 = random.choice(available_insults)
                        # Remove first insult from pool before selecting second
                        available_insults = [i for i in available_insults if i != insult1]
                        insult2 = random.choice(available_insults) if available_insults else random.choice(insults)
                        
                        # Add delay between insults for more natural appearance
                        await event.reply(insult1)
                        
                        # Cache the insult for later reference
                        message_cache[event.id] = {
                            'type': 'enemy_reply',
                            'text': insult1,
                            'time': time.time()
                        }
                        
                        # Random delay between 0.5 and 2 seconds
                        delay = random.uniform(0.5, 2.0)
                        await asyncio.sleep(delay)
                        
                        # Send second insult with different text
                        await event.reply(insult2)
                        
                        # Cache the second insult
                        message_cache[event.id + 1] = {
                            'type': 'enemy_reply',
                            'text': insult2,
                            'time': time.time()
                        }
                        
                        # Clean up old cache entries (older than 1 hour)
                        current_time = time.time()
                        old_entries = [msg_id for msg_id, data in message_cache.items()
                                    if current_time - data.get('time', 0) > 3600]
                        for msg_id in old_entries:
                            del message_cache[msg_id]
            except Exception as e:
                logger.error(f"Error in enemy handler: {e}")
                pass

        @client.on(events.NewMessage)
        async def font_handler(event):
            global current_font
            
            try:
                if not event.from_id or not event.raw_text:
                    return
                            
                if event.from_id.user_id != (await client.get_me()).id:
                    return

                text = event.raw_text.lower().split()
                
                # Font style settings
                if len(text) == 2 and text[1] in ['on', 'off'] and text[0] in font_styles:
                    font, status = text
                    
                    # Previous state for undo
                    prev_font = current_font
                    
                    if status == 'on':
                        current_font = font
                        await event.edit(f'✅ حالت {font} فعال شد')
                    else:
                        current_font = 'normal'
                        await event.edit(f'✅ حالت {font} غیرفعال شد')
                    
                    # Add to command history
                    command_history.append(('font', prev_font))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                
                # Apply font formatting to message
                elif current_font != 'normal' and current_font in font_styles:
                    await event.edit(font_styles[current_font](event.raw_text))
            except Exception as e:
                logger.error(f"Error in font handler: {e}")
                pass

        @client.on(events.NewMessage)
        async def check_locks(event):
            try:
                chat_id = str(event.chat_id)
                
                # Don't apply locks to the user's own messages
                if event.from_id and event.from_id.user_id == (await client.get_me()).id:
                    return
                
                # Check if message forwarding is locked in this chat
                if chat_id in locked_chats['forward'] and event.forward:
                    await event.delete()
                    logger.info(f"Deleted forwarded message in chat {chat_id}")
                    
                # Check if message copying is locked in this chat
                if chat_id in locked_chats['copy'] and event.forward_from:
                    await event.delete()
                    logger.info(f"Deleted copied message in chat {chat_id}")
                    
                # Check if links are blocked in this chat
                if chat_id in locked_chats['link'] and event.text:
                    # Simple regex for URL matching
                    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                    if url_pattern.search(event.text):
                        await event.delete()
                        logger.info(f"Deleted message with link in chat {chat_id}")
                        
                # Check if mentions are blocked in this chat
                if chat_id in locked_chats['mention'] and event.text:
                    if '@' in event.text:
                        await event.delete()
                        logger.info(f"Deleted message with mention in chat {chat_id}")
                    
                # Check if AI filter is enabled in this chat
                if chat_id in locked_chats['ai_filter'] and event.text:
                    # Simple keyword-based content filtering
                    config = load_config()
                    filter_level = config.get('ai_filter_level', 'low')
                    
                    # Define prohibited words for different filter levels
                    prohibited_words = {
                        'low': ['porn', 'xxx', 'sex', 'اکس صوتی', 'پورن', 'سکس', 'س ک س'],
                        'medium': ['porn', 'xxx', 'sex', 'аdult', 'nυde', 'аss', 'dick', 'اکس صوتی', 'پورن', 'سکس', 'س ک س', 'جنده', 'کص', 'کیر'],
                        'high': ['porn', 'xxx', 'sex', 'аdult', 'nυde', 'аss', 'dick', 'pussy', 'cock', 'cum', 'اکس صوتی', 'پورن', 'سکس', 'س ک س', 'جنده', 'کص', 'کیر', 'کون', 'جق']
                    }
                    
                    # Check if message contains prohibited words
                    words = event.text.lower()
                    if any(word in words for word in prohibited_words.get(filter_level, [])):
                        await event.delete()
                        logger.info(f"Deleted message with prohibited content in chat {chat_id}")
                        
                # Check if media is blocked in this chat
                if chat_id in locked_chats['media'] and event.media:
                    await event.delete()
                    logger.info(f"Deleted media message in chat {chat_id}")
                    
                # Anti-spam protection (basic implementation)
                if chat_id in locked_chats['spam']:
                    # Get recent messages from this sender
                    sender_id = event.from_id.user_id if event.from_id else None
                    if sender_id:
                        # Check recent messages in cache
                        recent_count = 0
                        current_time = time.time()
                        
                        for _, data in message_cache.items():
                            if data.get('sender_id') == sender_id and \
                               data.get('chat_id') == chat_id and \
                               current_time - data.get('time', 0) < 5:  # Messages in last 5 seconds
                                recent_count += 1
                        
                        # Store current message in cache
                        message_cache[event.id] = {
                            'sender_id': sender_id,
                            'chat_id': chat_id,
                            'time': current_time
                        }
                        
                        # If too many messages in short time, delete as spam
                        if recent_count >= 5:  # 5+ messages in 5 seconds = spam
                            await event.delete()
                            logger.info(f"Deleted spam message from {sender_id} in chat {chat_id}")
                        
                # Anti-raid protection
                if chat_id in locked_chats['raid']:
                    # Track number of new members joining in short time
                    # This is handled in chat_action_handler
                    pass
                    
            except Exception as e:
                logger.error(f"Error in check locks: {e}")

        @client.on(events.NewMessage)
        async def message_handler(event):
            try:
                # Track message stats if enabled
                if actions['stats']:
                    await track_message_stats(event)
                
                # Auto-read messages if enabled
                if actions['read']:
                    await auto_read_messages(event, client)
                
                # Auto-translate if enabled
                if actions['translate'] and event.text:
                    await auto_translate_message(event, client)
                
                # Check for custom commands
                text = event.raw_text if event.raw_text else ""
                
                # Process custom commands (if message is from self)
                if event.from_id and event.from_id.user_id == (await client.get_me()).id:
                    if text in custom_commands:
                        await event.edit(custom_commands[text])
                        return
                
                # Do not process further if message is not from the user
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    # Check for custom replies if auto_reply is enabled
                    if actions['auto_reply'] and text and text in custom_replies:
                        # Get sender info for personalized replies
                        sender = await event.get_sender()
                        sender_name = utils.get_display_name(sender) if sender else "Unknown"
                        
                        # Create a context for template variables
                        context = {
                            "name": sender_name,
                            "username": sender.username if hasattr(sender, 'username') and sender.username else "Unknown",
                            "time": datetime.now().strftime('%H:%M'),
                            "date": datetime.now().strftime('%Y-%m-%d'),
                            "message": text
                        }
                        
                        # Get the reply template
                        reply_template = custom_replies[text]
                        
                        # Apply template variables if present
                        for key, value in context.items():
                            placeholder = f"{{{key}}}"
                            if placeholder in reply_template:
                                reply_template = reply_template.replace(placeholder, str(value))
                        
                        await event.reply(reply_template)
                    
                    # Check for auto reactions
                    if actions['reaction']:
                        # Check for user-specific reaction
                        user_id = str(event.from_id.user_id) if event.from_id else None
                        chat_id = str(event.chat_id)
                        
                        if user_id and user_id in auto_reactions:
                            reactions = auto_reactions[user_id]
                            reaction = random.choice(reactions) if reactions else None
                            if reaction:
                                await event.message.react(reaction)
                        elif chat_id in auto_reactions:
                            reactions = auto_reactions[chat_id]
                            reaction = random.choice(reactions) if reactions else None
                            if reaction:
                                await event.message.react(reaction)
                        elif "all" in auto_reactions:
                            reactions = auto_reactions["all"]
                            reaction = random.choice(reactions) if reactions else None
                            if reaction:
                                await event.message.react(reaction)
                    
                    return

                # Check for blocked words
                if any(word in text.lower() for word in blocked_words):
                    await event.delete()
                    return

                # Auto actions
                if actions['typing']:
                    asyncio.create_task(auto_typing(client, event.chat_id))
                
                if actions['reaction']:
                    await auto_reaction(event)

                # Exit command
                if event.raw_text == 'exit':
                    await event.reply("✅ در حال خروج از برنامه...")
                    global running
                    running = False
                    await client.disconnect()
                    return
            except Exception as e:
                logger.error(f"Error in message handler: {e}")
                pass

        @client.on(events.NewMessage(pattern='وضعیت'))
        async def status_handler(event):
            try:
                if not event.from_id:
                    return
                    
                if event.from_id.user_id == (await client.get_me()).id:
                    await show_status(client, event)
            except Exception as e:
                logger.error(f"Error in status handler: {e}")
                print_error(f"Error showing status: {e}")

        @client.on(events.MessageDeleted)
        async def delete_handler(event):
            """Handle deleted messages for anti-delete feature"""
            try:
                for deleted_id in event.deleted_ids:
                    chat_id = str(event.chat_id)
                    if chat_id in locked_chats['delete']:
                        # Try to find the message in our cache
                        msg = await client.get_messages(event.chat_id, ids=deleted_id)
                        if msg and msg.text:
                            sender = await msg.get_sender()
                            sender_name = utils.get_display_name(sender) if sender else "Unknown"
                            
                            saved_text = f"🔴 پیام حذف شده از {sender_name}:\n{msg.text}"
                            await client.send_message(event.chat_id, saved_text)
            except Exception as e:
                logger.error(f"Error in delete handler: {e}")

        @client.on(events.MessageEdited)
        async def edit_handler(event):
            """Handle edited messages for anti-edit feature"""
            try:
                chat_id = str(event.chat_id)
                if chat_id in locked_chats['edit'] and event.message:
                    # Skip if message is from self
                    if event.from_id and event.from_id.user_id == (await client.get_me()).id:
                        return
                        
                    # We need to find the original message
                    msg_id = event.message.id
                    
                    # Check cache first
                    if msg_id in message_cache and 'text' in message_cache[msg_id]:
                        original_text = message_cache[msg_id]['text']
                        current_text = event.message.text
                        
                        if original_text != current_text:
                            sender = await event.get_sender()
                            sender_name = utils.get_display_name(sender) if sender else "Unknown"
                            
                            edit_text = f"🔄 پیام ویرایش شده از {sender_name}:\n\nقبل:\n{original_text}\n\nبعد:\n{current_text}"
                            await client.send_message(event.chat_id, edit_text)
                    else:
                        # Try to get edit history using API
                        try:
                            edit_history = await client(functions.channels.GetMessageEditHistoryRequest(
                                channel=event.chat_id,
                                id=msg_id
                            ))
                            
                            if edit_history and edit_history.messages:
                                # Get the original message (first in history)
                                original = edit_history.messages[-1]
                                current = event.message
                                
                                if original.message != current.message:
                                    sender = await event.get_sender()
                                    sender_name = utils.get_display_name(sender) if sender else "Unknown"
                                    
                                    edit_text = f"🔄 پیام ویرایش شده از {sender_name}:\n\nقبل:\n{original.message}\n\nبعد:\n{current.message}"
                                    await client.send_message(event.chat_id, edit_text)
                        except Exception as e:
                            logger.warning(f"Could not get edit history: {e}")
                            pass
            except Exception as e:
                logger.error(f"Error in edit handler: {e}")

        @client.on(events.ChatAction)
        async def chat_action_handler(event):
            """Handle chat actions like user joining"""
            try:
                chat_id = str(event.chat_id)
                
                # Handle welcome messages
                if (event.user_joined or event.user_added) and chat_id in welcome_messages:
                    user = await event.get_user()
                    user_name = user.first_name if user else "Unknown"
                    
                    # Get welcome message template
                    welcome_template = welcome_messages[chat_id]
                    
                    # Replace placeholders
                    welcome_text = welcome_template.replace("{user}", user_name)
                    welcome_text = welcome_text.replace("{chat}", event.chat.title if hasattr(event.chat, 'title') else "this chat")
                    welcome_text = welcome_text.replace("{date}", datetime.now().strftime('%Y-%m-%d'))
                    welcome_text = welcome_text.replace("{time}", datetime.now().strftime('%H:%M'))
                    
                    await client.send_message(event.chat_id, welcome_text)
                
                # Anti-raid protection
                if chat_id in locked_chats['raid'] and (event.user_joined or event.user_added):
                    # Check for multiple joins in short time
                    current_time = time.time()
                    
                    # Initialize raid tracking for this chat if not exists
                    if not hasattr(chat_action_handler, 'raid_tracking'):
                        chat_action_handler.raid_tracking = {}
                    
                    if chat_id not in chat_action_handler.raid_tracking:
                        chat_action_handler.raid_tracking[chat_id] = {
                            'join_times': [],
                            'raid_mode': False,
                            'raid_start': 0
                        }
                    
                    # Add current join time
                    chat_action_handler.raid_tracking[chat_id]['join_times'].append(current_time)
                    
                    # Remove old entries (older than 1 minute)
                    chat_action_handler.raid_tracking[chat_id]['join_times'] = [t for t in chat_action_handler.raid_tracking[chat_id]['join_times'] 
                                                                               if current_time - t < 60]
                    
                    # Check for raid (5+ joins within 1 minute)
                    recent_joins = len(chat_action_handler.raid_tracking[chat_id]['join_times'])
                    
                    if recent_joins >= 5 and not chat_action_handler.raid_tracking[chat_id]['raid_mode']:
                        # Activate raid mode
                        chat_action_handler.raid_tracking[chat_id]['raid_mode'] = True
                        chat_action_handler.raid_tracking[chat_id]['raid_start'] = current_time
                        
                        # Alert about raid
                        await client.send_message(event.chat_id, "⚠️ **هشدار**: شناسایی حمله گروهی! محافظت خودکار فعال شد.")
                        
                        # Add additional locks during raid
                        locked_chats['spam'].add(chat_id)
                        locked_chats['link'].add(chat_id)
                        locked_chats['mention'].add(chat_id)
                        
                        # Schedule task to disable raid mode after 30 minutes
                        async def disable_raid_mode():
                            await asyncio.sleep(30 * 60)  # 30 minutes
                            if chat_id in chat_action_handler.raid_tracking and chat_action_handler.raid_tracking[chat_id]['raid_mode']:
                                chat_action_handler.raid_tracking[chat_id]['raid_mode'] = False
                                await client.send_message(event.chat_id, "✅ حالت محافظت حمله گروهی غیرفعال شد.")
                        
                        asyncio.create_task(disable_raid_mode())
                
                # Join restriction
                if chat_id in locked_chats['join'] and (event.user_joined or event.user_added):
                    # Get user
                    user = await event.get_user()
                    user_id = user.id if user else None
                    
                    # Kick the user
                    if user_id:
                        try:
                            await client.kick_participant(event.chat_id, user_id)
                            await client.send_message(event.chat_id, f"🚫 کاربر {user.first_name} به دلیل محدودیت عضویت اخراج شد.")
                        except Exception as e:
                            logger.error(f"Error kicking user: {e}")
            except Exception as e:
                logger.error(f"Error in chat action handler: {e}")

        # Run the client until disconnected
        print_success("Self-bot is running")
        await client.run_until_disconnected()

    except KeyboardInterrupt:
        print_warning("\nKilling the self-bot by keyboard interrupt...")
        return
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        return
    finally:
        
        running = False
        if client and client.is_connected():
            await client.disconnect()
        print_info("Self-bot has been shut down")

def init():
    """Initialize and run the self-bot"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("\nExiting self-bot...")
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        logging.error(f"Unexpected init error: {e}")

if __name__ == '__main__':
    init()




این کد تمام باگ هاشو بگیر که انگار از روز اول باگ نداشته هیچ باگی نداشته باشه مخصوصا اون باگ global و تمام کد رو بدون هیچ کمی و کاستی در یک فایل index.py بنویس تاکید میکنم در یک فایل index.py بنویس کل کد رو بدون هیچ باگی