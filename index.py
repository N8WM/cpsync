"""Run the application"""

import os
import dotenv

from flask import Flask, request, jsonify
from database.contexts.database import DB
from database.contexts.functions import Functions
from database.schemas import schema_list
from agent.controller import Agent

dotenv.load_dotenv()


class Server:
    """The server class"""

    app = Flask(__name__)

    def __init__(self, current_term_id: str):
        """Initialize the server"""
        self.database = DB()
        self.functions = Functions(self.database)
        self.agent = Agent(schema_list, current_term_id, self.functions.aggregate)
        self.register_routes()

    def register_routes(self):
        """Register the routes"""
        self.app.add_url_rule("/ask", "ask", self.ask, methods=["GET"])

    def ask(self):
        query = request.args.get("query", "")
        response = {"answer": self.agent.respond(query)}
        return jsonify(response)

    def run(self, port):
        """Run the server"""
        self.app.run(port=port)


if __name__ == "__main__":
    server = Server("2242")
    server.run(port=5000)
