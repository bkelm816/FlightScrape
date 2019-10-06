import time
import datetime

# Data Frame for getting all the data
import pandas as pd

# Ability to send keys to the active field in the webpage.
from selenium.webdriver.common.keys import Keys


def spirit_flying_from(departing_airport, browser):
    flyFrom = browser.find_element_by_xpath("//select[@id='departCityCodeSelect']")
    time.sleep(1)
    # flyFrom.click()
    time.sleep(1)
    flyFrom.send_keys(departing_airport)
    time.sleep(1)


def spirit_flying_to(arriving_airport, browser):
    fly_to = browser.find_element_by_xpath("//select[@id='destCityCodeSelect']")
    time.sleep(1)
    # fly_to.clear()
    time.sleep(1)
    fly_to.send_keys(arriving_airport)
    time.sleep(1)


def spirit_departure_date(month, day, year, browser):
    dep_date = browser.find_element_by_xpath("//input[@id='departDate']")
    dep_date.clear()
    dep_date.send_keys(month + '/' + day + '/' + year)


def spirit_return_date(month, day, year, browser):
    ret_date = browser.find_element_by_xpath("//input[@id='returnDate']")

    for i in range(11):
        ret_date.send_keys(Keys.BACKSPACE)
    ret_date.send_keys(month + '/' + day + '/' + year)


dp = pd.DataFrame()
def spirit_compile_data(browser, browser_type):
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
            if browser_type == 'Safari':
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
            if browser_type == 'Safari':
                start = 0
                stop = 67
                # Spirit is weird, they use some sort od funky unicode and getting the times is a pain, so stripping
                #   back all the un-needed characters as well as '\xa0'
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
            if browser_type == 'Safari':
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


def spirit_create_msg(depart,
                      returning,
                      cheapest_dep_time,
                      cheapest_arrival_time,
                      cheapest_stops,
                      cheapest_fc_price,
                      cheapest_price):
    global msg
    departing_date = depart.month + '/' + depart.day + '/' + depart.year
    returning_date = returning.month + '/' + returning.day + '/' + returning.year

    msg = '\nCurrent Cheapest Spirit flight from {} to {}:\n\nDeparture time: {}\nArrival time: {}' \
          '\nNo. of stops: {}\n$9 Fare Club Prices: {}\nStandard Prices: {}\n'.format(departing_date,
                                                                                      returning_date,
                                                                                      cheapest_dep_time,
                                                                                      cheapest_arrival_time,
                                                                                      cheapest_stops,
                                                                                      cheapest_fc_price,
                                                                                      cheapest_price)


def spirit_checker(depart_airport_code, arrival_airport_code, depart, returning, browser, browser_type):
    link = 'https://www.spirit.com'
    browser.get(link)
    spirit_flying_from(depart_airport_code, browser)
    spirit_flying_to(arrival_airport_code, browser)

    spirit_departure_date(depart.month, depart.day, depart.year, browser)
    time.sleep(2)
    spirit_return_date(returning.month, returning.day, returning.year, browser)

    time.sleep(1)
    flights_only = browser.find_element_by_xpath("//button[@class='pull-right btn btn-sm btn-primary button primary secondary flightSearch']")
    flights_only.click()
    time.sleep(15)
    print("Results Ready!!!")

    iter_length = spirit_compile_data(browser, browser_type)
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
    if browser_type == 'Safari':
        if not '.' == dp.iloc[0][3]:
            cheapest_flight_fc = str(cheapest_flight_fc).replace('$', '')
            cheapest_flight_fc = float(cheapest_flight_fc)
            current_value_fc = dp.iloc[0]
        else:
            # Set this to a super high value since this is the first $9 Fare Club and it doesnt have usable data in it.
            cheapest_flight_fc = 10000
            current_value_fc = dp.iloc[0]
    else: # Chrome web browser does not put a '.' in the field
        if not '' == dp.iloc[0][3]:
            cheapest_flight_fc = str(cheapest_flight_fc).replace('$', '')
            cheapest_flight_fc = float(cheapest_flight_fc)
            current_value_fc = dp.iloc[0]
        else:
            # Set this to a super high value since this is the first $9 Fare Club and it doesnt have usable data in it.
            cheapest_flight_fc = 10000
            current_value_fc = dp.iloc[0]

    for n in range(iter_length-1):
        next_flight_fc = dp.iloc[n + 1][3]
        if browser_type == 'Safari':
            if '.' != next_flight_fc:
                next_flight_fc = str(next_flight_fc).replace('$', '')
                next_flight_fc = float(next_flight_fc)
                if not(cheapest_flight_fc < next_flight_fc):
                    cheapest_flight_fc = next_flight_fc
                    current_value_fc = dp.iloc[n+1]
        else:
            if '' != next_flight_fc:
                next_flight_fc = str(next_flight_fc).replace('$', '')
                next_flight_fc = float(next_flight_fc)
                if not (cheapest_flight_fc < next_flight_fc):
                    cheapest_flight_fc = next_flight_fc
                    current_value_fc = dp.iloc[n + 1]


# Compare the $9 Fare Club pricing
    if cheapest_flight_fc <= cheapest_flight:
        current_value = current_value_fc
    else:
        current_value = current_value_std

    cheapest_dep_time = current_value[0]
    cheapest_arrival_time = current_value[1]
    cheapest_stops = current_value[2]
    cheapest_fc_price = current_value[3]
    cheapest_price = current_value[-1]

    spirit_create_msg(depart,
                      returning,
                      cheapest_dep_time,
                      cheapest_arrival_time,
                      cheapest_stops,
                      cheapest_fc_price,
                      cheapest_price)

    now = datetime.datetime.now()

    date_and_time = (str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_')
    dp.to_excel('ExcelFiles/spirit-' + date_and_time + 'flights.xlsx')
    print('Excel Sheet Created!')

    return msg
