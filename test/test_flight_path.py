# type: ignore error
import pytest
from flight_path.flight_path import FlightPath
from geographiclib.geodesic import Geodesic
from flight_path.flight_path import FlightPath
from flight_path.exceptions import AirportNotFoundError

# Test to check for the return type. It should be a tuple of length 2.
def test_get_coordinates_valid():
    flight_path = FlightPath("JFK", "LAX") # => manually these are correct ones!
    assert isinstance(flight_path.departure, tuple)
    assert len(flight_path.departure) == 2

# Tests for invalid airports
def test_get_coordinates_invalid():
    """Test if __get_coordinates raises an AirportNotFoundError for an invalid airport code."""
    with pytest.raises(AirportNotFoundError):
        FlightPath("INVALID", "LAX")  # Invalid departure code

    with pytest.raises(AirportNotFoundError):
        FlightPath("JFK", "INVALID")  # Invalid destination code

    with pytest.raises(AirportNotFoundError):
        FlightPath("INVALID", "INVALID")  # Both invalid

# Tests the size of the waypoints list is correct.
# Essentially if n is the number of waypoints, the returned list should have n+2
# +2 for the departure airport, and destinaton airport
@pytest.mark.parametrize("n", [0, 1, 5, 10, 150, 202, 34468, 4444])
def test_get_waypoints_by_num(n: int):
    flight_path = FlightPath("JFK", "LAX")
    waypoints = flight_path.get_waypoints_by_num(n)
    assert len(waypoints) == n + 2 

# Test if waypoints list that is returned is a set of unique coordinates.
def test_waypoints_not_identical():
    flight_path = FlightPath("JFK", "LAX")
    waypoints = flight_path.get_waypoints_by_num(5)
    
    unique_waypoints = len(set(waypoints)) 
    assert unique_waypoints == len(waypoints), "Waypoints should be unique"

# Test if each waypoint lies on the great-circle path
@pytest.mark.parametrize("n", [1, 5, 10, 50])
def test_waypoints_on_great_circle(n):
    flight_path = FlightPath("JFK", "LAX")
    waypoints = flight_path.get_waypoints_by_num(n)

    # Calculate the initial bearing from the departure airport to the destination airport
    expected_bearing = Geodesic.WGS84.Inverse(
            flight_path.departure[0], flight_path.departure[1], 
            flight_path.destination[0], flight_path.destination[1],
        )["azi1"]

    # Check that each waypoint (excluding start & end) is aligned
    for waypoint in waypoints[1:-1]:  # Exclude departure and destination

        # Calculate the initial bearing from the departure airport to the waypoint
        waypoint_bearing = Geodesic.WGS84.Inverse(
            flight_path.departure[0], flight_path.departure[1], 
            waypoint[0], waypoint[1]
        )["azi1"]

        # Allow small margin of error because of floating point calculations
        assert abs(waypoint_bearing - expected_bearing) < 1.0, f"Waypoint {waypoint} deviates from the great-circle path."
