from constants import *
from category import Category
from base_functions import Base_Functions
import time
import random
import re

class Category_Functions():
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
    
    # create categories table
    def create_categories_table(self):
        query = CREATE_CATEGORY_TABLE_QUERY
        
        try:
            self.cur.execute(query)
            self.conn.commit()
        except Exception as err:
            print('ERROR BY CREATE TABLE CATEGORIES', err)

    # get main categories
    def get_main_categories(self, save_db = False):
        soup = Base_Functions.get_url(TIKI_URL)

        result = []
        for a in soup.find_all('a', {'class' : 'MenuItem__MenuLink-sc-181aa19-1 fKvTQu'}):
            name = a.find('span', {'class' : 'text'}).text
            url = a['href']
            
            main_cat = Category(conn = self.conn, cur = self.cur, name = name, url = url)
    
            if save_db:
                main_cat.save_into_db()
            result.append(main_cat)
        return result

    # get sub categories 
    def get_sub_categories(self, parent_category, save_db = False):

        print('RUN SUB CATEGORIES OF', parent_category.name)

        parent_url = parent_category.url

        result = []

        try:
            soup = Base_Functions.get_url(parent_url)

            div_containers = soup.find_all('div', {'class' : 'list-group-item is-child'})

            for div in div_containers:
                name = div.a.text

                name = re.sub('[\s{2,}\n]+\\(.*?\\)', ' ', name).strip()

                sub_url = TIKI_URL + div.a['href']

                sub_cat = Category(conn = self.conn, cur = self.cur, name = name,url = sub_url, parent_id = parent_category.cat_id)

                if save_db:
                    sub_cat.save_into_db()
                
                result.append(sub_cat)
            
        except Exception as err:
            print('ERROr BY GET SUB CATEGORIES', err)
            
        return result

    # get all categories
    def get_all_categories(self, categories, save_db = False):

        if len(categories) == 0 :
            return

        try: 
            for cat in categories:
                print('****** MAIN CATEGORY *****', cat.name)

                sub_categories = self.get_sub_categories(cat, save_db)

                time.sleep(random.randrange(1,3))

                if len(sub_categories) != 0:
                    self.get_all_categories(sub_categories, save_db)
                else:
                    self.category_is_last_level(cat, save_db)
                    
        except Exception as err:
            print('ERROR WITH GET ALL CATGORIES', err)
   
    # update cat to lowest level 
    def category_is_last_level(self, category, save_db=False):

        if save_db:
            category.update_category_to_last_level()
        else:
            print('------CATEGORY IS AT LOWEST LEVEL --------', category)

    def get_all_last_level_categories(self):

        query = SELECT_ALL_LAST_LEVEL_CATEGORIES_QUERY

        result = []

        try:
            categories_from_db = self.cur.execute(query).fetchall()
            for cat in categories_from_db:

                category = Category(
                    conn = self.conn,
                    cur = self.cur,
                    cat_id = cat[0],
                    name = cat[1],
                    url = cat[2],
                    parent_id= cat[3],
                    last_level = cat[4],
                )

                result.append(category)
            
        except Exception as err:
            print('ERROR WITH GET ALL LAST LEVEL CATEGORIES', err)

        return result