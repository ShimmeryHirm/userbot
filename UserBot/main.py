import logging

import config
from core.handlers import register_chat_handlers, register_pm_handlers

logging.basicConfig(level=logging.INFO)


def main():
    register_pm_handlers()
    register_chat_handlers()
    print('[+]: BOT STARTED')
    config.USERBOT.run_until_disconnected()


if __name__ == '__main__':
    main()
