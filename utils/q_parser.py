import csv
from pprint import pprint
import json



el_list = []
ids_dict = {}
parents_dict = {}


with open("all_q.csv", newline="") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        ids_dict[row['id']] = {
            "id": row['id'],
            "title": row["question"][:30] + "...",
            "question": row['question'],
            "answer": row['answer'],
            "parent_id": row['parent_id']
        }

        el_list.append({
            "id": row['id'],
            "title": row["question"][:30] + "...",
            "question": row['question'],
            "answer": row['answer'],
            "parent_id": row['parent_id']
        })

        if row['parent_id'] not in parents_dict:
            parents_dict[row['parent_id']] = [{
                "id": row['id'],
                "title": row["question"][:30] + "...",
                "question": row['question'],
                "answer": row['answer'],
                "parent_id": row["parent_id"],
            }]
        else:
            parents_dict[row['parent_id']].append({
                "id": row['id'],
                "title": row["question"][:30] + "...",
                "question": row['question'],
                "answer": row['answer'],
                "parent_id": row["parent_id"]
            })

print(len(ids_dict))
print(len(parents_dict))

final_list = []
messages_list = []


for key, value in ids_dict.items():
    children = parents_dict.get(key, [])
    if not children:
        continue
    if "tt5" in value["answer"] and value["id"] != "1":
        continue
    if "tt5" in children[0]["answer"] or children[0]["answer"] == "" or children[0]["answer"] == "None":
        messages_list.append(
            {
                "question_id": value["id"],
                "question_text": value["question"][:20],
                "message_text": children[0]["question"][:20]
            }
        )
        children = parents_dict.get(children[0]["id"], [])

    value["children"] = [child["id"] for child in children]
    final_list.append(value)


class Tree:

    def __init__(self, data):
        self.data = data
        self.__tree: dict = {}
        self.__children_groups: list = []
        self.__handled_stages = {}

    def __rec(self, stage):
        if not stage["children"]:
            return
        new_list = []
        for el in stage["children"]:
            try:
                new_list.append(self.__handled_stages[el])
            except:
                pass
        stage["children"] = new_list
        for child in stage["children"]:
            self.__rec(child)

    def get_tree(self, starts_with_id: int = 1):

        # stages = cls.objects.all() \
        #     .prefetch_related('question__stages', 'question__text', 'button') \
        #     .values('id', 'title', 'question__text__default_text', 'button__default_text', 'question__stages__id')

        stages = self.data
        handled_stages = {}
        for stage in stages:
            if stage["id"] not in handled_stages:
                handled_stages[stage["id"]] = {
                    "id": stage["id"],
                    "title": stage["title"],
                    "question_text": stage["question"],
                    "button": stage["answer"],
                    "messages": stage["messages"],
                    "children": stage["children"]
                }

        self.__handled_stages = handled_stages
        self.__tree = handled_stages[starts_with_id]
        self.__rec(self.__tree)
        return self.__tree


if __name__ == '__main__':

    tree = Tree(final_list)
    jsn = tree.get_tree("1")
    #

    with open("dump_1.json", "w") as f:
        f.write(json.dumps(jsn, ensure_ascii=False))


    with open("messages_list.json", "w") as f:
        f.write(json.dumps(messages_list, ensure_ascii=False))