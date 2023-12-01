import requests

url = 'http://161.246.5.61:11200/students/html'
response = requests.get(url)

if response.status_code == 200:
    print('Request is successful')
    print('Response: ',response.text)
else:
    print('Request is not successful')
    print('Status code: ',response.status_code)
