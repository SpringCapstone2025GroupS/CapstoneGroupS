
from airport_data.types import Airport

'''
Airport Code Validator Component

Features:
    - Validates if airport code exists and is from the Continental United States
'''
class AirportCodeValidator: 
    @staticmethod
    def is_valid(airport: Airport):
        """
        Validates if the airport is part of Continental United States

        Args:
            airport (Airport): Airport object.

        Returns:
            True: Valid Continental United States airport
            False: Airport outside Continental United States.
        """


        if airport.country != "United States":
            return False
        
        return airport.tz_name not in ["Pacific/Honolulu", "America/Anchorage"]