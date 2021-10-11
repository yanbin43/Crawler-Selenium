##=====================================================================================================================================##
##                                                Web Crawler (Product Nation Malaysia)                                                ##
##=====================================================================================================================================##

## Parameter Definitions:

# This crawler is for the following url:
url = "https://productnation.co/my/"

# Download the correct driver for your version of google chrome from https://chromedriver.chromium.org/downloads
# Locate the path to the driver, e.g.
driverpath = "C:/Users/User/Anaconda3/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe"

# Select a desired search keyword
keyword = "mixer"


##=====================================================================================================================================##
##                                                            Start Browser                                                            ##
##=====================================================================================================================================##

#----------------------------------------------------------- Google Chrome -------------------------------------------------------------#
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--start-maximized")
cap = DesiredCapabilities.CHROME
driver = webdriver.Chrome(options = options, desired_capabilities = cap, executable_path = driverpath)

driver.get(url)

#----------------------------------------------------------- Mozilla Firefox -----------------------------------------------------------#
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.common.keys import Keys

# options = Options()
# options.add_argument("--start-maximized")
# cap = DesiredCapabilities().FIREFOX
# driver = webdriver.Firefox(firefox_options = options, capabilities = cap, executable_path = driverpath)

# driver.get(url)


##=====================================================================================================================================##
##                                                        Search & Load Results                                                        ##
##=====================================================================================================================================##

# Find the search bar and clear old text
searchbar = driver.find_element_by_name("s")
searchbar.clear()

# Insert desired keyword and press enter
searchbar.send_keys(keyword)
searchbar.send_keys(Keys.RETURN)


import time

# Keep scrolling down to load more results until the "Load More" button appears
n = 0
while n <= 20: # Different number of max scrolls may be needed until the "Load More" button appears
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    n += 1
    
# Keep clicking "Load More" button until the end of search result
try:
    loadmore = driver.find_element_by_xpath("//div[@id = 'load-more-posts']/button[@class = 'btn-load-more']")
    while (loadmore != None):
        loadmore.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
except:
    pass
    

##=====================================================================================================================================##
##                                                            Get Contents                                                             ##
##=====================================================================================================================================##

# There are 2 sections in the search results - 'product-feed' and 'article-feed' - 'article-feed' is needed.
articlefeed = driver.find_elements_by_xpath("//div[@class = 'post-card-header']")
print('Total Number of Posts =', len(articlefeed))

# Get post links and save in a list:
articles = driver.find_elements_by_xpath("//div[@class='post-card-header']/a[@class='post-card-content']")
Link = []
i = 1
for href in articles:
    Link.append(href.get_attribute("href"))
    i += 1

print(*Link, sep = "\n")
print("Total Number of Links =", len(Link))

#--------------------------------------------------------- Organize Contents -----------------------------------------------------------#

Title = []
Author = []
AuthorProfile = []
DateTime = []
Content = []

i = 1
for a in Link:
    driver.get(a)
    print(i, a, "\n")
    time.sleep(2)
    
    # Article Title
    atitle = driver.find_element_by_xpath("//h1[@class = 'post-thumbnail__meta-title']")
    Title.append(atitle.text)
    print("Title =", atitle.text, "\n")
    
    # Author
    aauthor = driver.find_element_by_xpath("//span[@class = 'post-meta-author__name post-thumbnail__mr-0']/a")
    Author.append(aauthor.text)
    print("By", aauthor.text, end = " ")
    
    # Author's Profile
    aprofile = driver.find_element_by_xpath("//span[@class = 'post-meta-author__name post-thumbnail__mr-0']/a")
    AuthorProfile.append(aprofile.get_attribute("href"))
    print(aprofile.get_attribute("href"), end = " ")
    
    # Date & Time
    adatetime = driver.find_element_by_xpath("//time[@class = 'post-meta-author__date']")
    DateTime.append(adatetime.get_attribute("datetime"))
    print("on", adatetime.get_attribute("datetime"), "\n")
    
    # Post Content
    Paragraph = []
    for p in driver.find_elements_by_xpath("//article//p"):
        Paragraph.append(p.text)
    Paragraph = Paragraph[:-1]
    print("Post Content:\n", Paragraph, "\n")
    Content.append(Paragraph)
    
    print("---------------------------------------------------------------------------------------------------------------")
    time.sleep(5)
    i += 1

driver.quit()

#---------------------------------------------------------- Export as a File -----------------------------------------------------------#

import pandas as pd
from datetime import date

today = date.today().strftime('%Y_%m_%d')

ProductNation = pd.DataFrame({'Link': Link, 'Title': Title, 'Author': Author, 'Author_Profile': AuthorProfile,
                                    'Date_Time': DateTime, 'Content': Content})

ProductNation.to_csv('ProductNation_' + keyword + '_' + today + '.csv', encoding='utf-8')





