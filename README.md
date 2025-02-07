<p align="center">
  <img src="https://i.postimg.cc/CKPNbbwV/cryptodrain-banner.png">
</p>

<p align="center">CryptoDrain is a Flask-based Bitcoin wallet sweeping service. This project provides a secure and modular API to create and sweep wallets based on provided seed phrases and transfer funds to a specified receiver address. It is built with security, scalability, and maintainability in mind.</p>

<hr>

## Table of Contents
- Features
- Architecture & Modules
- Installation
- Configuration
- Usage
- API Endpoints
- Development & Testing
- Contributing
- License
- Acknowledgments

## Features
**Modular Design**<br>
- Separates configuration management, wallet operations, and API endpoints

**Security Enhancements**<br>
- Sensitive data is redacted from logs and notifications
- Environment variable overrides for credentials

**Input Validation**<br>
- Validates API keys, seed phrases, receiver addresses, and balance formats

**Performance & Scalability**<br>
- Utilizes Gevent monkey patching for non-blocking I/O
- Implements caching for IP lookup results per request

**Robust Logging & Error Handling**<br>
- Uses rotating file logging with detailed exception handling
- Provides structured logging for easier debugging

**Health-Check Endpoint**<br>
- A dedicated endpoint to check server health for monitoring and load balancing

## Architecture & Modules
The repository is organized as follows:
```
├── api
│   └── config.json       # JSON configuration file
├── app.py                # Main application file containing Flask app and API endpoints
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

Key modules include:
- **Config:** Manages configuration loading and environment variable overrides
- **WalletManager:** Encapsulates wallet creation and sweeping operations
- **Helper Functions:** Provide logging, IP lookup, input sanitization, and validation
- **API Endpoints:**
  - `/api:` Main endpoint for processing wallet sweep requests
  - `/health:` Health-check endpoint for server monitoring

## Installation

### Prerequisites
- **Python 3.7+**
- **pip** (Python package installer)

### Steps
**1. Clone the Repository:**
```
git clone https://github.com/fled-dev/cryptodrain.git
cd cryptodrain
```

**2. Create a Virtual Environment (Optional but Recommended):**
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies:**
```pip install -r requirements.txt```

**4. Set Up Environment Variables (Optional):**
You can override sensitive configuration values (e.g., Telegram API key, channel ID, host IP/port) by setting environment variables:
```
export TG_API_KEY='your_telegram_api_key'
export TG_CHANNEL_ID='your_telegram_channel_id'
export HOST_IP='127.0.0.1'
export HOST_PORT=8080
```

## Configuration
The application reads its configuration from the `api/config.json` file. An example configuration is provided below:
```
{
  "FLASK_API_KEYS": [
    "0c19e4d5-a705-4cd7-b107-be8fd9a7b122"
  ],
  "TG_NOTIFICATIONS": true,
  "TG_API_KEY": "",
  "TG_CHANNEL_ID": "",
  "HOST_IP": "127.0.0.1",
  "HOST_PORT": 8080
}
```
**Note:**<br>
_It is recommended to use environment variables for sensitive data such as TG_API_KEY and TG_CHANNEL_ID rather than storing them in plain text._

## Usage
After installation and configuration, you can run the application as follows:
```
python app.py
```
The server will start using Gevent’s WSGIServer on the specified `HOST_IP` and `HOST_PORT`. You should see a boot screen in the terminal followed by logs indicating the server is ready to receive requests.

## API Endpoints
**1. `/api`**
- **Method:** `GET`
- **Description:** Endpoint to validate inputs, create a wallet based on the provided seed phrase, and sweep funds to a specified receiver address
- **Query Parameters:**
  - `api-key` (str): A valid API key
  - `seedphrase` (str): Wallet seed phrase (12 to 24 words)
  - `receiver` (str): Bitcoin address to sweep funds to
  - `balance` (str): (Optional) Expected balance (for logging purposes)
- **Example:**
  ```
  curl "http://127.0.0.1:8080/api?api-key=0c19e4d5-a705-4cd7-b107-be8fd9a7b122&seedphrase=word1%20word2%20...%20word12&receiver=bc1qexampleaddress&balance=0.12345678"
  ```

**2. `/health`**
- **Method:** `GET`
- **Description:** Simple health-check endpoint for load balancers and monitoring tools
- **Response:**
  ```
  {
  "status": "ok"
  }
  ```

## Development & Testing

**Running Locally**
1. Activate your virtual environment.
2. Set any required environment variables.
3. Run the application:
   ```
   python app.py
   ```

**Testing**
- **Unit Tests:** Add your unit tests in a separate directory (e.g., `tests/`) and run them using a test framework like `pytest`
- **Linting:** Ensure your code follows PEP 8 standards by running:
  ```
  flake8 .
  ```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature or bugfix:
  ```
  git checkout -b feature/my-new-feature
  ```
3. Commit your changes with clear messages
4. Push your branch to your fork:
   ```
   git push origin feature/my-new-feature
   ```
5. Open a pull request detailing your changes

Please ensure that your code follows our coding standards and includes tests where applicable.

## License
This project is licensed under the MIT License.

## Acknowledgments
Thanks to all contributors (just me lol)
Special thanks to the maintainers of Flask, Gevent, and bitcoinlib for their great work.
