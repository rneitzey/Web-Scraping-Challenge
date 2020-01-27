from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd


def init_browser():
    # Replace path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url_news = "https://mars.nasa.gov/news/"
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    url_table = "https://space-facts.com/mars/"
    url_hems = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    # Boiler plate for connecting to websites with delay for load times
    browser.visit(url_news)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the News Title
    news_title = soup.find('div', class_='list_text').find('a').text.strip()

    # Get the News Paragraph
    news_p = soup.find('div', class_= 'rollover_description_inner').text.strip()

    
    #Visit image website
    browser.visit(url_image)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Get featured image
    relative_image_path = soup.find('footer').find('a').attrs['data-fancybox-href']
    feature_img = "https://www.jpl.nasa.gov" + relative_image_path


    # Visit twitter website
    browser.visit(url_twitter)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    
    weather_tweet = soup.find('div',class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").find('span').text.replace('\n', ' ')


    # Visit Mars Facts website
    browser.visit(url_table)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    # Read in tables
    facts_tables = pd.read_html(url_table)

    # Find first table and label columns
    df = facts_tables[0]
    df.columns = ['Description', 'Value']

    # Convert table to html
    mars_facts = df.to_html(index=False)

    # Visit Mars Hemispheres website
    browser.visit(url_hems)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")


    #Create variable for list of dictionaries.
    hem_img_title = []

    # Variable for attributes on initial page
    hemispheres = soup.find("div", class_="result-list").find_all("div", class_="item")

    # Loop through attributes to find each title and image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
    # Drop "Enhanced" from each scraped title
        title = title.replace("Enhanced", "")
    # Get link for full image page
        partial_link = hemisphere.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov/" + partial_link    
    # Visit page with full image and scrape image link
        browser.visit(img_link)
        soup = bs(browser.html, "html.parser")
        img_url = soup.find("div", class_="downloads").find("a")["href"]
    # Append dictionaries to list
        hem_img_title.append({"title": title, "img_url": img_url})


# Store all data in a dictionary
    
    mars_info = {
            "news_title": news_title,
            "news_p": news_p,
            "feature_img": feature_img,
            "mars_facts": mars_facts,
            "weather_tweet": weather_tweet,
            "hemispheres": hem_img_title
        }

    browser.quit()

    return mars_info