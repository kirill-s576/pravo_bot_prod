import json
import csv
from typing import List
from q_parser import Tree
import re


def get_json_from_csv(csv_path: str, fields: list, default_value) -> List[dict]:
    result = []
    with open(csv_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            dict_row = {field: row.get(field, default_value) for field in fields}
            result.append(dict_row)
    return result


def get_children_dict(data: List[dict]) -> dict:
    result = {int(item["id"]): item for item in data if item["id"] and item["id"] != ""}
    for r in result:
        result[r]["children"] = []
    for component in data:
        if component["id"] and component["id"] != "" and component["parent_id"] and component["parent_id"] != "":
            result[int(component["parent_id"])]["children"].append(int(component["id"]))
    return result


def remove_message_layers(data: dict) -> dict:

    for item_id, item in data.items():
        if item["parent_id"] == "":
            continue
        item_parent_data = data[int(item["parent_id"])]
        item_children_data = [data[child] for child in item["children"]]
        item_answer = item["answer"]
        if item_answer != "tt5" \
            and item_answer != "" \
            and item_answer != "None" \
            and len(item_children_data) == 1\
            and len(item_parent_data["children"]) > 1:
            # Item is the first message in chain
            child_0_data = item_children_data[0]
            child_0_children_ids = child_0_data["children"]
            child_0_children_data = [data[child] for child in child_0_children_ids]
            if len(child_0_children_ids) == 0:
                item["messages"] = []
                item["messages"].append(item_children_data[0]["question"])
                item["children"] = []

            elif len(child_0_children_ids) > 1:
                pass
                # Parent - prev question
                # Child - next question
                # Item - message
                item["messages"] = [item["question"]]
                item["question"] = item_children_data[0]["question"]
                item["children"] = item_children_data[0]["children"]

            elif len(child_0_children_ids) == 1:
                child_1_data = child_0_children_data[0]
                child_1_children_ids = child_1_data["children"]
                child_1_children_data = [data[child] for child in child_1_children_ids]
                if len(child_1_children_ids) == 0:
                    pass
                    item["messages"] = []
                    item["messages"].append(item_children_data[0]["question"])
                    item["messages"].append(child_0_children_data[0]["question"])
                    item["children"] = []

                elif len(child_1_children_ids) > 1:
                    pass
                    # item_parent_data - prev question
                    # child_0_children_data[0] - next question
                    # Item - message
                    # item_children_data[0] - Extended message
                    item["messages"] = [item["question"]]
                    item["messages"].append(item_children_data[0]["question"])
                    item["question"] = child_0_children_data[0]["question"]
                    item["children"] = child_0_children_data[0]["children"]
                elif len(child_1_children_ids) == 1:
                    child_2_data = child_1_children_data[0]
                    child_2_children_ids = child_2_data["children"]
                    if len(child_2_children_ids) > 1:
                        # item_parent_data - prev question
                        # child_1_children_data[0] - next question
                        # Item - message
                        # item_children_data[0] - Extended message
                        # child_0_children_data[0] - Extended message
                        item["messages"] = [item["question"]]
                        item["messages"].append(item_children_data[0]["question"])
                        item["messages"].append(child_0_children_data[0]["question"])
                        item["question"] = child_1_children_data[0]["question"]
                        item["children"] = child_1_children_data[0]["children"]
        else:
            item["messages"] = []
    for item_id, item in data.items():
        try:
            item["messages"].remove("Result")
        except ValueError:
            pass
        except KeyError:
            item["messages"] = []
    return data


def prepare_to_tree(children_dict) -> List[dict]:
    result = []
    for id, item in children_dict.items():
        children = item["children"]
        new_item = {
            "id": int(id),
            "title": item["question"][:20],
            "question": item["question"],
            "answer": item["answer"],
            "messages": item.get("messages", []),
            "parent_id": item["parent_id"],
            "children": children
        }
        result.append(new_item)
    return result


if __name__ == '__main__':
    csv_data = get_json_from_csv("all_q.csv",
                                 fields=["id", "parent_id", "title", "question", "answer"],
                                 default_value="")
    children_dict = get_children_dict(csv_data)
    children_dict_without_message_layers = remove_message_layers(children_dict)

    prepared_list = prepare_to_tree(children_dict_without_message_layers)
    tree = Tree(prepared_list)
    prepared_tree = tree.get_tree(1)

    string_tree = str(prepared_tree)
    ids = re.findall(r'\'id\':\s(\d+?),', string_tree)
    int_ids = [int(id) for id in ids]
    for_remove_ids = []
    for key, value in children_dict_without_message_layers.items():
        if key not in int_ids:
            for_remove_ids.append(key)

    for id in for_remove_ids:
        del children_dict_without_message_layers[id]

    with open("col_el_1.json", "w") as f:
        f.write(json.dumps(children_dict_without_message_layers, ensure_ascii=False, indent=4))

    with open("dump_3.json", "w") as f:
        f.write(json.dumps(prepared_tree, ensure_ascii=False, indent=4))
