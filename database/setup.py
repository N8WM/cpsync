from pymongo import MongoClient

from database import validators as vds

DBNAME = "cpsync"


class DB:
    """Database class for MongoDB client and database"""
    def __init__(self) -> None:
        self.client = MongoClient("localhost", 27017)
        self.db = self.client[DBNAME]

    def __enter__(self) -> "DB":
        return self

    def __exit__(self) -> None:
        self.close()

    def reset(self) -> None:
        """Reset the database"""
        self.client.drop_database(DBNAME)
        self.db = self.client[DBNAME]

        self.db.create_collection("terms", validator=vds.term_validator)
        self.db.create_collection("colleges", validator=vds.college_validator)
        self.db.create_collection("departments", validator=vds.department_validator)
        self.db.create_collection("courses", validator=vds.course_validator)
        self.db.create_collection("sections", validator=vds.section_validator)
        self.db.create_collection("instructors", validator=vds.instructor_validator)

    def close(self) -> None:
        """Close the database connection"""
        self.client.close()
