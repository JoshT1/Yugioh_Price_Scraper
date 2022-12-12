import sqlite3


def sql_insert(Table, card_):

    # connect to DB
    sqliteConnection = sqlite3.connect('yugiohproductID.db')

    # create cursor
    cursor = sqliteConnection.cursor()

    # Insert card data into the table
    cursor.execute('''INSERT INTO ''' + Table + ''' VALUES''' '''
                        (''' + "'" + str(card_.get_name()) + "'" + ''',
                        ''' + "'" + str(card_.get_set_code()) + "'" + ''',
                        ''' + "'" + str(card_.product_id) + "'" + ''',
                        ''' + "'" + str(card_.get_current_price()) + "'" + ''',
                        ''' + "'" + str(card_.get_week_price()) + "'" + ''',
                        ''' + "'" + str(card_.get_month_price()) + "'" + ''',
                        ''' + "'" + str(card_.get_three_month_price()) + "'" + ''')''')
    sqliteConnection.commit()

