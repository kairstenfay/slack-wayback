# Slack Wayback bot

This is a Slack bot that runs on AWS Lambda.

Make sure your environment variables are configured properly, or the app won't run.
The required variables are:
* SLACK_BOT_TOKEN

## Requirements

To build this bot, you'll need an AWS account.

## Related tutorials

If you're interested in setting up a similar Slack bot, I recommend starting with the [Slack API Bot tutorial](https://api.slack.com/bot-users).

Once you're ready to deploy, I recommend [this Medium post for configuring Slack bots on AWS Lambda](https://medium.com/glasswall-engineering/how-to-create-a-slack-bot-using-aws-lambda-in-1-hour-1dbc1b6f021c).

## Slack configuration

Currently, the configured Slack Bot Token Scopes are:
* `app_mentions:read`
* `channels:join`
* `chat:write`
* `chat:write.public`
* `links:read`
