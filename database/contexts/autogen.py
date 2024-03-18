import os
import json
import tempfile

import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from database.contexts.functions import Functions
from database.contexts.database import DB

current_term_id = "2242"
current_term = "Winter 2024"


def stringify_json_files(folder_path: str) -> str:
    json_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                json_data = json.load(file)
                fname = filename.split(".")[0]
                if fname != "ges":
                    json_dict[fname] = json_data
    return json.dumps(json_dict, indent=4)


class AutoGenDatabase:
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4-0125-preview",
                "api_key": os.environ.get("OPENAI_API_KEY"),
            },
            {
                "model": "gpt-4",
                "api_key": os.environ.get("OPENAI_API_KEY"),
            },
            {
                "model": "gpt-3.5-turbo",
                "api_key": os.environ.get("OPENAI_API_KEY"),
            },
        ],
        "temperature": 0,
        "top_p": 1,
        "seed": 42,
        "functions": [
            {
                "name": "aggregate",
                "description": "Run an aggregation pipeline in the Schedules database, given a pipeline and a collection name, and return a list of documents that match the pipeline.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collection_name": {
                            "type": "string",
                            "description": "The name of the collection to aggregate.",
                            "enum": [
                                "terms",
                                "buildings",
                                "rooms",
                                "colleges",
                                "subjects",
                                "courses",
                                "sections",
                                "instructors",
                            ],
                        },
                        "pipeline": {
                            "type": "string",
                            "description": "The pipeline to apply, must be a valid MongoDB JSON array representing a pipeline.",
                        },
                    },
                    "required": ["collection_name", "pipeline"],
                },
            }
        ],
    }

    assistant_prompt = """
    Only do as the user asks. Do not ask the user to perform any other actions.

    Your job is to constructing a MongoDB pipeline to retrieve specific data from a collection.

    Provide the collection name (collection_name: str) and a MongoDB JSON array (pipeline: str) representing the pipeline to aggregate data from the specified collection.

    Ensure to keep it simple and only use operations appropriate for reading data. Remember, the database is in READ-ONLY mode. Keep the pipeline as straightforward as possible.

    Below you can find the schemas for each collection. Follow the descriptions and examples to construct your pipeline.

    No code is allowed. Only provide the parameters. Unless otherwise specified, assume the user is asking about the current term, {current_term}, whose ID is {current_term_id}.

    {schemas}

    Now go ahead and construct the pipeline for me to paste in, making sure you've read the schemas very closely and understand the data you're working with.
    """

    temp_dir = tempfile.TemporaryDirectory()

    # Create a local command line code executor.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,  # Timeout for each code execution in seconds.
        work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
    )

    def __init__(self, database: DB, schemas_path: str) -> None:
        self.functions = Functions(database=database)
        self.assistant = autogen.AssistantAgent(
            name="schedules_expert",
            system_message=self.assistant_prompt.format(
                schemas=stringify_json_files(schemas_path),
                current_term=current_term,
                current_term_id=current_term_id,
            ),
            llm_config=self.llm_config,
            code_execution_config={"use_docker": False},
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            llm_config=self.llm_config,
            system_message="Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
            is_termination_msg=lambda x: (x.get("content", "") or "")
            .rstrip()
            .endswith("TERMINATE"),
            code_execution_config=False,
        )
        self.user_proxy.register_function(
            function_map={
                "aggregate": self.functions.aggregate,
            }
        )
        self.assistant.register_function(
            function_map={
                "aggregate": self.functions.aggregate,
            }
        )

    def initiate_assistant(self, message: str):
        self.user_proxy.initiate_chat(self.assistant, message=message)

    def get_all_conversations(self):
        return self.assistant.chat_messages

    def get_last_message(self):
        return self.assistant.last_message()
