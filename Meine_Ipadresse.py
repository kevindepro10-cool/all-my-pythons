import requests

response = requests.get('https://api.ipify.org')
public_ip = response.text

print(f"Ihre öffentliche IP-Adresse lautet: {public_ip}")
