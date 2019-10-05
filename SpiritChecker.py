import time
from selenium.webdriver.common.keys import Keys




def spirit_flying_from(departing_airport, browser):
    flyFrom = browser.find_element_by_xpath("//select[@id='departCityCodeSelect']")
    time.sleep(1)
    #flyFrom.click()
    time.sleep(1)
    flyFrom.send_keys(departing_airport)
    time.sleep(1)


def spirit_flying_to(arriving_airport, browser):
    fly_to = browser.find_element_by_xpath("//select[@id='destCityCodeSelect']")
    time.sleep(1)
    #fly_to.clear()
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

