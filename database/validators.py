"""Validators for the database collections"""

term_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Term Object Validation",
        "additionalProperties": False,
        "required": ["_id", "path", "start", "end", "season", "year"],
        "properties": {
            "_id": {
                "bsonType": "string",
                "description": "term id",
            },
            "start": {
                "bsonType": "date",
                "description": "the term's start date",
            },
            "end": {
                "bsonType": "date",
                "description": "the term's end date",
            },
            "buildings": {
                "bsonType": "array",
                "description": "an array of building ids associated with the term",
                "items": { "bsonType": "string" },
            },
            "colleges": {
                "bsonType": "array",
                "description": "an array of college ids associated with the term",
                "items": { "bsonType": "string" },
            },
            "path": {
                "bsonType": "string",
                "description": "the path to the term's page (useful for end users)",
            }
        }
    }
}

building_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Building Object Validation",
        "additionalProperties": False,
        "required": ["_id", "term_id", "number", "name", "rooms", "path"],
        "properties": {
            "_id": {
                "bsonType": "string",
                "description": "building id",
            },
            "term_id": {
                "bsonType": "string",
                "description": "the term id associated with the building",
            },
            "number": {
                "bsonType": "string",
                "description": "the building number",
            },
            "name": {
                "bsonType": "string",
                "description": "the building's friendly name",
            },
            "rooms": {
                "bsonType": "array",
                "description": "an array of room ids for rooms in the building",
                "items": { "bsonType": "string" },
            },
            "path": {
                "bsonType": "string",
                "description": "the path to the building's page (useful for end users)",
            }
        }
    }
}

room_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Room Object Validation",
        "additionalProperties": False,
        "required": [
            "_id", "term_id", "building_id", "number", "sections",
            "schedule_path", "registered_location_capacity", "path"
        ],
        "properties": {
            "_id": {
                "bsonType": "string",
                "description": "room id",
            },
            "term_id": {
                "bsonType": "string",
                "description": "the term id associated with the room",
            },
            "building_id": {
                "bsonType": "string",
                "description": "the building id of the building the room is in",
            },
            "number": {
                "bsonType": "string",
                "description": "the room number",
            },
            "sections": {
                "bsonType": "array",
                "description": "an array of section ids for sections held in the room",
                "items": { "bsonType": "string" },
            },
            "schedule_path": {
                "bsonType": "string",
                "description": "the path to the room's schedule page (useful for end users)",
            },
            "registered_location_capacity": {
                "bsonType": "int",
                "description": "the room's registered location capacity",
            },
            "path": {
                "bsonType": "string",
                "description": "the path to the room's page (useful for end users)",
            }
        }
    }
}

college_validator = {}          # TODO: Add  college   validator

course_validator = {}           # TODO: Add   course   validator

section_validator = {}          # TODO: Add  section   validator

ge_validator = {}               # TODO: Add     ge     validator

instructor_validator = {}       # TODO: Add instructor validator
