from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url_news = "https://mars.nasa.gov/news/"
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # url_twitter = "https://twitter.com/marswxreport?lang=en"
    # url_table = "https://space-facts.com/mars/"
    # url_hems = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_news)

    #Create a Delay for load time
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    # Get the News Title
    news_title = soup.find('div', class_='list_text').find('a').text.strip()

   # Get the News Paragraph
    news_p = soup.find('div', class_= 'rollover_description_inner').text.strip()

    #Visit image website
    browser.visit(url_image)

    #Create a Delay for load time
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")
    
    # Get featured image
    relative_image_path = soup.find('footer').find('a').text()
    feature_img = url_news + relative_image_path


    # info["headline"] = soup.find("a", class_="result-title").get_text()
    # info["price"] = soup.find("span", class_="result-price").get_text()
    # info["hood"] = soup.find("span", class_="result-hood").get_text()

# Store data in a dictionary
    
    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_img": feature_img
    }

    browser.quit()

    return mars_info