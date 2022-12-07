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

# Initialize lists for card attributes.
    conditionList = []
    variantList = []
    languageList = []
    quantityList = []
    titleList = []
    purchasepriceList = []
    shippingpriceList = []
    orderdateList = []

# Iterates through the request and adds data to them.
    for i in range(0, len(latest_sales_list)):
        if latest_sales_list[i].startswith('"data":[{"condition":'):
            conditionList.append(latest_sales_list[22:-1])

        if latest_sales_list[i].startswith('{"condition":'):
            conditionList.append(latest_sales_list[14:-1])

        if latest_sales_list[i].startswith('"variant":'):
            variantList.append(latest_sales_list[i][11:-1])

        if latest_sales_list[i].startswith('"language":'):
            languageList.append(latest_sales_list[i][12:-1])

        if latest_sales_list[i].startswith('"quantity":'):
            quantityList.append(latest_sales_list[i][11:])

        if latest_sales_list[i].startswith('"title":'):
            titleList.append(latest_sales_list[i][9:-1])

        if latest_sales_list[i].startswith('"purchasePrice":'):
            purchasepriceList.append(latest_sales_list[i][16:])

        if latest_sales_list[i].startswith('"shippingPrice":'):
            shippingpriceList.append(latest_sales_list[i][16:])

        if latest_sales_list[i].startswith('"orderDate":'):
            orderdateList.append(latest_sales_list[i][13:-19])

# Initialize variables
    average_priceFirst = 0
    average_priceUn = 0
    average_priceLi = 0
    first_count = 0
    un_count = 0
    li_count = 0

# This get the average price of English versions of near mint and lightly played cards.
# Might need to have separate values for the conditions, and also maybe include lower quality cards.
# Might also need date added for daily values, as latest sales goes into previous days.
# 1st, unlimited, and limited editions are averaged and returned separately.
    for j in range(0, len(purchasepriceList)):
        if (conditionList[j] == 'Near Mint' or 'Lightly Played') and (languageList[j] == 'English'):
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
# Rounding and data types may need to be adjusted for more accurate pricing
    if first_count != 0:
        average_priceFirst = average_priceFirst / first_count
        average_priceFirst = round(average_priceFirst, 2)
    if un_count != 0:
        average_priceUn = average_priceUn / un_count
        average_priceUn = round(average_priceUn, 2)
    if li_count != 0:
        average_priceLi = average_priceLi / li_count
        average_priceLi = round(average_priceLi, 2)
    latest_sales = [average_priceFirst, average_priceUn, average_priceLi]
    return latest_sales
