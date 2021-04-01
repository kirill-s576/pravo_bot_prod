# Django Environment activation stage
import os
import django
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('/Users/kirill/own-projects/freelance/pravo_bot/environments.env')
load_dotenv(dotenv_path=env_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
#####


from tg_bot.models import BotUser, Message, Language
from quiz.interface import SimpleInterface, SessionInterface
from tg_bot.logic_module import LogicModule, DjangoRegisterBotLogicModule
from tg_bot.interface import Bot


def main():
    pass


if __name__ == '__main__':
    main()
