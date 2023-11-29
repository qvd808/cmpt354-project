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

# Example: execute a SQL query
cursor.execute("SELECT * FROM business")
rows = cursor.fetchall()

# Example: iterate through the results
for row in rows:
    print(row)

# Close the cursor and connection when done
cursor.close()
connection.close()