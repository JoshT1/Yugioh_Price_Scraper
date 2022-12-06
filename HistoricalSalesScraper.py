import json
from decimal import Decimal
import requests
import time
import datetime


def historical_sales_scraper(product_id):
    url = "https://infinite-api.tcgplayer.com/price/history/" + product_id + "/?range=quarter"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': '/',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.tcgplayer.com/',
        'cache-control': 'no-cache',
        'Origin': 'https://www.tcgplayer.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'TE': 'trailers'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    dataList = response.text.split(',')

    historical_sales_list = []

# Iterate through the request to get the date, variant, and market price
# double-dipping in conditions from the LatestSalesScraper, but it is used in this
# for formatting purposes later on.
    for i in range(0, len(dataList)):
        if dataList[i].startswith('"result":[{"date":'):
            historical_sales_list.append(dataList[i][19:-1])
        if dataList[i].startswith('{"date":'):
            historical_sales_list.append(dataList[i][9:-1])

        if dataList[i].startswith('"variant":"Unlimited"}'):
            historical_sales_list.append("Unlimited")
        if dataList[i].startswith('"variant":"Limited"}'):
            historical_sales_list.append("Limited")
        if dataList[i].startswith('"variant":"1st Edition"}'):
            historical_sales_list.append("1st Edition")

        if dataList[i].startswith('"marketPrice":'):
            historical_sales_list.append(dataList[i][15:-1])

# Cards only have 3 variants, and AFAIK limited edition is mutually exclusive from 1st/Unlimited.
# This deals with them logically and gets the appropriate values, but may cause issues down the line.
    try:
        if (historical_sales_list[2] and historical_sales_list[5] == "Limited") or (historical_sales_list[2] and historical_sales_list[5] == "Unlimited") or (historical_sales_list[2] and historical_sales_list[5] == "1st Edition"):
            historical_sales_week = [historical_sales_list[6], historical_sales_list[7], historical_sales_list[8]]
            historical_sales_month = [historical_sales_list[30], historical_sales_list[31], historical_sales_list[32]]
            historical_sales_3month = [historical_sales_list[87], historical_sales_list[88], historical_sales_list[89]]
            historical_sales_list = historical_sales_week + historical_sales_month + historical_sales_3month
        if (historical_sales_list[2] == "Unlimited" and historical_sales_list[4] == "1st Edition") or (historical_sales_list[2] == "1st Edition" and historical_sales_list[4] == "Unlimited"):
            historical_sales_week = [historical_sales_list[10], historical_sales_list[11], historical_sales_list[12], historical_sales_list[13], historical_sales_list[14]]
            historical_sales_month = [historical_sales_list[50], historical_sales_list[51], historical_sales_list[52], historical_sales_list[53], historical_sales_list[54]]
            historical_sales_3month = [historical_sales_list[145], historical_sales_list[146], historical_sales_list[147], historical_sales_list[148], historical_sales_list[149]]
            historical_sales_list = historical_sales_week + historical_sales_month + historical_sales_3month
    except IndexError as e:
        print("There is an error:" + str(e))

    return historical_sales_list
