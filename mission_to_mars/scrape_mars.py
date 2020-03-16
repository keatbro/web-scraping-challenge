# Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import time
import re

def scrape():

    # Scrape Nasa website for latest title
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(nasa_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('div', class_='slide')
    titles = []
    paragraphs = []

    for title in soup.find_all('div', class_='content_title'):
        titles.append(title.text.strip())

    for paragraph in soup.find_all('div', class_='rollover_description_inner'):
        paragraphs.append(paragraph.text.strip())

    latestTitle = titles[0]
    latestParagraph = paragraphs[0]

    
    # Get featured space image from Nasa Jet Propulsion laboratory
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    newJPLURL = browser.url

    response = requests.get(newJPLURL)
    soup = BeautifulSoup(response.text, 'html.parser')
    for result in soup.find_all('figure', class_='lede'):
        link = result.a['href']

    imageURL = 'https://www.jpl.nasa.gov' + link
    
    browser.quit()
    
    # Scrape the latest Mars Weather Tweet
    twitterURL = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitterURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    tweets = []

    for result in soup.find_all('p', class_={re.compile(r'^TweetTextSize')}):
        tweet = result.text.strip()
        tweets.append(tweet)
    
    weatherTweets = [i for i in tweets if i.startswith('InSight')] 
    
    lastestWeaterTweet = weatherTweets[0]

    # Scrape Mars data
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    
    marsdataDF = tables[0]

    # Get images of each of Mars' hemispheres
    marsURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    browser.visit(marsURL)

    # Cerberus Hemisphere
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    browser.click_link_by_partial_text('Sample')
    hem1 = browser.url

    #Return to previous window
    browser.windows[1].close() 
    browser.back()

    # Schiaparelli Hemisphere
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    browser.click_link_by_partial_text('Sample')
    hem2 = browser.url

    #Return to previous window
    browser.windows[1].close() 
    browser.back()

    # Syrtis Major Hemisphere
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    browser.click_link_by_partial_text('Sample')
    hem3 = browser.url

    #Return to previous window
    browser.windows[1].close() 
    browser.back()

    # Valles Marineris Hemisphere
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    browser.click_link_by_partial_text('Sample')
    hem4 = browser.url

    browser.quit()

    dataDict = {
        'latestNewsTitle' : latestTitle, 
        'latestNewsParagraph' : latestParagraph,
        'featuredMarsImage' : imageURL,
        'latestTweet' : lastestWeaterTweet,
        'marsData' : marsdataDF,
        'cerberus' : hem1,
        'schiaparelli' : hem2,
        'syrtis' : hem3,
        'Valles' : hem4
    }
    return dataDict