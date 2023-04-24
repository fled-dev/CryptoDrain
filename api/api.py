# Import libraries
from flask import Flask, request
from bitcoinlib.wallets import *
import random, requests

# Valid API keys
valid_api_keys = ['0c19e4d5-a705-4cd7-b107-be8fd9a7b122', 'cbf816fd-fc14-407f-86e4-4838c15ef0e3', '694820b0-888c-4154-ad1c-9a53a9feb278']

# Create the app
app = Flask(__name__)


# Create the index page
@app.route('/api')
def api():
    # Read API key (http://0.0.0.0/api?api-key=0)
    api_key = request.args.get('api-key')
    # Check if API key is valid
    if api_key not in valid_api_keys:
        return 'Error: Invalid API Key'
    
    # Get seed phrase and receiver
    seedphrase = request.args.get('seedphrase')
    receiver = request.args.get('receiver')

    # Run the sweep function
    return sweep(seedphrase, receiver)


def sweep(seedphrase, receiver):
    print('---')
    print('---')
    print('Seed Phrase: ' + seedphrase)
    print('Receiver: ' + receiver)
    print('---')
    print('Scanning Wallet ...')

    # Generate random wallet name (12 random characters)
    random_wallet_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12))

    # Validate the seed phrase
    if wallet_delete_if_exists(str(random_wallet_name), force=True):
        pass

    # Create the wallet
    w = Wallet.create(str(random_wallet_name), keys=str(seedphrase), network='bitcoin', witness_type='segwit')
    w.scan()
    w.info()

    # Sweep the wallet
    try:
        t = w.sweep(str(receiver), offline=False)
    except Exception as e:
        swept = False
        return 'Error: ' + str(e)

    print('---')
    print('Success : Wallet Swept')
    return 'Success : Wallet Swept'
    

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)