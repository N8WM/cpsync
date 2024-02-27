# CPSync
An AI agent designed to answer your scheduling-related questions at Cal Poly

## Introduction

### Outline
- Python (backend)
  - Maintains a database of classes
    - Routinely updated through BeautifulSoup4 webscraping of
    schedules.calpoly.edu
    - Database is stored in a file or series of files in JSON format
    - Everything is loaded into memory when the backend is booted up
  - Runs the NLP-based agent
    - Take in a message from a user and any previous conversation context
    - Use function calling to retrieve relevant information about courses
    - Construct a comprehensive answer for a user
    - Output answer
  - Hosts API endpoints for the frontend to use, e.g., Respond(message, user)
- Discord.js ("frontend")
  - JavaScript Discord bot to interface with student users
  - Users can either tag the bot in a public channel, or DM the bot
  - When a user sends the bot a message, it makes an API call to the Python
  backend, sending over the message and user ID

## Setup

## Resources

