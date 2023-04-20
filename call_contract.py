from flask import Flask, request, jsonify
from web3 import Web3
import requests
from functools import cache
import json
import ast

ETHERSCAN_API_KEY = '<Your etyhercan api key>'

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/GLfjhndE2L3YJmb0-hDX635D-ioTIOD6'))

# Cache contract abi fetches to make  
# - Contract reads faster
# - Bypass rate limiting from Etherscan
@cache
def get_abi(contract_address):
    url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        return data['result']
    else:
        return None

@app.route('/call_contract', methods=['GET'])
def get_contract_data():
    contract_address = request.args.get('contract_address')
    function_name = request.args.get('function_name')
    arguments = request.args.get('arguments', default='[]')

    if not contract_address or not function_name:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        contract_address = w3.to_checksum_address(contract_address)
        # Safe eval of arguments
        arguments = ast.literal_eval(arguments)
        print(arguments)
    except ValueError:
        return jsonify({'error': 'Invalid input format'}), 400

    # Get ABI for specific contract
    contract_abi = get_abi(contract_address)
    if not contract_abi:
        return jsonify({'error': 'Unable to fetch contract ABI'}), 400

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    try:
        function = contract.functions.__getattribute__(function_name)
        print(arguments)
        result = function(*arguments).call()
    except AttributeError:
        return jsonify({'error': 'Invalid function name'}), 400
    except TypeError:
        return jsonify({'error': 'Invalid number or type of arguments'}), 400

    if isinstance(result, bytes):
        result = w3.to_hex(result)
    elif isinstance(result, int):
        result = w3.to_int(result)

    return jsonify({'result': result}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)