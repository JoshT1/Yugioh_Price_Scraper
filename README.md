This is a program that parses/scrapes yu-gi-oh card data from TCGPlayer.com. I have staggered the requests to only do 1 card every 10 seconds. 
The data acquired from each card (1st Ed, Unlimited, and/or limited edition) is: 
Card name, set code, product ID, current price, week price, month price, and 3 month price.

main.py runs the main loop for parsing cards
with  historical_sales_scraper.py, latest_sales_scraper.py, name_set_scraper.py, sql_insert.py, and xml_parser.py
being functions to get specific data.

all the card data is temporarily stored in a card object, defined in card.py.
