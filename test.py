from tools.functionality import Functionality, SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER, SEARCH_USER_YELP
import pypyodbc
from dotenv import dotenv_values

config = dotenv_values(".env")  # take environment variables from .env.

db_host = config['DB_HOST']
db_name = config['DB_NAME']
db_user = config['DB_USER']
db_password = config['DB_PASSWORD']

try:
    connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
    # Establish a connection
    connection = pypyodbc.connect(connection_string)
    print(connection)

except pypyodbc.DatabaseError:
    print("None")
    
# Create a cursor to interact with the database
cursor = connection.cursor()

tool = Functionality()
tool.setCursor(cursor)
# # #Search for business
# # filter = SEARCH_BUSINESS_FILTER("NAME", "The")
# # order = SEARCH_BUSINESS_ORDER("NAME")
# # row = tool.search_business(filter, order)

#Search for user
filter = SEARCH_USER_YELP('NAME', "Vi")
row = tool.search_users(filter)

for r in row:
    print(r)

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