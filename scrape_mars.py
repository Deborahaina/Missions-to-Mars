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
    news_title= soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    

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
    featured_img_url = base_url + img_url
   

# Scraping Mars Weather, get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    

# Mars Facts
    url_facts='https://space-facts.com/mars/'
    table = pd.read_html(url_facts)
    table[0]
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])
    mars_table = df_mars_facts.to_html()
    mars_table = mars_table.replace("\n", "")
    


# Mars Hemisphere
    url_hemisphere= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items= soup.find_all('div', class_='item')
    hemispheres = []
    for i in items:
        hem = i.h3.text
        hemispheres.append(hem)


    images = []
    for h in hemispheres:
        url_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_hemisphere)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.click_link_by_partial_text(h)
        img_url = browser.find_by_tag('img')[3]['src']
        images.append(img_url)



    hemisphere_image_urls = [
        {"title": hemispheres[0], "img_url": images[0]},
        {"title": hemispheres[1], "img_url": images[1]},
        {"title": hemispheres[2], "img_url": images[2]},
        {"title": hemispheres[3], "img_url": images[3]},
    ]
      

# Store data in a dictionary
    mars_data = {
        "news_p": news_p,
        "news_title": news_title,
        "featured_img_url": featured_img_url,
         "mars_weather": mars_weather,
         "mars_table": mars_table,
         "hemisphere_image_urls":hemisphere_image_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
    return table




    