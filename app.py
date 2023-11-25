import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC46ac61224e60d3a2414e7c9830ece8a3'
    TWILIO_SYNC_SERVICE_SID = 'IS5293b6fff6a1a30ee07914e4861d971f'
    TWILIO_API_KEY = 'SK4d595437a799575ee415ed617382f00f'
    TWILIO_API_SECRET = 'EVloGd3Pu3Y0hWpWAxoDX8S4UWtyqw9Z'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    x = request.form['text']
    with open('work.txt','w') as f:
        f.write(x)
    g = "work.txt"
    return send_file(g, as_attachment = True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
