import json
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import *
import sys

# Load withdrawal address
file = open('settings.json')
data = json.load(file)
rawOutput = data['output']
language = data['lang']

# Remove the spaces
output = rawOutput.replace(' ', '')

# Validate language
def validateLang(language):
  if language == 'en':
    inputMsg = 'Enter the seed phrase: '
    outputAddrNotChanged = 'You need to define the output address first. Please check the docs.'
    outputAddrEmpty = 'The output address is empty. Please check the docs.'
    return inputMsg, outputAddrNotChanged, outputAddrEmpty
  elif language == 'de':
    inputMsg = 'Gib die Wiederherstellungsphrase ein: '
    outputAddrNotChanged = 'Du musst zuerst die Ausgabeadresse definieren. Bitte überprüfe die Documentation.'
    outputAddrEmpty = 'Die Ausgabeadresse ist nicht angegeben. Bitte überprüfe die Documentation.'
    return inputMsg, outputAddrNotChanged, outputAddrEmpty
  elif language == 'fr':
    inputMsg = 'Saisis la phrase de récupération: '
    outputAddrNotChanged = "Vous devez d'abord définir l'adresse de sortie. Veuillez consulter la documentation."
    outputAddrEmpty = "L'adresse de sortie est vide. Veuillez consulter la documentation."
    return inputMsg, outputAddrNotChanged, outputAddrEmpty
  elif language == 'cn':
    inputMsg = '输入恢复短语：'
    outputAddrNotChanged = '你需要先定义输出地址。请查看文档。'
    outputAddrEmpty = '输出地址为空。请查看文档。'
    return inputMsg, outputAddrNotChanged, outputAddrEmpty
  elif language == 'ru':
    inputMsg = 'Введите фразу восстановления: '
    outputAddrNotChanged = 'Сначала необходимо определить адрес вывода. Пожалуйста, проверьте документацию.'
    outputAddrEmpty = 'Адрес вывода пуст. Пожалуйста, проверьте документацию.'
    return inputMsg, outputAddrNotChanged, outputAddrEmpty
  else:
    print('The language you entered is not supported. Please check the docs.')
    print('Setting language to English ...')
    language = 'en'
    validateLang(language)

# Get user input
langData = validateLang(language)
passphrase = input(langData[0])

# Validate withdrawal address
if output == 'enter your wallet address':
  print(langData[1])
  sys.exit()
elif output == '':
  print(langData[2])
  sys.exit()

#print(passphrase)

print("\nScanning ...")


if wallet_delete_if_exists('wallet', force=True): pass

# Validate mnemonic and create wallet
try: 
  w = Wallet.create('wallet', keys=passphrase, network='bitcoin',witness_type='segwit')
except Exception as e:
  print(e)
  sys.exit()

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