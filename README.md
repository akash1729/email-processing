# Happyfox assignment


## Description
Python application to read, store and process emails using gmail APIs


## Table of Contents

- [Setup](#setup)
- [Database](#database)
- [Tests](#tests)
- [Improvements](#improvements-that-can-be-made)


## Setup
1. Setup venv and install dependencies. You can run the make command for that `make init`
2. Add your gmail credential file to `/artifact` directory
3. Configure rules for the application in `/artifact/rules.json`
4. To run the fetch and store email script, run `python fetch_email.py`. You can set number of emails needed and email label in the script
5. To run the rules on the emails, run `python process_emails.py`


## Database
I have used a simple sqlite database for this project. For a production distributed system Postgres or MySQL should be used.
Wrappers for database operations can be written based on the datastore interface

## Tests
I have written a few tests for the models used. For a production system a lot more tests are need to ensure significant coverage

## Improvements that can be made
1. Add more configuration to the scripts to be passed as command line arguments
2. Docker images could be created for the scripts