import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def check_data_entry(prompt, valid_entries): 
    
    """
    Function that asks the user to input data and verifies if it's valid.
    This simplifies the get_filters() function, where we need to ask the user for three inputs.
    Args:
        (str) prompt - message to show to the user
        (list) valid_entries - list of accepted strings 
    Returns:
        (str) user_input - user's valid input
    """
	
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries : 
            print('It looks like your entry is incorrect.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! You\'ve chosen: {}\n'.format(user_input))
        return user_input

    except:
        print('There seems to be an issue with your input.')
              

              
def get_filters():
	
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
	
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs  
    valid_cities = CITY_DATA.keys()
    prompt_cities = '\nChoose one of the 3 cities (chicago, new york city, washington):\n>> '
    city = check_data_entry(prompt_cities, valid_cities)          

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Choose a month (all, january, february, ... , june):\n>> '
    month = check_data_entry(prompt_month, valid_months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Choose a day (all, monday, tuesday, ... sunday):\n>> '
    day = check_data_entry(prompt_day, valid_days)


    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a DataFrame
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    
    # Convert the 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of the week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Filter by month
    if month != 'all':
       months_list = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months_list.index(month) + 1
       df = df[df['month'] == month]
    
    # Filter by day of the week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month for travel is:", common_month)

    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week for travel is:", common_day_of_week)


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour for travel is:", common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is:\n", df ['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print("\nThe most commonly used end station is:\n", df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    start_station, end_station = common_combination
    print("\nThe most frequent combination of start station and end station is:")
    print("* Start Station:", start_station)
    print("* End Station:", end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time:", total_travel_time/3600.0, "hours")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_travel_time/3600.0, "hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types)
    
    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)
    else:
        print("\nCounts of Gender: Data not available !")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])

        print("\nEarliest Birth Year:", earliest_birth)
        print("Most Recent Birth Year:", most_recent_birth)
        print("Most Common Birth Year:", most_common_birth)
    else:
        print("\nEarliest, most recent, and most common year of birth: Data not available !\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
    # Function for displays individual trip data to the user.
def display_data(df):
    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n>> ').lower()           
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("\nDo you wish to continue? Enter yes or no:\n>> ").lower()
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n>> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
