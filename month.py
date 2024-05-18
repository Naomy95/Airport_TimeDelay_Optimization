import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_days = 30  # Number of days for the month
num_flights_per_day = 50  # Number of flight departures and landings per day
start_time = datetime.now()
runways = [1, 2, 3, 4]
airlines = [
    'American Airlines', 'Delta Air Lines', 'United Airlines', 'Southwest Airlines', 'Lufthansa',
    'British Airways', 'Air France', 'KLM Royal Dutch Airlines', 'Emirates', 'Qatar Airways',
    'Singapore Airlines', 'Cathay Pacific', 'Qantas', 'ANA (All Nippon Airways)', 'Japan Airlines',
    'Turkish Airlines', 'Air Canada', 'Etihad Airways', 'Virgin Atlantic', 'Alaska Airlines'
]
min_flight_duration = 30  # Minimum flight duration in minutes
max_flight_duration = 120  # Maximum flight duration in minutes

# Function to generate flight data for a single day
def generate_daily_flight_schedule(day):
    np.random.seed(day)  # Set seed based on day for reproducibility
    flight_intervals = np.random.exponential(scale=5, size=num_flights_per_day)  # Shorter intervals
    flight_times = [start_time + timedelta(minutes=int(sum(flight_intervals[:i+1]))) for i in range(num_flights_per_day)]
    
    landing_intervals = np.random.exponential(scale=5, size=num_flights_per_day)  # Shorter intervals
    landing_times = [start_time + timedelta(minutes=int(sum(landing_intervals[:i+1]))) for i in range(num_flights_per_day)]

    aircraft_assigned_for_departure = np.random.choice(airlines, size=num_flights_per_day)
    aircraft_assigned_for_landing = np.random.choice(airlines, size=num_flights_per_day)

    plane_numbers_for_departure = [f"{aircraft}_{i}_dep" for i, aircraft in enumerate(aircraft_assigned_for_departure)]
    plane_numbers_for_landing = [f"{aircraft}_{i}_land" for i, aircraft in enumerate(aircraft_assigned_for_landing)]

    runways_for_departure = np.random.choice(runways, size=num_flights_per_day)
    runways_for_landing = np.random.choice(runways, size=num_flights_per_day)

    departures = pd.DataFrame({
        'Event': 'Departure',
        'Time': flight_times,
        'Aircraft Type': aircraft_assigned_for_departure,
        'Plane Number': plane_numbers_for_departure,
        'Runway': runways_for_departure
    })

    landings = pd.DataFrame({
        'Event': 'Landing',
        'Time': landing_times,
        'Aircraft Type': aircraft_assigned_for_landing,
        'Plane Number': plane_numbers_for_landing,
        'Runway': runways_for_landing
    })

    daily_schedule = pd.concat([departures, landings]).sort_values(by='Time').reset_index(drop=True)
    return daily_schedule

# Function to optimize schedule for a single day
def optimize_daily_schedule(daily_schedule):
    runway_dict = {}
    for index, row in daily_schedule.iterrows():
        runway = row['Runway']
        event_time = row['Time']
        if runway in runway_dict:
            prev_event_time = runway_dict[runway]
            if event_time < prev_event_time + timedelta(hours=1):
                available_runways = set(runways) - {runway}
                for alt_runway in available_runways:
                    if alt_runway not in runway_dict or event_time >= runway_dict[alt_runway] + timedelta(hours=1):
                        daily_schedule.at[index, 'Runway'] = alt_runway
                        runway_dict[alt_runway] = event_time
                        print(f"Changed runway for {row['Event']} at index {index} to runway {alt_runway}")
                        break
            else:
                runway_dict[runway] = event_time
        else:
            runway_dict[runway] = event_time
    return daily_schedule

# Generate and display flight schedule for each day of the month
print("Flight Schedule for Each Day of the Month (Raw Data and Optimized Data):")
for day in range(num_days):
    start_day = start_time + timedelta(days=day)
    print(f"\nDay {day+1} ({start_day.strftime('%Y-%m-%d')}):")
    daily_schedule_raw = generate_daily_flight_schedule(day)
    print("\nRaw Data:")
    print(daily_schedule_raw)
    
    daily_schedule_optimized = optimize_daily_schedule(daily_schedule_raw.copy())
    print("\nOptimized Data:")
    print(daily_schedule_optimized)
