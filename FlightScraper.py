import datetime
import time
import platform

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Tell the user which OS we are running on.
print(platform.system())
if platform.system() == 'Darwin':
    # Darwin is MacOS
    browser = webdriver.Safari()
else:
    # Linux or Windows means we can use the ChromeDriver
    browser = webdriver.Chrome()


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


def flying_from(departing_airport) :
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
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.set_debuglevel(1)

def create_msg(cheapest_dep_time, cheapest_arrival_time, cheapest_airline, cheapest_duration, cheapest_stops, cheapest_price):
    global msg
    msg = '\nCurrent Cheapest flight:\n\nDeparture time: {}\nArrival time: {}\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrices: {}\n'.format(cheapest_dep_time,
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

    server.sendmail(username, 'r00kie81693@gmail.com', msg)


def spirit_flying_from(departing_airport):
    flyFrom = browser.find_element_by_xpath("//select[@id='departCityCodeSelect']")
    time.sleep(1)
    #flyFrom.click()
    time.sleep(1)
    flyFrom.send_keys(departing_airport)
    time.sleep(1)


def spirit_flying_to(arriving_airport):
    fly_to = browser.find_element_by_xpath("//select[@id='destCityCodeSelect']")
    time.sleep(1)
    #fly_to.clear()
    time.sleep(1)
    fly_to.send_keys(arriving_airport)
    time.sleep(1)


def spirit_departure_date(month, day, year):
    dep_date = browser.find_element_by_xpath("//input[@id='departDate']")
    dep_date.clear()
    dep_date.send_keys(month + '/' + day + '/' + year)


def spirit_return_date(month, day, year):
    ret_date = browser.find_element_by_xpath("//input[@id='returnDate']")

    for i in range(11):
        ret_date.send_keys(Keys.BACKSPACE)
    ret_date.send_keys(month + '/' + day + '/' + year)


dp = pd.DataFrame()
def spirit_compile_data():
    global dp
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    # Departure times
    dep_times = browser.find_elements_by_xpath("//div[@class='col-sm-2 col-xs-6 depart']")
    dep_times_list = [value.text for value in dep_times]

    # Arrival times
    arr_times = browser.find_elements_by_xpath("//div[@class='col-sm-2 col-xs-6 arrive']")
    arr_times_list = [value.text for value in arr_times]

    # Spirit
    # Airlines
    # airline = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")d
    # airlines_list = [value.text for value in airline]

    # $9 FC Prices
    fc_prices = browser.find_elements_by_xpath("//label[contains(text(),'$9 Fare Club:')]/following-sibling::div[1]")
    fc_price_list = [value.text for value in fc_prices]

    # StandardPrices
    prices = browser.find_elements_by_xpath("//label[starts-with(@for,'DLXRadio')]")
    price_list = [value.text for value in prices]

    # Stops
    stops = browser.find_elements_by_xpath("//a[@class='stopsLink']")
    stops_list = [value.text for value in stops]

    # Layovers
    # layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-info']")
    # layovers_list = [value.text for value in layovers]

    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'Price' + '(' + current_date + '---' + current_time + ')'
    fc_current_price = 'Fare Club Price' + '(' + current_date + '---' + current_time + ')'

    for i in range(len(dep_times_list)):
        try:
            # Strip the encoding off the values we pulled from the website. This is only required for Safari setups
            if platform.system() == 'Darwin':
                start = 0
                stop = 67
                if len(dep_times_list[i]):
                    dep_times_list[i] = dep_times_list[i][0:start:] + dep_times_list[i][stop+1::]
                    dep_times_list[i] = str(dep_times_list[i]).replace(u'\xa0', u' ')
                    dep_times_list[i] = str(dep_times_list[i]).rstrip()
            # Add the departure time into the data frame
            dp.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            # Strip the encoding off the values we pulled from the website. This is only required for Safari setups
            if platform.system() == 'Darwin':
                start = 0
                stop = 67
                # Spirit is weird, they use some sort od funky unicode and getting the times is a pain, so stripping
                #   back all the unneeded characters as well as '\xa0'
                if len(arr_times_list[i]):
                    arr_times_list[i] = arr_times_list[i][0:start:] + arr_times_list[i][stop+1::]
                    arr_times_list[i] = str(arr_times_list[i]).replace(u'\xa0', u' ')
                    arr_times_list[i] = str(arr_times_list[i]).rstrip()
            # Add the arrival time into the data frame
            dp.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            dp.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            if platform.system() == 'Darwin':
                stripped_fc_price_list = str(fc_price_list[i])
                head, sep, tail = stripped_fc_price_list.partition('\n')
                dp.loc[i, str(fc_current_price)] = head
            else:
                dp.loc[i, str(fc_current_price)] = fc_price_list[i]
        except Exception as e:
            pass
        try:
            dp.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass

    return len(dep_times_list)


def spirit_create_msg(depart, returning, cheapest_dep_time, cheapest_arrival_time, cheapest_stops, cheapest_fc_price, cheapest_price):
    global msg
    departing_date = depart.month + '/' + depart.day + '/' + depart.year
    returning_date = returning.month + '/' + returning.day + '/' + returning.year

    msg = '\nCurrent Cheapest Spirit flight from {} to {}:\n\nDeparture time: {}\nArrival time: {}\nNo. of stops: {}\n$9 Fare Club Prices: {}\nStandard Prices: {}\n'.format(departing_date,
                                                                                                                                                                             returning_date,
                                                                                                                                                                             cheapest_dep_time,
                                                                                                                                                                             cheapest_arrival_time,
                                                                                                                                                                             cheapest_stops,
                                                                                                                                                                             cheapest_fc_price,
                                                                                                                                                                             cheapest_price)


def spirit_checker(depart_airport_code, arrival_airport_code, depart, returning):
    link = 'https://www.spirit.com'
    browser.get(link)
    spirit_flying_from(depart_airport_code)
    spirit_flying_to(arrival_airport_code)

    spirit_departure_date(depart.month, depart.day, depart.year)
    time.sleep(2)
    spirit_return_date(returning.month, returning.day, returning.year)

    flights_only = browser.find_element_by_xpath("//button[@class='pull-right btn btn-sm btn-primary button primary secondary flightSearch']")
    flights_only.click()
    time.sleep(15)
    print("Results Ready!!!")

    iter_length = spirit_compile_data()
    cheapest_flight = dp.iloc[0][-1]
    cheapest_flight = str(cheapest_flight).replace('$', '')
    cheapest_flight = float(cheapest_flight)
    current_value_std = dp.iloc[0]

    # TODO: Add in logic to handle the $9 Fare Club prices too, if the cheapest Fare Club prices are
    #  cheaper than the cheapest standard price, then output that one
    for n in range(iter_length-1):
        next_flight = dp.iloc[n + 1][-1]
        next_flight = str(next_flight).replace('$', '')
        next_flight = float(next_flight)
        if not(cheapest_flight <= next_flight):
            cheapest_flight = next_flight
            current_value_std = dp.iloc[n+1]

    # Look at the $9 Fare Club pricing
    cheapest_flight_fc = dp.iloc[0][3]
    cheapest_flight_fc = str(cheapest_flight_fc).replace('$', '')
    cheapest_flight_fc = float(cheapest_flight_fc)
    current_value_fc = dp.iloc[0]

    for n in range(iter_length-1):
        next_flight_fc = dp.iloc[n + 1][3]
        if '.' != next_flight_fc:
            next_flight_fc = str(next_flight_fc).replace('$', '')
            next_flight_fc = float(next_flight_fc)
            if not(cheapest_flight_fc < next_flight_fc):
                cheapest_flight_fc = next_flight_fc
                current_value_fc = dp.iloc[n+1]

    # Compare the $9 Fare Club pricing
    if current_value_fc <= current_value_std:
        current_value = current_value_fc
    else:
        current_value = current_value_std

    cheapest_dep_time = current_value[0]
    cheapest_arrival_time = current_value[1]
    cheapest_stops = current_value[2]
    cheapest_fc_price = current_value[3]
    cheapest_price = current_value[-1]

    print('Spirit run {} completed!'.format(i))
    spirit_create_msg(depart, returning, cheapest_dep_time, cheapest_arrival_time, cheapest_stops, cheapest_fc_price,cheapest_price)
    connect_mail(username, password)
    send_email(msg)
    print('Email sent!')

    now = datetime.datetime.now()

    date_and_time = (str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_')
    dp.to_excel('ExcelFiles/spirit-' + date_and_time + 'flights.xlsx')
    print('Excel Sheet Created!')


# Check  the Expedia website for flight deals
def expedia_checker(depart_airport_code, arrival_airport_code, depart, returning):
    link = 'https://www.expedia.com'

    # This is necessary since by default Expedia does not set the roundtrip field
    return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
    browser.get(link)
    time.sleep(5)
    flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
    flights_only.click()

    # This chooses the Roundtrip indication on the website
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
    dp.to_excel('ExcelFiles/expedia-' + date_and_time + 'flights.xlsx')
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


username = 'flightchecker2@outlook.com'
password = 'Cheapflights'
username = 'flightchecker@yahoo.com'
password = 'Cheapairlines'
i = 0
while(True):
    if platform.system() != 'Darwin':
        chrome_clear_cache(browser)
    departing_city = 'DTW'
    arriving_city = 'MCO'

    depart = Date()
    depart.month = '11'
    depart.day = '26'
    depart.year = '2019'

    returning = Date()
    returning.month = '12'
    returning.day = '03'
    returning.year = '2019'
    
    if platform.system() == 'Linux':
        spirit_checker('Detroit', 'Orlando', depart, returning)
    else:
        spirit_checker(departing_city, arriving_city, depart, returning)

    expedia_checker(departing_city, arriving_city, depart, returning)

    depart.month = '11'
    depart.day = '27'
    depart.year = '2019'

    returning.month = '12'
    returning.day = '03'
    returning.year = '2019'

    if platform.system() == 'Linux':
        spirit_checker('Detroit', 'Orlando', depart, returning)
    else:
        spirit_checker(departing_city, arriving_city, depart, returning)

    expedia_checker(departing_city, arriving_city, depart, returning)

    i = i + 1
    # Check again in an hour
    time.sleep(1600)

