import requests

cookies = {
    '_ga': 'GA1.1.1980951099.1696607288',
    'data': 'f4c797c11c533d661d97754783db4838',
    'device_auth_8170512': 'mattqt4N7w3ZXXbsrQWgIJqLodCPiEqHmrW16iBEgtnvrRtmkLYZd1xe2ksB',
    'csgoempire': 'dyd97QWZUVidPtGtkAnQBqYfgFFvX1bEeovhTlNq',
    'do_not_share_this_with_anyone_not_even_staff': '8170512_Cyfr1BeZ5dORtaQNTwNDnwrJLbMT5y5bWY9PrRl7hdCnQ40RjADurdunrKoT',
    '__cf_bm': 'VzUERNGq82eek1zd8E1pNb7f6B8umDBUJ.YNPhM1Kmg-1696875441-0-Af/lcUOPPS2TKMQoiRb5DABdP5I6SslrDg0/TOvsWe6e/PIb+53ww1tTlucdK75RHo9hzqNw1pizrMEm+3P0ztI=',
    '_ga_DHPQBHR4YL': 'GS1.1.1696875440.12.1.1696875842.8.0.0',
}

headers = {
    'authority': 'csgoempire.io',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': '_ga=GA1.1.1980951099.1696607288; data=f4c797c11c533d661d97754783db4838; device_auth_8170512=mattqt4N7w3ZXXbsrQWgIJqLodCPiEqHmrW16iBEgtnvrRtmkLYZd1xe2ksB; csgoempire=dyd97QWZUVidPtGtkAnQBqYfgFFvX1bEeovhTlNq; do_not_share_this_with_anyone_not_even_staff=8170512_Cyfr1BeZ5dORtaQNTwNDnwrJLbMT5y5bWY9PrRl7hdCnQ40RjADurdunrKoT; __cf_bm=VzUERNGq82eek1zd8E1pNb7f6B8umDBUJ.YNPhM1Kmg-1696875441-0-Af/lcUOPPS2TKMQoiRb5DABdP5I6SslrDg0/TOvsWe6e/PIb+53ww1tTlucdK75RHo9hzqNw1pizrMEm+3P0ztI=; _ga_DHPQBHR4YL=GS1.1.1696875440.12.1.1696875842.8.0.0',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

response = requests.get('https://csgoempire.vegas/withdraw/steam/market', cookies=cookies, headers=headers)

with open('result.html', 'w', encoding='utf-8') as file:
    file.write(response.text)