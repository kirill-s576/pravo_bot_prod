import telebot


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

    def get_web_hook_info(self):
        response = self.prepared_bot.get_webhook_info()
        return response

    def remove_web_hook(self):
        response = self.prepared_bot.remove_webhook()
        return response
