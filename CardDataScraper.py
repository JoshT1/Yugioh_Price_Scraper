import sqlite3
from time import sleep

from HistoricalSalesScraper import historical_sales_scraper
from LatestSalesScraper import latest_sales_parser
from NameSetParser import name_set_parser
from XMLParser import xml_parser

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
listID = xml_parser('https://www.tcgplayer.com/sitemap/yugioh.0.xml')
x = listID[500]

# Request card name and set name via a GET method to TCGPlayer API
data_list = name_set_parser(listID[500])
print(data_list)

# Request the latest sales price via a POST method to TCGPlayer API, returns the average card sale price for today.
current_price = latest_sales_parser(listID[500])
print(current_price)

# Request the 6 day, 1 month, and 3 month sales price via a POST method to TCGPlayer API, returns the sales prices for those days.
historical_price = historical_sales_scraper(listID[500])
print(historical_price)

if current_price[0] != 0:
    cursor.execute('''INSERT INTO CARD_DATA_FIRST VALUES
        (''' + "'" + str(data_list[0]) + "'" + ''',
        ''' + "'" + str(data_list[1]) + "'" + ''',
        ''' + "'" + str(x) + "'" + ''',
        ''' + "'" + str(current_price[0]) + "'" + ''',
        ''' + "'" + str(historical_price[3]) + "'" + ''',
        ''' + "'" + str(historical_price[8]) + "'" + ''',
        ''' + "'" + str(historical_price[13]) + "'" + ''')''')

if current_price[1] != 0:
    cursor.execute('''INSERT INTO CARD_DATA_UN VALUES
        (''' + "'" + str(data_list[0]) + "'" + ''',
        ''' + "'" + str(data_list[1]) + "'" + ''',
        ''' + "'" + str(x) + "'" + ''',
        ''' + "'" + str(current_price[1]) + "'" + ''',
        ''' + "'" + str(historical_price[1]) + "'" + ''',
        ''' + "'" + str(historical_price[6]) + "'" + ''',
        ''' + "'" + str(historical_price[11]) + "'" + ''')''')

if current_price[2] != 0:
    cursor.execute('''INSERT INTO CARD_DATA_LI VALUES 
        (''' + "'" + data_list[0] + "'" + ''',
        ''' + "'" + data_list[1] + "'" + ''',
        ''' + "'" + x + "'" + ''',
        ''' + "'" + str(current_price[2]) + "'" + ''',
        ''' + "'" + historical_price[1] + "'" + ''',
        ''' + "'" + historical_price[4] + "'" + ''',
        ''' + "'" + historical_price[7] + "'" + ''')''')

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
