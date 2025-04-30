# Humanity Protocol Reward Claim Bot

Welcome to the **Kachal Reward Claim Bot**! 🚀 This Python script automates claiming daily rewards on the Humanity Protocol testnet. It processes multiple wallets and runs every 18 hours, making your life easier.

## Features
- Automatically claims daily rewards for multiple wallets.
- Runs on a 18-hour cycle to align with reward availability.
- Handles transaction retries with dynamic gas price adjustments.
- Colorful console output for easy monitoring.
- Simple setup and wallet management.

## Prerequisites
- Python 3.8+
- Required Python packages:
  - `web3`
  - `rich`
  - `colorama`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sinak1023/Humanity-Protocol-Reward-Claim-Bot.git
   cd Humanity-Protocol-Reward-Claim-Bot
   ```

2. Install dependencies:
   ```bash
   pip install web3 rich colorama
   ```

3. Create a `private_keys.txt` file in the project root and add your private keys (one per line):
   ```
   0xYourPrivateKey1
   0xYourPrivateKey2
   ```

## Usage
1. Ensure `private_keys.txt` is set up with your wallet private keys.
2. Run the script:
   ```bash
   python3 bot.py
   ```

3. Watch the bot connect to the Humanity Protocol testnet, process your wallets, and claim rewards. It will wait 18 hours before the next cycle.

## Configuration
- **RPC_URL**: Set to `https://rpc.testnet.humanity.org` by default.
- **CONTRACT_ADDRESS**: Pre-configured for the Humanity Protocol reward contract.
- **PRIVATE_KEYS_FILE**: Default is `private_keys.txt`. Ensure it exists and contains valid private keys.

## Notes
- Keep your `private_keys.txt` file secure and never share it.
- The script includes error handling for transaction issues, with up to 15 retries per claim.
- Monitor the console for detailed logs of the claim process.

## Support the Project
Loved the bot? Buy me a coffee to keep the code flowing! ☕

**ETH Address**: `0xE1e879DbACC13363A6be32c15d7aBCF652335d88`

## Contributing
Feel free to fork, submit issues, or send pull requests. Let's make this bot even better!


---

Built with 💪 by Kachal
