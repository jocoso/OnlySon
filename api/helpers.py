# Helper Functions
import xml.etree.ElementTree as ET
from api.core.IO import IO


def element_to_dict(elem):

    d = {}
    # Add element attributes under '@' prefix in dict
    d.update({f"@{k}": v for k, v in elem.attrib.items()})

    # Add element text if present and not only whitespace
    text = elem.text.strip() if elem.text else ""
    if text:
        d["#text"] = text

    # Recursively add children
    for child in elem:
        child_dict = element_to_dict(child)
        tag = child.tag
        if tag in d:
            # If the tag already exists, convert the list or append
            if not isinstance(d[tag], list):
                d[tag] = [d[tag]]
            d[tag].append(child_dict)
        else:
            d[tag] = child_dict
    return d


def parse_game_objects_to_dict(xml_string):
    from api.actionables import Examinable
    from api.core.game_object import GameObject
    from api.core.IO import IO

    root = ET.fromstring(xml_string)
    game_objects_dict = {}
    io = IO(0.07)

    for go_elem in root.findall("GameObject"):
        go_id = go_elem.get("id")
        go_name = go_elem.get("name")

        actionables = {}
        actionables_elem = go_elem.find("Actionables")
        if actionables_elem is not None:
            for actionable_node in actionables_elem:
                tag = actionable_node.tag
                if tag == "Examinable":
                    message = actionable_node.find("Message").text
                    actionables["examine"] = Examinable(message, io)
        game_objects_dict[go_id] = GameObject(go_id, go_name, actionables)
    return game_objects_dict


def parse_multiple_game_objects(xml_string):
    from api.actionables import Examinable
    from api.core.game_object import GameObject

    root = ET.fromstring(xml_string)
    game_objects = []

    for go_elem in root.findall("GameObject"):
        obj_id = go_elem.attrib.get("id")
        obj_name = go_elem.attrib.get("name")

        actionables = {}
        actionables_elem = go_elem.find("Actionables")
        if actionables_elem is not None:
            for actionable_node in actionables_elem:
                tag = actionable_node.tag
                if tag == "Examinable":
                    message = actionable_node.find("Message").text
                    actionables["examine"] = Examinable(message)
        game_objects.append(GameObject(obj_id, obj_name, actionables))

    return game_objects


def parse_game_object(xml_string):
    from api.actionables import Examinable
    from api.core.game_object import GameObject

    root = ET.fromstring(xml_string)
    obj_id = root.attrib.get("id")

    actionables = {}
    for actionable_node in root.find("Actionables"):
        tag = actionable_node.tag
        if tag == "Examinable":
            message = actionable_node.find("Message").text
            actionables["examine"] = Examinable(message)
        # Add further actionable types here

    return GameObject(obj_id, actionables)


def format_list(items):
    """
    Formats a list of objects as a cohesive, comma-separated string.
    Example: ['apple', 'banana', 'cherry'] -> 'apple, banana, cherry'
    """
    return ", ".join(str(item) for item in items)


def get_choice(
    range_min, range_max, error_msg="You can't pick this option.", caret="> "
):
    """
    Prompts user for input within a specified range and returns the selected option as an integer.
    """
    while True:

        choice = input(caret).strip().lower()
        if choice == "esc":
            return "esc"
        try:
            c = int(choice)
            if range_min <= c <= range_max:
                return c
            print(error_msg)
        except ValueError:
            print("Please enter a valid number or type 'esc' to return to main menu.")


# Simple replacements for missing stringformatter and clicksimulator


def stringformatter(options):
    """
    Displays numbered option list to the player.
    """
    io = IO(0.07)
    for idx, option in enumerate(options, start=1):
        io.type_print(f"{idx}. {option}")


def clicksimulator(min_choice, max_choice, error_msg="Invalid choice."):
    """
    Simulated input choice with validation.
    """
    return get_choice(min_choice, max_choice, error_msg)


def optionBox(gameObject, *params):
    actions = {}
    string_actions = []
    open_box = True

    if gameObject.has_actionable("examine"):
        string_actions.append(f"EXAMINE {gameObject.get_name()}")
        actions[len(actions)] = {
            "method": lambda: gameObject.execute_actionable("examine")
        }
    if gameObject.has_actionable("open"):
        string_actions.append(f"OPEN {gameObject.core.get_name()}")
        actions[len(actions)] = {
            "method": lambda: gameObject.core.execute_actionable("open", *params),
        }
    string_actions.append("CLOSE OPTION BOX")

    def close_box():
        nonlocal open_box
        open_box = False

    actions[len(actions)] = {"method": close_box}

    while open_box:
        stringformatter(string_actions)
        user_choice = clicksimulator(1, len(string_actions))
        if user_choice == "esc":
            break
        actions[user_choice - 1]["method"]()
