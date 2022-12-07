import requests


def name_set_parser(product_id):
    # Request Card Info via a GET method to TCGPlayer API
    url = "https://mpapi.tcgplayer.com/v2/product/" + product_id + "/details"

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

    # Acquire and Parse Card Name
    cardName = [item for item in cardinfoList if item.startswith('"productUrlName"')]
    cardName = str(cardName)[20:-3]

    # Acquire and Parse Set Code
    setCode = [item for item in cardinfoList if item.startswith('"formattedAttributes"')]
    setCode = str(setCode)[35:-3]
    data_list = [cardName, setCode]
    if (cardinfoList[3] != '"productLineUrlName":"YuGiOh"') or (cardinfoList[4] != '"productTypeName":"Cards"'):
        data_list = 'Not a valid card'
    return data_list

