"""Validators for the database collections"""

term_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Term Object Validation",
        "required": ["id", "path", "start", "end", "season", "year"],
        "properties": {
            "id": {
                "bsonType": "string",
                "description": "'id' must be a string and is required",
            },
            "path": {
                "bsonType": "string",
                "description": "'path' must be a string and is required",
            },
            "start": {
                "bsonType": "int",
                "description": "'start' must be an int and is required",
            },
            "end": {
                "bsonType": "int",
                "description": "'end' must be an int and is required",
            },
        },
    }
}

college_validator = {  # TODO
    "$jsonSchema": {
        "bsonType": "object",
        "title": "College Object Validation",
        "required": [],
        "properties": {},
    }
}

department_validator = {  # TODO
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Department Object Validation",
        "required": [],
        "properties": {},
    }
}

course_validator = {  # TODO
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Course Object Validation",
        "required": [],
        "properties": {},
    }
}

section_validator = {  # TODO
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Section Object Validation",
        "required": [],
        "properties": {},
    }
}

instructor_validator = {  # TODO
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Instructor Object Validation",
        "required": [],
        "properties": {},
    }
}
