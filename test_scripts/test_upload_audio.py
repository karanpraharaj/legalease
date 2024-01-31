import requests

url = 'http://localhost:5000/upload_audio'
files = {'file': open('/Users/karanpraharaj/whisper.cpp/samples/test2.mp3', 'rb')}
response = requests.post(url, files=files)

print(response.text)