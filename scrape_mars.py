from bs4 import BeautifulSoup 
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path":'C:\\Users\\debor\\GWARL201811DATA3\\01-Class-Activities\\12-Web-Scraping-and-Document-Databases\\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data= {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    #scrapping latest news about mars from nasa icluding title 
    ##and each paragraph
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p 

 #Mars Featured Image
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    time.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(2)
    html_image = browser.html
    soup = BeautifulSoup(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    mars_featured_img_url = base_url + img_url
    mars_data["featured_image"] = mars_featured_img_url

# Scraping Mars Weather, get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather

# Mars Facts
    url_facts='https://space-facts.com/mars/'
    table = pd.read_html(url_facts)
    table[0]
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])
    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data["mars_facts_table"] = mars_html_table


# Mars Hemisphere
    url_hemisphere= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
    #xpath=//img[@class='wide-image']
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    # Loop through the all items that contains hemisphere information
    for i in items: 
    # Store title
        title = i.find('h3').text
    # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
        browser.visit(hemisphere_base_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
        hemisphere_image_urls
        mars_data['hemisphere_image_urls'] = hemisphere_image_urls

        browser.quit()
        
        return mars_data

