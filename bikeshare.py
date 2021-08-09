import time
import datetime
import pandas as pd
import numpy as np
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 99}

week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6, 'all': 99}

filter_opts = {'day': ['all', ''], 'month': ['', 'all'], 'both': ['',''], 'none': ['all', 'all']}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    clear()
    print('Hello! Let\'s explore some US bikeshare data!')
        
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city, month, day, filter_opt = '', '', '', ''
    
    while city not in CITY_DATA:
        print('\nWould you like to see data for')
        for city in CITY_DATA.keys():
            print(color.BOLD + city.title() + color.END)
        city = input('\nSelect a city (input is not case sensitive): ').lower()
        
        if city not in CITY_DATA:
            try_again(city)
      
    clear()
    
    while filter_opt not in filter_opts:
        print('\nWould you like to filter the data for ' + color.BOLD + city.title() + color.END + ' by:')
        for opt in filter_opts:
            print(color.BOLD + opt.title() + color.END)
        filter_opt = input('\nSelect Day, Month, Both or None (input is not case sensitive): ').lower()
        if filter_opt not in filter_opts:
            try_again(filter_opt)
        else:
            month, day = filter_opts[filter_opt]    
        
    
    # TO DO: get user input for month (all, january, february, ... , june)
    if month == '':
        clear()
        while month not in months:
            print('\n' + color.BOLD + city.title() + color.END +'\nWhich month:')
            for month in months:
                print(color.BOLD + month.title() + color.END)
            month = input('\nSelect a month or ALL (input is not case sensitive): ').lower()

            if month not in months:
                try_again(month)
            

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if day == '':
        clear()
        while day not in week:
            print('\n' + color.BOLD + city.title() + color.END +'\nWhich day:')
            for day in week:
                print(color.BOLD + day.title() + color.END)
            day = input('\nSelect a day or ALL (input is not case sensitive): ').lower()
            if day not in week:
                try_again(day)

    print('-'*40)
    return city, month, day


def try_again(input_str):
    clear()
    print(color.BOLD + color.RED + input_str.title() + color.END + ' is not a valid option, please try again')

def clear():
    os.system('clear')


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

    df = pd.read_csv(CITY_DATA[city], parse_dates = ['Start Time'])
    if (month != 'all' and day == 'all'):
        df = df[(df['Start Time'].dt.month == months[month])]
    elif (month == 'all' and day != 'all'):
        df = df[(df['Start Time'].dt.dayofweek == week[day])]
    elif (month != 'all' and day != 'all'):
        df = df[(df['Start Time'].dt.month == months[month]) & (df['Start Time'].dt.dayofweek == week[day])]
    
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Start Time'].dt.month.mode()[0]
    
    agg_months = df.groupby(df['Start Time'].dt.month.rename('Month')).agg('count').sort_values(['Start Time'], ascending=False)
    count = agg_months.iloc[0]['Start Time']
    
    for key, value in months.items():
        if value == common_month:
            print('The most common month is:\n{} with {} trips\n'.format(color.BOLD + key.title() + color.END, color.BOLD + str(count) + color.END))
    

    # TO DO: display the most common day of week
    common_day = df['Start Time'].dt.dayofweek.mode()[0]
    agg_days = df.groupby(df['Start Time'].dt.dayofweek.rename('Day')).agg('count').sort_values(['Start Time'], ascending=False)
    count = agg_days.iloc[0]['Start Time']

    for key, value in week.items():
        if value == common_day:
            print('The most common day is:\n{} with {} trips\n'.format(color.BOLD + key.title() + color.END, color.BOLD + str(count) + color.END))
            
    # TO DO: display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    agg_hours = df.groupby(df['Start Time'].dt.hour.rename('Hour')).agg('count').sort_values(['Start Time'], ascending=False)
    count = agg_hours.iloc[0]['Start Time']

    print('The most common hour of the day is:\n{} with {} trips\n'.format(color.BOLD + str(common_hour) + color.END, color.BOLD + str(count) + color.END))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_st = df['Start Station'].mode()[0]
    
    print('The most common used start station is:\n{}\n'.format(color.BOLD + common_start_st + color.END))

    # TO DO: display most commonly used end station
    common_end_st = df['End Station'].mode()[0]
    print('The most common used end station is:\n{}\n'.format(color.BOLD + common_end_st + color.END))


    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + 'to' + df['End Station']
    common_comb_sts = df['Station Combination'].mode()[0]
    print('The most frequent combination of start and end stations is:\n{}\n'.format(color.BOLD + common_comb_sts + color.END))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time was:\n{} seconds\n'.format(color.BOLD + str(total_time) + color.END))

    # TO DO: display mean travel time
    
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time was:\n{} senconds\n'.format(color.BOLD + str(mean_time) + color.END))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    # TO DO: Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('There is no gender information for users for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_bd = str(int(df['Birth Year'].min()))
        recent_bd = str(int(df['Birth Year'].max()))
        common_bd_year = str(int(df['Birth Year'].mode()[0]))

        print('\n\nUsers years of birth:\nThe earliest is {}\nThe most recent is {}\nThe most common is {}'.format(color.BOLD + earliest_bd + color.END,
                                                                                                          color.BOLD + recent_bd + color.END,
                                                                                                          color.BOLD + common_bd_year + color.END))
    else:
        print('There is no birth year information for users for this city')
                                                                                                      
                                                                                                      

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw(df):
    row_position, raw_display = 0 ,''
    
    RAW_OPTIONS = ['yes','no']
    
    while raw_display not in RAW_OPTIONS:
        print('\n\nWould you like to see bikeshare raw data for your selection?')
        raw_display = input('\nEnter yes or no (input is not case sensitive): ').lower()
        
        if raw_display not in RAW_OPTIONS:
            try_again(raw_display)

    print(raw_display)
    
    while raw_display != 'no':
        if raw_display == 'yes':
            print(df[row_position : row_position + 5])
            row_position += 5
        
        print('\n\nWould you like to see five more rows of data')
        raw_display = input('\nEnter yes or no (input is not case sensitive): ').lower()
        
        if raw_display not in RAW_OPTIONS:
            try_again(raw_display)

def main():
    
    
                      
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
