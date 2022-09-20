import base64
import io
from time import strftime
from typing import List

import aiohttp
import telethon
from telethon.tl import types
from telethon.tl.patched import Message

from config import USERBOT


async def get_profile_data(user: types.User):
    avatar = await USERBOT.download_profile_photo(user.id, bytes)
    return telethon.utils.get_display_name(user), base64.b64encode(avatar).decode() if avatar else None


def get_message_media(message: Message):
    data = None
    if message and message.media:
        data = message.photo or message.sticker or message.video or message.video_note or message.gif or message.web_preview
    return data


def get_message_text(message: Message, reply: bool = False):
    return (
        "📷 Фото"
        if message.photo and reply
        else message.file.emoji + " Стикер"
        if message.sticker and reply
        else "📹 Видеосообщение"
        if message.video_note and reply
        else "📹 Видео"
        if message.video and reply
        else "🖼 GIF"
        if message.gif and reply
        else "📊 Опрос"
        if message.poll
        else "📍 Местоположение"
        if message.geo
        else "👤 Контакт"
        if message.contact
        else f"🎵 Голосовое сообщение: {strftime(message.voice.attributes[0].duration)}"
        if message.voice
        else f"🎧 Музыка: {strftime(message.audio.attributes[0].duration)} | {message.audio.attributes[0].performer} - {message.audio.attributes[0].title}"
        if message.audio
        else f"💾 Файл: {message.file.name}"
        if type(message.media) == types.MessageMediaDocument and not get_message_media(message)
        else f"{message.media.emoticon} Дайс: {message.media.value}"
        if type(message.media) == types.MessageMediaDice
        else f"Service message: {message.action.to_dict()['_']}"
        if type(message) == types.MessageService
        else ""
    )


def get_entities(entities: List[types.TypeMessageEntity]):
    # coded by @droox
    r = []
    if entities:
        for entity in entities:
            entity = entity.to_dict()
            entity["type"] = entity.pop("_").replace("MessageEntity", "").lower()
            r.append(entity)
    return r


async def quote_parse_messages(message: Message, count: int):
    payloads = []
    messages = [
        msg async for msg in USERBOT.iter_messages(
            message.chat_id, count, reverse=True, add_offset=1,
            offset_id=(await message.get_reply_message()).id,
        )
    ]

    for message in messages:
        avatar = rank = reply_id = reply_name = reply_text = None
        entities = get_entities(message.entities)

        if message.fwd_from:
            if message.fwd_from.from_id:
                if type(message.fwd_from.from_id) == types.PeerChannel:
                    user_id = message.fwd_from.from_id.channel_id
                else:
                    user_id = message.fwd_from.from_id.user_id
                try:
                    user = await USERBOT.get_entity(user_id)
                except Exception as e:
                    name, avatar = await get_profile_data(message.sender)
                    return f"ошибка {e}", None, message.sender.id, name, avatar, "ошибка :(", None, None, None, None
                name, avatar = await get_profile_data(user)
                user_id = user.id

            elif name := message.fwd_from.from_name:
                user_id = message.chat_id
        else:
            if reply := await message.get_reply_message():
                reply_id = reply.sender.id
                reply_name = telethon.utils.get_display_name(reply.sender)
                reply_text = get_message_text(reply, True) + (
                    ". " + reply.raw_text
                    if reply.raw_text and get_message_text(reply, True)
                    else reply.raw_text or ""
                )

            user = await USERBOT.get_entity(message.sender)
            name, avatar = await get_profile_data(user)
            user_id = user.id

            if message.is_group and message.is_channel:
                admins = await USERBOT.get_participants(message.chat_id, filter=types.ChannelParticipantsAdmins)
                if user in admins:
                    admin = admins[admins.index(user)].participant
                    rank = admin.rank or ("creator" if type(admin) == types.ChannelParticipantCreator else "admin")

        media = await USERBOT.download_media(get_message_media(message), bytes, thumb=-1)
        media = base64.b64encode(media).decode() if media else None

        via_bot = message.via_bot.username if message.via_bot else None
        text = (message.raw_text or "") + (
            ("\n\n" + get_message_text(message) if message.raw_text else get_message_text(message)) if get_message_text(
                message) else "")

        payloads.append(
            {
                "text": text,
                "media": media,
                "entities": entities,
                "author": {
                    "id": user_id,
                    "name": name,
                    "avatar": avatar,
                    "rank": rank or "",
                    "via_bot": via_bot
                },
                "reply": {
                    "id": reply_id,
                    "name": reply_name,
                    "text": reply_text
                }
            }
        )

    return payloads


async def sticker_quote(event):
    if not event.text:
        return

    cmd, *args = event.text.split(maxsplit=1)
    args = args[0] if args else ""
    if cmd != ".qq":
        return

    is_file = "-file" in args
    payload = {
        "messages": await quote_parse_messages(event, 1),
        "bg_color": "#162330",
        "text_color": "#fff",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://quotes.fl1yd.su/generate", json=payload) as resp:
            #
            if resp.status != 200:
                await event.reply("какая-то ошибка")
            quote = io.BytesIO(await resp.content.read())
            quote.name = "SQuote" + (".png" if is_file else ".webp")
            await USERBOT.send_message(entity=event.chat_id, file=quote, )
