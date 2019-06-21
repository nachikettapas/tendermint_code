from BaseClass import LogOperation
import requests
import base64

class TendermintLog(LogOperation):
        def createLog(self, _id, _senderpk, _receiverpk, _data):
                varParam = "\"id:" + _id + ",senderpk:" + _senderpk + ",receiverpk:" + _receiverpk + "=" + _data + "\"" 
                params = (
                        #('tx', '"id:0,senderpk:abc,receiverpk:pqr=abcd"'),  
                        ('tx', varParam.replace('\n','')),  
                )
                response = requests.get('http://localhost:26657/broadcast_tx_commit', params=params)
                return response.text

        def queryLog(self, _id, _senderpk=None, _receiverpk=None):
                varParam = "\"id:" + _id + ",senderpk:" + (_senderpk, "")[not _senderpk == None] + ",receiverpk:" + (_receiverpk, "")[not _receiverpk == None] + "\""
                params = (
                        #('data', '"id:0,senderpk:,receiverpk:"'),
                        ('data', varParam),  
                        ('path', '""'),
                        ('prove', 'false'),
                )
                response = requests.get('http://localhost:26657/abci_query', params=params)
                output = response.json()['result']['response']['value']
                return base64.b64decode(output)

a = TendermintLog()
with open("security_group.yaml", "r") as f:
	output = f.read()
print(a.createLog('0','abc','pqr',output))
#print(a.queryLog('0','abc','pqr'))
#print(a.queryLog('0','','pqr'))
#print(a.queryLog('0','abc',''))
#print(a.queryLog('0','',''))
