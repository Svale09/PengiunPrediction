from flask import Flask, render_template, request, jsonify
import requests
import json
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get data from the form
    data_from_form = request.get_json()

    # Your Azure endpoint URL
    azure_endpoint_url = 'http://9afafb4a-79e9-4c39-b047-28980f51b22a.germanywestcentral.azurecontainer.io/score'

    request_id = str(uuid.uuid4())

    headers = {
      "Content-Type": "application/json",
      "x-ms-client-request-id": request_id
    }

    # Make a request to the Azure endpoint
    response = requests.post(azure_endpoint_url, json=data_from_form, headers=headers)

    # Return the response from Azure as JSON
    if response.status_code == 200:
        # Check if the response contains data before attempting to parse
        if response.text:
            return jsonify(response.json())
        else:
            return jsonify({'message': 'Empty response from Azure endpoint'})
    else:
        return jsonify({'error': f'Azure endpoint returned status code {response.status_code}'})

if __name__ == '__main__':
    app.run(debug=True)
