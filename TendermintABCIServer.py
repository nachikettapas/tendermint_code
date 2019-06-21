"""Impletements kvstore application of Tenderminti
from golang to python.

The KVStoreApplication is a simple merkle key-value store.
Transactions of the form key=value are stored as key-value
pairs in the tree. Transactions without an = sign set both
key and value to the value given. The app has no replay 
protection (other than what the mempool provides)

https://github.com/tendermint/tendermint/tree/master/abci/example/kvstore
"""
from BaseClass import LogOperation

import logging
import sys
import os
import re

from math import ceil
import rlp
from trie import Trie
from trie.db.memory import MemoryDB
from rlp.sedes import big_endian_int, binary
from abci import (
    ABCIServer,
    BaseApplication,
    ResponseInfo,
    ResponseInitChain,
    ResponseCheckTx, ResponseDeliverTx,
    ResponseQuery,
    ResponseCommit,
    CodeTypeOk,
)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))
logger = logging.getLogger(__name__)

STATE_KEY = b'stateKey'
KV_PAIR_PREFIX_KEY = b'kvPairKey'
BLANK_ROOT_HASH = b''


def prefix_key(key):
    """Takes key as a byte string and returns a byte string
    """
    return KV_PAIR_PREFIX_KEY + key


class stateMetaData(rlp.Serializable):
    fields = [
        ('size', big_endian_int),
        ('height', big_endian_int),
        ('apphash', binary)
    ]

    def __init__(self, size, height, apphash):
        super().__init__(size, height, apphash)


class State(object):
    """
    Talks directly to cold storage and the merkle
    only
    """

    def __init__(self, db, size, height, apphash):
        self.db = db
        self.size = size
        self.height = height
        self.apphash = apphash

    @classmethod
    def load_state(cls, dbfile=None):
        """ Create or load State.
        returns: State
        """
        if not dbfile:
            return (cls(MemoryDB(), 0, 0, BLANK_ROOT_HASH))

    def save(self):
        # Save to storage
        meta = stateMetaData(self.size, self.height, self.apphash)
        serial = rlp.encode(meta, sedes=stateMetaData)
        self.db.set(STATE_KEY, serial)
        return self.apphash


class KVStoreApplication(BaseApplication):

    def __init__(self):
        self.state = State.load_state()

    def info(self, req):
        """
        Since this will always respond with height=0, Tendermint
        will resync this app from the begining
        """
        r = ResponseInfo()
        r.version = "1.0"
        r.last_block_height = self.state.height
        r.last_block_app_hash = b''
        return r

    def deliver_tx(self, tx):
        """Validate the transaction before mutating the state.

        Args:
            raw_tx: a raw string (in bytes) transaction.
        """
        logger.info("Transaction recived %s", tx)

        parts = tx.split(b'=')
        if len(parts) == 2:
            key, value = parts[0], parts[1]
        else:
            key, value = tx
        self.state.db.set(prefix_key(key), value)
        self.state.size += 1

        logger.info("Transaction delivered succesfully")
        return ResponseDeliverTx(code=CodeTypeOk)

    def check_tx(self, tx):
        return ResponseCheckTx(code=CodeTypeOk)

    def commit(self):
        byte_length = max(ceil(self.state.size.bit_length() / 8), 1)
        app_hash = self.state.size.to_bytes(byte_length, byteorder='big')
        self.state.app_hash = app_hash
        self.state.height += 1
        self.state.save()
        return ResponseCommit(data=app_hash)

    def query(self, req):
        output = dict()
        param = req.data.split(b',')
        varId = param[0].split(b':')[1]
        varSpk = param[1].split(b':')[1]
        varRpk = param[2].split(b':')[1]
        srchStr = "id:" + varId.decode('ascii') + ","
        srchStr = srchStr + "senderpk:" + (varSpk.decode('ascii'),".*")[varSpk == b''] + ","
        srchStr = srchStr + "receiverpk:" + (varRpk.decode('ascii'),".*")[varRpk == b'']
        for key,val in self.state.db.snapshot().items():
            x = re.search(srchStr, key.decode('ascii')) 
            if not x is None:
                value = self.state.db.get(key)
                output[key] = value
        return ResponseQuery(code=CodeTypeOk, value=str(output).encode('ascii'))

if __name__ == '__main__':
    logger.info("Initalisation is complete. KV Store Application is ready")

    app = ABCIServer(app=KVStoreApplication(), port=46658)
    app.run()
