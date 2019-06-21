import requests
import struct
import json
import logging
import time
import csv
import scipy
import scipy.stats

from shutil import move, copyfile
import os

import base64
import hashlib
import json
from binascii import hexlify
import json
from uuid import uuid4

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def encode_transaction(value):
    """Encode a transaction (dict) to Base64."""

    return base64.b64encode(json.dumps(value).encode('utf8')).decode('utf8')


def post_transaction():
    """Submit a valid transaction to the mempool."""
    tx_dict = encode_transaction("gautham=awesome") 
    print(tx_dict)

    tendermint_host = 'localhost'
    tendermint_port = 26657
    endpoint = 'http://{}:{}/'.format(tendermint_host, tendermint_port)

    payload = {
        'method': 'broadcast_tx_commit',
        'jsonrpc': '2.0',
        #'params': [encode_transaction(tx_dict)],
        'params': [tx_dict],
        'id': str(uuid4())
    }
    # TODO: handle connection errors!
    print(payload)
    return requests.post(endpoint, json=payload)


def _query_transaction():
    """Submit a valid transaction to the mempool."""
    # if not mode or mode not in mode_list:
    #     raise ValidationError('Mode must be one of the following {}.'
    #                             .format(', '.join(mode_list)))

    tx_dict = "gautham=awesome"

    tendermint_host = 'localhost'
    tendermint_port = 26657
    endpoint = 'http://{}:{}/'.format(tendermint_host, tendermint_port)

    payload = {
        "method": "abci_query",
        "jsonrpc": "2.0",
        #"params": [None, tx_dict, None, None],
        "params": [None, encode_transaction(tx_dict), None, False],
        #"params": [None, encode_transaction(tx_dict), None],
        "id": str(uuid4())
    }

    # TODO: handle connection errors!
    print(payload)
    return requests.post(endpoint, json=payload)

def decode_output(value):
    value_in_base64 = base64.b64decode(value)
    return int.from_bytes(value_in_base64, byteorder='big')

def decode_output_str(value):
    return value.decode('utf-8')

if __name__ == '__main__':
    logger.info("Running the client application.")
    resp = post_transaction()
    print(resp.json())
    resp = _query_transaction()
    print(resp.json())
