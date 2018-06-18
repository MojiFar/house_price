#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 17:17:36 2018

@author: mojtaba
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

data_set = pd.read_csv('Apartments_koopen.csv')

quote_page = 'https://www.jaap.nl/koophuizen/noord+holland/groot-amsterdam/amsterdam'
page = requests.get(quote_page, verify=False, timeout=20)
soup = BeautifulSoup(page.content, "lxml")
A = []
Dataset = []
for line in soup.find_all('span', class_='page-info'):
    A = line.text.strip().split('van')
    last_page = int(A[-1])

for counter in range(1, last_page):
        page = requests.get("https://www.jaap.nl/koophuizen/noord+holland/groot-amsterdam/amsterdam/p"+str(counter)
                            , verify=False, timeout=20)
        soup = BeautifulSoup(page.content, "lxml")
        #print(counter)
        # finding reviews-container since all the input located there
        for row in soup.find_all('a', class_='property-inner', href=True):
            link = row.attrs['href']
            page2 = requests.get(link, verify=False, timeout=20)
            soup2 = BeautifulSoup(page2.content, "lxml")



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