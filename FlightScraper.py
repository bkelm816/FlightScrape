import datetime
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart


browser = webdriver.Safari()

def flight_chooser():
    try:
        flights = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
        flights.click()
    except Exception as e:
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
    time.sleep(1)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1)
    first_item.click()


def flying_to(arriving_airport):
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    fly_to.clear()
    time.sleep(1)
    fly_to.send_keys('  ' + arriving_airport)
    time.sleep(1)
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
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(username, password)


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
    message['Subject'] = 'Current Best Flight'
    message['From'] = 'bkelm816@gmail.com'
    message['to'] = 'r00kie81693@gmail.com'

    server.sendmail('bkelm816@gmail.com', 'r00kie81693@gmail.com', msg)


def spirit_flying_from(departing_airport):
    flyFrom = browser.find_element_by_xpath("//select[@id='departCityCodeSelect']")
    flyFrom.clear()
    time.sleep(1)
    flyFrom.send_keys(' ' + departing_airport)
    time.sleep(1)


def spirit_flying_to(arriving_airport):
    fly_to = browser.find_element_by_xpath("//select[@id='destCityCodeSelect']")
    fly_to.clear()
    time.sleep(1)
    fly_to.send_keys('  ' + arriving_airport)
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
    fc_prices = browser.find_elements_by_xpath("//div[@class='radio invisible']|starts-with(@for,'FCRadio')")
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
            dp.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            dp.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        #try:
        #    dp.loc[i, 'airline'] = airlines_list[i]
        #except Exception as e:
        #    pass
        #try:
        #    dp.loc[i, 'duration'] = durations_list[i]
        #except Exception as e:
        #    pass
        try:
            dp.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        #try:
        #    dp.loc[i, 'layovers'] = layovers_list[i]
        #except Exception as e:
        #    pass
        try:
            dp.loc[i, str(fc_current_price)] = fc_price_list[i]
        except Exception as e:
            pass
        try:
            dp.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass


def spirit_checker():
    link = 'https://www.spirit.com'
    browser.get(link)
    spirit_flying_from('MCO')
    spirit_flying_to('DTW')

    spirit_departure_date('09', '20', '2019')
    time.sleep(2)
    spirit_return_date('09', '26', '2019')

    flights_only = browser.find_element_by_xpath("//button[@class='pull-right btn btn-sm btn-primary button primary secondary flightSearch']")
    flights_only.click()
    time.sleep(15)
    print("Results Ready!!!")

    spirit_compile_data()

def expedia_checker():
    link = 'https://www.expedia.com'
    return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
    browser.get(link)
    time.sleep(5)
    flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
    flights_only.click()

    ticket_chooser(return_ticket)
    # try:
    flying_from('MCO')
    flying_to('DTW')

    # Must be in mm/dd/yyyy format in order to work
    departure_date('09', '20', '2019')
    time.sleep(2)
    return_date('09', '26', '2019')

    time.sleep(4)
    search()
    compile_data()

    current_value = df.iloc[0]

    cheapest_dep_time = current_value[0]
    cheapest_arrival_time = current_value[1]
    cheapest_airline = current_value[2]
    cheapest_duration = current_value[3]
    cheapest_stops = current_value[4]
    cheapest_price = current_value[-1]

    print('run {} completed!'.format(i))

    create_msg(cheapest_dep_time, cheapest_arrival_time, cheapest_airline, cheapest_duration, cheapest_stops, cheapest_price)
    connect_mail(username, password)
    send_email(msg)

    print('Email sent!')

    df.to_excel('flights.xlsx')
    print('Excel Sheet Created!')

    # except Exception as e:
    # pass
    # browser.quit()


username = 'bkelm816@gmail.com'
password = 'redsox@1'
for i in range(8):
    spirit_checker()
    # expedia_checker()

    # Quit the browser to save on resources
    browser.quit()

    # Check again in an hour
    time.sleep(3600)

