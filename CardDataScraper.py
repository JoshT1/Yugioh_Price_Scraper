import sqlite3
from time import sleep
import random

from HistoricalSalesScraper import historical_sales_scraper
from LatestSalesScraper import latest_sales_parser
from NameSetParser import name_set_parser
from XMLParser import xml_parser

# The purpose of this program is to get card pricing data from TCGPlayer.com.
# This can be used in any form of card data analysis.
# There are 3 editions of cards, 1 table for each: 1st Edition, Unlimited, and Limited.
# The current iteration of the program takes 10 random cards, parses the data,
# and adds it to the appropriate table.
# A 10-second wait occurs between cards to adhere to the rulings at https://www.tcgplayer.com/robots.txt

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
Product_ID INT(1000000),
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
Product_ID INT(1000000),
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
Product_ID INT(1000000),
Current_Price DECIMAL(13,4),
Week_Price DECIMAL(13,4),
Month_Price DECIMAL(13,4),
Three_Month_Price DECIMAL(13,4)
); '''

# Initialize table
cursor.execute(table)

# Use XML parse function to get product ID of every card
list_id = xml_parser('https://www.tcgplayer.com/sitemap/yugioh.0.xml')

i = 0

while i < 10:
    n = random.randint(0, len(list_id))
    print(n)

# Request card name and set name via a GET method to TCGPlayer API
    data_list = name_set_parser(list_id[n])

# Request the latest sales price via a POST method to TCGPlayer API, returns the average card sale price for today.
    if data_list != "Not a valid card":
        current_price = latest_sales_parser(list_id[n])

# Request the 6 day, 1 month, and 3 month sales price via a POST method to TCGPlayer API, returns the sales prices for those days.
        historical_price = historical_sales_scraper(list_id[n])

        if current_price[0] != 0:
            cursor.execute('''INSERT INTO CARD_DATA_FIRST VALUES
                (''' + "'" + str(data_list[0]) + "'" + ''',
                ''' + "'" + str(data_list[1]) + "'" + ''',
                ''' + "'" + str(list_id[n]) + "'" + ''',
                ''' + "'" + str(current_price[0]) + "'" + ''',
                ''' + "'" + str(historical_price[1]) + "'" + ''',
                ''' + "'" + str(historical_price[6]) + "'" + ''',
                ''' + "'" + str(historical_price[11]) + "'" + ''')''')

        if current_price[1] != 0:
            cursor.execute('''INSERT INTO CARD_DATA_UN VALUES
                (''' + "'" + str(data_list[0]) + "'" + ''',
                ''' + "'" + str(data_list[1]) + "'" + ''',
                ''' + "'" + str(list_id[n]) + "'" + ''',
                ''' + "'" + str(current_price[1]) + "'" + ''',
                ''' + "'" + str(historical_price[3]) + "'" + ''',
                ''' + "'" + str(historical_price[8]) + "'" + ''',
                ''' + "'" + str(historical_price[13]) + "'" + ''')''')

        if current_price[2] != 0:
            cursor.execute('''INSERT INTO CARD_DATA_LI VALUES 
                (''' + "'" + data_list[0] + "'" + ''',
                ''' + "'" + data_list[1] + "'" + ''',
                ''' + "'" + str(list_id[n]) + "'" + ''',
                ''' + "'" + str(current_price[2]) + "'" + ''',
                ''' + "'" + historical_price[1] + "'" + ''',
                ''' + "'" + historical_price[6] + "'" + ''',
                ''' + "'" + historical_price[11] + "'" + ''')''')

    i += 1
    print('waiting 10 seconds...')
    sleep(10)

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
