import os
import xml.etree.ElementTree as ET
from api.helpers import parse_game_objects_to_dict

# Get directory where this __init__.py files lives
here = os.path.dirname(__file__)

# XML file is in same folder
xml_path = os.path.join(here, "Objects.xml")

# Ensure files exits
if not os.path.isfile(xml_path):
    raise FileNotFoundError(f"Missing XML file at {xml_path}")

# Parse the XML file content
tree = ET.parse(xml_path)
root = tree.getroot()

# Convert the root back to a string as expected by your parser function
xml_string = ET.tostring(root, encoding="unicode")

# Use your helper function to parser XML string into dictionary of game Objects
parsed_object = parse_game_objects_to_dict(xml_string)
