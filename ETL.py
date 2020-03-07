#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
end_page_num = 1
i =0
while i <= end_page_num:
    i +=1
    page = requests.get("https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/?page={}".format(i))

# page = requests.get("https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/?page=30")
# page


# In[2]:


from bs4 import BeautifulSoup
italian = BeautifulSoup(page.content, 'html.parser')


# In[3]:


_ = italian.find_all('article', class_='fixed-recipe-card')


# In[4]:


italian_dishes = italian.select('.fixed-recipe-card__title-link ')
italian_descriptors = italian.select('.fixed-recipe-card__description')
# removes /n from names
italian_dishes_ls = [item.get_text().replace('\n', '') for item in italian_dishes]
italian_descriptors_ls = [item.get_text() for item in italian_descriptors]


# In[5]:


from collections import OrderedDict
italian_dishes_ls = list(OrderedDict.fromkeys(italian_dishes_ls))


# In[15]:


# Here the aim is to have the full dataframe. Change the name to final and do not forget 
# to create column for label which we drop for labelling
import pandas as pd
italian_df = pd.DataFrame({'recipe_name':italian_dishes_ls,
                       'description':italian_descriptors_ls})
italian_df['label'] = 'Italian'


# In[8]:


import sqlalchemy as db
engine = db.create_engine('postgresql://postgres:recipedb@recipedb.csymvihl5lcx.us-east-2.rds.amazonaws.com:5432/postgres')


# In[11]:


# this everytime will replace the content of one table we are scraping in the RDS
italian_df.to_sql('test2', con = engine, index=False, if_exists = 'replace')

