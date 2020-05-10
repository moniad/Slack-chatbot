# -*- coding: utf-8 -*-
"""
In this file, we'll create a routing layer to handle incoming and outgoing
requests between our bot and Slack.
"""
import jinja2
from flask import render_template, request
from slackeventsapi import SlackEventAdapter

from bot import Bot

mybot = Bot()
events_adapter = SlackEventAdapter(mybot.verification, "/slack")

template_loader = jinja2.ChoiceLoader([
    events_adapter.server.jinja_loader,
    jinja2.FileSystemLoader(['templates']),
])
events_adapter.server.jinja_loader = template_loader


@events_adapter.server.route("/install", methods=["GET"])
def before_install():
    """
    This route renders an installation page for our app!
    """
    client_id = mybot.oauth["client_id"]
    return render_template("install.html", client_id=client_id)


@events_adapter.server.route("/thanks", methods=["GET"])
def thanks():
    """
    This route renders a page to thank users for installing our app!
    """
    auth_code = request.args.get('code')
    print(auth_code)
    mybot.auth(auth_code)
    return render_template("thanks.html")


# Here we'll add a route to listen for incoming message button actions
@events_adapter.server.route("/after_button", methods=["GET", "POST"])
def respond():
    """
    This route listens for incoming message button actions from Slack.
    """
    pass


# Let's add an event handler for actions taken from message buttons
@events_adapter.on("action")
def action_handler(action_value):
    pass


@events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    mybot.react_to_message(message)


# Here's some helpful debugging hints for checking that env vars are set
@events_adapter.server.before_first_request
def before_first_request():
    client_id = mybot.oauth.get("client_id")
    client_secret = mybot.oauth.get("client_secret")
    verification = mybot.verification
    if not client_id:
        print("Can't find Client ID, did you set this env variable?")
    if not client_secret:
        print("Can't find Client Secret, did you set this env variable?")
    if not verification:
        print("Can't find Verification Token, did you set this env variable?")


if __name__ == '__main__':
    events_adapter.start(debug=True)
