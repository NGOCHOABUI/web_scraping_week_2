from constants import *

# last level is 0 or 1, 1 means it is the last level categor, 0 mean not.
class Category:
    def __init__(self, conn, cur, name, url, parent_id = None, cat_id = None, last_level = 0):
        self.conn = conn
        self.cur = cur
        self.name  = name
        self.url = url
        self.parent_id = parent_id
        self.cat_id = cat_id
        self.last_level = last_level
       

    def __repr__(self):
        return f"""ID : {self.cat_id}, Name:{self.name}, 
            URL: {self.url}, Parent: {self.parent_id}"""
    
    
    
    def save_into_db(self):
        query = INSERT_CATEGORY_QUERY
        val = (self.name, self.url, self.parent_id)

        try:
            self.cur.execute(query, val)
            self.cat_id = self.cur.lastrowid
            self.conn.commit()
        except Exception as err:
            print('ERROR BY CATEGORY INSERT', err)

    def update_category_to_last_level(self):
        query  = UPDATE_CATEGORY_QUERY

        val = (1 , self.cat_id)

        try:
            self.cur.execute(query, val)
            self.last_level = 1
            self.conn.commit()
        except Exception as err:
            print('ERROR BY CATEGORY UPDATE', err)