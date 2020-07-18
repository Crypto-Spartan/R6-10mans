import requests

response = requests.get('https://r6.apitab.com/search/uplay/crypto-spartan')

print(response.text)