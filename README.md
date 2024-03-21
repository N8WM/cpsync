# CPSync

An AI agent designed to answer your scheduling-related questions at Cal Poly

## Introduction

CPSync is a Discord bot that uses natural language processing (NLP) to answer questions about Cal Poly classes. It is designed to be a helpful tool for students to quickly find information about classes, professors, and more. The bot is built using Python for the backend and Discord.js for the frontend.

## Setup

Start by cloning the repository and navigating to the project directory in your terminal:

```bash
git clone https://github.com/N8WM/cpsync.git
cd cpsync
```

To run locally, there are several steps you need to follow to set up the project. You must set up MongoDB, the Discord bot, an OpenAI API key, and Python, according to the instructions below.

### MongoDB Setup

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

### Discord Bot Setup

Node.js and npm are required to run the Discord bot. You can install them from the [official website](https://nodejs.org/en/download/).

Start by installing the required npm packages:

```bash
npm install
```

To run the Discord bot, you need to set up a Discord bot application in your developer portal, obtain its token and client ID, and add it to a server of your choice. These will be used in the Python setup.

- [**Creating a Discord Bot (and Token**](https://discordjs.guide/preparations/setting-up-a-bot-application.html)
- [**Adding a Bot to a Server**](https://discordjs.guide/preparations/adding-your-bot-to-servers.html)

### OpenAI Key

This project requires access to a valid OpenAI API key. You can obtain one by signing into your account at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys). The key will be used in the Python setup.

### Python Setup

This project was developed using Python 3.11.7, but anything as new as 3.10+ should suffice. You can install it from the [official website](https://www.python.org/downloads/).

You may want to use a virtual environment to manage the dependencies for this project. You can create and activate a virtual environment using the following command:

```bash
python3 -m venv .venv
source .venv/bin/activate # On Windows, use .venv\Scripts\activate
```

After installing Python and optionally setting up a virtual environment, you can install the required packages using pip:

```bash
pip install -r requirements.txt
```

To run the Python backend, you need to set up a `.env` file. We have created an automated script to help you set up the `.env` file. Run the following command and follow the prompts to input the various keys and tokens required to run the project:

```bash
python3 setup.py
```

## Usage

Before running the Discord bot, you need to load data into the MongoDB database. Then you can start the Discord bot and the Python backend.

### Data Loading

Data can be loaded into the MongoDB database using either of the following methods:

**Scraping Data** - Most up-to-date but slowest method

_Note: This method only works on Cal Poly network or VPN_

```bash
python3 scrape.py [-t TERM_HISTORY]
```

Where `TERM_HISTORY` is an optional argument that specifies the number of terms before the current term to scrape. If not provided, the default value is 0. The scraper will always scrape as many future terms as are available.

Once the data has been scraped, if you want to save it, you can dump the data into the `./dump` directory using the following command:

```bash
./dump_mongo.sh
```

This will overwrite the existing data in the `./dump` directory.

**Loading from Database Dump** - Fastest method but data may be outdated

```bash
./load_mongo.sh
```

This will load the data from `./dump/*` into the MongoDB database. The data currently provided in the `./dump` directory is a snapshot of Schedules from March 20th, 2024, and includes data for the Winter 2024 and unofficial Spring 2024 terms.

### Running the Discord Bot

To run the Discord bot, you also need the Python backend server running. Start the Python backend with the following command:

```bash
python3 index.py
```

Then, you can start the Discord bot by opening a new terminal and running the following command:

```bash
npm start
```

The bot should now be running and you can interact with it in your Discord server.

### Interacting with the Bot

The bot is designed to respond to natural language queries about any of the following topics:

- Terms
- Buildings and Rooms
- Colleges (e.g. CENG, CSM, etc.)
- Subjects (e.g. CSC, MATH, etc.)
- Courses (e.g. CSC 349, MATH 141, etc.)
- Sections
- Instructors

You can ask the bot questions with the `/ask` slash command.

### Examples

**`/ask` Who is teaching CSC-357 in Spring 2024**

> The instructors teaching CSC-357 next quarter are:
>
> - Phillip L. Nico
> - Joydeep Mukherjee
> - Christopher E. Siu
> - Devkishen Sisodia

**`/ask` What quarter is CSC-582 available?**

> The course CSC-582, "Computational Linguistics," is available in the Winter 2024 quarter.

**`/ask` Do I need to take CSC 202 before CSC 203**

> Yes, you need to take CSC-202 before CSC-203. The requirement is to complete CPE/CSC 202 (formerly CPE/CSC 103) with a grade of C- or better.

**`/ask` Tell me about Dr. Khosmood**

> Dr. Foaad Khosmood is an instructor with the job title "Instr Fac AY". He teaches for the College of Engineering (CENG) and is associated with the subjects Computer Engineering (CPE) and Computer Science (CSC). His office is located in room 014-0204. More information about Dr. Khosmood can be found on his [profile page](https://schedules.calpoly.edu/person_foaad_curr.htm).

**`/ask` Where is room 014-0255?**

Room 014-0255 is located in building 014 during the Winter 2024 term. It has a registered location capacity of 30. You can find more information and its schedule at [this link](https://schedules.calpoly.edu/location_014-0255_curr.htm). For general information about the building, you can visit [this page](https://schedules.calpoly.edu/all_location_curr.htm#014).

## Resources

- [MongoDB](https://www.mongodb.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [AutoGen](https://microsoft.github.io/autogen/docs/Getting-Started)
- [OpenAI API](https://platform.openai.com/docs/)
- [Node.js](https://nodejs.org/en/)
- [Discord.js](https://discord.js.org/)
- [Cal Poly Schedules](https://schedules.calpoly.edu/) (only accessible on Cal Poly network or VPN)
