# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)
    print(news_title)

    # Run all scraping functions and store results in a dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': mars_hemi()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    print('starting mars_news', flush=True)
    # scrape Mars News
    # Visit the webite to scrape  -------> used a shortened URL
    print('executing mars_news')
    url = 'https://rb.gy/fqggqy'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Parse the HTML
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the summary paragraph text for the first article
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    try:
        # create df of web table using pandas
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        print("Exception ", BaseException)
        return None


    # assign column names and set index of df
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # convert df to html-ready, add bootstrap
    return df.to_html(classes='table table-striped')
def mars_hemi():
    # scraping the hemisphere urls and title
   # Mac users
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # 1. Use browser to visit the hemisphere URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # b. Cerberus
    browser.click_link_by_partial_text('Cerberus')
    cerberus_html = browser.html
    cerberus_soup = soup(cerberus_html, 'html.parser')

    # find title
    cerberus_title = cerberus_soup.find("h2", class_ = 'title').text

    # Find the relative image url
    cerberus = cerberus_soup.find('img', class_ = 'wide-image')
    cerberus_img = cerberus['src']

    # add base url to rel url
    hemi_url = 'https://astrogeology.usgs.gov'
    cerberus_url = hemi_url + cerberus_img

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # c. Schiaparelli
    browser.back()
    browser.click_link_by_partial_text('Schiaparelli')
    schiaparelli_html = browser.html
    schiaparelli_soup = soup(schiaparelli_html, 'html.parser')

    # find title
    schiaparelli_title = schiaparelli_soup.find("h2", class_ = 'title').text

    # find the relative image url
    schiaparelli = schiaparelli_soup.find('img', class_ = 'wide-image')
    schiaparelli_img = schiaparelli['src']

    # add base url to rel url
    hemi_url = 'https://astrogeology.usgs.gov'
    schiaparelli_url = hemi_url + schiaparelli_img

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # d. Syrtis Major
    browser.back()
    browser.click_link_by_partial_text('Syrtis')
    syrtis_html = browser.html
    syrtis_soup = soup(syrtis_html, 'html.parser')

    # find title
    syrtis_title = syrtis_soup.find("h2", class_ = 'title').text

    # find the relative image url
    syrtis = syrtis_soup.find('img', class_ = 'wide-image')
    syrtis_img = syrtis['src']

    # add base url to rel url
    hemi_url = 'https://astrogeology.usgs.gov'
    syrtis_url = hemi_url + syrtis_img

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # e. Valles Marineris
    browser.back()
    browser.click_link_by_partial_text('Valles')
    valles_html = browser.html
    valles_soup = soup(valles_html, 'html.parser')

    # find title
    valles_title = valles_soup.find("h2", class_ = 'title').text

    # find the relative image url
    valles = valles_soup.find('img', class_ = 'wide-image')
    valles_img = valles['src']

    # add base url to rel url
    hemi_url = 'https://astrogeology.usgs.gov'
    valles_url = hemi_url + valles_img

    return [{'img_url': cerberus_url, 'title': cerberus_title},
            {'img_url': schiaparelli_url, 'title': schiaparelli_title},
            {'img_url': syrtis_url, 'title': syrtis_title}, 
            {'img_url': valles_url, 'title': valles_title}]
    
# scraping complete
if __name__ == '__main__':
    print('something to print', flush=True)
    print(scrape_all())