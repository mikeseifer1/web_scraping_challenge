from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    

    title, body = scrape_news()

    mars_data={"news_title":title,
                "paragraph":body,
                "main_image":featured_image(),
                "Mars_Facts":mars_facts(),
                "Hemisphere_urls":mars_images()
    }

    browser.quit()
    return mars_data

def scrape_news():

    browser = init_browser()

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')

    try:
        results = soup.find_all('div', class_='content_title')
        title = results[1].text
        results1 = soup.find_all('div', class_='article_teaser_body')
        body = results1[0].text 
    except AttributeError:
        return None, None
    
    browser.quit()

    return title, body

def featured_image():

    browser = init_browser()

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    time.sleep(1)

    image_element = browser.find_by_id("full_image")
    image_element.click()

    more_info_element = browser.links.find_by_partial_text('more info')
    more_info_element.click()

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    try:
        image1 = soup2.select_one('figure.lede a img').get("src")
        url3 = "https://www.jpl.nasa.gov"
        featured_image_url = url3 + image1
    except AttributeError:
        return None, None
    browser.quit()
    return featured_image_url

def mars_facts():
    browser = init_browser()

    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    df1 = tables[1]
    df1.set_index(["Mars - Earth Comparison"],inplace=True)
    html_table = df1.to_html()


    browser.quit()
    return html_table

def mars_images():
    browser = init_browser()
    mars_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    hemisphere_image_urls = []
    for mars in mars_urls:
        #url_mars = mars
        browser.visit(mars)
        html_mars = browser.html
        soup_mars = BeautifulSoup(html_mars, 'html.parser')
        results4 = soup_mars.find('div', class_='downloads')
        image_url = results4.a['href']
        mars_title = soup_mars.find('h2', class_='title').text
        
        hemisphere_image_urls.append({'title': mars_title,'image_url': image_url})
    
    browser.quit()
    return hemisphere_image_urls