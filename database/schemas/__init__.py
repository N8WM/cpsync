"""JSON Validator Schema Loader"""

import json
from typing import Any


def load_json(file_path: str) -> dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)


term = load_json("database/schemas/terms.json")
building = load_json("database/schemas/buildings.json")
room = load_json("database/schemas/rooms.json")
college = load_json("database/schemas/colleges.json")
subject = load_json("database/schemas/subjects.json")
course = load_json("database/schemas/courses.json")
section = load_json("database/schemas/sections.json")
ge = load_json("database/schemas/ges.json")
instructor = load_json("database/schemas/instructors.json")
