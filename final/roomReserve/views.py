# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.
#@param: takes in a wustl username, password, date, start time, ending time, and event name
#Returns the name of the room booked and a given room, returns null
#Date format: mm/dd/yyyy
def bookRoom(username, password, date, sTime, eTime, eventName):
    driver = webdriver.Chrome(executable_path='/Users/adamschwartz/Documents/PycharmProjects/WebAutomation/chromedriver')

    driver.get('https://reserve.wustl.edu/')  # loads up
    time.sleep(3)
    driver.get(driver.current_url)  #connect to re-directed site - login

    # log in
    txtUsername = driver.find_element_by_xpath('//*[@id="ucWUSTLKeyLogin_txtUsername"]')
    txtUsername.send_keys(username)

    txtPassword = driver.find_element_by_xpath('//*[@id="ucWUSTLKeyLogin_txtPassword"]')
    txtPassword.send_keys(password)

    btnLogin = driver.find_element_by_xpath('//*[@id="ucWUSTLKeyLogin_btnLogin"]')
    btnLogin.click()

    print('Sleeping for 5 sec')
    time.sleep(5)
    print('5 sec later')

    driver.get(driver.current_url)  #connect to re-directed site - main page

    #book now button on main page
    btnBookNow = driver.find_element_by_xpath('//*[@id="templates-grid"]/div/div[6]/div[2]/button[1]')
    driver.execute_script("return arguments[0].scrollIntoView();", btnBookNow)
    driver.execute_script("arguments[0].click();", btnBookNow)
    print("Book now was clicked")

    txtDate = driver.find_element_by_xpath('//*[@id="booking-date-input"]')
    txtDate.clear()
    txtDate.send_keys(date) #mm/dd/yyyy

    txtStartTime = driver.find_element_by_xpath('//*[@id="start-time-input"]')
    txtStartTime.clear()
    txtStartTime.send_keys(sTime) #replace with variable

    txtEndTime = driver.find_element_by_xpath('//*[@id="end-time-input"]')
    txtEndTime.clear()
    txtEndTime.send_keys(eTime) #replace with variable

    btnET = driver.find_element_by_xpath('//*[@id="booking-end"]/span')
    driver.execute_script("return arguments[0].scrollIntoView();", btnET)
    driver.execute_script("arguments[0].click();", btnET)
    driver.execute_script("arguments[0].click();", btnET)

    btnSearch = driver.find_element_by_xpath('//*[@id="location-filter-container"]/div[2]/button')
    driver.execute_script("return arguments[0].scrollIntoView();", btnSearch)
    driver.execute_script("arguments[0].click();", btnSearch)
    print("Search rooms was clicked")

    print('1 second sleep')
    time.sleep(1)
    tabList = driver.find_element_by_xpath('//*[@id="result-tabs"]/li[1]/a')
    driver.execute_script("arguments[0].click();", tabList)
    print("list tab was clicked")
    time.sleep(1.5)

    emptyDiv = driver.find_element_by_xpath('//*[@id="list"]/div/div[1]')
    #if the list is empty
    if (emptyDiv.is_displayed()):
        print ('No rooms are available at the selected times')
        return ('No rooms are available at the selected times')
    else:
        #there's at least one room left
        print("sleeping for 1 second to let rooms load")
        time.sleep(1)

        btnAddRoom = driver.find_element_by_xpath('//*[@id="available-list"]/tbody/tr[2]/td[1]/a')
        lblRoom = driver.find_element_by_xpath('//*[@id="available-list"]/tbody/tr[2]/td[3]/a')
        roomText = lblRoom.get_attribute('text')
        room = roomText[:14] #'Bauer Hall 151'
        print(room + 'was booked')
        driver.execute_script("arguments[0].click();", btnAddRoom)
        print("room was added to cart")

        print("1 second sleep")
        time.sleep(1)
        btnNextStep = driver.find_element_by_xpath('//*[@id="next-step-btn"]')
        driver.execute_script("arguments[0].click();", btnNextStep)
        print("next step was clicked")

        txtEventName = driver.find_element_by_xpath('//*[@id="event-name"]')
        txtEventName.send_keys(eventName)

        btnTermsAndCond = driver.find_element_by_xpath('//*[@id="terms-and-conditions"]')
        driver.execute_script("return arguments[0].scrollIntoView();", btnTermsAndCond)
        driver.execute_script("arguments[0].click();", btnTermsAndCond)


        btnCreateReservation = driver.find_element_by_xpath('//*[@id="details"]/div[3]/div/span[2]/button')
        driver.execute_script("arguments[0].click();", btnCreateReservation)
        print('create reservation was clicked')
        
        return HttpResponse(room, date)
#https://mkdev.me/en/posts/fundamentals-of-front-end-django
class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})