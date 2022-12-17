import sqlite3
from time import sleep
import random

from historical_sales_scraper import historical_sales_scraper
from latest_sales_scraper import latest_sales_scraper
from name_set_scraper import name_set_scraper
from sql_insert import sql_insert
from xml_parser import xml_parser
import card

if __name__ == '__main__':
    '''
    The purpose of this program is to get card pricing data from TCGPlayer.com.
    This can be used in any form of card data analysis.
    There are 3 editions of cards, 1 table for each: 1st Edition, Unlimited, and Limited.
    # The current iteration of the program takes 100 random cards, parses the data,
    # and adds it to the appropriate table.
    # A 10-second wait occurs between cards to adhere to the rulings at https://www.tcgplayer.com/robots.txt
    '''

    # connect to DB
    sqliteConnection = sqlite3.connect('yugiohproductID.db')

    # create cursor
    cursor = sqliteConnection.cursor()

    # Drop tables if already exists
    cursor.execute("DROP TABLE IF EXISTS CARD_DATA_FIRST")
    cursor.execute("DROP TABLE IF EXISTS CARD_DATA_UN")
    cursor.execute("DROP TABLE IF EXISTS CARD_DATA_LI")

    # Creating table for 1st edition card data
    table = '''
    CREATE TABLE CARD_DATA_FIRST
    (
    Card_Name VARCHAR(255) NOT NULL,
    Set_Code VARCHAR(255) NOT NULL,
    Product_ID INT(1000000) PRIMARY KEY,
    Current_Price DECIMAL(13,4),
    Week_Price DECIMAL(13,4),
    Month_Price DECIMAL(13,4),
    Three_Month_Price DECIMAL(13,4)
    ); '''

    # Initialize table
    cursor.execute(table)

    # Creating table for unlimited edition card data
    table = '''
    CREATE TABLE CARD_DATA_UN
    (
    Card_Name VARCHAR(255) NOT NULL,
    Set_Code VARCHAR(255) NOT NULL,
    Product_ID INT(1000000) PRIMARY KEY,
    Current_Price DECIMAL(13,4),
    Week_Price DECIMAL(13,4),
    Month_Price DECIMAL(13,4),
    Three_Month_Price DECIMAL(13,4)
    ); '''

    # Initialize table
    cursor.execute(table)

    # Creating table for limited edition card data
    table = '''
    CREATE TABLE CARD_DATA_LI
    (
    Card_Name VARCHAR(255) NOT NULL,
    Set_Code VARCHAR(255) NOT NULL,
    Product_ID INT(1000000) PRIMARY KEY,
    Current_Price DECIMAL(13,4),
    Week_Price DECIMAL(13,4),
    Month_Price DECIMAL(13,4),
    Three_Month_Price DECIMAL(13,4)
    ); '''

    # Initialize table
    cursor.execute(table)

    # Use XML parse function to get product ID of every yugioh card on TCGPlayer.com
    list_id = xml_parser('https://www.tcgplayer.com/sitemap/yugioh.0.xml')

    i = 0

    while i < 10:
        n = random.randint(0, len(list_id))

        # Initialize 3 card objects for each possible card edition, set the product ID
        card_first = card.Card(list_id[n])
        card_un = card.Card(list_id[n])
        card_li = card.Card(list_id[n])
        card_list = [card_first, card_un, card_li]

        # Request card name and set name via a GET method to TCGPlayer API
        card_list = name_set_scraper(card_list)

        # Request the latest sales price via a POST method to TCGPlayer API, returns the average card sale price for today.
        if card_first.get_is_card():
            card_list = latest_sales_scraper(card_list)

            # Request the 6 day, 1 month, and 3 month sales price via a POST method to TCGPlayer API, returns the sales prices for those days.
            card_list = historical_sales_scraper(card_list)

            if card_list[0].get_current_price() != 0:
                sql_insert("CARD_DATA_FIRST", card_list[0])

            if card_list[1].get_current_price() != 0:
                sql_insert("CARD_DATA_UN", card_list[1])

            if card_list[2].get_current_price() != 0:
                sql_insert("CARD_DATA_LI", card_list[2])

        i += 1
        print(list_id[n])
        print(i)
        print('waiting 10 seconds...')
        sleep(10)

    sqliteConnection.commit()

    print("Data Inserted in the 1st Edition table: ")
    data = cursor.execute('''SELECT * FROM CARD_DATA_FIRST''')
    for row in data:
        print(row)

    print("Data Inserted in the Unlimited Edition table: ")
    data = cursor.execute('''SELECT * FROM CARD_DATA_UN''')
    for row in data:
        print(row)

    print("Data Inserted in the Limited Edition table: ")
    data = cursor.execute('''SELECT * FROM CARD_DATA_LI''')
    for row in data:
        print(row)
