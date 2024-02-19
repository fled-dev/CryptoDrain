<p align="center">
  <img src="https://i.postimg.cc/CKPNbbwV/cryptodrain-banner.png">
</p>

<p align="center">CryptoDrain is a Python tool revolutionizing the way Bitcoin wallets are swept. By leveraging only the seed phrase and bypassing the need for a derivation path, it offers a fast, efficient, and user-friendly solution for securely transferring funds from Bitcoin wallets with minimal effort.</p>

<hr>

### How CryptoDrain Works
- **Technology Stack:** Developed with Python 3.11, CryptoDrain utilizes the python-bitcoinlib library for Bitcoin-related operations.
- **API Integration:** Implemented as a Flask web server, allowing seamless interaction through a straightforward API, facilitating integration with other systems.
- **Secure Authentication:** Utilizes API keys for secure access, denying unauthorized requests without valid keys.
- **Dynamic Sweeping:** Creates wallets dynamically, validates seed phrases, scans for funds, and executes sweeps to specified addresses.
- **Real-Time Feedback:** Provides users with live updates on wallet scanning and transaction progress, promptly addressing errors with informative messages.
- **Flexible Network Settings:** Configured for Bitcoin network compatibility, utilizing SegWit witness type for transactions.

<hr>

### Usage
Using CryptoDrain for sweeping Bitcoin wallets is designed to be intuitive and user-friendly. Follow these steps to get started:
1. **Clone the Repository**: Start by cloning the CryptoDrain repository from GitHub to your local machine. This will give you access to all the necessary files and code.
2. **Install Dependencies**: After cloning the repository, you need to install the required dependencies. Navigate to the CryptoDrain directory and run:
   ```
   pip install -r requirements.txt
   ```
   This command will install all the necessary Python libraries, including python-bitcoinlib and Flask.
3. **Configure the Application**: Before running the program, configure some stuff in the config.json
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

### CryptoDrain Development Roadmap
#### Short-Term Goals (Q2 2024)
2. **Multi-Currency Support**: Expand the functionality to support additional cryptocurrencies beyond Bitcoin, such as Ethereum, Litecoin, and others.
3. **API Rate Limiting**: Introduce rate limiting to the API to prevent abuse and ensure stable and reliable service for all users.
4. **Logging and Monitoring**: Develop a logging system to record API usage and errors, aiding in troubleshooting and improving user experience.
5. **Dockerization**: Package CryptoDrain in a Docker container for easier deployment and scalability.

#### Mid-Term Goals (Q4 2025)
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
