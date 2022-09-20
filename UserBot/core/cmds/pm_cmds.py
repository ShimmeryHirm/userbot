from telethon.events import NewMessage

from config import USERBOT


async def eval_cmd(event: NewMessage.Event):
    if not event.text.startswith('.eval'):
        return
    _, *args = event.text.split(maxsplit=1)
    args = args[0] if args else ""
    if args:
        try:
            res = eval(args)
        except Exception as e:
            res = f"{type(e).__name__}: {e}"
        await event.edit("<i>Выполненный код:</i>\n"
                         f"<code>{args}</code>\n"
                         f"<i>Результат:</i>\n"
                         f"<code>{res}</code>",
                         parse_mode="html")
    else:
        await event.delete()


async def anti_stairs(event: NewMessage.Event):
    # TODO: outgoing check
    last_msg = (await USERBOT.get_messages(event.to_id, limit=2))[-1]
    if last_msg.sender_id == event.sender_id and not last_msg.fwd_from and not event.media and '//' not in event.text:
        text = last_msg.text
        text += "\n" * 2
        text += event.text
        if event.is_reply and last_msg.is_reply:
            if event.reply_to.reply_to_msg_id == last_msg.reply_to.reply_to_msg_id:
                await event.delete()
                await last_msg.edit(text, parse_mode='markdown')
        elif not event.is_reply and not last_msg.is_reply:
            await event.delete()
            await last_msg.edit(text, parse_mode='markdown')

    elif '//' in event.text:
        text = event.text
        text = text.replace('// ', '')
        await event.edit(text)
