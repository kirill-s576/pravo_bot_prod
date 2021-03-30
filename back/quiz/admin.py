from django.contrib import admin
from .models import Stage
from .models import QButton, Message
from .models import MessageTranslation, QButtonTranslation
from .models import Language
from .models import StageMessage
from .models import Session


admin.site.register(QButton)
admin.site.register(MessageTranslation)
admin.site.register(QButtonTranslation)
admin.site.register(Language)


class StageAdmin(admin.ModelAdmin):
    filter_horizontal = ('children', )


admin.site.register(Message)
admin.site.register(Stage, StageAdmin)
admin.site.register(StageMessage)
admin.site.register(Session)