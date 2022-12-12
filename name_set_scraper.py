import requests


def name_set_scraper(card_list):
    # Request Card Info via a GET method to TCGPlayer API
    url = "https://mpapi.tcgplayer.com/v2/product/" + card_list[0].product_id + "/details"

    payload = {}
    headers = \
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tcgplayer.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tcgplayer.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'TE': 'trailers'
        }

    response = requests.request("GET", url, headers=headers, data=payload)

    # Parse Card Data
    cardinfoList = response.text.split(",")

    if (cardinfoList[3] == '"productLineUrlName":"YuGiOh"') and (cardinfoList[4] == '"productTypeName":"Cards"'):
        card_list[0].set_is_card()
        # Acquire and Parse Card Name
        cardName = [item for item in cardinfoList if item.startswith('"productUrlName"')]
        card_list[0].set_name(str(cardName)[20:-3])
        card_list[1].set_name(str(cardName)[20:-3])
        card_list[2].set_name(str(cardName)[20:-3])

        # Acquire and Parse Set Code
        setCode = [item for item in cardinfoList if item.startswith('"formattedAttributes"')]
        card_list[0].set_set_code(str(setCode)[35:-3])
        card_list[1].set_set_code(str(setCode)[35:-3])
        card_list[2].set_set_code(str(setCode)[35:-3])
    return card_list
