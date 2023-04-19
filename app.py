import json
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import *

passphrase = input("Enter the 12 word Seed Phrase: ")#"fork solution awesome violin embody this speed glide buyer end loop cool"

# Load withdrawal address
file = open('settings.json')
data = json.load(file)
rawOutput = data['output']

# Remove the spaces
output = rawOutput.replace(' ', '')

# Validate withdrawal address
if output == 'enter your wallet address':
  print('You need to define the output address first. Please check the docs on https://github.com/fledpaul/cryptodrain/README.md')
  quit()
elif output == '':
  print('The output address is empty. Please check the docs on https://github.com/fledpaul/cryptodrain/README.md')
  quit()

#print(passphrase)

print("\nScanning...")


if wallet_delete_if_exists('wallet', force=True): pass

w = Wallet.create('wallet', keys=passphrase, network='bitcoin',witness_type='segwit')

w.scan()

w.info()

t = w.sweep(str(output), offline=False)

print()
print(t.info())
print()
print("HEX TRANSACTION :")
print(t.raw_hex())
print()
print("TXID :")
print(t)
