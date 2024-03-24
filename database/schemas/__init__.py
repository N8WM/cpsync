"""JSON Validator Schema Loader"""

import json
from typing import Any


__cache: dict[str, dict[str, Any]] = {}


def __load_json(file_path: str) -> dict[str, Any]:
    if file_path not in __cache:
        with open(file_path, "r") as file:
            __cache[file_path] = {"$jsonSchema": json.load(file)}
    return __cache[file_path]


term = __load_json("database/schemas/terms.json")
building = __load_json("database/schemas/buildings.json")
room = __load_json("database/schemas/rooms.json")
college = __load_json("database/schemas/colleges.json")
subject = __load_json("database/schemas/subjects.json")
course = __load_json("database/schemas/courses.json")
section = __load_json("database/schemas/sections.json")
# ge = __load_json("database/schemas/ges.json")
instructor = __load_json("database/schemas/instructors.json")

schema_list = json.dumps(
    {
        "terms": term,
        "buildings": building,
        "rooms": room,
        "colleges": college,
        "subjects": subject,
        "courses": course,
        "sections": section,
        # "ges": ge,
        "instructors": instructor,
    },
    indent=2,
)
