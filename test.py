import requests

API = "c3859cd14f7fea3de58ca4b5a0df4fa4"

headers = {
    "Authorization": f"Bearer {API}",
}

response = requests.get('https://csgoempire.io/api/v2/trading/items?per_page=200&page=1&auction=yes', headers=headers)
resp = response.json()

with open('result.json', 'w', encoding='utf-8') as file:
    file.write(str(resp))