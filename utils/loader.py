import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
###

from quiz.models import (
    Stage,
    Message,
    QButton,
    StageMessage
)
import json


def get_json_as_object(path):
    with open(path, "r") as f:
        return json.loads(f.read())


def fill_messages_and_buttons(data):
    for item_id, item in data.items():
        question: str = item["question"]
        messages: list = item["messages"]
        button: str = item["answer"]
        if question == "?":
            question = "Очень жаль, что нам не удалось вам помочь..."
        try:
            defaults = {
                "title": question[:20],
                "is_hint": False
            }
            Message.objects.get_or_create(default_text=question, defaults=defaults)
        except:
            pass
        for message in messages:
            try:
                defaults = {
                    "title": question[:20],
                    "is_hint": True
                }
                Message.objects.get_or_create(default_text=message, defaults=defaults)
            except:
                pass

        QButton.objects.get_or_create(default_text=button)


def fill_stages(data):
    for item_id, item in data.items():
        title = item["id"]
        question: str = item["question"]
        button: str = item["answer"]
        is_final = False
        if question == "?":
            question = "Очень жаль, что нам не удалось вам помочь..."
        question_model = Message.objects.get(default_text=question)
        try:
            button_model = QButton.objects.get(default_text=button)
        except:
            button_model = None
        if len(item["children"]) == 0:
            is_final = True
        Stage.objects.create(title=title, button=button_model, question=question_model, is_final=is_final)


def relate_stages(data):
    for item_id, item in data.items():
        if len(item["children"]) == 0:
            continue
        stage = Stage.objects.get(title=item_id)
        related_stage_models = Stage.objects.filter(title__in=item["children"])
        stage.children.set(related_stage_models)


def relate_messages_to_stage(data):
    for item_id, item in data.items():
        if len(item["messages"]) == 0:
            continue
        stage = Stage.objects.get(title=item_id)
        for number, message_text in enumerate(item["messages"]):
            if message_text == "?":
                message_text = "Очень жаль, что нам не удалось вам помочь..."
            message = Message.objects.get(default_text=message_text)
            if len(item["children"]) == 0:
                number = len(item["messages"]) - 1 - number
            StageMessage.objects.create(
                stage=stage,
                message=message,
                index=number
            )

def main():
    json_tree: dict = get_json_as_object("/Users/kirill/own-projects/freelance/pravo_bot/dump_3.json")
    json_elements_dict: dict = get_json_as_object("/Users/kirill/own-projects/freelance/pravo_bot/col_el.json")
    # Fill messages
    # Fill buttons
    fill_messages_and_buttons(json_elements_dict)
    # Fill stages
    fill_stages(json_elements_dict)
    # Relate stages
    relate_stages(json_elements_dict)
    # stages = Stage.objects.all()
    # for stage in stages:
    #     stage.children.set([])
    relate_messages_to_stage(json_elements_dict)

def remove_similar_message(removing_id, to_message_id):
    removing_message = Message.objects.get(id=removing_id)
    to_message = Message.objects.get(id=to_message_id)
    stages = Stage.objects.filter(question=removing_message)
    for stage in stages:
        stage.question = to_message
        stage.save()
    relations = StageMessage.objects.filter(message=removing_message)
    for relation in relations:
        relation.message = to_message
        relation.save()
    removing_message.delete()


def clean_all_db():
    Stage.objects.all().delete()
    Message.objects.all().delete()
    QButton.objects.all().delete()
    StageMessage.objects.all().delete()


if __name__ == '__main__':
    main()
    # clean_all_db()
    # remove_similar_message(198, 199)

