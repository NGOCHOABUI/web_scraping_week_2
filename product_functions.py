from constants import * 
from product import Product
from base_functions import Base_Functions
import time
import random
import re

class Product_Functions():
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
    
    # create products table
    def create_products_table(self):
        query = CREATE_PRODUCT_TABLE_QUERY

        try:
            self.cur.execute(query)
            self.conn.commit()
        except Exception as err:
            print('ERROR BY CREATE TABLE PRODUCTS', err)

    # get all products by category by single page
    def get_products_single_page(self, url, cat_id, save_db = False):

        print('RUN PAGE URL', url)

        soup = Base_Functions.get_url(url)

        result = []
        
        try:
            for div in soup.find_all('div', {'class': 'product-item'}):
                try:
                    t = div.find('p', {'class': 'title'})
                    title = t.text.strip() if t else ''
                except Exception as err:
                    print('Tilte', err)

                try:   
                    i = div.img['src']
                    img_url = i.strip() if i else ''
                except Exception as err:
                    print('Img', err)

                try:
                    u = div.find("a")
                    url = TIKI_URL + u['href'] if u else ''
                except Exception as err:
                    print('Url', err)

                try:
                    p_sale = div.find('span', {'class': 'final-price'})
                    price_sale = int(p_sale.text.strip().split()[0][:-1].strip().replace('.','')) if p_sale else 0
                except Exception as err:
                    print('Price_sale', err)    

                try:
                    s = div.find('span', {'class': 'sale-tag'})
                    sale = int(s.text.strip(' -%')) if s else 0
                except Exception as err:
                    print('Sale', err)
                
                try:
                    p_regular = div.find('span', {'class': 'price-regular'})
                    price_regular = int(p_regular.text.strip()[:-1].replace('.','')) if p_regular else 0
                except Exception as err:
                    print('Price regular', err)
                
                try:
                    rating_percentage = div.find('span', {'class': 'rating-content'})
                    if rating_percentage:
                        r = int(rating_percentage.span['style'].split(':')[-1][:-1].strip())
                    # rating has 100% for 5 stars, 1 star is 20% so divide the rating for 20 
                        rating = round((r) / 20, 1)
                    else:
                        rating  = 0
                except Exception as err:
                    print('Rating', err)
                
                try:
                    revs = div.find('p', {'class': 'review'}).text.strip('(').split()[0].strip()
                    rev = re.sub('\D+', '', revs)
                    reviewers = int(rev) if rev else 0
                except Exception as err:
                    print('Reviewers', err)

                product = Product(
                    conn = self.conn,
                    cur = self.cur,
                    cat_id = cat_id,
                    title = title,
                    img_url = img_url,
                    url = url,
                    price_sale = price_sale,
                    sale = sale,
                    price_regular = price_regular,
                    rating = rating,
                    reviewers = reviewers
                )
                
                if save_db:
                    product.save_into_db()
                
                result.append(product)
        except Exception as err:
            print('ERROR WITH GET PRODUCTS SINGEL PAGE', err)
        
        return result

    # generate pages
    def get_products_by_category(self, url, cat_id, save_db = False):

        page = 1
        page_url = '&page='

        result = []

        while page > 0:

            url_per_page = url + page_url + str(page)

            print('RUN PAGE', page)

            products = self.get_products_single_page(url_per_page, cat_id , save_db)

            if len(products) == 0 :
                break
            else:
                for i in products:

                    result.append(i)

            time.sleep(random.randrange(2,4))

            page = page + 1

        return result
    
    # get all products
    def get_all_products(self, categories, save_db = False):

        if len(categories) == 0:
            return
        
        try:

            for cat in categories:

                print('******* RUN CATEGORY ******', cat.name)

                self.get_products_by_category(url = cat.url, cat_id = cat.cat_id, save_db = save_db)
                
        except Exception as err:
            print('ERROR WITH GET ALL PRODUCTS', err)

