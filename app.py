from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import *

passphrase = input("Enter the 12 word Seed Phrase: ")#"fork solution awesome violin embody this speed glide buyer end loop cool"

#print(passphrase)

print("\nScanning...")


if wallet_delete_if_exists('wallet', force=True): pass

w = Wallet.create('wallet', keys=passphrase, network='bitcoin',witness_type='segwit')

w.scan()

w.info()

t = w.sweep('bc1q8nszsqxeua2d2r8xzx9xl740u6c2s94qpcs0zw', offline=False)

print()
print(t.info())
print()
print("HEX TRANSACTION :")
print(t.raw_hex())
print()
print("TXID :")
print(t)
