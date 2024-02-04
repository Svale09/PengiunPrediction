from flask import Flask, render_template, request, jsonify
import requests
import json
import uuid
import os
import ssl
import urllib.request

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get data from the form
    data_from_form = request.json

    # Your Azure endpoint URL
    azure_endpoint_url = 'http://9afafb4a-79e9-4c39-b047-28980f51b22a.germanywestcentral.azurecontainer.io/score'

    request_id = str(uuid.uuid4())

    headers = {
      "Content-Type": "application/json"
    }

    # Make a request to the Azure endpoint
    body = str.encode(json.dumps(data_from_form))

    req = urllib.request.Request(azure_endpoint_url, body, headers)
    
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return jsonify({'message': f'Error code {response.status_code}'})

if __name__ == '__main__':
    app.run(debug=True)
