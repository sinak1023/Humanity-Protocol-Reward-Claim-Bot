import sys
import time
from web3 import Web3
from colorama import init, Fore
from rich.console import Console

init(autoreset=True)
console = Console()

RPC_URL = 'https://rpc.testnet.humanity.org'
PRIVATE_KEYS_FILE = 'private_keys.txt'
CONTRACT_ADDRESS = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'

CONTRACT_ABI = [{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]

def display_banner():
    banner = """
    ╔════════════════════════════════════╗
    ║          Kachal is here!           ║
    ╚════════════════════════════════════╝
    """
    console.print(f"[bold magenta]{banner}[/bold magenta]")

def setup_blockchain_connection():
    console.print("[bold cyan]🔗 Connecting to Humanity Protocol...[/bold cyan]")
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if web3.is_connected():
        console.print("[bold green]✅ Connection successful![/bold green]")
    else:
        console.print(f"{Fore.RED}❌ Connection failed!")
        sys.exit(1)
    
    return web3

def load_wallets():
    try:
        with open(PRIVATE_KEYS_FILE, 'r') as file:
            keys = [line.strip() for line in file if line.strip()]
            wallets = [{"private_key": key, "address": Web3().eth.account.from_key(key).address} for key in keys]
            console.print(f"[bold magenta]🔑 Found {len(wallets)} wallets![/bold magenta]")
            
            for w in wallets:
                console.print(f"🔹 Wallet Address: {w['address']}")
            
            return wallets
    except FileNotFoundError:
        console.print(f"{Fore.RED}🚨 File {PRIVATE_KEYS_FILE} not found!")
        sys.exit(1)

def claim_reward(wallets, web3, contract):
    for wallet in wallets:
        try:
            account = web3.eth.account.from_key(wallet["private_key"])
            sender_address = account.address

            genesis_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()
            current_epoch = contract.functions.currentEpoch().call()
            _, claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()

            if genesis_claimed and not claim_status:
                console.print(f"🟢 [bold green]Claiming reward for {sender_address} (Genesis reward claimed).[/bold green]")
                process_claim(sender_address, wallet["private_key"], web3, contract)
            elif not genesis_claimed:
                console.print(f"🟢 [bold green]Claiming reward for {sender_address} (Genesis reward not claimed).[/bold green]")
                process_claim(sender_address, wallet["private_key"], web3, contract)
            else:
                console.print(f"🟡 [bold yellow]Reward already claimed for {sender_address} in epoch {current_epoch}, skipping.[/bold yellow]")

        except Exception as e:
            console.print(f"🚨 [red]Error claiming reward for {wallet['address']}: {e}[/red]")

def process_claim(sender_address, private_key, web3, contract):
    try:
        max_retries = 15
        retry_count = 0
        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(sender_address, 'pending')

        while retry_count < max_retries:
            try:
                gas_amount = contract.functions.claimReward().estimate_gas({
                    'chainId': web3.eth.chain_id,
                    'from': sender_address,
                    'gasPrice': int(gas_price),
                    'nonce': nonce
                })

                transaction = contract.functions.claimReward().build_transaction({
                    'chainId': web3.eth.chain_id,
                    'from': sender_address,
                    'gas': gas_amount,
                    'gasPrice': int(gas_price),
                    'nonce': nonce
                })

                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                
                console.print(f"✅ [bold green]Transaction successful for {sender_address} | TX Hash: {web3.to_hex(tx_hash)}[/bold green]")
                return

            except Exception as e:
                error_message = str(e)
                if "ALREADY_EXISTS: already known" in error_message or "replacement transaction underpriced" in error_message:
                    console.print(f"⚠️ [yellow]Duplicate transaction detected. Increasing gas price...[/yellow]")
                    gas_price = int(gas_price * 3.2)
                    nonce += 1
                    retry_count += 1
                    time.sleep(5)
                else:
                    console.print(f"🚨 [red]Error processing claim for {sender_address}: {error_message}[/red]")
                    return

        console.print(f"❌ [bold red]Failed to send transaction after {max_retries} attempts for {sender_address}.[/bold red]")

    except Exception as e:
        console.print(f"🚨 [red]Failed to execute claim for {sender_address}: {str(e)}[/red]")

def main_loop():
    display_banner()  # Display the banner before starting
    web3 = setup_blockchain_connection()
    contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
    wallets = load_wallets()

    while True:
        console.print("[bold cyan]🚀 Starting reward claim process...[/bold cyan]")
        claim_reward(wallets, web3, contract)
        console.print("[bold cyan]🕒 Waiting 18 hours before next claim cycle...[/bold cyan]")
        time.sleep(18 * 3600)  # 18 hours in seconds

if __name__ == "__main__":
    main_loop()
