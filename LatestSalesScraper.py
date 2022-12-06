import json
from decimal import Decimal
import requests


# Needs some work done on the average prices!
def latest_sales_parser(product_id):
    url = "https://mpapi.tcgplayer.com/v2/product/" + product_id + "/latestsales"

    payload = json.dumps({})
    headers = {
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

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.text

# split request into list and remove junk data.
    latest_sales_list = response.split(",")
    latest_sales_list.pop(0)
    latest_sales_list.pop(0)
    latest_sales_list.pop(0)
    latest_sales_list.pop(0)

# Initialize lists
    conditionList = []
    variantList = []
    languageList = []
    quantityList = []
    titleList = []
    purchasepriceList = []
    shippingpriceList = []
    orderdateList = []

    i = 0

    # Iterates through the request and adds data to them.
    while i < len(latest_sales_list):
        z = latest_sales_list[i].split(":")
        conditionList.append(z[len(z) - 1][1:-1])

        z = latest_sales_list[i + 1].split(":")
        variantList.append(z[len(z) - 1][1:-1])

        z = latest_sales_list[i + 2].split(":")
        languageList.append(z[len(z) - 1][1:-1])

        z = latest_sales_list[i + 3].split(":")
        quantityList.append(z[len(z) - 1])

        z = latest_sales_list[i + 4].split(":")
        titleList.append(z[len(z) - 1][1:-1])

        z = latest_sales_list[i + 7].split(":")
        purchasepriceList.append(z[len(z) - 1])

        z = latest_sales_list[i + 8].split(":")
        shippingpriceList.append(z[len(z) - 1])

        orderdateList.append(latest_sales_list[i + 9][13:-21])

        i += 10

    print(purchasepriceList)
    print(conditionList)
    print(variantList)
    print(orderdateList)

    # Initialize variables
    average_priceFirst = 0
    average_priceUn = 0
    average_priceLi = 0
    first_count = 0
    un_count = 0
    li_count = 0

    # This get the average price of near mint and lightly played cards.
    # Might need to have separate values for the conditions, and also maybe include lower quality cards.
    # Might also need date added for daily values.
    # 1st, unlimited, and limited editions are averaged and returned separately.
    for j in range(0, len(purchasepriceList)):
        if conditionList[j] == 'Near Mint' or 'Lightly Played':
            if variantList[j] == '1st Edition':
                average_priceFirst += Decimal(purchasepriceList[j])
                first_count += 1
            if variantList[j] == 'Unlimited':
                average_priceUn += Decimal(purchasepriceList[j])
                un_count += 1
            if variantList[j] == 'Limited':
                average_priceLi += Decimal(purchasepriceList[j])
                li_count += 1

# Average calculation is not required if the count is 0, also prevents divide by 0 error.
    if first_count != 0:
        average_priceFirst = average_priceFirst / first_count
    if un_count != 0:
        average_priceUn = average_priceUn / un_count
    if li_count != 0:
        average_priceLi = average_priceLi / li_count
    latest_sales = [average_priceFirst, average_priceUn, average_priceLi]
    return latest_sales
