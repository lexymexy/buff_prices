import urllib
import aiohttp
import asyncio
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1kZ47kD1cvOeKjMNZMYrW_TMB3HuwnuOgymfJk_k9lLg"
API = "c3859cd14f7fea3de58ca4b5a0df4fa4"

with open("goodsIds.txt", encoding='utf-8') as f:
    lines = f.readlines()
stored_items = list(lines)
stored_ids = []
stored_names = []
for item in stored_items:
    stored_ids.append(''.join(list(item)[:(item.index(";"))]))
    stored_names.append(''.join(list(item)[(item.index(";")+1):-1]))

async def fetch_buff(session, item_id_list, item_name_list, item_empire_price_list):
    # item_id = int(input("Item ID: "))
    # num_offers_to_check = int(input("Max number of offers: "))

    num_offers_to_check = 1

    base_url = f"https://buff.163.com/api/market/goods/"

    for i, item_id in enumerate(item_id_list):
        credentials = None
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                credentials = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(credentials.to_json())


        params = {
            "game": "csgo",
            "page_num": "1",
            "goods_id": item_id
        }

        sell_url = base_url + 'sell_order' + '?' + urllib.parse.urlencode(params)

        async with session.get(sell_url) as response:
            resp = await response.json()
            if len(resp["data"]["items"]) == 0:
                print(f"Not offers found for item with id: {item_id}")
            else:
                # item_name = resp["data"]["goods_infos"][item_id]["market_hash_name"]
                items = resp["data"]["items"][:num_offers_to_check]
                item_buff_price = round(float(items[0]["price"])/7.196, 2)
                item_empire_price = item_empire_price_list[i]
                item_name = item_name_list[i]

                try:
                    service = build("sheets", "v4", credentials=credentials)
                    sheets = service.spreadsheets()

                    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"SHEET1!A{i + 2}",
                                           valueInputOption="USER_ENTERED", body={"values": [[item_name]]}).execute()
                    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"SHEET1!B{i + 2}",
                                           valueInputOption="USER_ENTERED",
                                           body={"values": [[item_buff_price]]}).execute()
                    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"SHEET1!C{i + 2}",
                                           valueInputOption="USER_ENTERED",
                                           body={"values": [[item_empire_price]]}).execute()

                except HttpError as error:
                    print(error)

                print(item_name, ' - ', round(item_buff_price/item_empire_price*100-100, 2), '% - ', round(item_buff_price-item_empire_price, 2), '$', sep='')
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"SHEET1!A{len(item_id_list) + 2}",
                               valueInputOption="USER_ENTERED", body={"values": [['-']]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"SHEET1!B{len(item_id_list) + 2}",
                               valueInputOption="USER_ENTERED",
                               body={"values": [['-']]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"SHEET1!C{len(item_id_list) + 2}",
                               valueInputOption="USER_ENTERED",
                               body={"values": [['-']]}).execute()

    except HttpError as error:
        print(error)

async def fetch_empire(session):
    base_url = f"https://csgoempire.io/api/v2/trading/items"
    params = {
        "Authorization": f"Bearer {API}",
    }
    per_page = 200
    page = 1
    auction_url = base_url + "?" + f"per_page={per_page}&" + f"page={page}&" + f"auction=yes"
    async with session.get(auction_url, headers=params) as response:
        resp = await response.json()
        item_list = resp["data"]
        item_name_list = []
        item_empire_price_list = []
        item_id_list = []
        for item in item_list:
            if 'Phase' in item["market_name"]:
                item_name_list.append(item["market_name"][:-10])
            elif 'Black Pearl' in item["market_name"]:
                item_name_list.append(item["market_name"][:-14])
            elif 'Blue Gem' in item["market_name"]:
                item_name_list.append(item["market_name"][:-11])
            elif 'Sapphire' in item["market_name"]:
                item_name_list.append(item["market_name"][:-11])
            elif 'Ruby' in item["market_name"]:
                item_name_list.append(item["market_name"][:-7])
            elif ' - Emerald' in item["market_name"]:
                item_name_list.append(item["market_name"][:-10])
            else:
                item_name_list.append(item["market_name"])
            item_empire_price_list.append(round(item["market_value"]*0.00614, 2))
            item_id_list.append(stored_ids[stored_names.index(item_name_list[-1])])
        return item_id_list, item_name_list, item_empire_price_list

async def main():

    for i in range(1):
        await asyncio.sleep(1)
        async with aiohttp.ClientSession() as session:
            item_id_list, item_name_list, item_empire_price_list = await fetch_empire(session)
            await fetch_buff(session, item_id_list, item_name_list, item_empire_price_list)

asyncio.run(main())