from django.db import models


class Stage(models.Model):
    """
    Stage of chat logic tree.
    Stage can contain links to other stages.
    """
    title = models.CharField(max_length=255, verbose_name="Stage title")
    button = models.ForeignKey('quiz.QButton',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='stage',
                               verbose_name='Stage link button')
    question = models.ForeignKey('quiz.Message',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='stage',
                                 verbose_name='Stage question')
    messages = models.ManyToManyField("quiz.Message", blank=True, related_name="messages", through="quiz.StageMessage")
    children = models.ManyToManyField('self', symmetrical=False, related_name='related_to')
    is_final = models.BooleanField(default=False, verbose_name="Is final stage")

    __tree: dict = {}
    __children_groups: list = []
    __handled_stages = {}

    def __str__(self):
        return self.title

    @classmethod
    def __rec(cls, stage):
        if not stage["children"]:
            return
        new_list = []
        for el in stage["children"]:
            new_list.append(cls.__handled_stages[el])
        stage["children"] = new_list
        for child in stage["children"]:
            cls.__rec(child)

    @classmethod
    def get_tree(cls, starts_with_id: int = 1):

        stages = cls.objects.all()\
            .prefetch_related('children', 'question', 'button')\
            .values('id', 'title', 'question__default_text', 'button__default_text', 'children__id')
        handled_stages = {}
        for stage in stages:
            if stage["id"] not in handled_stages:
                handled_stages[stage["id"]] = {
                    "id": stage["id"],
                    "title": stage["question__default_text"][:25],
                    "question_text": stage["question__default_text"],
                    "button": stage["button__default_text"],
                    "children": [stage["children__id"]] if stage["children__id"] else []
                }
            else:
                if stage["children__id"]:
                    handled_stages[stage["id"]]["children"].append(stage["children__id"])
        cls.__handled_stages = handled_stages

        cls.__tree = handled_stages[starts_with_id]
        cls.__rec(cls.__tree)
        return cls.__tree

    @property
    def parent(self):
        parents_filter = self.related_to.all()
        if len(parents_filter) > 0:
            return parents_filter.first()
        else:
            return None
