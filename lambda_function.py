import os
import ast
import json
import urllib
import urllib.request
from typing import Dict, Any


SLACK_URL = "https://slack.com/api/chat.postMessage"


def create_wayback_machine_response(event: Dict[str, Any]) -> str:
    """ """
    elements = event['blocks'] \
        .pop()['elements'] \
        .pop()['elements']

    links = list(filter(lambda el: el['type'] == "link", elements))

    results = set()

    for link in links:
        url = f"http://archive.org/wayback/available?url={link['url']}"
        with urllib.request.urlopen(url) as request:
            response = json.loads(request.read().decode('utf-8'))
            print(response)
            print(type(response))

        snapshot = response.get('archived_snapshots')
        if not snapshot:
            continue

        results.add(snapshot['closest']['url'])

    return "Here are your results! \n" + '\n'.join(results)


def respond_to_mention(event):
    channel_id = event.get("channel")

    data = urllib.parse.urlencode(
        (
            ("token", os.environ["SLACK_BOT_TOKEN"]),
            ("channel", channel_id),
            ("text", create_wayback_machine_response(event))
        )
    )
    data = data.encode('ascii')
    request = urllib.request.Request(SLACK_URL, data=data, method="POST")
    request.add_header( "Content-Type", "application/x-www-form-urlencoded" )

    # Fire off the request!
    x = urllib.request.urlopen(request).read()


def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")

    respond_to_mention(json.loads(event['body'])['event'])
    return "200 OK"
