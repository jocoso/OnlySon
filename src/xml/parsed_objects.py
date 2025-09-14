import os
import xml.etree.ElementTree as ET
from api.helpers import parse_multiple_game_objects

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
xml_string = ET.tostring(root, encoding="unicode")

parsed_object = parse_multiple_game_objects(xml_string)
