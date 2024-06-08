import requests
import json

# URL for the web service
scoring_uri = "YOUR_SCORING_URI"

# Example data to send to the endpoint
data = {"data": [ ... ]}

# Convert to JSON string
input_data = json.dumps(data)

# Set the content type
headers = {'Content-Type': 'application/json'}

# Make the request and display the response
response = requests.post(scoring_uri, data=input_data, headers=headers)
print(response.json())
