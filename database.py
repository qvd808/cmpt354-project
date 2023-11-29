import pypyodbc

class Database:
    def __init__(self, db_host, db_name, db_user, db_password) -> None:
        connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
        self.database = pypyodbc.connect(connection_string)
    
    def get_cursor(self):
        return self.database.cursor()

    