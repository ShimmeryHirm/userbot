import asyncio
import random

from telethon.events import NewMessage


async def cat_anim(event: NewMessage.Event):
    if event.message.text != '!cat':
        return
    nw = []

    len_way = random.randint(2, 5)
    mousses = random.randint(2, 4)
    way = [len_way * '🌱' for i in range(len_way)]
    nw.append(way[0] + '🐭' * mousses)

    for mouse_count in range(mousses, 0, -1):
        x = 0

        for i in way:
            i = list(i)
            i[x] = '😼'
            nw.append(''.join(i) + '🐭' * mouse_count)
            x += 1
        mouse_count -= 1
        nw.append(len(way) * '🌱' + '😼' + mouse_count * '🐭')
        x -= 1
        for i in way:
            i = list(i)
            i[x] = '😼'
            nw.append(''.join(i) + '🐭' * mouse_count)
            x -= 1
        nw.append(way[0] + '🐭' * mouse_count)
    nw = ['🏠' + i for i in nw]
    [nw.append("<code>" + '😻' + '❤️' * i + "</code>") for i in range(1, 4)]
    for i in nw:
        await event.edit(f'<code>{i}</code>',
                         parse_mode='html')
        await asyncio.sleep(0.4)
    await event.edit('✨')
    await asyncio.sleep(5)
    await event.delete()


async def clock_anim(event: NewMessage.Event):
    if event.fwd_from or event.message.text != '!clock':
        return
    deq = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛"
    for d in deq:
        await asyncio.sleep(0.3)
        await event.edit(d)