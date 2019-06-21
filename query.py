import requests
import base64

params = (
    ('data', '"id:0,senderpk:,receiverpk:"'),
    ('path', '""'),
    ('prove', 'false'),
)

response = requests.get('http://localhost:26657/abci_query', params=params)
output = response.json()['result']['response']['value']
print(base64.b64decode(output))
#print(response.json())
