<p align="center">
  <img src="https://fled.dev/cryptodrain-banner.png">
</p>

<p align="center">CryptoDrain is a Python tool revolutionizing the way Bitcoin wallets are swept. By leveraging only the seed phrase and bypassing the need for a derivation path, it offers a fast, efficient, and user-friendly solution for securely transferring funds from Bitcoin wallets with minimal effort.</p>

<hr>

### How CryptoDrain Works
1. **Technology Stack:** Built on Python 3.11, CryptoDrain leverages the versatility and power of the latest Python features. The program extensively utilizes the python-bitcoinlib library, which is specifically tailored for handling Bitcoin-related cryptographic operations.
2. **API-Driven Approach:** The application is set up as a Flask web server, allowing users to interact with it via a simple API. This design makes it easy to integrate with other systems or to operate remotely.
3. **Secure API Key Authentication:** For security, CryptoDrain uses a system of valid API keys. Requests to the API without a valid key are promptly denied, ensuring that only authorized users can access the sweeping functionality.
4. **Efficient Wallet Management:** Upon receiving a request with a valid API key, the user provides a seed phrase and a receiver Bitcoin address. CryptoDrain uses this information to generate a temporary wallet using the given seed phrase.
5. **Dynamic Wallet Creation and Sweeping:** The application dynamically creates a wallet with a unique, randomly generated name. It then validates the seed phrase, scans the wallet for funds, and performs the sweep to the specified receiver address.
6. **Real-Time Feedback and Error Handling:** Throughout the process, CryptoDrain provides real-time feedback, including wallet scanning and transaction status. In case of errors during the sweeping process, it promptly returns an informative error message to the user.
7. **Network and Witness Type Flexibility:** CryptoDrain is configured to work with the Bitcoin network and uses the SegWit witness type for transactions, ensuring compatibility with modern Bitcoin standards.
8. **Accessible Remotely:** Hosted on a server, CryptoDrain can be accessed and operated remotely, giving users the flexibility to manage Bitcoin wallets from any location.

<hr>

