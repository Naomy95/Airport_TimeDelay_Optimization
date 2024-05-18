import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_flights = 100  # Number of flights (plane departures)
start_time = datetime.now()
runways = [1, 2, 3, 4]
aircraft_types = ['A320', 'B737', 'B747', 'A380', 'C343']

# Generate flight times
np.random.seed(42)
flight_intervals = np.random.exponential(scale=10, size=num_flights)  # Exponential distribution for inter-arrival times
flight_times = [start_time + timedelta(minutes=int(sum(flight_intervals[:i+1]))) for i in range(num_flights)]

# Assign aircraft types
aircraft_assigned = np.random.choice(aircraft_types, size=num_flights)

# Generate unique plane numbers for each aircraft type
plane_numbers = [f"{aircraft}_{i}" for i, aircraft in enumerate(aircraft_assigned)]

# Assign runways
runway_assigned = np.random.choice(runways, size=num_flights)

# Create DataFrame
flight_schedule = pd.DataFrame({
    'Flight Time': flight_times,
    'Aircraft Type': aircraft_assigned,
    'Plane Number': plane_numbers,
    'Runway': runway_assigned
})

# Display the first few rows of the flight schedule
print(flight_schedule.head())
