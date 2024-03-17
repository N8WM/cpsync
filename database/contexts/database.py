"""CPSync Database - MongoDB Client and Database"""

from pymongo import MongoClient
from database import schemas

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
        # self.db.create_collection("ges", validator=schemas.ge)
        self.db.create_collection("instructors", validator=schemas.instructor)

    def add_term(self, term: dict) -> None:
        """Add a term to the database"""
        self.db.terms.insert_one(term)

    def add_building(self, building: dict) -> None:
        """Add a building to the database"""
        self.db.buildings.insert_one(building)

    def add_room(self, room: dict) -> None:
        """Add a room to the database"""
        self.db.rooms.insert_one(room)

    def add_college(self, college: dict) -> None:
        """Add a college to the database"""
        self.db.colleges.insert_one(college)

    def add_subject(self, subject: dict) -> None:
        """Add a subject to the database"""
        self.db.subjects.insert_one(subject)

    def add_course(self, course: dict) -> None:
        """Add a course to the database"""
        existing_course = self.db.courses.find_one({"_id": course["_id"]})
        if not existing_course:
            self.db.courses.insert_one(course)
        else:
            existing_course["types"] += course["types"]
            existing_course["requirement_codes"] += course["requirement_codes"]
            existing_course["requirement_messages"] += course["requirement_messages"]
            self.db.courses.update_one(
                {"_id": course["_id"]}, {"$set": existing_course}
            )

    def add_section(self, section: dict) -> None:
        """Add a section to the database"""
        self.db.sections.insert_one(section)

    # def add_ge(self, ge: dict) -> None:
    #     """Add a GE to the database"""
    #     self.db.ges.insert_one(ge)

    def add_instructor(self, instructor: dict) -> None:
        """Add an instructor to the database"""
        self.db.instructors.insert_one(instructor)

    def close(self) -> None:
        """Close the database connection"""
        self.client.close()
