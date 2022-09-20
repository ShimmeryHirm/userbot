from telethon import events

from config import USERBOT
from core.cmds.animations import cat_anim, clock_anim
from core.cmds.chat_cmds import who_is, demot_cmd, check_media, rr_cmd, tag_all
from core.cmds.notes import add_note, view_note, rm_note, view_list_note
from core.cmds.pm_cmds import eval_cmd
from core.cmds.stickerquote import sticker_quote


def register_pm_handlers():
    USERBOT.add_event_handler(clock_anim, events.NewMessage())
    USERBOT.add_event_handler(cat_anim, events.NewMessage())
    USERBOT.add_event_handler(eval_cmd, events.NewMessage())
    # USERBOT.add_event_handler(anti_stairs, events.NewMessage())


def register_chat_handlers():
    USERBOT.add_event_handler(tag_all, events.NewMessage())
    USERBOT.add_event_handler(clock_anim, events.NewMessage())
    USERBOT.add_event_handler(rr_cmd, events.NewMessage())
    USERBOT.add_event_handler(check_media, events.NewMessage())
    USERBOT.add_event_handler(demot_cmd, events.NewMessage())
    USERBOT.add_event_handler(who_is, events.NewMessage())

    USERBOT.add_event_handler(add_note, events.NewMessage())
    USERBOT.add_event_handler(view_note, events.NewMessage())
    USERBOT.add_event_handler(rm_note, events.NewMessage())
    USERBOT.add_event_handler(view_list_note, events.NewMessage())

    USERBOT.add_event_handler(sticker_quote, events.NewMessage())
