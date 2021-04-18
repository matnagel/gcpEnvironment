from flask import Flask
import os

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/cert/')
def cert():
    """This handler makes flask redirect '/cert' to '/cert/', which then
    gets caught by app.yaml. This gets never called"""
    return 'cert - Hello World!'

@app.route('/valheim/start')
def valheim():
    """Starts the valheim server"""
    secret = os.getenv('VALHEIMSECRET')
    secret_input = request.args.get('secret')
    if secret == secret_input:
        return 'Starting Server'
    else:
        return 'Wrong secret'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
