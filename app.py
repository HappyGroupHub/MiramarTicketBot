"""This python file is the main file of the program."""
import sys
import time

from playsound import playsound
from selenium import webdriver
from selenium.common import TimeoutException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import utilities as utils

config = utils.read_config()

options = webdriver.ChromeOptions()
if config.get("headless"):
    options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)


def driver_send_keys(locator, key):
    """Send keys to element.

    :param locator: Locator of element.
    :param key: Keys to send.
    """
    wait.until(ec.presence_of_element_located(locator)).send_keys(key)


def driver_click(locator):
    """Click element.

    :param locator: Locator of element.
    """
    wait.until(ec.presence_of_element_located(locator)).click()


def driver_select(locator, select_value, select_by='index'):
    """Select element.

    :param locator: Locator of element.
    :param select_value: Value to select.
    :param select_by: Select by index, value or visible_text. Default is index.
    """
    select = Select(wait.until(ec.presence_of_element_located(locator)))
    if select_by == 'index':
        select.select_by_index(select_value)
    elif select_by == 'value':
        select.select_by_value(select_value)
    elif select_by == 'visible_text':
        select.select_by_visible_text(select_value)


def driver_screenshot(locator, path):
    """Take screenshot of element.

    :param locator: Locator of element.
    :param path: Path to save screenshot.
    """
    wait.until(ec.presence_of_element_located(locator)).screenshot(path)


def driver_get_text(locator):
    """Get text of element.

    :param locator: Locator of element.
    :return: Text of element.
    """
    return wait.until(ec.presence_of_element_located(locator)).text


def driver_get_background_color(locator):
    """Get background color of element.

    :param locator: Locator of element.
    :return: Background color of element.
    """
    return wait.until(ec.presence_of_element_located(locator)).value_of_css_property(
        'background-color')


def login():
    driver.get('https://www.miramarcinemas.tw/Member/Login')
    cookies = utils.read_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except (TimeoutException, NoAlertPresentException):
        print(
            "Login Failed, cookies might not be correct or expired, please login manually then copy cookies value to cookies.json")
        driver.quit()
        sys.exit()
    print('-------------------------------------')
    print("Login Success!")
    grab_tickets()


def grab_tickets():
    driver.get('https://www.miramarcinemas.tw/Timetable/Index?cinema=imax')
    while True:
        try:
            driver.find_element(By.XPATH, f"//*[contains(text(), '{config.get('date')}')]").click()
            break
        except (TimeoutException, NoSuchElementException):
            time.sleep(1)
            driver.refresh()
    try:
        selected_time = driver.find_element(By.XPATH,
                                            f"//div[contains(@class, '{config['cn_date']}')]"
                                            f"//a[contains(text(), '{config['time']}')]")
        driver.get(selected_time.get_attribute('href'))
    except (TimeoutException, NoSuchElementException):
        print('Time not available, please select manually.')
        playsound('ding.wav')
        while True:
            try:
                wait.until(ec.url_contains('https://www.miramarcinemas.tw/Booking/'))
                break
            except TimeoutException:
                continue
    print('-------------------------------------')
    if config.get("imax_adults") > 0:
        driver_select((By.ID, "ticket_type_select_0149"), config.get("imax_adults"))
        print(f"Imax_adults tickets: {config.get('imax_adults')}")
    if config.get("imax_students") > 0:
        driver_select((By.ID, "ticket_type_select_0150"), config.get("imax_students"))
        print(f"Imax_adults tickets: {config.get('imax_students')}")
    if config.get("imax_seniors") > 0:
        driver_select((By.ID, "ticket_type_select_0050"), config.get("imax_seniors"))
        print(f"Imax_adults tickets: {config.get('imax_seniors')}")
    if config.get("imax_disabled") > 0:
        driver_select((By.ID, "ticket_type_select_0051"), config.get("imax_disabled"))
        print(f"Imax_adults tickets: {config.get('imax_disabled')}")
    print(
        f'Total tickets: {config["imax_adults"] + config["imax_students"] + config["imax_seniors"] + config["imax_disabled"]}')
    print('-------------------------------------')
    driver_click(
        (By.XPATH, "/html/body/div[1]/section[3]/section/div/div/div[2]/form/div[5]/label"))
    seats = utils.get_seats()
    checkout = True
    for seat in seats:
        selected = (By.XPATH,
                    f"/html/body/div[1]/section[3]/section[2]/div/div/div/table/tbody/tr[{seat[0]}]/td[{seat[1]}]")
        if driver_get_background_color(selected) == 'rgba(128, 128, 128, 1)':
            print(f"Seat {seat[2]} is not available.")
            checkout = False
            playsound('ding.wav')
            continue
        else:
            driver_click(selected)
            print(f"Seat {seat[2]} selected.")
    if not checkout:
        print('-------------------------------------')
        print('Some seats are not available, please select manually.')
        while True:
            try:
                wait.until(ec.url_contains('https://www.miramarcinemas.tw/Booking/Confirm'))
                break
            except TimeoutException:
                continue
    else:
        driver_click((By.XPATH, "/html/body/div[1]/section[3]/section[2]/div/form/div/label[2]"))
    if config.get("invoice") != '':
        driver_send_keys((By.ID, "invoice_vehicle"), config.get("invoice"))
    driver_send_keys((By.ID, "AgreeRule"), Keys.SPACE)


if __name__ == "__main__":
    login()
    time.sleep(9999999999)
    print('Time out, quit.')
    driver.quit()
