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

### MongoDB

To run the project locally, you need to install [MongoDB Server](https://www.mongodb.com/docs/manual/installation/) on your machine and have a MongoDB instance running on the default host and port. On MacOS, you can use Homebrew to install it:

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0
```

To start a MongoDB instance as a MacOS service (`mongod` process), run:

```bash
brew services start mongodb-community@7.0
```

To stop a `mongod` running as a macOS service, use the following command as needed:

```bash
brew services stop mongodb-community@7.0
```

## Resources
