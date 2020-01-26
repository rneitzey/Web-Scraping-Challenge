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
    url_twitter = "https://twitter.com/marswxreport?lang=en"
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
    relative_image_path = soup.find('footer').find('a').attrs['data-fancybox-href']
    feature_img = "https://www.jpl.nasa.gov" + relative_image_path


    # # Visit twitter website
    flag = False
    while flag == False:
        try:
            url_twitter = "https://twitter.com/marswxreport?lang=en"
            browser.visit(url_twitter)
            time.sleep(5)
            html = browser.html
            soup = bs(html,'html.parser')
            weather_tweet = soup.find('div',class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").find('span').text.replace('\n', ' ')
            flag = True
        except:
            flag = False
            print('Wrong twitter version trying again')
            weather_tweet = soup.find('p',class_='tweet-text').text.replace('\n', ' ')


# Store data in a dictionary
    
    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_img": feature_img,
        "weather_tweet": weather_tweet
    }

    browser.quit()

    return mars_info