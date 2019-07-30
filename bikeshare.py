import time
import pandas as pd
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all')


# cities, months, weekdays 선택 코드
def choice(prompt, choices=('y', 'n')):
    while True:
        choice = input(prompt).lower().strip()  # 양쪽 공백제거, 소문자로 변경
        if choice == 'end':
            raise SystemExit
        elif choice == 'all':
            choice = []
            for i in range(len(choices)-1):
                choice.append(choices[i])
            break
        elif ',' not in choice:
            if choice in choices:
                break
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\n  Something is wrong. Please re-enter. \n")
    return choice


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
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        city = choice("Please type city name what you want:chicago, new york city, washington.\n", CITY_DATA.keys())
        month = choice("Please type month what you want:january, february, march, april, may, june.\n", months)
        day = choice("Please type day what you wnat:sunday, monday, tuesday, wednesday, thursday, friday, saturday.\n", weekdays)

        confirm = choice("\n Are you select City: {}, Month: {},   day: {}? \n Please answer y/n.".format(city, month, day))
        if confirm == 'y':
            break
        else:
            print("\n Let's try again.")
            city = choice("Please type city name what you want:chicago, new york city, washington.\n", CITY_DATA.keys())
            month = choice("Please type month what you want:january, february, march, april, may, june.\n", months)
            day = choice("Please type day what you want:sunday, monday, tuesday, wednesday, thursday, friday, saturday.\n", weekdays)

            confirm = choice("\n Are you select City: {}, Month: {},   day: {}? \n Please answer y/n.".format(city, month, day))

    print('-' * 40)
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

    start_time = time.time()


    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        try:
            df = df.reindex(
                columns=['Unnamed:0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station',
                         'User Type', 'Gender', 'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month) + 1)], month))

    else:
        df = df[df['Month'] == (months.index(month) + 1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))  # title() : 첫글자 대문자로 변환
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-' * 40)
    print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['Month'].mode()[0]  # mode()함수 : 최빈값 구하기
    print('Most common month is ' + str(months[most_common_month-1]).title() + '.')

    # TO DO: display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('Most common day is ' + most_common_day + '.')

    # TO DO: display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('Most common start hour is ' + str(most_common_hour) + '.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common start station is ' + most_common_start_station  + '.')

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common end station is ' + most_common_end_station + '.')

    # TO DO: display most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_start_end_combition = df['Start-End Combination'].mode()[0]
    print('Most common combination of start and end station is ' + most_common_start_end_combition + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = str(int(total_travel_time//(24*60*60))) + ' days ' + str(int((total_travel_time % (24*60*60))//(60*60))) + ' hours ' + \
                        str(int(((total_travel_time % (24*60*60))%(60*60))//60)) + ' minutes ' + str(int(((total_travel_time % (24*60*60))%(60*60))%60)) + ' seconds'
    print('Total travel time is ' + total_travel_time + '.')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = str(int(mean_travel_time//60)) + ' minutes ' + str(int(mean_travel_time % 60)) + ' seconds'
    print('Mean travel time is ' + mean_travel_time + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print('User type Distribution: \n' + user_types)

    if city == 'washington':
        pass
    else:
        # TO DO: Display counts of gender
        gender_counts = df['Gender'].value_counts().to_string()
        print('Gender Distribution : \n' + gender_counts)

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('Earliest birth year is {}.\nMost recent birth year is {}.\nMost common birth year is {}.'.format(earliest_birth_year,most_recent_birth_year, most_common_birth_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def data_display(df):    #사용자가 원할 시에만 5행 데이터 보여줌
    row_length = df.shape[0]
    for i in range(0,row_length, 5):
        answer = input("\nDo you like see the particular data? Please type yes/no.\n")
        if answer.lower() != 'yes':
            break
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)
         
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        data_display(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
