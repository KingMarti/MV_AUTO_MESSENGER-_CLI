from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta, date
import random
import string
import os
import keyboard
import time
import pandas as pd

def codeGen(stringLength=5):
    letters=string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class manyvids:
    def __init__(self,username,password):
            print('def init')
            self.username = username
            self.password = password
            self.bot = webdriver.Firefox(executable_path=r'C:\\\geckodriver.exe')

    def login(self):
        print('running login')
        bot=self.bot
        bot.get('https://www.manyvids.com/Login/')
        time.sleep(3)
        email = bot.find_element_by_id('triggerUsername')
        password = bot.find_element_by_id('triggerPassword')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(10)
    def make_promo(self):
        bot=self.bot
        bot.get('https://www.manyvids.com/Promo-codes/')
        time.sleep(3)
        bot.find_element_by_xpath('//a[contains(text(),"Create New Promo Code")]').click()
        time.sleep(3)
        promo_title= bot.find_element_by_id("promo_code_title")
        promo_title_text=codeGen()
        print('promo code is : ',promo_title_text)
        promo_title.send_keys(promo_title_text)
        time.sleep(3)
        bot.find_element_by_xpath('//span[contains(text(),"Select the")]').click()
        time.sleep(3)
        bot.find_element_by_xpath('//li[contains(text(),"-10%")]').click()
        time.sleep(3)
        bot.find_element_by_xpath('//label[@for="apply_store"]').click()
        bot.find_element_by_xpath('//label[@for="apply_membership"]').click()
        bot.find_element_by_xpath('//label[@for="apply_skype"]').click()
        bot.find_element_by_xpath('//label[@for="apply_customvid"]').click()
        bot.find_element_by_xpath('//label[@for="apply_texting"]').click()
        bot.find_element_by_xpath('//label[@for="apply_phone"]').click()
        bot.find_element_by_xpath('//label[@for="apply_crush"]').click()
        promo_start = datetime.today().strftime('%Y-%m-%d')
        bot.find_element_by_id('dp1').send_keys(promo_start)
        bot.find_element_by_xpath('//label[@for="discountDateEnd"]').click()
        end_date = datetime.today() + timedelta(days=7)
        print(end_date.strftime('%Y-%m-%d'))
        bot.find_element_by_id('dp2').send_keys(end_date.strftime('%Y-%m-%d'))
        time.sleep(3)
        bot.find_element_by_xpath('//button[contains(text(),"Save")]').click()
        time.sleep(3)
        for row in bot.find_elements_by_xpath('//table[contains(@id,"promo_code_history")]'):
            print('Hello I am in a row')
            cells= row.find_elements_by_css_selector('td')
            promo_names = cells[1].get_attribute('innerHTML')
            if promo_names == promo_title_text:
                print('promo code: ',cells[0].get_attribute('innerHTML'), 'for promo name : ',promo_names)
                global promo
                promo = cells[0].get_attribute('innerHTML')
                global expiery
                expiery = cells[4].get_attribute('innerHTML')
                expiery = expiery[expiery.find("<td>")+48:expiery.find("<br>")]
            print(promo_names)
        time.sleep(3)
    def sales(self):
        bot=self.bot 
        bot.get('https://manyvids.com/View-my-earnings/#recentSalesBody')
        today_date = datetime.today().strftime('%Y-%m-%d')
        print('Todays Date is :', today_date)
        current_day = datetime.today().strftime('%d')
        print("today is :", current_day)
        current_month = datetime.today().strftime('%m')
        print("current Month is :", current_month)
        current_year = datetime.today().strftime('%Y')
        print('the current year is :', current_year)
        target_date = datetime.today() + timedelta(days=-7)
        print('the target date is :', target_date)
        target_day= target_date.strftime('%d')
        print('the target day is :',target_day)
        target_month = target_date.strftime('%m')
        print('The Target Month is :', target_month)
        target_year = target_date.strftime('%Y')
        print('The Target Year Is :', target_year)
        target_date = target_date.strftime('%Y-%m-%d')
        print("The Target Date is :", target_date)
        daterrange = pd.date_range(target_date,today_date)
        date_list = []
        sales_list =[]
        messaged = []
        for single in daterrange:
            
            #print(single.strftime('%b %d, %Y'))
            single= single.strftime('%b'),int(single.strftime('%d')),single.strftime('%Y')
            sd = str(single[1])
            single = single[0],' ', sd,', ',single[2]
            single = ''.join(single)
            print('single is now:', type(single), single)
            for row in bot.find_elements_by_xpath('//tr[contains(@id,"earnings_video_")]'):
                #print(row.text)
                cells= row.find_elements_by_css_selector('td')
                links = cells[1].get_attribute('innerHTML')              
                username = links[links.find("<b>")+3:links.find("</b>")]
                pm = links[links.find('<a href="/Inbox/New')+9:links.find('" class')]
                #sales_list = [username, pm, purchased]
                sale_date = cells[0].text[:12].strip()
                #print ('sale date : ',sale_date)
                purchased = cells[3].text
                if sale_date == single:
                    #print("Result", sale_date, ' ',username, ' ',pm,'', purchased )
                    sales = [sale_date,username,pm,purchased]
                    sales_list.append(sales)
        for s in sales_list:
            print(s[1])
            print('///////////////////////////////////////////')

            if s[1] not in messaged:
                bot.get('https://manyvids.com'+s[2])
                time.sleep(5)
                message="Hey. ", s[1], " \nThank you for purchasing ", s[3],"\nI hope you enjoy it.\nPlease do not forget to leave a review. \nAs a thank you for your recent purchase, here is a discount code for 10% off your next video purchase, this code is valid for the next 7 days. \n Discount Code: ", promo, "\n Expires : ",expiery
                message_box =bot.find_element_by_class_name('inbox-new-message-input')
                message_box.clear()
                message_box.send_keys(message)
                messaged.append(s[1])
                time.sleep(10)
                bot.find_element_by_id('jsConversationSubmit').click()
                
            else:
                print("Message Skipped as Already Messgaged")
        bot.close()        
run = manyvids('username','password')
run.login()
run.make_promo()
run.sales()