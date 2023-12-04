from tools.functionality import Functionality, SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc
from dotenv import dotenv_values

config = dotenv_values(".env")  # take environment variables from .env.

db_host = config['DB_HOST']
db_name = config['DB_NAME']
db_user = config['DB_USER']
db_password = config['DB_PASSWORD']


try:
    import sys

    db_host="cypress.csil.sfu.ca"
    db_name="qvd354"
    db_user="s_qvd"
    db_password="Ttmq6yAbH4FAnFgJ"

    if sys.platform == 'darwin':
        connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
    else:
        connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'

    # Establish a connection
    connection = pypyodbc.connect(connection_string)

except pypyodbc.DatabaseError:
    print("None")
    
# # Create a cursor to interact with the database
cursor = connection.cursor()

tool = Functionality()
tool.setCursor(cursor)
tool.setConnection(connection)
#Search for business
# filter = SEARCH_BUSINESS_FILTER("NAME", "The")
# order = SEARCH_BUSINESS_ORDER("NAME")
# row = tool.search_business(filter, order)

tool.review_business(business_id="HcpNb94i-VDtEqwNPcXuQQ", user_id="ZDZbC0SOcq6J7DMQ3so4jA", star=1)
# #Search for user
# filter = SEARCH_USER_YELP('NAME', "Vi")
# row = tool.search_users(filter)

# for r in row:
#     print(r)
# cursor.execute("INSERT INTO review (review_id, user_id, business_id, stars) \
#                    VALUES ('10000000001', 'ZDZbC0SOcq6J7DMQ3so4jA', 'HcpNb94i-VDtEqwNPcXuQQ', 1);")

cursor.execute("SELECT * FROM review WHERE review.business_id = 'HcpNb94i-VDtEqwNPcXuQQ' ORDER BY review.date")
row  = cursor.fetchall()

for r in row:
    print(r)

# cursor.execute("SELECT * FROM business WHERE business_id = 'HcpNb94i-VDtEqwNPcXuQQ'")
# row  = cursor.fetchall()

# for r in row:
#     print(r)

# # id = 'zwtWUXjp4BT0JPeMP9GcWA'
# # if tool.login(id):
# #     print("True")
# # else:
# #     print("False")

# # Check a user friendship
# if tool.make_friend('Q5jOFJYhIsN8ouJ1rnsLQQ', 'Txw2jX2ltayJOiMvvTW8A'):
#     print("Make friend")
# else:
#     print("They exists")

# # Close the cursor and connection when done
# cursor.close()
# connection.close()