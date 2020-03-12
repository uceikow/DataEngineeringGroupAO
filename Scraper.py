#!/usr/bin/env python
# coding: utf-8

# In[20]:


# Import standard libraries
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import pandas as pd


# -----------------------------------

# ### 2nd attempt (Dominik) // different website / JS scraping

# In[3]:


import csv
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver import Firefox
from time import sleep
from datetime import datetime
import sqlalchemy as db
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
# pd.set_option('display.max_colwidth', 0)


# In[10]:


#! pip install beatifulsoup


# Warning: I installed geckodriver with Homebrew (brew install geckodriver)

# In[33]:


# open browser and create empty data array
# /usr/local/bin/geckodriver /home/ubuntu/.linuxbrew/Cellar/geckodriver
from time import sleep
from datetime import datetime

driver = webdriver.Firefox(executable_path="/home/ubuntu/.linuxbrew/Cellar/geckodriver/0.26.0/bin/geckodriver",options=options)
data = []


# In[34]:

# click GDPR full-width banner 
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# start_time = datetime.now()
# driver.get("http://allrecipes.co.uk/consent/?dest=/")

# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick^='sendAndRedirect']"))).click()

# gdpr_button = driver.find_element_by_link_text("Continue")
#gdpr_button = driver.find_element_by_xpath('//button[text()="Continue"]')


# driver.find_element_by_xpath("//input[type='button']]").click()

# //input[@onclick='sendAndRedirect()']
# <button style="order:2" onclick="sendAndRedirect();">Continue</button>
# scrape indian



# scrape (start with page 2)
for i in range(2,90):
    urlpage = (f"http://allrecipes.co.uk/recipes/indian-recipes.aspx?page={i}&o_is=LV_Pgntn")
    driver.get(urlpage)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(5)
    results = driver.find_elements_by_xpath('//*[@id="sectionTopRecipes"]//*[@class="row recipe"]')
    for result in results:
        product_name = result.find_element_by_tag_name("h3").text
        description = result.find_element_by_class_name("js-truncate").text
        data.append({"product" : product_name, "description": description, "cuisine": "indian"})
    print(f"Number of scraped recipes: {len(data)}")
    i =+ 1
    
stop_time = datetime.now()
elapsed_time = stop_time - start_time
print(f"Finished! Scraped {len(data)} recipes in total.")
print(f"Elapsed Time: {elapsed_time}")


# In[36]:


# scrape mexican

start_time = datetime.now()

# scrape (start with page 2)
for i in range(2,60):
    urlpage = (f"http://allrecipes.co.uk/recipes/mexican-recipes.aspx?page={i}&o_is=LV_Pgntn")
    driver.get(urlpage)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(5)
    results = driver.find_elements_by_xpath('//*[@id="sectionTopRecipes"]//*[@class="row recipe"]')
    for result in results:
        product_name = result.find_element_by_tag_name("h3").text
        description = result.find_element_by_class_name("js-truncate").text
        data.append({"product" : product_name, "description": description, "cuisine": "mexican"})
    print(f"Number of scraped recipes: {len(data)}")
    i =+ 1
    
stop_time = datetime.now()
elapsed_time = stop_time - start_time
print(f"Finished! Scraped {len(data)} recipes in total.")
print(f"Elapsed Time: {elapsed_time}")


# In[37]:


# scrape italian

start_time = datetime.now()

# scrape (start with page 2)
for i in range(2,90):
    urlpage = (f"http://allrecipes.co.uk/recipes/italian-recipes.aspx?page={i}&o_is=LV_Pgntn")
    driver.get(urlpage)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(5)
    results = driver.find_elements_by_xpath('//*[@id="sectionTopRecipes"]//*[@class="row recipe"]')
    for result in results:
        product_name = result.find_element_by_tag_name("h3").text
        description = result.find_element_by_class_name("js-truncate").text
        data.append({"product" : product_name, "description": description, "cuisine": "italian"})
    print(f"Number of scraped recipes: {len(data)}")
    i =+ 1
    
stop_time = datetime.now()
elapsed_time = stop_time - start_time
print(f"Finished! Scraped {len(data)} recipes in total.")
print(f"Elapsed Time: {elapsed_time}")


# In[66]:


# Show results and DON'T clean

df1 = pd.DataFrame(data)
df1.columns = ["Title", "Description", "label"]
df1


# In[67]:


# df.to_csv("final_scrape_not_cleaned.csv", encoding='utf-8', index=False)


# In[63]:


# Show results and clean

df = pd.DataFrame(data)
df.columns = ["Title", "Description", "label"]
df['Title'] = df['Title'].replace('►', '', regex=True)
df['Title'].replace(r'\s+|\\n', ' ', regex=True, inplace=True) 
df = df.replace(to_replace= '\.', value= '', regex=True)
df = df.replace(to_replace= '\[', value= '', regex=True)
df = df.replace(to_replace= '\]', value= '', regex=True)
df = df.replace(to_replace= '\?', value= '', regex=True)
df = df.replace(to_replace= '\!', value= '', regex=True)


# In[ ]:



engine = db.create_engine('postgresql://postgres:recipedb@recipedb.csymvihl5lcx.us-east-2.rds.amazonaws.com:5432/postgres')


# In[64]:


# save results to a csv
df.to_sql('cleaned_scraped', con = engine, index=False, if_exists = 'replace')
df1.to_sql('dirty_scraped',con = engine, index=False, if_exists = 'replace')


# In[65]:


driver.quit()

