import requests

'''
params = (
    ('tx', '"gautham=awesome"'),
)

response = requests.get('http://localhost:26657/broadcast_tx_commit', params=params)
#response = requests.get('http://localhost:26658/deliver_txbroadcast_tx_commit', params=params)
print(response.json())
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('http://localhost:26658/broadcast_tx_commit?tx=b"gautham=awesome"')
'''
params = (
    ('data', '"gautham"'),
)
response = requests.get('http://localhost:26658/abci_query', params=params)

print(response)
