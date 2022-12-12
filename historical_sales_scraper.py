import requests


def historical_sales_scraper(card_list):
    url = "https://infinite-api.tcgplayer.com/price/history/" + card_list[0].product_id + "/?range=quarter"

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
# double-dipping in conditions from the latest_sales_scraper, but it is used in this
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

# Cards only have 3 variants, and this logic is assuming limited edition is mutually exclusive from 1st/Unlimited.
# This deals with them logically and gets the appropriate values and adds them to a card object.
# TO DO: Add
    try:
        if historical_sales_list[2] and historical_sales_list[5] == "1st Edition":
            card_list[0].set_week_price(historical_sales_list[7])
            card_list[0].set_month_price(historical_sales_list[31])
            card_list[0].set_three_month_price(historical_sales_list[88])
        if historical_sales_list[2] and historical_sales_list[5] == "Unlimited":
            card_list[1].set_week_price(historical_sales_list[7])
            card_list[1].set_month_price(historical_sales_list[31])
            card_list[1].set_three_month_price(historical_sales_list[88])
        if historical_sales_list[2] and historical_sales_list[5] == "Limited":
            card_list[1].set_week_price(historical_sales_list[7])
            card_list[2].set_month_price(historical_sales_list[31])
            card_list[2].set_three_month_price(historical_sales_list[88])

        if historical_sales_list[2] == "1st Edition" and historical_sales_list[4] == "Unlimited":
            card_list[0].set_week_price(historical_sales_list[11])
            card_list[0].set_month_price(historical_sales_list[51])
            card_list[0].set_three_month_price(historical_sales_list[146])

            card_list[1].set_week_price(historical_sales_list[13])
            card_list[1].set_month_price(historical_sales_list[51])
            card_list[1].set_three_month_price(historical_sales_list[148])

        if historical_sales_list[2] == "Unlimited" and historical_sales_list[4] == "1st Edition":
            card_list[0].set_week_price(historical_sales_list[13])
            card_list[0].set_month_price(historical_sales_list[51])
            card_list[0].set_three_month_price(historical_sales_list[148])

            card_list[1].set_week_price(historical_sales_list[11])
            card_list[1].set_month_price(historical_sales_list[51])
            card_list[1].set_three_month_price(historical_sales_list[146])

    except IndexError as e:
        print("There is an error:" + str(e))
        print(historical_sales_list)

    return card_list
