from typing import List

from sqlalchemy import select, insert
from telethon.events import NewMessage

from core.db import async_session
from core.db.tables import Notes


async def add_note(event: NewMessage.Event):
    if not event.text:
        return

    cmd, *args = event.text.split(maxsplit=1)
    args = args[0] if args else ""
    if cmd != ".addnote":
        return
    if not args:
        await event.reply("укажи имя заметки в команде")
        return

    async with async_session() as session:
        stmt = select(Notes).where(Notes.name == args)
        note: Notes = (await session.execute(stmt)).scalars().first()
        if not note:
            chat_id = int(str(event.chat_id)[2:]) if str(event.chat_id).startswith("-100") else event.chat_id

            msg_id = event.message.id if not event.reply_to else event.reply_to.reply_to_msg_id
            stmt = insert(Notes).values(msg_id=msg_id,
                                        chat_id=chat_id,
                                        name=args)
            await session.execute(stmt)
            await session.commit()
            await event.reply("заметка создана")
        else:
            await event.reply("такое имя занято занято")


async def view_note(event: NewMessage.Event):
    if not event.text:
        return

    cmd, *args = event.text.split(maxsplit=1)
    args = args[0] if args else ""
    if cmd != ".note":
        return
    if not args:
        await event.reply("укажи имя заметки в команде")
        return

    async with async_session() as session:

        stmt = select(Notes).where(Notes.name == args)
        note: Notes = (await session.execute(stmt)).scalars().first()
        if not note:
            await event.reply("заметка не найдена")
        else:
            await event.reply(f"https://t.me/c/{note.chat_id}/{note.msg_id}")


async def rm_note(event: NewMessage.Event):
    if not event.text:
        return

    cmd, *args = event.text.split(maxsplit=1)
    args = args[0] if args else ""
    if cmd != ".rmnote":
        return
    if not args:
        await event.reply("укажи имя заметки в команде")
        return

    async with async_session() as session:
        stmt = select(Notes).where(Notes.name == args)
        note: Notes = (await session.execute(stmt)).scalars().first()
        if note:

            await session.delete(note)
            await session.commit()
            await event.reply("заметка удалена")
        else:
            await event.reply("заметка не найдена")


async def view_list_note(event: NewMessage.Event):
    if not event.text:
        return

    if event.text != ".viewnotes":
        return
    chat_id = int(str(event.chat_id)[2:]) if str(event.chat_id).startswith("-100") else event.chat_id
    async with async_session() as session:
        stmt = select(Notes).where(Notes.chat_id == chat_id)
        notes: List[Notes] = (await session.execute(stmt)).scalars().all()
        if not notes:
            await event.reply("заметок нету")
            return
        n = 1
        t = ''
        for note in notes:
            t += f"<b>{n}.</b> <code>{note.name}</code>\n"
            n += 1
        await event.reply(t, parse_mode="html")
