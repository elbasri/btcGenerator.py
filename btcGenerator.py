#pip install requests bitcoinaddress 
from bitcoinaddress import Wallet
import requests
import multiprocessing
import time

API_URL = "https://chidomainkifmakan.ma/process_wallet/"

def generate_wallet_and_send(retry_count=3, retry_delay=2):
    wallet = Wallet()

    # Extracting values directly from the __dict__ structure
    key_data = wallet.key.__dict__
    mainnet_key_data = key_data['mainnet'].__dict__
    address_data = wallet.address.__dict__
    mainnet_address_data = address_data['mainnet'].__dict__

    data = {
        'private_key_hex': key_data['hex'],
        'private_key_wif': mainnet_key_data['wif'],
        'private_key_wif_compressed': mainnet_key_data['wifc'],
        'public_key': address_data['pubkey'],
        'public_key_compressed': address_data['pubkeyc'],
        'address_p2pkh': mainnet_address_data['pubaddr1'],
        'address_p2pkh_compressed': mainnet_address_data['pubaddr1c'],
        'address_p2sh': mainnet_address_data['pubaddr3'],
        'address_p2wpkh': mainnet_address_data['pubaddrbc1_P2WPKH'],
        'address_p2wsh': mainnet_address_data['pubaddrbc1_P2WSH'],
        'server': "git1"
    }

    for attempt in range(retry_count):
        try:
            response = requests.post(API_URL, json=data, timeout=1)
            if response.status_code == 200:
                #print(f"Data sent successfully for address: {data['address_p2pkh']}")
                break
        except requests.exceptions.Timeout:
            print("Request timed out, retrying...")
            time.sleep(retry_delay)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

def worker():
    while True:
        generate_wallet_and_send()

def main():
    cpu_count = multiprocessing.cpu_count()
    processes = []

    for _ in range(cpu_count):
        p = multiprocessing.Process(target=worker)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
