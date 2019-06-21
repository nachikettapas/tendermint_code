import requests

params = (
    ('tx', '"id:0,senderpk:abc,receiverpk:pqr=abcd"'),
)

response = requests.get('http://localhost:26657/broadcast_tx_commit', params=params)
