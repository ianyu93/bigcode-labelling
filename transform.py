import argparse
import json
import re
import xml.etree.ElementTree as ET


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", help="tasks data file by annotators")
    parser.add_argument("code", help="original code data")
    return parser.parse_args()


def post_entities(entities):
    def fn(entity):
        return f'    <Label value="{entity}"/>'

    return "\n".join([fn(entity) for entity in entities])


def get_index(task_name: str) -> int:
    return int(re.match(r"Code (\d{1,})", task_name)[1]) - 1


def main():
    args = get_args()

    with open(args.tasks, "r") as f:
        tasks = json.load(f)["batch"]["tasks"]

    with open(args.code, "r") as f:
        data = json.load(f)

    pre_annotated_data = []

    # Each task is a data point, convert to expected format
    # See format example here:
    # https://labelstud.io/guide/predictions.html#Example-JSON-2
    for task in tasks:
        index = get_index(task["task_name"])

        curr = {
            "data": {"text": data[index]},
            "predictions": [{"model_version": "one", "score": 0.5}],
        }
        result = [
            {
                "id": str(label["id"]),
                "from_name": "label",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "start": label["start_offset"],
                    "end": label["end_offset"],
                    "score": 0.7,
                    "text": label["text"],
                    "labels": [label["label"]],
                },
            }
            for label in task["labels"]
        ]
        curr["predictions"][0]["result"] = result
        pre_annotated_data.append(curr)

    # Get interface code based on what entities are in the data
    interface_code = f"""
    <View>
    <Labels name="label" toName="text">
    {post_entities({label['label'] for task in tasks for label in task['labels']})}
    </Labels>
    <TextArea name="annotation review notes" 
                value="Note: Put any notes to the annotation here"
                editable="true"
                showSubmitButton="true"
                rows="3"
                ></TextArea>
    <Text name="text" value="$text"/>
    </View>
    """
    with open("pre_annotated_data.json", "w") as outfile:
        json.dump(pre_annotated_data, outfile)

    # Parse the XML string and create the root element
    root = ET.fromstring(interface_code)

    # Create the ElementTree object
    tree = ET.ElementTree(root)

    # Write the XML tree to a file
    tree.write("config.xml")


if __name__ == "__main__":
    main()
