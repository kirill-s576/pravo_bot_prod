from abc import ABC, abstractmethod
from .models import Session, Language, Stage
from typing import List


SESSION_LIFETIME = 1000


class NextStageError(Exception):
    pass


class StageResponseSerializer:
    """

    """
    def __init__(self, stage, language: Language = None):
        self.stage = stage
        self.language = language
        self.id: int = None
        self.button: str = None
        self.question: str = None
        self.children: list = []
        """ [{"id": ***, "button": ***}, {...}, ...] """
        self.messages: list = []
        """ [{"index": ***, "text": ***}, {...}, ...] """
        self.__set_fields()

    def __set_fields(self):
        self.id = self.stage.id
        if self.language:
            self.button = self.stage.button.get_translate(self.language) if self.stage.button else None
            self.question = self.stage.question.get_translate(self.language) if self.stage.question else None
        else:
            self.button = self.stage.button.default_text if self.stage.button else None
            self.question = self.stage.question.default_text if self.stage.question else None
        for child in self.stage.children.all():
            self.children.append({
                "id": child.id,
                "button": child.button.get_translate(self.language) if self.language else child.button.default_text
            })
        for message in self.stage.stagemessage_set.all():
            self.messages.append({
                "index": message.index,
                "text": message.message.get_translate(self.language) if self.language else message.message.default_text
            })

    def json(self):
        return {
            "id": self.id,
            "button": self.button,
            "question": self.question,
            "children": self.children,
            "messages": self.messages
        }


class BasicInterface(ABC):
    """
    This is abstract interface...
    """
    def __init__(self, lang_code: str, main_stage_id: int):
        self.lang_code = lang_code
        self.main_stage_id = main_stage_id
        self.language_model = self._get_language_model()
        self.main_stage_model = self._get_main_stage_model()

    def _get_language_model(self):
        try:
            lang = Language.objects.get(label=self.lang_code)
        except:
            lang = None
        return lang

    def _get_main_stage_model(self):
        return Stage.objects.get(id=self.main_stage_id)

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def get_next_stage(self, from_stage_id, to_stage_id):
        pass

    @classmethod
    def get_languages(cls):
        languages = Language.objects.all().values("label", "name")
        return languages


class SimpleInterface(BasicInterface):

    def restart(self) -> StageResponseSerializer:
        stage = self.main_stage_model
        serializer = StageResponseSerializer(stage, self.language_model)
        return serializer

    def get_next_stage(self, from_stage_id, to_stage_id) -> StageResponseSerializer:
        next_stage = Stage.objects.get(id=to_stage_id)
        if next_stage.parent:
            if next_stage.parent.id == from_stage_id:
                return StageResponseSerializer(next_stage, self.language_model)
            else:
                raise NextStageError("Parent stage hasn't this child.")
        else:
            return StageResponseSerializer(next_stage, self.language_model)


class SessionInterface(SimpleInterface):

    def __init__(self, lang_code, main_stage_id, user_id, user_type):
        super().__init__(lang_code, main_stage_id)
        self.user_id = user_id
        self.user_type = user_type
        self.session, self.is_new_session = self.__get_or_create_session()

    def __get_or_create_session(self):
        sessions_time_filter = Session.objects.filter_for_last(SESSION_LIFETIME)
        user_sessions_filter = sessions_time_filter.filter(user_id=self.user_id, finished=False)
        if len(user_sessions_filter) == 0:
            return Session.objects.create(
                user_id=self.user_id,
                user_from=self.user_type,
                language=self.language_model
            ), True
        else:
            return user_sessions_filter.last(), False

    def restart(self):
        first_stage_response = super().restart()
        self.session.clear_steps()
        self.session.add_step(first_stage_response.id)
        return first_stage_response

    def get_next_stage(self, from_stage_id, to_stage_id):
        next_stage_response = super().get_next_stage(from_stage_id=from_stage_id, to_stage_id=to_stage_id)
        self.session.add_step(to_stage_id)
        return next_stage_response

    def get_previous_stage(self):
        prev_stage_id = self.session.pop_step()
        previous_stage = Stage.objects.get(id=prev_stage_id)
        serializer = StageResponseSerializer(previous_stage, self.language_model)
        return serializer

    def get_report(self) -> List[StageResponseSerializer]:
        stages = Stage.objects.filter(id__in=self.session.steps)
        objects = dict([(obj.id, obj) for obj in stages])
        sorted_objects = [objects[id] for id in self.session.steps]
        serializers = [StageResponseSerializer(stage, self.language_model) for stage in sorted_objects]
        return serializers
