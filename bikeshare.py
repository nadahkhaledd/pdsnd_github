import time
import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

choices = ('month', 'day', 'both', 'none')


def looping(msg, array):
    """
    takes choice and loop until it gets it right

    Returns:
        (str) data - choice after modification
    """
    flag = True
    while flag:
        data = input(msg).lower().strip()
        if data in array:
            flag = False
        else:
            print('wrong input, please try again and enter valid name')
    return data


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = looping('Would you like to see data for Chicago, New York, or Washington?\n', CITY_DATA)

    month, day = 'all', 'all'
    while(True):
        # get input for how user would like to filter data displayed
        choice = input('Would you like to filter the data by month, day, both, none?\n').lower().strip()
        if (choice in choices):
            if choice == 'month':
                # get user input for month (all, january, february, ... , june)
                month = looping('Which month - January, February, March, April, May, or June?\n', months)

            elif choice == 'day':
                # get user input for day of week (all, monday, tuesday, ... sunday)
                day = looping('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n', days)

            elif choice == 'both':
                # get user input for both month and day of week
                month = looping('Which month - January, February, March, April, May, or June?\n', months)
                day = looping('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n', days)
            break
        else:
            print('wrong input, please try again')



    print('-' * 40)
    return city, month, day, choice


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

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day and hour of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, choice):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month: ', common_month)

    # display the most common day of week
    common_weekday = df['day_of_week'].mode()[0]
    print('Most common day of week: ', common_weekday)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour: ', common_hour)

    #display filter
    print('\nchosen filter: ', choice)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df, choice):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start - End Stations Combination'] = '(' + df['Start Station'] + ')' + ' -> ' + '(' + df['End Station'] + ')'
    common_combination_stations = df['Start - End Stations Combination'].mode()[0]
    print('Most frequent combination of start station and end station trip: ', common_combination_stations)

    # display filter
    print('\nchosen filter: ', choice)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df, choice):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print('total travel time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    print('total travel time: ', mean_travel_time)

    # display filter
    print('\nchosen filter: ', choice)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print('Count of each user type:-\n', user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts().to_string()
        print('\nCount of each gender:-\n', gender_types)
    except KeyError:
        print("There is no data for gender in {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_person = int(df['Birth Year'].min())
        print('\noldest person to ride a bike was born in: ', oldest_person)

        youngest_person = int(df['Birth Year'].max())
        print('youngest person to ride a bike was born in: ', youngest_person)

        most_common_year = int(df['Birth Year'].mode()[0])
        print('most common year of birth is: ', most_common_year)
    except KeyError:
        print('There is no data for birth years in {}'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day, choice = get_filters()
        df = load_data(city, month, day)

        # showing statistics
        time_stats(df, choice)
        station_stats(df, choice)
        trip_duration_stats(df, choice)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
