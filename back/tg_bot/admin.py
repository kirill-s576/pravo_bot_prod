from django.contrib import admin
from .models import Language
from .models import BotUser
from .models import Message
from .models import MessageTranslate


admin.site.register(Language)
admin.site.register(BotUser)
admin.site.register(Message)
admin.site.register(MessageTranslate)

