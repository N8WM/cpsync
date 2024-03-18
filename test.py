from database.contexts.database import DB
from database.contexts.autogen import AutoGenDatabase

database = DB()
autogen = AutoGenDatabase(database=database, schemas_path="database/schemas")

# message = "What building is building 14?"
# message = "Where is Foaad's office?"
# message = "What is the average number of students in a section?"
# message = "What 300 level computer science classes are available next quarter?"
message = "What prereqs do I need for CSC349?"
# message = "Who is foaad?"
# message = "When is CSC101 available next?"


autogen.initiate_assistant(message)

last_message = autogen.get_last_message()
print(last_message)
