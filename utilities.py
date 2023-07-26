"""This python file will handle some extra functions."""
import json
import sys
from datetime import datetime, timedelta
from os.path import exists

import yaml
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# ++--------------------------------++
# | MiramarTicketBot                 |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# Login instructions
# Please log in manually on your local browser first 
# Then copy cookies value to cookies.json

# Tickets date and time
# Enter the date and time you want to book.
date: '8/3'
time: '23:10'
# Buffer time mode can be before, after or around.
# Minute range is the range of time buffer.
# Example: 10:00, buffer_time_mode: 'before', minute_range: 30 => 9:30 ~ 10:00
# Example: 10:00, buffer_time_mode: 'around', minute_range: 30 => 9:30 ~ 10:30
buffer_time_mode: 'around'
minute_range: 30

# Tickets selection
# Please enter the amount of ticket you want to book.
imax_adults: 2
imax_students: 0
imax_seniors: 0
imax_disabled: 0

# Seat selection
# Please enter the seat you want to book.
seats:
  - 'G23'
  - 'G24'
  
# Invoice settings (optional)
# Invoice number should start with / and contains 7 character behind.
# Example: /A123456
invoice: ''

# Headless mode
# If you want to run this script in headless mode, please set this to true.
headless: false
"""
                )
    sys.exit()


def read_config():
    """Read config file.

    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.

    :rtype: dict
    """
    if not exists('./config.yml'):
        print("Config file not found, create one by default.\nPlease finish filling config.yml")
        with open('config.yml', 'w', encoding="utf8"):
            config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            config = {
                'date': data['date'],
                'time': data['time'],
                'buffer_time_mode': data['buffer_time_mode'],
                'minute_range': data['minute_range'],
                'imax_adults': data['imax_adults'],
                'imax_students': data['imax_students'],
                'imax_seniors': data['imax_seniors'],
                'imax_disabled': data['imax_disabled'],
                'seats': data['seats'],
                'invoice': data['invoice'],
                'headless': data['headless']
            }
            config['cn_date'] = config['date'].replace('/', '月') + '日'
            start_time, end_time = get_buffered_time(config['time'], config['buffer_time_mode'],
                                                     config['minute_range'])
            config['start_time'] = start_time.strftime("%H:%M")
            config['end_time'] = end_time.strftime("%H:%M")
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def cookies_file_generator():
    """Generate the template of cookies files"""
    with open('cookies.json', 'w', encoding="utf8") as f:
        f.write("""[
    {
        "name": "__RequestVerificationToken",
        "value": "",
        "domain": "www.miramarcinemas.tw"
    },
    {
        "name": "ASP.NET_SessionId",
        "value": "",
        "domain": "www.miramarcinemas.tw"
    }
]"""
                )
    sys.exit()


def read_cookies():
    """Read cookies file.

    Check if cookies file exists, if not, create one.
    if exists, read cookies file and return cookies with list type.

    :rtype: list
    """
    if not exists('./cookies.json'):
        print(
            "Cookies file not found, please login manually then copy cookies value to cookies.json")
        with open('cookies.json', 'w', encoding="utf8"):
            cookies_file_generator()
        sys.exit()
    try:
        with open('cookies.json', 'r', encoding="utf8") as file:
            cookies = json.loads(file.read())
            return cookies
    except (KeyError, TypeError):
        print(
            "An error occurred while reading cookies.json, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete cookies.json and restart the program.\n")
        sys.exit()


def get_buffered_time(selected_time, buffer_time_mode, minute_range):
    """Get buffered time.

    :param selected_time: Time.
    :param buffer_time_mode: Buffer time mode, before , after or around.
    :param minute_range: Minute range.
    """
    selected_time = datetime.strptime(selected_time, "%H:%M")
    start_time = end_time = selected_time
    if buffer_time_mode == 'before':
        start_time = selected_time - timedelta(minutes=minute_range)
    elif buffer_time_mode == 'after':
        end_time = selected_time + timedelta(minutes=minute_range)
    elif buffer_time_mode == 'around':
        start_time = selected_time - timedelta(minutes=minute_range)
        end_time = selected_time + timedelta(minutes=minute_range)
    return start_time, end_time


def get_seats():
    config = read_config()
    seats = config['seats']
    seat_table = {'A': 2, 'B': 3, 'C': 4, 'D': 5, 'E': 6, 'F': 7, 'G': 8, 'H': 10, 'I': 11, 'J': 12,
                  'K': 13, 'L': 21, 'M': 22}
    seats_list = []
    for seat in seats:
        if seat[0:1] not in seat_table:
            print(f"Seat {seat} is not valid, please fix it in config.yml.")
            sys.exit()
        temp = []
        if int(seat_table[seat[0:1]]) <= 13 and int(seat[1:]) <= 11:
            temp = [seat_table[seat[0:1]], int(seat[1:]), seat]
        elif int(seat_table[seat[0:1]]) <= 13 and 14 <= int(seat[1:]) <= 25:
            temp = [seat_table[seat[0:1]], int(seat[1:]) + 1, seat]
        elif int(seat_table[seat[0:1]]) <= 13 and 28 <= int(seat[1:]) <= 37:
            temp = [seat_table[seat[0:1]], int(seat[1:]) + 2, seat]
        elif int(seat[1:]) >= 21:
            temp = [seat_table[seat[0:1]], int(seat[1:]), seat]
        seats_list.append(temp)
    return seats_list
