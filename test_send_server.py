import requests

ip = '172.24.156.5'
url = f'http://{ip}:4000/ask_abadi'

file_path = 'inf_server/testimg.jpg'

texts_data = {"texts": "bench . car . person ."}
# texts_data = {"texts": "$: coco"}

files = {'file': open(file_path, 'rb')}  # Open the file in binary mode

data = {'texts': str(texts_data)}

response = requests.post(url, files=files, data=data)

files['file'].close()

# Check the response status
if response.status_code == 200:
    print("Request was successful!")
    print("Response JSON:", response.json())  # If the response is JSON, print it
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response:", response.text)
