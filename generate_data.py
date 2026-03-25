import pandas as pd
import numpy as np
from datetime import timedelta, date
import random

# Generate a date range for 365 days starting from 2025-01-01
def generate_date_series(start_date, num_days):
    return [start_date + timedelta(days=i) for i in range(num_days)]

# Function to generate random normal distributed data
# Given mean, std deviation, minimum, and maximum

def generate_normal_data(size, mean, std, min_val, max_val):
    data = np.random.normal(mean, std, size)
    data = np.clip(data, min_val, max_val)  # Ensuring values are within min and max
    return data

# Introduce random NaN values for 5% of the data
def introduce_nan(data, nan_fraction=0.05):
    # Convert integer arrays to float to allow NaN insertion
    if np.issubdtype(data.dtype, np.integer):
        data = data.astype(float)

    total_values = data.size
    num_nans = int(total_values * nan_fraction)
    indices = random.sample(range(total_values), num_nans)
    flat_data = data.flatten()
    for index in indices:
        flat_data[index] = np.nan
    return flat_data.reshape(data.shape)

# Main function to generate and save the data
def generate_fitness_data():
    num_days = 365
    start_date = date(2025, 1, 1)
    dates = generate_date_series(start_date, num_days)
    
    # Generate columns with realistic data
    steps = generate_normal_data(num_days, 8500, 2500, 3000, 18000)
    sleep_hours = generate_normal_data(num_days, 7.2, 1, 4.5, 9.5)
    heart_rate_bpm = generate_normal_data(num_days, 68, 10, 48, 110)
    calories_burned = np.random.randint(1800, 4200, num_days)
    active_minutes = np.random.randint(20, 180, num_days)

    # Introduce random NaN values
    steps = introduce_nan(steps)
    sleep_hours = introduce_nan(sleep_hours)
    heart_rate_bpm = introduce_nan(heart_rate_bpm)
    calories_burned = introduce_nan(calories_burned)
    active_minutes = introduce_nan(active_minutes)

    # Create a DataFrame
    data = pd.DataFrame({
        'date': dates,
        'steps': steps,
        'sleep_hours': sleep_hours,
        'heart_rate_bpm': heart_rate_bpm,
        'calories_burned': calories_burned,
        'active_minutes': active_minutes
    })
    
    # Save to CSV
    data.to_csv('data/health_data.csv', index=False)

if __name__ == '__main__':
    generate_fitness_data()

