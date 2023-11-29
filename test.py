from tools.functionality import Functionality, SEARCH_BUSINESS_FILTER, SEARCH_BUSINESS_ORDER
import pypyodbc
from dotenv import dotenv_values

config = dotenv_values(".env")  # take environment variables from .env.

db_host = config['DB_HOST']
db_name = config['DB_NAME']
db_user = config['DB_USER']
db_password = config['DB_PASSWORD']

connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
# Establish a connection
connection = pypyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()

filter = SEARCH_BUSINESS_FILTER("MIN_STAR", 5)
order = SEARCH_BUSINESS_ORDER("NAME")

tool = Functionality(cursor)
row = tool.search_business(filter, order)
for r in row:
    print(r)

# Close the cursor and connection when done
cursor.close()
connection.close()