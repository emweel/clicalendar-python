import calendar
import csv
import datetime
import os

YEAR = 2017
MONTH = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',\
    'August', 'September', 'October', 'November', 'December'
    ]

WEEK_HEADER = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
WEEK_HD_len = 22
FIRSTWEEKDAY = 0
CAL_MAPPING = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]

cal = calendar.Calendar(firstweekday = FIRSTWEEKDAY)
yearDays = cal.yeardatescalendar(YEAR)

EVENT_DICT = {}

########################################
# CSV DB

def check_db():
    '''
        Check whether csv file exist if not this function will create
        and empty csv file for database.
    '''
    if os.path.isfile('calendar_events.csv'):
        return True
    else:
        with open('calendar_events.csv', 'w') as f:
            print('intializing db...')

        return True

def event_db_write(event_dict):
    '''
        Save the added events by the end of program into a csv file.
    '''
    with open('calendar_events.csv', 'w') as f:
        fieldnames = ['date', 'event_type', 'event_des']
        writer = csv.DictWriter(f, fieldnames)

        dates = list(event_dict.keys())
        dates.sort()

        writer.writeheader()
        for date in dates:
            for event in event_dict[date]:
                writer.writerow({'date': date, 'event_type': event[0], 'event_des': event[1]})

def event_db_read(event_dict):
    '''
        Reads the event datebase from the calendar_events.csv.
    '''
    check_db()
    with open('calendar_events.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_data = list(map(int, row['date'].split('-')))
            date = datetime.date(date_data[0], date_data[1], date_data[2])
            
            if date in event_dict.keys():
                event_dict[date].append((row['event_type'], row['event_des']))
            else:
                event_dict[date] = [(row['event_type'], row['event_des'])]

########################################
# TASK CONTROL

def add_event(evType, event_dict):
    '''
        Add event/tasks into a dictionary with datetime.date as key.
        Each key will have a lists of event/task in them.
    '''
    print('Event date (yyyy m d): ')
    dtString = input('> ')
    print('Event description: ')
    evString = input('> ')

    dt_data = list(map(int, dtString.split(' ')))
    print(dt_data) ##
    date = datetime.date(dt_data[0], dt_data[1], dt_data[2])

    if date in event_dict.keys():
        event_dict[date].append((evType, evString))
        print('Added!')
    else:
        event_dict[date] = [(evType, evString)]
        print('Added!')

def del_event(event_dict):
    ''' TODO '''
    pass

def display_event(event_dict):
    '''
        Display available event/task sorted by its dates.
    '''
    evDates = list(event_dict.keys())
    evDates.sort()

    if not evDates:
        print('-- NO TASK TO DISPLAY --')
    else:
        for date in evDates:
            for event in event_dict[date]:
                print(date, ':', event[1])

def task_control(tasks):
    '''
        Control the menu for adding events, showing events and reprinting calendar.
    '''
    while True:
        print('\'help\' for more command.')
        ans = input('> ')
        if ans == 'help':
            print('\'addevent\' to add event.')
            print('\'addtask\' to add task.')
            print('\'event\' to print events.')
            print('\'show\' to print calendar.')
            print('\'close\' to close calendar.')
        elif ans == 'addevent':
            add_event('event', tasks)
        elif ans == 'addtask':
            add_event('task', tasks)
        elif ans == 'event':
            display_event(tasks)
        elif ans == 'show':
            print_calender()
        elif ans == 'close':
            if check_db():
                event_db_write(tasks)
            break
        else:
            print('command not recognized. \'help\' for available command.')

########################################
# PRINTING CALENDER

def check_date_event(date, event_dict = EVENT_DICT):
    if date in event_dict.keys():
        return event_dict[date][0][0]

    return None

def print_weekend(date, today):
    # CLEAN UP
    '''
        Prints weekend dates with red font color.
    '''
    if date < today:
        if len(str(date.day)) == 1:
            print('\033[2;31m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[2;31m' + str(date.day) + '\033[0m', end=' ')
    elif date == today:
        if len(str(date.day)) == 1:
            print('\033[1;41;37m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[1;41;37m' + str(date.day) + '\033[0m', end=' ')
    else:
        if len(str(date.day)) == 1:
            print('\033[31m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[31m' + str(date.day) + '\033[0m', end=' ')

def print_weekday(date, today):
    '''
        Prints weekday part of calendar.
    '''
    if date < today:
        if len(str(date.day)) == 1:
            print('\033[2m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[2m' + str(date.day) + '\033[0m', end=' ')
    elif date == today:
        if len(str(date.day)) == 1:
            print('\033[1;42m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[1;42m' + str(date.day) + '\033[0m', end=' ')
    else:
        if len(str(date.day)) == 1:
            print(' ' + str(date.day), end=' ')
        else:
            print(str(date.day), end=' ')

def print_blank():
    '''
        Avoid calendar clutter with printing dates as blank if that date doesnt belong to a month.
    '''
    print(' ' * 2, end=' ')#,

def print_event(date, today):
    '''
        Prints holiday / non task event with cyan color background.
    '''
    if date < today:
        if len(str(date.day)) == 1:
            print('\033[2;30;43m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[2;30;43m' + str(date.day) + '\033[0m', end=' ')
    elif date == today:
        if len(str(date.day)) == 1:
            print('\033[1;42m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[1;42m' + str(date.day) + '\033[0m', end=' ')
    else:
        if len(str(date.day)) == 1:
            print('\033[30;46m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[30;46m' + str(date.day) + '\033[0m', end=' ')

def print_task(date, today):
    '''
        Prints task dates with yellow background.
    '''
    if date < today:
        if len(str(date.day)) == 1:
            print('\033[33m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[33m' + str(date.day) + '\033[0m', end=' ')
    elif date == today:
        if len(str(date.day)) == 1:
            print('\033[1;42m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[1;42m' + str(date.day) + '\033[0m', end=' ')
    else:
        if len(str(date.day)) == 1:
            print('\033[30;43m' + ' ' + str(date.day) + '\033[0m', end=' ')
        else:
            print('\033[30;43m' + str(date.day) + '\033[0m', end=' ')

def print_date(date):
    '''
        Primary function to check how to print a date on calendar.
        Serve as a data checker to sort if a date have a task or event and
        whether its weekdays or weekends.
    '''
    today = datetime.date.today()
    is_event = check_date_event(date)

    if is_event == 'task':
        print_task(date, today)
    elif is_event == 'event':
        print_event(date, today)
    elif date.weekday() == 6:
        print_weekend(date, today)
    else:
        print_weekday(date, today)

def print_calender():
    '''
        Main function to print out the calendar.
        Will print month header of the calendar and iterates the datetime objects for each dates
        on each months.
        Serve also as the controller of where the cursor is printing.
    '''
    yearBatchNum = 0
    for row in CAL_MAPPING:
        for month in row:
            print('{:^22}'.format(MONTH[month] + ' ' + str(YEAR)), end='')

        print('')#,
        for month in row:
            print(' ' + ' '.join(WEEK_HEADER) + ' ', end='')#,

        print('')#,
        weekNum = 0
        maxWeekNum = max([len(w) for w in yearDays[yearBatchNum]])
        while weekNum < maxWeekNum:
            for month in CAL_MAPPING[yearBatchNum]:
                x = CAL_MAPPING[yearBatchNum].index(month)
                print('', end=' '),
                try:
                    for weekday in yearDays[yearBatchNum][x][weekNum]:
                        if weekday.month != month + 1:
                            print_blank()
                        else:
                            print_date(weekday)
                except IndexError:
                    pass

                print('', end='')

            print('')
            weekNum += 1

        print('')
        yearBatchNum += 1

##################################
# Main

def main(event_dict):
    '''
        main function
    '''
    event_db_read(event_dict)
    print_calender()
    task_control(event_dict)

if __name__ == '__main__':
    main(EVENT_DICT)
