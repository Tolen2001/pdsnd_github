import time
import pandas as pd
import numpy as np
from tabulate import tabulate

# Dictionary storing the file names for each city
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def validate_input(prompt, valid_options):
    """
    Function to validate user input.

    Inputs:
        prompt (str): The message shown to the user.
        valid_options (list): List of valid options.

    Output:
        str: The valid user input.
    """
    while True:
        user_input = input(prompt).strip().casefold()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from: {', '.join(valid_options)}")

def get_filters():
    """
         Get filters from the user for data analysis, including city, month, day, and analysis type (customers or trips).
    """
    analysis_type = validate_input("Do you want to analyze customer data or trip data? (customers/trips): ", ['customers', 'trips'])

    # For customer analysis
    if analysis_type == 'customers':
        city = validate_input("Enter the city name (Chicago, New York City, Washington): ", ['chicago', 'new york city', 'washington'])
        month = validate_input("Enter the month (January, February, ..., December, all): ", ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all'])
        day = validate_input("Enter the day of the week (Monday, Tuesday, ..., Sunday, all): ", ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])
        gender = validate_input("Would you like to analyze by gender? (yes/no): ", ['yes', 'no'])
        birth_year = validate_input("Would you like to analyze by birth year? (yes/no): ", ['yes', 'no'])

        return analysis_type, [city], month, day, gender, birth_year

    # For trip analysis
    elif analysis_type == 'trips':
        cities_input = input("Enter the city name(s) (Chicago, New York City, Washington) separated by commas: ").casefold()
        cities = [city.strip() for city in cities_input.split(',') if city.strip() in CITY_DATA.keys()]
        if not cities:
            print("Error: No valid cities entered. Please try again.")
            return get_filters()

        month = validate_input("Enter the month (January, February, ..., December, all): ", ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all'])
        day = validate_input("Enter the day of the week (Monday, Tuesday, ..., Sunday, all): ", ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

        return analysis_type, cities, month, day, None, None

def load_data(city, month='all', day='all'):
    """
    Load data for the specified city and filter by month and day if applicable.

    Inputs:
        city (str): The city name.
        month (str): The month to filter by or 'all' if no filtering.
        day (str): The day of the week to filter by or 'all' if no filtering.

    Output:
        DataFrame: The filtered data or None if no valid data is found.
    """
    if city not in CITY_DATA:
        print(f"Error: Invalid city name '{city}'. Skipping this city.")
        return None

    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"Error: Data file for {city} not found.")
        return None

    # Convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of the week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.casefold()

    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month_index = months.index(month.casefold()) + 1
        if month_index in df['month'].unique():
            df = df[df['month'] == month_index]
        else:
            print(f"No data available for the month '{month.title()}'.")
            return None

    # Filter by day of the week
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day.casefold() in days:
            df = df[df['day_of_week'] == day.casefold()]
        else:
            print(f"Error: Invalid day '{day}'. Please enter a valid day of the week.")
            return None

    return df

def analyze_customers(df, gender, birth_year):
    if gender == 'yes' and 'Gender' in df.columns:
        gender_stats(df)

    if birth_year == 'yes' and 'Birth Year' in df.columns:
        birth_year_stats(df)

def gender_stats(df):
    print(f"\nGender Analysis:")
    print(f"Number of male customers: {df[df['Gender'] == 'Male'].shape[0]}")
    print(f"Number of female customers: {df[df['Gender'] == 'Female'].shape[0]}")

def birth_year_stats(df):
    print(f"\nBirth Year Analysis:")
    print(f"Oldest customer: {df['Birth Year'].min()}")
    print(f"Youngest customer: {df['Birth Year'].max()}")
    print(f"Average birth year: {df['Birth Year'].mean():.2f}")

def analyze_trips(city, df):
    print(f"\nAnalyzing data for {city.title()}...\n")
    trip_duration_stats(df)
    time_stats(df)
    station_stats(df)
    return df['Rental Duration'].sum(), df.shape[0]

def trip_duration_stats(df):
    df['Rental Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    total_duration = df['Rental Duration'].sum() / 60
    print(f"Total trip duration: {total_duration:.2f} minutes")
    avg_duration = df['Rental Duration'].mean() / 60
    print(f"Average trip duration: {avg_duration:.2f} minutes")

def time_stats(df):
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of the week: {most_common_day.title()}")

    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")

def station_stats(df):
    print(f"\nMost common start and end stations:")
    start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {start_station}")
    end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {end_station}")

def display_data(df):
    """
    Displays data rows in batches of 5 and asks the user if they want to see more.
    
    Input:
        df (DataFrame): The data to be displayed.
    """
    row_count = 0
    while row_count < df.shape[0]:
        
        print("\nDisplaying data rows:")
        print(df.iloc[row_count:row_count + 5])  
        
        row_count += 5
        
        if row_count < df.shape[0]:
            more_data = input("Would you like to see 5 more rows? (yes/no): ").lower()
            while more_data not in ['yes', 'no']:
                more_data = input("Invalid input. Please enter 'yes' or 'no': ").lower()
            if more_data == 'no':
                break


def repeat_analysis():
    while True:
        analysis_type, cities, month, day, gender, birth_year = get_filters()

        if analysis_type == 'trips':
            total_durations = {}
            total_counts = {}

            for city in cities:
                print(f"\nAnalyzing data for {city.title()}...\n")
                df = load_data(city, month, day)
                if df is not None:
                    total_duration, total_count = analyze_trips(city, df)
                    total_durations[city] = total_duration
                    total_counts[city] = total_count
                    display_data(df)
                else:
                    print(f"No data available for {city.title()}. Skipping analysis for this city.")

            # Display summary of cities with the most trips and longest duration
            if total_durations:
                most_duration_city = max(total_durations, key=total_durations.get)
                most_trips_city = max(total_counts, key=total_counts.get)

                print("\nSummary:")
                print(f"City with the longest total trip duration: {most_duration_city.title()} ({total_durations[most_duration_city]:.2f} minutes)")
                print(f"City with the most trips: {most_trips_city.title()} ({total_counts[most_trips_city]} trips)")

        elif analysis_type == 'customers':
            city = cities[0]
            df = load_data(city, month, day)
            if df is not None:
                analyze_customers(df, gender, birth_year)
                display_data(df)

        # Ask user if they want to perform another analysis
        repeat = validate_input("Would you like to perform another analysis? (yes/no): ", ['yes', 'no'])
        if repeat == 'no':
            print("Thank you for using the data analysis tool. Goodbye!")
            break

if __name__ == "__main__":
    repeat_analysis()
