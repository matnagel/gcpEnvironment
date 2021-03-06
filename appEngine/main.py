from flask import Flask, request

import os
from datetime import datetime, time
import pytz

from google.cloud import pubsub_v1

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

local_timezone = pytz.timezone('Europe/Berlin')

publisher = pubsub_v1.PublisherClient()


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/cert/')
def cert():
    """This handler makes flask redirect '/cert' to '/cert/', which then
    gets caught by app.yaml. This gets never called"""
    return 'cert - Hello World!'

def checkValheimPreconditions(secret_input):
    secret = os.getenv('VALHEIMSECRET')
    if not secret == secret_input:
        return 'Wrong secret'

    now_time = datetime.now(tz=pytz.utc)
    now_date_local = datetime.now(tz=local_timezone).date()
    begin_time = local_timezone.localize(datetime.combine(now_date_local, time(17,0)))
    end_time = local_timezone.localize(datetime.combine(now_date_local, time(21,27)))
    time_cond = now_time >= begin_time and now_time <= end_time
    if not time_cond:
        return f'{now_time.astimezone(local_timezone)} not between {begin_time.astimezone(local_timezone)} and {end_time.astimezone(local_timezone)}'
    return False

@app.route('/valheim/start')
def valheim():
    """Starts the valheim server"""
    secret_input = request.args.get('secret')
    error = checkValheimPreconditions(secret_input)
    if error:
        return error 
    else:    
        topic_name = os.getenv('VALHEIMTOPIC')
        topic_path = publisher.topic_path(
                os.environ['GOOGLE_CLOUD_PROJECT'],
                topic_name)
        publisher.publish(topic_path, data=b'start')
        return f"Message to {topic_name} to start server was sent"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
