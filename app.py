"""
From the tutorial at https://api.slack.com/start/building/bolt-python

useage:
    python app.py

Required environment variables:
    * SLACK_BOT_TOKEN
    * SLACK_SIGNING_SECRET

"""
import os
import requests
from slack_bolt import App

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# use message.im events for receiving messages in DMs
@app.event("app_mention")
def ask_for_introduction(event, say):
    import json

    # Keep only links
    elements = event['blocks'] \
        .pop()['elements'] \
        .pop()['elements']

    links = list(filter(lambda el: el['type'] == "link", elements))
    print(json.dumps(links, indent=4))

    results = set()

    for link in links:
        url = f"http://archive.org/wayback/available?url={link['url']}"
        response = requests.get(url)
        response.raise_for_status()

        snapshot = response.json().get('archived_snapshots')
        if not snapshot:
            continue

        results.add(snapshot['closest']['url'])

    say(text="Here are your results! \n" + '\n'.join(results))


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
