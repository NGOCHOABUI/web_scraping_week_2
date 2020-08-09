from constants import *

class Product:
    def __init__(self, 
        conn, cur, cat_id , title, price_sale, sale, price_regular, 
        rating, reviewers, url, img_url, product_id = None):
        self.conn = conn
        self.cur = cur
        self.title = title
        self.price_sale = price_sale
        self.cat_id = cat_id
        self.product_id = product_id
        self.sale = sale
        self.price_regular = price_regular
        self.rating = rating
        self.reviewers = reviewers
        self.url = url
        self.img_url = img_url
        

    def __repr__(self):
        return f"""ID : {self.product_id}, Name:{self.title}, 
            PRICE_SALE: {self.price_sale}, SALE: {self.sale},
            RATING: {self.rating},
            REVIEWERS: {self.reviewers},
            URL: {self.url}, 
            IMAGE_URL: {self.img_url},
            Parent: {self.cat_id}"""

    def save_into_db(self):
        query = INSERT_PRODUCT_QUERY

        val = (
            self.cat_id, 
            self.title, 
            self.price_sale, 
            self.sale, 
            self.price_regular,
            self.rating,
            self.reviewers,
            self.url,
            self.img_url
            )
        
        try:

            self.cur.execute(query, val)
            self.product_id = self.cur.lastrowid
            self.conn.commit()

        except Exception as err:
            print("ERROR WITH INSERT PRODUCT:", err)