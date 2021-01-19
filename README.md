# Slack Wayback bot

## Setup
Install python dependencies with `pipenv`.

    pipenv sync

## Running
Assuming you've installed your pythong dependencies via `pipenv`, run the following to start the app:

    pipenv run python app.py

Make sure your environment variables are configured properly, or the app won't run.
The required variables are:
    * SLACK_BOT_TOKEN
    * SLACK_SIGNING_SECRET
