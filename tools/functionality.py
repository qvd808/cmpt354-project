import pypyodbc

class SEARCH_BUSINESS_FILTER:
    def __init__(self, variant, value):
        allowed_variant = ['MIN_STAR', "CITY", "NAME"]
        if variant not in allowed_variant:
            raise ValueError(f"The variant is not in {allowed_variant}")
        self.variant = variant
        self.value = value

class SEARCH_BUSINESS_ORDER:
    def __init__(self, variant):
        allowed_variant = ['NO_OF_STARS', "CITY", "NAME"]
        if variant not in allowed_variant:
            raise ValueError(f"The variant is not in {allowed_variant}")
        
        self.variant = variant

        match self.variant:
            case "NO_OF_STARS":
                self.value = "stars"
            case "CITY":
                self.value = "city"
            case "NAME":
                self.value = "name"

class SEARCH_USER_YELP:
    def __init__(self, variant, value):
        allowed_variant = ['MIN_REVIEW_COUNT', "MIN_AVG_STAR", "NAME"]
        if variant not in allowed_variant:
            raise ValueError(f"The variant is not in {allowed_variant}")
        
        self.variant = variant

        match self.variant:
            case "MIN_REVIEW_COUNT":
                if not (isinstance(value, float) or isinstance(value, int)):
                    raise ValueError(f"MIN_REVIEW_COUNT must be float or int")
            case "MIN_AVG_STAR":
                if not (isinstance(value, float) or isinstance(value, int)):
                    raise ValueError(f"MIN_REVIEW_COUNT must be float or int")
            case "NAME":
                if not isinstance(value, str):
                    raise ValueError(f"MIN_REVIEW_COUNT must be str")
                
        self.value = value


class Functionality:
    def __init__(self) -> None:
        self.cursor = None
        self.connection = None

    def cursorCheck(self):
        if self.cursor == None:
            raise ValueError("Cursor have not exists yet")

    def setCursor(self, cursor):
        self.cursor = cursor
    
    def setConnection(self, connection):
        self.connection = connection

    def init_connection(self, db_host, db_name, db_user, db_password):
        
        connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
        # Establish a connection
        connection = pypyodbc.connect(connection_string)
               
        return connection.cursor()

    def login(self, user_id) -> None:
        '''
        Does it log the current user???
        '''
        self.cursorCheck()
        self.cursor.execute(f"SELECT * FROM user_yelp WHERE user_yelp.user_id = '{user_id}'")

        if len(self.cursor.fetchall()) != 0:
            return True
        
        return False

    def search_business(self, filter:SEARCH_BUSINESS_FILTER, orders: SEARCH_BUSINESS_ORDER) -> str:
        '''
        Return the business the user search, 
        if the result is empty the application should handle that

        When search for the name do we search match anything after the string or do we 
        search for a string that contains the specific str

        '''
        self.cursorCheck()
        
        search = "SELECT business.business_id, business.name, business.address, business.city, business.stars FROM business"

        search += " "

        match filter.variant:
            case "MIN_STAR":
                search += f"WHERE business.stars >= {filter.value}"
            case "CITY":
                search += f"WHERE business.city = {filter.value}"
            case "NAME":
                search += f"WHERE business.name LIKE '{filter.value}%'"

        search += " "
        
        match orders.variant:
            case "NO_OF_STARS":
                search += f"ORDER BY business.{orders.value}"
            case "CITY":
                search += f"ORDER BY business.{orders.value}"
            case "NAME":
                search += f"ORDER BY business.{orders.value}"
        
        self.cursor.execute(search)

        return self.cursor.fetchall()

    def search_users(self, filter:SEARCH_USER_YELP):
        self.cursorCheck()
        
        search = "SELECT u.user_id, u.name, u.review_count, u.useful, u.funny, u.cool, u.average_stars, u.yelping_since FROM user_yelp u"
        search += " "

        match filter.variant:
            case "MIN_REVIEW_COUNT":
                search += f"WHERE u.review_count >= {filter.value}"
            case "MIN_AVG_STAR":
                search += f"WHERE u.average_stars >= {filter.value}"
            case "NAME":
                search += f"WHERE u.name like '{filter.value}%'"

        self.cursor.execute(search)
        return self.cursor.fetchall()

    def make_friend(self, user1, user2) -> bool:
        self.cursorCheck()

        '''
        Add two user to a friend ship table. Should check if the friend ship already exists
        '''
        self.cursor.execute(f"SELECT * FROM friendship WHERE user_id = '{user1}' AND friend = '{user2}'")
        row = self.cursor.fetchall()

        if len(row) != 0:
            return False

        self.cursor.execute(f"INSERT INTO friendship VALUES('{user1}', '{user2}')")
        self.connection.commit()
        return True

    
    def review_business(self,user_id, business_id, star):
        self.cursorCheck()
        import string
        import random
        
        # initializing size of string
        N = 22
        
        # using random.choices()
        # generating random strings
        random_id = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=N))
        command = f"INSERT INTO review (review_id, user_id, business_id, stars) VALUES ('{random_id}', '{user_id}', '{business_id}', {star});"
        self.cursor.execute(command)
        self.connection.commit()
        