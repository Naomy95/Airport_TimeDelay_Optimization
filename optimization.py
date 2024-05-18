import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_flights = 100  # Number of flight departures and landings
start_time = datetime.now()
runways = [1, 2, 3, 4]
aircraft_types = ['A320', 'B737', 'B747', 'A380', 'C343']
min_flight_duration = 30  # Minimum flight duration in minutes
max_flight_duration = 300  # Maximum flight duration in minutes
buffer_time = timedelta(hours=1)  # Buffer time between events on the same runway

# Generate flight times
np.random.seed(42)
flight_intervals = np.random.exponential(scale=10, size=num_flights)
flight_times = [start_time + timedelta(minutes=int(sum(flight_intervals[:i+1]))) for i in range(num_flights)]

# Generate landing times
landing_intervals = np.random.exponential(scale=10, size=num_flights)
landing_times = [start_time + timedelta(minutes=int(sum(landing_intervals[:i+1]))) for i in range(num_flights)]

# Assign aircraft types
aircraft_assigned_for_departure = np.random.choice(aircraft_types, size=num_flights)
aircraft_assigned_for_landing = np.random.choice(aircraft_types, size=num_flights)

# Generate unique plane numbers for each aircraft type
plane_numbers_for_departure = [f"{aircraft}_{i}_dep" for i, aircraft in enumerate(aircraft_assigned_for_departure)]
plane_numbers_for_landing = [f"{aircraft}_{i}_land" for i, aircraft in enumerate(aircraft_assigned_for_landing)]

# Assign runways
runways_for_departure = np.random.choice(runways, size=num_flights)
runways_for_landing = np.random.choice(runways, size=num_flights)

# Create DataFrame for departures
departures = pd.DataFrame({
    'Event': 'Departure',
    'Time': flight_times,
    'Aircraft Type': aircraft_assigned_for_departure,
    'Plane Number': plane_numbers_for_departure,
    'Runway': runways_for_departure
})

# Create DataFrame for landings
landings = pd.DataFrame({
    'Event': 'Landing',
    'Time': landing_times,
    'Aircraft Type': aircraft_assigned_for_landing,
    'Plane Number': plane_numbers_for_landing,
    'Runway': runways_for_landing
})

# Combine departures and landings into one DataFrame
flight_schedule = pd.concat([departures, landings]).sort_values(by='Time').reset_index(drop=True)

# Function to optimize schedule by avoiding runway conflicts
def optimize_schedule(flight_schedule, runways, buffer_time):
    for runway in runways:
        runway_events = flight_schedule[flight_schedule['Runway'] == runway].sort_values(by='Time')
        for i in range(1, len(runway_events)):
            if i >= len(runway_events):
                break  # Ensure we don't access out-of-bounds indices
            if runway_events.iloc[i]['Time'] < runway_events.iloc[i-1]['Time'] + buffer_time:
                available_runways = set(runways) - {runway_events.iloc[i]['Runway']}
                if not available_runways:
                    break  # No available runways, exit loop
                new_runway = next(iter(available_runways))
                flight_schedule.at[runway_events.index[i], 'Runway'] = new_runway
                runway_events = flight_schedule[flight_schedule['Runway'] == runway].sort_values(by='Time')
    return flight_schedule

# Optimize the flight schedule to avoid conflicts
optimized_schedule = optimize_schedule(flight_schedule, runways, buffer_time)

# Display the first few rows of the optimized flight schedule
print(optimized_schedule.head())

# Additional check to see multiple departures and landings on the same runway
print(optimized_schedule.groupby(['Runway', 'Event']).size())
