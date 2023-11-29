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


class Functionality:
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def search_business(self, filter:SEARCH_BUSINESS_FILTER, orders: SEARCH_BUSINESS_ORDER) -> str:
        search = "SELECT * FROM business"

        search += " "

        match filter.variant:
            case "MIN_STAR":
                search += f"WHERE business.stars >= {filter.value}"
            case "CITY":
                search += f"WHERE business.city = {filter.value}"
            case "NAME":
                search += f"WHERE business.name LIKE '%{filter.value}%'"

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

    def search_users():
        pass

    def make_friend():
        pass
    
    def review_business():
        pass