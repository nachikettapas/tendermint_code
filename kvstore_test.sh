#! /bin/bash
set -ex

function toHex() {
    echo -n $1 | hexdump -ve '1/1 "%.2X"' | awk '{print "0x" $0}'

}

#####################
# kvstore with curl
#####################
TESTNAME=$1

# store key value pair
KEY="abcd"
VALUE="dcba"
echo $(toHex $KEY=$VALUE)
curl -s 127.0.0.1:26657/broadcast_tx_commit?tx=$(toHex $KEY=$VALUE)
echo $?
echo ""

#############################
# test using the /abci_query
#############################

echo "... testing query with /abci_query 2"

# we should be able to look up the key
RESPONSE=`curl -s "127.0.0.1:26657/abci_query?path=\"\"&data=$(toHex $KEY)&prove=false"`
RESPONSE=`echo $RESPONSE | jq .result.response.log`

set +e
A=`echo $RESPONSE | grep 'exists'`
if [[ $? != 0 ]]; then
    echo "Failed to find 'exists' for $KEY. Response:"
    echo "$RESPONSE"
    exit 1
fi
set -e

echo "Passed Test: $TESTNAME"
