"""This python file will handle some extra functions."""
import sys
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

# Login information
username: ''
password: ''

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
                'username': data['username'],
                'password': data['password'],
                'imax_adults': data['imax_adults'],
                'imax_students': data['imax_students'],
                'imax_seniors': data['imax_seniors'],
                'imax_disabled': data['imax_disabled'],
                'seats': data['seats'],
                'invoice': data['invoice'],
                'headless': data['headless']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


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
        temp = [seat_table[seat[0:1]], int(seat[1:]) + 1, seat]
        seats_list.append(temp)
    return seats_list
