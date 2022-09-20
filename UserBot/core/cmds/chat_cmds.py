import asyncio
import datetime
import random
from collections import deque

from m2h import Hum2Sec, Sec2Hum
from telethon.events import NewMessage
from telethon.tl import functions

from config import USERBOT, DEMOT_TEXTS


async def tag_all(event: NewMessage.Event):
    if not event.text:
        return

    cmd, *args = event.text.split(maxsplit=1)
    if cmd != ".all":
        return

    args = args[0] + ' ' if args else ""
    participants = await USERBOT.get_participants(event.chat_id)
    mentions = []
    for participant in participants:
        if args:
            mentions.append(f'<a href="tg://user?id={participant.id}">\u2060</a>')
        else:
            name = participant.first_name
            mentions.append(f'<a href="tg://user?id={participant.id}">{name}</a> ')

    mentions = [mentions[i:i + 5] for i in range(0, len(mentions), 5)]
    for mention in mentions:
        await event.respond(args + ''.join(mention) + f' ({mentions.index(mention) + 1}/{len(mentions)})',
                            parse_mode='html')


async def clock_anim(event: NewMessage.Event):
    # TODO: outgoing check
    cmd, *args = event.text.split(maxsplit=1)

    args = args[0] if args else ""

    if not args or cmd != '.timer':
        await event.delete()
        return

    if ':' in event.message.text:

        hours = int(args.split(':')[0])
        minutes = int(args.split(':')[1])
        t = int((datetime.timedelta(hours=24) - (
                datetime.datetime.now() - datetime.datetime.now().replace(hour=hours, minute=minutes, second=0,
                                                                          microsecond=0))).total_seconds() % (
                        24 * 3600))
    else:
        t = Hum2Sec(args).seconds
    end = datetime.datetime.now() + datetime.timedelta(seconds=t)
    deq = deque(reversed(list("🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛")))
    while (end - datetime.datetime.now()).seconds > 0:
        res = Sec2Hum((end - datetime.datetime.now()).seconds).string
        if 'час' in res:
            sl = 15
        elif 'минут' in res:
            sl = 5
        elif 'секунд' in res:
            sl = 1
        else:
            sl = 1
        await event.edit(f"{deq[0]} <b>Таймер</b>"
                         "\n"
                         f"\n<i>Осталось:</i>  <b>{res}</b>",
                         parse_mode='html')
        deq.rotate(1)
        await asyncio.sleep(sl)
        t -= sl
    await event.edit('✅ <i>Время вышло!</i>',
                     parse_mode='html')
    await asyncio.sleep(300)
    await event.delete()


async def rr_cmd(event: NewMessage.Event):
    if not event.text:
        return
    cmd, *args = event.text.split(maxsplit=1)
    args = args[0] if args else ""
    if cmd != '.rr' or event.chat_id not in (-1001598063769, -1001100911692):
        return

    await USERBOT.get_participants(event.chat_id)

    if not args.isdecimal():
        bullets = 5
    else:
        bullets = int(args)

    if bullets < 0:
        await event.respond("пульки в минус уйти не могут")
    elif bullets == 0:
        await event.respond("пулек в барабане нету:(")
    elif bullets > 6:
        await event.respond("слишком много пулек, максмум 6")
    else:
        if random.randint(1, 6) <= bullets:
            if 6 - bullets:
                await event.respond(f"бам! не повезло,мут на {Sec2Hum((6 - bullets) * 60).string}")
                # user = await event.client.get_entity(event.sender_id)
                print((6 - bullets))
                await USERBOT.edit_permissions(entity=event.peer_id.channel_id,
                                               user=event.message.from_id,
                                               until_date=datetime.timedelta(minutes=(6 - bullets)),
                                               send_messages=False,
                                               view_messages=True
                                               )
            else:
                await event.respond(f"бам! не повезло")
        else:
            await event.respond("пуф! выстрел не произошел")


async def check_media(message):
    reply = await message.get_reply_message()
    is_reply = True
    if not reply:
        reply = message
        is_reply = False
    if not reply.file:
        return False, ...
    mime = reply.file.mime_type.split("/")[0].lower()
    if mime != "image":
        return False, ...
    return reply, is_reply


async def demot_cmd(msg):
    if not msg.text.startswith('.demot'):
        return

    event, is_reply = await check_media(msg)
    if not event:
        await msg.edit("<b>Ответ командой на картинку!</b>")
        return

    _, *args = msg.text.split(maxsplit=1)
    text = args[0] if args else ""
    if not text:
        text = random.choice(DEMOT_TEXTS)
    elif text == 'r1':
        text = ''
    await msg.edit("<i>Демотивирую...</i>", parse_mode='html')

    await USERBOT.send_message("@demotik_bot", text, file=event.media)
    await asyncio.sleep(3)
    demotivator = (await USERBOT.get_messages("@demotik_bot", limit=1))[0].media
    if is_reply:
        await msg.delete()
        await event.reply(file=demotivator)

    else:
        await event.edit(file=demotivator, text="")
    await USERBOT(functions.messages.DeleteHistoryRequest(
        peer='@demotic_bot',
        max_id=0,
        revoke=True,
        just_clear=True

    ))


async def who_is(event: NewMessage.Event):
    if not event.text.startswith('.кто '):
        return
    _, *args = event.text.split(maxsplit=1)
    args = args[0] + ' ' if args else ""
    if not args:
        return
    participants = await USERBOT.get_participants(event.chat_id)

    user = random.choice(participants)
    await event.respond(f'<a href="tg://user?id={user.id}">{user.first_name}</a> - {args}',
                        parse_mode='html')
