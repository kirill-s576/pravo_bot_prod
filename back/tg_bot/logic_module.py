import telebot
from abc import ABC, abstractmethod
from quiz.interface import BasicInterface


class EndOfLogicException(Exception):
    pass


def end_of_logic_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except EndOfLogicException:
            pass
        except Exception as e:
            raise e
        return func
    return wrapper


class LogicModule(ABC):

    def __init__(self, bot: telebot.TeleBot, **kwargs):
        self.bot = bot

    @abstractmethod
    def process_with_logic(self) -> telebot.TeleBot:
        bot = self.bot

        @bot.message_handler(commands=["start"])
        def start(message):
            bot.reply_to(message, "Test Message")

        return bot


class DjangoRegisterBotLogicModule(LogicModule):

    def __init__(self, bot, language_model, message_model, user_model, quiz_interface, **kwargs):
        super().__init__(bot)
        self.language_model = language_model
        self.message_model = message_model
        self.user_model = user_model
        self.quiz_interface = quiz_interface
        self.user = None

    def __middleware(self, message):
        defaults = {
            "user_name": message.chat.username,
            "first_name": message.chat.first_name,
            "last_name": message.chat.last_name
        }
        user, created = self.user_model.objects.get_or_create(
            chat_id=message.chat.id,
            defaults=defaults
        )
        self.user = user
        if created:
            self.ask_language(message.chat.id)

    def get_translated_message(self, message_label):
        message_filter = self.message_model.objects.filter(label=message_label)
        if message_filter:
            translation = message_filter[0].get_translation(self.user.language)
            return translation
        else:
            return None

    def ask_language(self, chat_id):
        markup = telebot.types.InlineKeyboardMarkup()
        for language in self.languages:
            markup.row(telebot.types.InlineKeyboardButton(
                language["name"],
                callback_data=f"lang:{language['label']}"
            ))
        self.bot.send_message(chat_id, "Choose Language", reply_markup=markup)
        raise EndOfLogicException

    def save_selected_language(self, chat_id, language_label):
        lang = self.language_model.objects.get(label=language_label)
        self.user.language = lang
        self.user.save()

    def send_greeting(self, chat_id):
        greeting_text = self.get_translated_message("greeting")
        if greeting_text:
            self.bot.send_message(chat_id, greeting_text)
        raise EndOfLogicException

    @property
    def languages(self):
        """
        Returns languages from database in format:
        [
            {
                "label": "EN",
                "name": "English"
            }, ...
        ]
        """
        queryset = self.language_model.objects.all()
        return queryset.values("name", "label")

    def process_with_logic(self) -> telebot.TeleBot:

        bot = self.bot

        @bot.message_handler(commands=["start"])
        @end_of_logic_catcher
        def start(message):
            self.__middleware(message)
            if not self.languages:
                bot.send_message(message.chat.id, "Technical problems")

        @bot.callback_query_handler(func=lambda call: "lang:" in call.data)
        @end_of_logic_catcher
        def language_handler(call):
            self.__middleware(call.message)
            lang_label = call.data.split("lang:")[1]
            self.save_selected_language(call.message.chat.id, lang_label)
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.send_greeting(call.message.chat.id)

        @bot.callback_query_handler(func=lambda call: "stage:" in call.data)
        @end_of_logic_catcher
        def quiz_handler(call):
            """ Send next step or result for message """
            self.__middleware(call.message)
            # self.bot.delete_message(call.message.chat.id, call.message.message_id)
            from_stage_id = int(call.data.split(":")[1])
            to_stage_id = int(call.data.split(":")[2])
            lang_label = self.user.language.label
            quiz = self.quiz_interface(lang_label, 30001, call.message.chat.id, "site")
            stage = quiz.get_next_stage(from_stage_id, to_stage_id)

            messages = list(stage.messages)
            messages.sort(key=lambda x: x["index"])

            if len(stage.children) != 0:
                for message in messages:
                    self.bot.send_message(call.message.chat.id, message["text"], parse_mode="html")

            markup = telebot.types.InlineKeyboardMarkup()
            for child in stage.children:
                markup.row(telebot.types.InlineKeyboardButton(child["button"], callback_data=f"stage:{stage.id}:{child['id']}"))
            self.bot.send_message(call.message.chat.id, stage.question, reply_markup=markup, parse_mode="html")

            if len(stage.children) == 0:
                for message in messages:
                    self.bot.send_message(call.message.chat.id, message["text"],parse_mode="html")

        @bot.message_handler(commands=["quiz"])
        @end_of_logic_catcher
        def quiz_restart(message):
            self.__middleware(message)
            """ Start or restart quiz """
            if not self.user.language:
                self.ask_language(message.chat.id)
            lang_label = self.user.language.label
            quiz = self.quiz_interface(lang_label, 30001, message.chat.id, "site")
            stage = quiz.restart()
            markup = telebot.types.InlineKeyboardMarkup()
            for child in stage.children:
                markup.row(telebot.types.InlineKeyboardButton(child["button"], callback_data=f"stage:{stage.id}:{child['id']}"))
            self.bot.send_message(message.chat.id, stage.question, reply_markup=markup, parse_mode="html")
        return bot