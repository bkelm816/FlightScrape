import datetime
import time
import platform
from SpiritChecker import spirit_checker
# import SpiritChecker as spirit

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Tell the user which OS we are running on.
print(platform.system())
if platform.system() == 'Darwin':
    # Darwin is MacOS
    browser = webdriver.Chrome()
    browser_type = 'Chrome'
else:
    # Linux or Windows means we can use the ChromeDriver
    browser = webdriver.Chrome()
    browser_type = 'Chrome'


def flight_chooser():
    try:
        flights = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
        flights.click()
    except Exception as e:
        print("Cannot find the Flight tab in Expedia")
        pass


def ticket_chooser(ticket):
    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass


def flying_from(departing_airport):
    flyFrom = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    flyFrom.clear()
    time.sleep(1)
    flyFrom.send_keys(' ' + departing_airport)
    time.sleep(2)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1)
    first_item.click()


def flying_to(arriving_airport):
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    fly_to.clear()
    time.sleep(1)
    fly_to.send_keys('  ' + arriving_airport)
    time.sleep(2)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1)
    first_item.click()


def departure_date(month, day, year):
    dep_date = browser.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
    dep_date.clear()
    dep_date.send_keys(month + '/' + day + '/' + year)


def return_date(month, day, year):
    ret_date = browser.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")

    for i in range(11):
        ret_date.send_keys(Keys.BACKSPACE)
    ret_date.send_keys(month + '/' + day + '/' + year)


def search():
    searching = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    searching.click()
    time.sleep(15)
    print("Results Ready!!!")


df = pd.DataFrame()
def compile_data():
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    # Departure times
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]

    # Arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]

    # Airlines
    airline = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airline]

    # Prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text for value in prices]

    # Duration
    duration = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in duration]

    # Stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]

    # Layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-info']")
    layovers_list = [value.text for value in layovers]

    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'Price' + '(' + current_date + '---' + current_time + ')'

    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass


def connect_mail(username,password):
    global server
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.set_debuglevel(0)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)


def create_msg(depart,
               returning,
               cheapest_dep_time,
               cheapest_arrival_time,
               cheapest_airline,
               cheapest_duration,
               cheapest_stops,
               cheapest_price):
    global msg
    departing_date = depart.month + '/' + depart.day + '/' + depart.year
    returning_date = returning.month + '/' + returning.day + '/' + returning.year

    msg = '\nCurrent Cheapest flight from {} to {}:\n\nDeparture time: {}\nArrival time: {}' \
          '\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrices: {}\n'.format(departing_date,
                                                                                      returning_date,
                                                                                      cheapest_dep_time,
                                                                                      cheapest_arrival_time,
                                                                                      cheapest_airline,
                                                                                      cheapest_duration,
                                                                                      cheapest_stops,
                                                                                      cheapest_price)


def send_email(msg):
    global message
    message = MIMEMultipart()
    message['Subject'] = Header('Current Best Flight')
    message['From'] = username
    message['to'] = 'r00kie81693@gmail.com'
    message.attach(MIMEText(msg))

    server.sendmail(username, 'r00kie81693@gmail.com', message.as_string())
    server.quit()


# Check  the Expedia website for flight deals
def expedia_checker(depart_airport_code, arrival_airport_code, depart, returning):
    link = 'https://www.expedia.com'

    # This is necessary since by default Expedia does not set the roundtrip field
    return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
    browser.get(link)
    time.sleep(5)
    flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
    flights_only.click()

    # This chooses the Round trip indication on the website
    ticket_chooser(return_ticket)
    # try:
    # Fill out the airport codes for the departing and arriving airports.
    flying_from(depart_airport_code)
    flying_to(arrival_airport_code)

    # IMPORTANT: Must be in mm/dd/yyyy format in order to work
    # These functions set the departing and returning dates
    departure_date(depart.month, depart.day, depart.year)
    time.sleep(2)
    return_date(returning.month, returning.day, returning.year)

    # Allow time for the webpage to respond, then select the Search button
    time.sleep(4)
    search()

    # This is where the magic happens, compile all the necessary data that we need and throw it into a dataframe so
    #  we can reliably look at the data and manipulate it if needed.
    compile_data()

    # Since Expedia is filtered to have the cheapest flights first, we set the current value as the first index
    current_value = df.iloc[0]

    # Packaging the data up into variables so we can email it out. These values are all based off the first index
    cheapest_dep_time = current_value[0]
    cheapest_arrival_time = current_value[1]
    cheapest_airline = current_value[2]
    cheapest_duration = current_value[3]
    cheapest_stops = current_value[4]
    cheapest_price = current_value[-1]

    print('Expedia run {} completed!'.format(i))

    # Create the email message we are going to send out, include all the details we require
    create_msg(cheapest_dep_time, cheapest_arrival_time, cheapest_airline, cheapest_duration, cheapest_stops, cheapest_price)

    # Sign into the mailing account
    connect_mail(username, password)

    # Finally send the email out
    send_email(msg)

    print('Email sent!')

    now = datetime.datetime.now()

    # Create the Excel sheet with the custom name based on the time of population
    date_and_time = (str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_')
    df.to_excel('ExcelFiles/expedia-' + date_and_time + 'flights.xlsx')
    print('Excel Sheet Created!')

    # except Exception as e:
    # pass
    # browser.quit()


def chrome_clear_cache(browser, timeout=60):
    browser.get('chrome://settings/clearBrowserData')

    browser.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)


# Class used for departure and returning dates
class Date:
    month = '09'
    day = '28'
    year = '2019'


global username
global password

username = 'flightchecker2@outlook.com'
password = 'Cheapflights'
username = 'flightchecker@yahoo.com'
password = 'Cheapairlines'
i = 0
while True:
    if platform.system() != 'Darwin':
        chrome_clear_cache(browser)

    departing_city = 'Detroit'
    arriving_city = 'Orlando'

    depart = Date()
    depart.month = '11'
    depart.day = '26'
    depart.year = '2019'

    returning = Date()
    returning.month = '12'
    returning.day = '03'
    returning.year = '2019'

    spirit_msg = spirit_checker(departing_city, arriving_city, depart, returning, browser, browser_type)
    connect_mail(username, password)
    send_email(spirit_msg)
    print("Spirit email sent {}", spirit_msg)
    print('Spirit run {} completed!'.format(i))

    expedia_checker(departing_city, arriving_city, depart, returning)

    depart.month = '11'
    depart.day = '27'
    depart.year = '2019'

    returning.month = '12'
    returning.day = '03'
    returning.year = '2019'

    spirit_checker(departing_city, arriving_city, depart, returning, browser, browser_type)

    expedia_checker(departing_city, arriving_city, depart, returning)

    i = i + 1
    # Check again in an hour
    time.sleep(1600)

