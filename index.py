"""Run the application"""

import os
import dotenv

from flask import Flask, request, jsonify
from database.contexts.database import DB
from database.contexts.autogen import AutoGenDatabase

dotenv.load_dotenv()


class Server:
    """The server class"""

    app = Flask(__name__)

    def __init__(self):
        """Initialize the server"""
        self.database = DB()
        self.autogen = AutoGenDatabase(
            database=self.database, schemas_path="database/schemas"
        )
        self.register_routes()

    def register_routes(self):
        """Register the routes"""
        self.app.add_url_rule("/ask", "ask", self.ask, methods=["GET"])

    def ask(self):
        query = request.args.get("query", "")
        self.autogen.initiate_assistant(query)
        response = {"answer": self.autogen.get_last_message()}
        return jsonify(response)

    def run(self, port):
        """Run the server"""
        self.app.run(port=port)


if __name__ == "__main__":
    server = Server()
    server.run(port=5000)
