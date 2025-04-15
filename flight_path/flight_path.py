# type: ignore
import logging
from typing import Tuple, List
import pandas as pd
from geopy import Point
from collections import defaultdict
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
from .exceptions import AirportNotFoundError, GapIsNotValid
# to visualize
import folium

class FlightPath:
    '''
    Flight Path Component.

    This script calculates waypoints between two airports based on their ICAO/IATA codes.

    Features:
        - Reads airport data from a CSV file. (This will need to be changed when merging with the driver!!!!)
        - Retrieves coordinates for given airport codes. (Private)
        - Computes equally spaced waypoints along a great-circle path. (We can choose how may points along the path we want)
        - Uses GeographicLib for precise bearing calculations. (precise just means not in a straight line. Instead, this library takes into consideration the curvature of the earth!)

    '''

    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
    airport_data = pd.read_csv("airports.dat", names=columns, header=None)
    logger = logging.getLogger("FlightPath")

    def __init__(self, departure_code: str, destination_code: str):
        self.departure = self.__get_coordinates(departure_code)
        self.destination = self.__get_coordinates(destination_code)
        self.logger.info(f"Will be computing a flight path between "
                f"{departure_code} ({self.departure[0]},{self.departure[1]}) and "
                f"{destination_code} "
                f"({self.destination[0]},{self.destination[1]})")
        pass
    

    def __get_coordinates(self, airport_code) -> Tuple[float, float]:
        """
        Translates Airport Codes to Coordinates.

        Args:
            airport_code (str): Aiport Code (for now it is accepting both ICAO and IATA format)
    
        Returns:
            (latitude, longitude) tuple(str): Tuple of latitude and longitude of the airport position
        """
        row = self.airport_data.loc[(self.airport_data["ICAO"] == airport_code) | (self.airport_data["IATA"] == airport_code)] # This can be changed to only ICAC in the future when merging.

        if row.empty:
            raise AirportNotFoundError(f"Airport code '{airport_code}' not found in the dataset.")
        
        latitude = row.iloc[0]["Latitude"]
        longitude = row.iloc[0]["Longitude"]

        return latitude, longitude
    
    
    def get_waypoints_by_num(self, n: int) -> List[Tuple[float, float]]:
        """
        Generates `n` waypoints along the flight path.

        Uses the great-circle distance to compute equally spaced waypoints from 
        the departure airport to the destination.

        Args:
            n (int): Number of waypoints to generate.

        Returns:
            list: A list of tuples containing the latitude and longitude of each waypoint, including the departure and destination airport
        """
        # turn the coords into points using geopy library
        depart = Point(self.departure[0], self.departure[1])
        dest = Point(self.destination[0], self.destination[1])
        result = [(depart.latitude, depart.longitude)]
        
        # when dest == depart, we return the coordinates of the departure airport
        if (depart == dest):
            return result
        
        # find n points on the way
        total_dist = geodesic(depart, dest).miles # this is real world distance on earth, great-circle distance.
        step_size = total_dist/ (n+1)
        # get the direction of the two points, bearing (angle of the line)
        bearing = Geodesic.WGS84.Inverse(self.departure[0], self.departure[1], self.destination[0], self.destination[1])

        self.logger.debug(f"Computing {n} waypoints along route of length "
                f"{total_dist:.3f} nm with step size of {step_size:.3f} nm")

        for i in range(1, n+1):
            current_distance = step_size * i
            next_point = geodesic(miles = current_distance).destination(depart, bearing["azi1"]) # --> az1 here is the initial bearing (the angle of the line from the departure to the destination airport)
            result.append((next_point.latitude, next_point.longitude))
            self.logger.debug(f"Computed point {i}: ({next_point.latitude}, "
                    f"{next_point.longitude}), {current_distance:.3f} nm along route "
                    f"({(current_distance/total_dist)*100:.3f}%)" )
        
        result.append((dest.latitude, dest.longitude))
        
        return result
    
    def get_waypoints_by_gap(self, gap: float) -> List[Tuple[float, float]]:
        """
        Generates waypoints along the flight path based on a specified gap distance.

        Uses the great-circle distance to compute waypoints from 
        the departure airport to the destination, ensuring that each waypoint is approximately 'gap' miles apart.

        Args:
            gap (float): The distance (in miles) between each waypoint.

        Returns:
            list: A list of tuples containing the latitude and longitude of each waypoint.
        """
        depart = Point(self.departure[0], self.departure[1])
        dest = Point(self.destination[0], self.destination[1])

        # Calculate total great-circle distance between departure and destination
        total_dist = geodesic(depart, dest).miles  

        # Determine the number of waypoints based on the gap
        if gap <= 0:
            raise GapIsNotValid("Gap is not a valid number.")
        
        num_waypoints = int(total_dist // gap)  # Number of waypoints along the route

        return self.get_waypoints_by_num(num_waypoints)


# for testing purposes only!
def main():
    departure = input("Enter Departure Airport\n")
    destination = input("Enter Destination Airport\n")

    flight_path = FlightPath(departure, destination)

    gap = input("What is the gap?\n")
    waypoints = flight_path.get_waypoints_by_gap(float(gap)) # you can choose how many points you want between the depart and destination here.

    # to visualize
    m = folium.Map(location=waypoints[0], zoom_start=5)

    # Add pins for each coordinate on the map
    for coord in waypoints:
        folium.Marker(coord).add_to(m)

    m.save("../map.html")
    print("Map saved")

if __name__ == "__main__":
    main()
