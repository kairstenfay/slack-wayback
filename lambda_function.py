import os
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
    if not links:
        return "Please include a link when you mention me."

    results = set()

    for link in links:
        url = f"http://archive.org/wayback/available?url={link['url']}"
        with urllib.request.urlopen(url) as request:
            response = json.loads(request.read().decode('utf-8'))
            print(response)

        snapshot = response.get('archived_snapshots')
        if not snapshot:
            continue

        results.add(snapshot['closest']['url'])

    if not results:
        return "Sorry, I couldn't find any results for that. If your linked webpage(s) are new, we may not have picked them up in our latest crawl."

    return "Here's what I found: \n" + '\n'.join(results)


def respond_to_mention(event):
    channel_id = event.get("channel")

    data = urllib.parse.urlencode((
        ("token", os.environ["SLACK_BOT_TOKEN"]),
        ("channel", channel_id),
        ("text", create_wayback_machine_response(event))
        )).encode('ascii')

    request = urllib.request.Request(SLACK_URL, data=data, method="POST")
    request.add_header( "Content-Type", "application/x-www-form-urlencoded" )

    # Fire off the request!
    urllib.request.urlopen(request).read()


def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")

    respond_to_mention(json.loads(event['body'])['event'])
    return "200 OK"
