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
    def __init__(self, cursor) -> None:
        self.cursor = cursor
    
    def login(self, user_id) -> None:
        '''
        Does it log the current user???
        '''
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
        
        search = "SELECT * FROM business"

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

    def make_friend():
        pass
    
    def review_business(business_id, stars):
        pass