### Prerequisites
To ensure a smooth experience with CryptoDrain, make sure the following prerequisites are met:
1. **Python 3.11**: CryptoDrain is developed using Python 3.11, offering the latest features and optimizations of the language. Ensure that your system has Python 3 installed, with a recommendation for Python 3.11. You can download it from the [official Python website](https://www.python.org/downloads/).
2. **python-bitcoinlib Library**: This library is essential for CryptoDrain's interaction with the Bitcoin blockchain. It enables the program to execute Bitcoin-related cryptographic functions effectively. Install it via pip, the Python package manager, using the command:
   ```
   pip install python-bitcoinlib
   ```
3. **Flask Framework**: As CryptoDrain operates as a Flask web application, having Flask installed is crucial. It can be installed through pip with the following command:
   ```
   pip install Flask
   ```
4. **Random Module**: The random module, a standard part of Python's library, is used for generating unique identifiers within the application. It comes pre-installed with Python, so no additional steps are needed for this module.
5. **json Module**: For processing JSON data, CryptoDrain utilizes Python's built-in json module. It's included in the standard Python distribution, so you don't need to install it separately.

<hr>

### Usage
Using CryptoDrain for sweeping Bitcoin wallets is designed to be intuitive and user-friendly. Follow these steps to get started:
1. **Clone the Repository**: Start by cloning the CryptoDrain repository from GitHub to your local machine. This will give you access to all the necessary files and code.
2. **Install Dependencies**: After cloning the repository, you need to install the required dependencies. Navigate to the CryptoDrain directory and run:
   ```
   pip install -r requirements.txt
   ```
   This command will install all the necessary Python libraries, including python-bitcoinlib and Flask.
3. **Configure the Application**: Before running the program, define the receiver Bitcoin address in the `settings.json` file. This is where the swept funds will be sent.
4. **Launch CryptoDrain**: Open your Python environment and navigate to the CryptoDrain directory. Run the program by executing:
   ```
   python api.py
   ```
   This will start the Flask server and make CryptoDrain operational.
5. **Interact with the API**: To initiate a wallet sweep, make an API request to the running Flask server. Include the seed phrase of the wallet you wish to sweep and the receiver address as parameters in your request. The API endpoint will typically be:
   ```
   http://[server-ip]/api?api-key=[your-api-key]&seedphrase=[your-seed-phrase]&receiver=[receiver-address]
   ```
6. **Monitor the Process**: Follow the on-screen prompts and instructions provided by CryptoDrain. The application will display real-time updates about the wallet scanning and sweeping process.
7. **Completion**: Once the sweeping process is complete, the funds from the wallet will be successfully transferred to the specified receiver address. You will receive a confirmation message indicating the successful completion of the process.
With these steps, you can effectively use CryptoDrain to sweep Bitcoin wallets using only the seed phrase, offering a streamlined and efficient approach to managing your crypto assets.

<hr>

### Setting Up the API
#### Self-Setup
To set up the CryptoDrain API on your own, follow these straightforward steps:
1. **Server Setup**: Begin by setting up a server. While you can use any operating system, Ubuntu 23.04 is recommended for its latest features and support.
2. **Configure API Settings**: Open the `api.py` file and configure the host and port settings according to your server setup.
3. **Organize Files**: Place the `api.py` file in a suitable subdirectory within your server environment.
4. **Install Dependencies**: Ensure all required Python libraries are installed. This includes `bitcoinlib` and `flask`, which are crucial for the API's functionality. You can install these libraries using pip:
   ```
   pip install bitcoinlib flask
   ```
5. **Run the API**: Launch the API by running the `api.py` script. This will activate the Flask server and make your API operational.
6. **API Access**: Once the API is running, it’s ready to handle HTTP requests. You can make requests to your API using the appropriate URL structured as follows:
   ```
   http://[your-server-ip]:[port]?api-key=[your-api-key]&seedphrase=[your-seed-phrase]&receiver=[receiver-address]
   ```

#### Obtaining an API Key
If you prefer to use a pre-configured API, you can request an API key:
1. **Request via Email**: Send an email to mail@fled.dev explaining your intended use for the API key. Make sure to detail your project or use-case.
2. **Server Costs Contribution**: Depending on your usage needs, you may be asked to contribute towards server costs. This helps in maintaining the service quality and availability.
3. **Receiving the API Key**: If your request is approved, you will receive an API key via email. In some cases, requests might not be granted based on the assessment of the intended use.
4. **Using the API Key**: With the API key, you can make GET requests to the provided API endpoint. Format your request URL as follows:
   ```
   http://[api-server-ip]:[port]?api-key=[your-api-key]&seedphrase=[your-seed-phrase]&receiver=[receiver-address]
   ```

<hr>

### CryptoDrain Development Roadmap
#### Short-Term Goals (1-3 Months)
2. **Multi-Currency Support**: Expand the functionality to support additional cryptocurrencies beyond Bitcoin, such as Ethereum, Litecoin, and others.
3. **API Rate Limiting**: Introduce rate limiting to the API to prevent abuse and ensure stable and reliable service for all users.
4. **Logging and Monitoring**: Develop a logging system to record API usage and errors, aiding in troubleshooting and improving user experience.
5. **Dockerization**: Package CryptoDrain in a Docker container for easier deployment and scalability.

#### Mid-Term Goals (4-6 Months)
1. **Automated Testing Suite**: Create a suite of automated tests to ensure code quality, functionality, and facilitate easier updates and maintenance.
2. **Blockchain Analytics**: Incorporate analytics features to provide users with insights into transaction histories, wallet balances, and network fees.
3. **Web Interface**: Develop a user-friendly web interface, allowing less technically-savvy users to interact with CryptoDrain without needing to use the command line or API directly.
4. **Smart Contract Integration**: For supported blockchains like Ethereum, integrate functionality to interact with smart contracts.
5. **Internationalization**: Prepare the software for a global audience by adding multi-language support.

<hr>

### Contributing to CryptoDrain
#### How to Contribute

If you have ideas to improve CryptoDrain or add new features, we encourage you to contribute in the following way:
1. **Fork the Repository**: Begin by forking the CryptoDrain repository. This creates your own copy of the project, allowing you to make changes freely.
2. **Create a Feature Branch**: In your forked repository, create a new branch for your feature or improvement. Use a clear and descriptive name, like `git checkout -b feature/YourAmazingFeature`.
3. **Commit Your Changes**: After making your changes, commit them to your branch. Write a clear, concise commit message that explains the changes you've made, for example, `git commit -m 'Add YourAmazingFeature'`.
4. **Push to Your Branch**: Upload your changes to your branch on GitHub with `git push origin feature/YourAmazingFeature`.
5. **Open a Pull Request**: Navigate to the original CryptoDrain repository and open a pull request from your feature branch. Provide a detailed description of your changes and the value they add to the project.

#### Additional Ways to Contribute
- **Issue Tracking**: If you find issues or have enhancement suggestions but are not ready to contribute code, you can still help by opening an issue on the GitHub repository. Please tag your issues with "enhancement" for feature requests.
- **Starring the Project**: Show your support for CryptoDrain by giving it a star on GitHub. This helps to increase its visibility and encourages others in the community.

<hr>

### License
CryptoDrain is released under the GNU General Public License v3.0 (GPLv3), a free and open-source software license that provides users with the freedom to use, modify, and distribute CryptoDrain. The GPLv3 ensures that CryptoDrain remains free and open-source, and any modifications or improvements made to the software are also shared with the community.
