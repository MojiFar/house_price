#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 17:17:36 2018

@author: mojtaba
"""
import pandas as pd
from re import search
import requests
from bs4 import BeautifulSoup
import re

# data_set = pd.read_csv('Apartments_koopen.csv')

quote_page = 'https://www.jaap.nl/koophuizen/noord+holland/groot-amsterdam/amsterdam'
page = requests.get(quote_page, verify=False, timeout=20)
soup = BeautifulSoup(page.content, "lxml")
A = []
Dataset = []
for line in soup.find_all('span', class_='page-info'):
    A = line.text.strip().split('van')
    last_page = int(A[-1])

def address(soup2):
	for row2 in soup2.find_all('div', class_='detail-address'):
		#finding street name
		street = row2.find('div', class_= 'detail-address-street')
		street = street.text
		zipcode = row2.find('div', class_='detail-address-zipcity')
		zipcode = zipcode.text
		zipcode2 = re.search(r'^\d{4}\s*\w{2}', zipcode).group()
		price = row2.find('div', class_='detail-address-price')
		price = price.text.strip().replace('€','')
		return street, zipcode2,price

def broker(soup2):
	for row3 in soup2.find_all('div', class_='detail-broker'):
		broker_name = row3.find('div', class_='broker-name')
		broker_name = broker_name.text
		return broker_name

def kenmerk(soup2):
	kenmerk = []
	for row in soup2.find_all('div', class_='detail-tab-content kenmerken'):
		for row2 in row.find_all('td', class_='value'):
			kenmerk.append(row2.text.strip())
	return kenmerk

def woning(soup2):
	woning = []
	for row in soup2.find_all('div', class_='detail-tab-content woningwaarde'):
		for row2 in row.find_all('td', class_='value'):
			woning.append(row2.text.strip())
		for row3 in row.find_all('td', class_='value-3-3'):
		    woning.append(row3.text.strip())
	return woning

def buurt(soup2):
	buurt_target = []
	buurt_distance = []
	buurt_dict = {}
	for row in soup2.find_all('table', class_='voorzieningen'):
		for row2 in row.find_all('td', class_='value-1-2'):
			buurt_target.append(row2.text.strip())
		for row3 in row.find_all('td', class_='value-2-2'):
			buurt_distance.append(row3.text.strip().replace('\xa0',' '))
	for i in range(len(buurt_target)):
		buurt_dict[buurt_target[i]] = buurt_distance[i]
	return buurt_dict

def inwoner(soup2):
	inwoner = []
	for row in soup2.find_all('table', class_='two-blocks'):
		for row2 in row.find_all('td', class_='value'):
			inwoner.append(row2.text.strip().replace('\t',''))
	return inwoner


for counter in range(1, last_page):
        page = requests.get("https://www.jaap.nl/koophuizen/noord+holland/groot-amsterdam/amsterdam/p"+str(counter)
                            , verify=False, timeout=20)
        soup = BeautifulSoup(page.content, "lxml")
        #print(counter)
        # finding reviews-container since all the input located there
        for row in soup.find_all('a', class_='property-inner', href=True):
            buurt1 = {}
            inowner1 = []
            link = row.attrs['href']
            page2 = requests.get(link, verify=False, timeout=20)
            soup2 = BeautifulSoup(page2.content, "lxml")
            street, zipcode, price = address(soup2)
            broker_name = broker(soup2)
            kenmerken = kenmerk(soup2)
            woningwarde = woning(soup2)
            buurt1.clear()
            buurt1 = buurt(soup2)
            inwoner1 = inwoner(soup2)
            OutCome = [street, zipcode, price, broker_name, kenmerken, woningwarde, buurt1, inwoner1]
            Dataset.append(OutCome)

df = pd.DataFrame(Dataset)#,  columns = ['Street','Zipcode','Price','Broker','Type', 'Construnction_year','Living_area',
									   #'LOT','Plot', 'Other', 'Insulation', 'Heating', 'Energy_label', 'Energy_consumption',
									   #'inside_maintenance_state', 'Rooms', 'Bedrooms', 'Sanitation', 'kitchen',
									   #'outside_maintenace_state','outside_state_painting','Graden','view','Balcony', 'Garage',
									   #'number_of_times_shown', 'number_of_times_shown_yesterday', 'posted_date',
									   #'current_price', 'original_price', 'changes_in_price', 'price', 'price_per_m2', 'times_in_sales',
									   #])
df.to_csv('AllReviewsF.csv', sep = ',', encoding ='utf-8')







def Web_Scraper(page):
    quote_page = page
    page = requests.get(quote_page ,verify=False, timeout=3)
    soup = BeautifulSoup(page.content, "lxml")
    A = []
    Dataset = []   
    # it finds the total number of pages in trustpilot
    for line in soup.find_all('a', class_='pagination-page'):
        A = line.text.strip().split('van')
        last_page = int(A[-2])
    # it goes over all the pages one by one to get all the info for each review.
    QuotePage = '/review/www.rebtel.com'
    for counter in range(0,last_page):
        page = requests.get("https://www.jaap.nl/koophuizen/noord+holland/groot-amsterdam/amsterdam/p"+str(counter)
                            ,verify=False, timeout=20)
        soup = BeautifulSoup(page.content, "lxml")
        #print(counter)
        # finding reviews-container since all the input located there
        for row in soup.find_all('div', class_='property-inner', href=True):
            AllReviews= row.find_all('div', class_='card')
            for cells in row.find_all('div', class_='card'):
                # finding customer name
                Name = cells.find('h3', class_='consumer-info__details__name')
                Name = Name.text.strip()
                Review = cells.find('div', class_='review-info__header__verified')
                # finding star review or rating
                StarReview = Review.contents[1].attrs['class'][1]
                StarReview = StarReview.split('-')[1]
                # finding the title of the review
                Title = cells.find('h2', class_='review-info__body__title')
                Title = Title.text.strip()
                # finding the body of the review
                Body = cells.find('p', class_='review-info__body__text')
                Body = Body.text.strip()
                # finding the date and time
                DateTime = cells.find('time', class_='ndate')
                Date, Time = DateTime.attrs['datetime'].split('T')
                Time = Time.split(".")
                Time = Time[0]
                OutCome = [Name, StarReview, Title,Body,Date, Time]
                Dataset.append(OutCome)
        # trigger for going to the next page
        for line in soup.find_all('a', class_='pagination-page'):
            if line.text == "Next page":
                NextPage = line.attrs['href']
                QuotePage = NextPage

    df = pd.DataFrame(Dataset,  columns = ['Name','StarRating','Title','Body','Date', 'Time'])
    df.to_csv('AllReviewsF.csv', sep = ',', encoding ='utf-8')
#page = 'https://www.trustpilot.com/review/www.rebtel.com'
#Web_Scraper(page)
