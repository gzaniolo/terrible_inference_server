import requests
import json

ip = '172.22.139.165'

url = 'http://' + ip + ':4000/ask_abadi'

file_path = 'inf_server/testimg.jpg'

texts_data = {"texts": "bench . car ."}

files = {'file': open(file_path, 'rb')}  # 'rb' mode to read the file as binary
data = {'texts': json.dumps(texts_data)}  # Convert the Python dictionary to a JSON string

response = requests.post(url, files=files, data=data)

files['file'].close()

# Check the response status
if response.status_code == 200:
    print("Request was successful!")
    print("Response JSON:", response.json())  # If the response is JSON, print it
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response:", response.text)
