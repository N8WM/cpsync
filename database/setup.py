from pymongo import MongoClient

from database import schemas  # TODO: support for individual validators

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

        self.db.create_collection("terms", validator=schemas.term)
        self.db.create_collection("buildings", validator=schemas.building)
        self.db.create_collection("rooms", validator=schemas.room)
        self.db.create_collection("colleges", validator=schemas.college)
        self.db.create_collection("subjects", validator=schemas.subject)
        self.db.create_collection("courses", validator=schemas.course)
        self.db.create_collection("sections", validator=schemas.section)
        self.db.create_collection("ges", validator=schemas.ge)
        self.db.create_collection("instructors", validator=schemas.instructor)

    def close(self) -> None:
        """Close the database connection"""
        self.client.close()
