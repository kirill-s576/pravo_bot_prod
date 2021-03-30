import os
import django
import telebot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from tg_bot.models import BotUser, Message, Language
from quiz.interface import SimpleInterface, SessionInterface
from tg_bot.logic_module import LogicModule, DjangoRegisterBotLogicModule


class Bot:

    def __init__(self, token: str, logic_module, logic_module_kwargs: dict={}):
        self.token = token
        self.logic_module = logic_module
        self.logic_module_kwargs = logic_module_kwargs
        self.prepared_bot: telebot.TeleBot = self.logic_module(telebot.TeleBot(self.token), **self.logic_module_kwargs).process_with_logic()

    def process_updates(self, updates):
        self.prepared_bot.process_new_updates(updates)

    def start_polling(self):
        self.prepared_bot.polling(none_stop=True)

    def set_web_hook(self, url):
        response = self.prepared_bot.set_webhook(url)
        return response

    def remove_web_hook(self):
        pass


if __name__ == '__main__':
    TOKEN = ""
    logic_module_kwarg = {
        "language_model": Language,
        "message_model": Message,
        "user_model": BotUser,
        "quiz_interface": SessionInterface
    }
    bot = Bot(TOKEN, DjangoRegisterBotLogicModule, logic_module_kwarg)
    print(bot.set_web_hook("https://telbot.refugee.ru/tg_bot"))
