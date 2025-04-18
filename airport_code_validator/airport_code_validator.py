
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


        if airport.country != "US":
            return False
        
        return airport.state_name not in ["HAWAII", "ALASKA", "PUERTO RICO", "GUAM", "AMERICAN SAMOA", "N MARIANA ISLANDS", "PUERTO RICO-VIRGIN ISLANDS"]