# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser
#create a function called scrape to get the data
def scrape():
    browser = init_browser()
    # MARS IMAGE
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    #traversing the website HTML to get the title and the paragraph
    news_title = soup.find_all("div", class_="content_title")[1].text
    news_p = soup.find("div", class_="article_teaser_body").text


    #MARS Image
    #visit the JPL website
    mars_url= 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(mars_url)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    #traversing the website HTML to get the image
    #image_url= soup.find_all("img", class_="BaseImage")[0]['src']
    mars_text=soup.find_all('h2', class_ ="mb-3 text-h5")[0].text
    #look for link that have the HRES
    browser.find_by_css('.BaseImage').first.click()
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    h_res_mars_1=soup.find_all("img", class_="BaseImage")[0]['src']
    print(h_res_mars_1)
    h_res_mars=soup.find('div', class_ ="lg:pt-0 pt-8 mb-12").find_all('div',class_="lg:w-auto w-full")[1].find('a')['href']

    #get Mars facts
    mars_facts_url = 'https://space-facts.com/mars/'
    #as pandas as the read_html function, we can use it to scrape the tabular data
    tables = pd.read_html(mars_facts_url)
    #get the first table
    df_mars=tables[0]
    df_renamed=df_mars.rename(columns={0:'Parameters', 1:'Values'})
    df_renamed.set_index("Parameters", inplace = True)
    #converting and saving to html table
    html_table = df_renamed.to_html(classes=["table", "table-striped", "table-hover", "table-sm"])
     # df_renamed.to_html('html_table.html', classes=["table", "table-striped", "table-hover", "table-sm"])

    #mars Hemispheres
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    results= soup.findAll('div', attrs={"class":"description"})
    num_results = len(results)

    #creating an empty list
    hemisphere_image_urls= []
    print('#############')
    print(num_results)
    print('#############')
    for num in range(num_results):

        browser.find_by_css("a.product-item h3")[num].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        names = soup.find('h2', class_='title').get_text()
        relative_image_path=soup.find_all("img", class_="wide-image")[0]['src']
        mars_img = "https://astrogeology.usgs.gov/" + relative_image_path
        mars_dictionary= {'Title':names, 'Hemisphere':mars_img}


        hemisphere_image_urls.append(mars_dictionary)
        browser.back()


    #create a dictionary with the code above
    mars_data = {'news_title': news_title, 'news_paragraph': news_p, 'image_url': h_res_mars_1 , 'image':h_res_mars, 'mars_text': mars_text,'facts_table': html_table, 'hemispheres': hemisphere_image_urls }
    #quit browser
    browser.quit()
    print('All done!')
    return mars_data
