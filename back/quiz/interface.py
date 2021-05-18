from abc import ABC, abstractmethod
from django.db.models.query import QuerySet
from .models import Session, Language, Stage
from typing import List
import datetime
from django.db.models import Count
from django.db.models.functions import TruncDate

SESSION_LIFETIME = 1000


class NextStageError(Exception):
    pass


class StageResponseSerializer:
    """

    """
    def __init__(self, stage: Stage, language: Language = None):
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
        removed_stage_id = self.session.pop_step()
        prev_stage_id = self.session.steps[-1]
        previous_stage = Stage.objects.get(id=prev_stage_id)
        serializer = StageResponseSerializer(previous_stage, self.language_model)
        return serializer, removed_stage_id

    def get_report(self) -> List[StageResponseSerializer]:
        stages = Stage.objects.filter(id__in=self.session.steps)
        objects = dict([(obj.id, obj) for obj in stages])
        sorted_objects = [objects[id] for id in self.session.steps]
        serializers = [StageResponseSerializer(stage, self.language_model) for stage in sorted_objects]
        return serializers

    def finish_session(self):
        self.session.finished = True
        self.session.save()


class SessionStatistic:

    def __init__(self, sessions_queryset: QuerySet[Session]):
        self.session_queryset = sessions_queryset

    @property
    def total_sessions_count(self) -> int:
        """
        Total sessions count
        """
        count = self.session_queryset.count()
        return count

    @property
    def finished_sessions_count(self) -> int:
        """
        Finished sessions count
        """
        count = self.session_queryset.filter(finished=True).count()
        return count

    @property
    def sessions_count_by_language(self) -> List[dict]:
        """
        Is this function put on sessions count for each language
        Returns data in format
        [
            {
                "language_id": 1,
                "sessions_count": 15,
                "sessions_count_percent": 15
            }, ...
        ]
        """
        languages = self.session_queryset.values_list("language", flat=True)
        languages_list = list(languages)
        all_length = len(languages_list)
        unique = list(set(languages_list))
        languages_final_list = [
            {
                "language_id": item,
                "sessions_count": list(languages_list).count(item),
                "sessions_count_percent": round(list(languages_list).count(item) / all_length * 100, 2)
            } for item in unique
        ]
        return languages_final_list

    @property
    def sessions_per_day(self):
        stat = self.session_queryset \
            .annotate(date=TruncDate('created_at')) \
            .values('date') \
            .annotate(total=Count('id')) \
            .values('date', 'total')
        for el in stat:
            el["date"] = el["date"].isoformat()
        return list(stat)

    def get_json(self):
        return {
            "total_sessions_count": self.total_sessions_count,
            "finished_sessions_count": self.finished_sessions_count,
            "sessions_count_by_language": self.sessions_count_by_language,
            "sessions_per_day": self.sessions_per_day
        }


class PeriodSessionStatistic(SessionStatistic):

    def __init__(self, date_from: datetime.datetime, date_to: datetime.datetime):
        queryset = Session.objects.filter(created_at__gte=date_from, created_at__lte=date_to)
        super().__init__(queryset)


class SessionUserInterface:

    def __init__(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id
        self.session_model = self.__get_session_model()

    @property
    def __user_sessions_queryset(self):
        return Session.objects.filter(user_id=self.user_id)

    def __get_session_model(self):
        try:
            return self.__user_sessions_queryset.get(id=self.session_id)
        except:
            return None

    def get_all_sessions(self):
        return self.__user_sessions_queryset

    def get_stages_queryset(self):
        if not self.session_model:
            return []
        stage_ids = self.session_model.steps
        stages_queryset = Stage.objects.filter(id__in=stage_ids)
        output_stages = []
        for stage_id in stage_ids:
            needed_stage = list(filter(lambda x: x.id == stage_id, stages_queryset))[0]
            output_stages.append(needed_stage)
        return output_stages

    def get_language_model(self):
        if self.session_model:
            return self.session_model.language
        else:
            return None


