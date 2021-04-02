import telebot
from abc import ABC, abstractmethod
from quiz.interface import BasicInterface
import traceback


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

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    @abstractmethod
    def process_with_logic(self) -> telebot.TeleBot:
        bot = self.bot

        @bot.message_handler(commands=["start"])
        def start(message):
            bot.reply_to(message, "Test Message")

        return bot


class DjangoRegisterBotLogicModule(LogicModule):

    def __init__(self, bot, language_model, message_model, user_model, quiz_interface, source: str = 'telegram', **kwargs):
        super().__init__(bot)
        self.language_model = language_model
        self.message_model = message_model
        self.user_model = user_model
        self.quiz_interface = quiz_interface
        self.source = source
        self.user = None

    def __middleware(self, message):
        """
        Middleware layer.
        We should use it in each bot handler.
        """
        defaults = {
            "user_name": getattr(message.chat, "username", "-"),
            "first_name": getattr(message.chat, "first_name", "-"),
            "last_name": getattr(message.chat, "last_name", "-")
        }
        user, created = self.user_model.objects.get_or_create(
            chat_id=message.chat.id,
            defaults=defaults
        )
        self.user = user
        if created:
            self.ask_language(message.chat.id)

    def get_translated_message(self, message_label):
        """
        Returns translated message by message label
        """
        message_filter = self.message_model.objects.filter(label=message_label)
        if message_filter:
            translation = message_filter[0].get_translation(self.user.language)
            return translation
        else:
            return None

    def ask_language(self, chat_id):
        """

        """
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
            self.send_menu(chat_id)

    def send_menu(self, chat_id):

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(
            telebot.types.KeyboardButton(self.get_translated_message("change_language_button")),
            telebot.types.KeyboardButton(self.get_translated_message("about_button"))
        )
        markup.row(
            telebot.types.KeyboardButton(self.get_translated_message("important_button"))
        )
        markup.row(
            telebot.types.KeyboardButton(self.get_translated_message("quiz_button"))
        )

        self.bot.send_message(chat_id, self.get_translated_message("menu_message"), reply_markup=markup)

    def send_about(self, chat_id):
        self.bot.send_message(chat_id, self.get_translated_message("about"))

    def send_important(self, chat_id):
        self.bot.send_message(chat_id, self.get_translated_message("important"))

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
        """
        This method appends logic to bot.
        """
        bot = self.bot


        @bot.message_handler(commands=["menu"])
        @end_of_logic_catcher
        def menu(message):
            """ /menu command handler """
            self.__middleware(message)
            self.send_menu(message.chat.id)

        @bot.message_handler(commands=["about"])
        @end_of_logic_catcher
        def about(message):
            """ /about command handler """
            self.__middleware(message)
            self.send_about(message.chat.id)

        @bot.message_handler(commands=["important"])
        @end_of_logic_catcher
        def important(message):
            """ /about command handler """
            self.__middleware(message)
            self.send_important(message.chat.id)

        @bot.message_handler(commands=["quiz"])
        @end_of_logic_catcher
        def quiz_restart(message):
            self.__middleware(message)
            """ Start or restart quiz """
            if not self.user.language:
                self.ask_language(message.chat.id)
            lang_label = self.user.language.label
            quiz = self.quiz_interface(lang_label, 30001, message.chat.id, self.source)
            stage = quiz.restart()
            markup = telebot.types.InlineKeyboardMarkup()
            for child in stage.children:
                markup.row(telebot.types.InlineKeyboardButton(child["button"],
                                                              callback_data=f"stage:{stage.id}:{child['id']}"))
            bot.delete_message(message.chat.id, self.user.memory_message_id)
            sended_message = self.bot.send_message(
                message.chat.id,
                stage.question,
                reply_markup=markup,
                parse_mode="html"
            )
            messages_memory = dict()
            messages_memory[str(stage.id)] = [sended_message.message_id]
            self.user.messages_memory = messages_memory
            self.user.save()

        @bot.message_handler(commands=["start"])
        @end_of_logic_catcher
        def start(message):
            """ /start command handler """
            self.__middleware(message)
            self.send_greeting(message.chat.id)
            quiz_restart(message)

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
            """ Send next step or result """
            self.__middleware(call.message)

            # Remove question with answers
            self.bot.delete_message(call.message.chat.id, call.message.message_id)

            # Parse callback_data
            from_stage_id = int(call.data.split(":")[1])
            to_stage_id = int(call.data.split(":")[2])

            # Initialize quiz interface.
            lang_label = self.user.language.label
            quiz = self.quiz_interface(lang_label, 30001, call.message.chat.id, self.source)

            # Get user memory slot.
            messages_memory = self.user.messages_memory

            if to_stage_id != 0:

                # Get next stage for view
                stage = quiz.get_next_stage(from_stage_id, to_stage_id)

                # Reply question and user answer in pretty format.
                keyboard_buttons = call.message.reply_markup.keyboard
                keyboard_button = list(filter(lambda button: button[0].callback_data == call.data, keyboard_buttons))[0]
                sended_message = self.bot.send_message(
                    call.message.chat.id,
                    "⁉️" + call.message.text + "\n\n" + "✅" + keyboard_button[0].text
                )
                try:
                    messages_memory[str(from_stage_id)].append(sended_message.message_id)
                except:
                    messages_memory[str(from_stage_id)] = [sended_message.message_id]
            else:

                # Get previous stage for view
                stage, removed_stage_id = quiz.get_previous_stage()

                # Remove messages for removed_stage.
                for_remove_messages = messages_memory.get(str(removed_stage_id), [])
                for message_id in for_remove_messages:
                    try:
                        self.bot.delete_message(call.message.chat.id, message_id)
                    except:
                        pass
                for_remove_messages = messages_memory.get(str(stage.id), [])
                for message_id in for_remove_messages:
                    try:
                        self.bot.delete_message(call.message.chat.id, message_id)
                    except:
                        pass
                del messages_memory[str(stage.id)]

            # Get info messages, which must be after question.
            messages = list(stage.messages)
            messages.sort(key=lambda x: x["index"])

            info_text = "📖 -  "

            if len(stage.children) != 0:

                # Send info message.
                if len(messages) > 0:
                    for message in messages:
                        info_text += message["text"] + "\n\n"
                    sended_message = self.bot.send_message(call.message.chat.id, info_text, parse_mode="html")
                    try:
                        messages_memory[str(stage.id)].append(sended_message.message_id)
                    except:
                        messages_memory[str(stage.id)] = [sended_message.message_id]

                # Send question with keyboard
                markup = telebot.types.InlineKeyboardMarkup()
                for child in stage.children:
                    markup.row(telebot.types.InlineKeyboardButton(child["button"],
                                                                  callback_data=f"stage:{stage.id}:{child['id']}"))
                if len(stage.children) != 0 and stage.id != 30001:
                    markup.row(
                        telebot.types.InlineKeyboardButton("🔙 Back",
                                                           callback_data=f"stage:{stage.id}:0")
                    )
                sended_question = self.bot.send_message(call.message.chat.id, stage.question, reply_markup=markup, parse_mode="html")
                self.user.memory_message_id = sended_question.message_id
            else:
                for message in messages:
                    info_text += message["text"] + "\n\n"
                if stage.question:
                    info_text += stage.question + "\n\n"
                sended_message = self.bot.send_message(call.message.chat.id, info_text, parse_mode="html")
                try:
                    messages_memory[str(stage.id)].append(sended_message.message_id)
                except:
                    messages_memory[str(stage.id)] = [sended_message.message_id]

            self.user.messages_memory = messages_memory
            self.user.save()

        @bot.message_handler(func=lambda message: True, content_types=['text'])
        def menu_handler(message):
            db_message = self.message_model.get_message_by_translate_text(message.text)
            if message:
                label = db_message.label
                if label == "quiz_button":
                    quiz_restart(message)
                elif label == "about_button":
                    about(message)
                elif label == "important_button":
                    important(message)
                elif label == "change_language_button":
                    self.ask_language(message.chat.id)
            else:
                bot.send_message(message.chat.id, "Даже и не знаю, что на это ответить...")
        return bot




