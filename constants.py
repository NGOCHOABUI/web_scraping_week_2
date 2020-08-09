TIKI_URL = 'https://tiki.vn'
CONNECTION_STRING = 'tiki.db'

# ************CATEGORY*************

# create categories table
CREATE_CATEGORY_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        url TEXT,
        parent_id INTEGER,
        last_level INTEGER,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

# insert category into categories tables
INSERT_CATEGORY_QUERY = """
INSERT INTO categories (name, url, parent_id)
VALUES(?, ?, ?);                    
"""

# update category 
UPDATE_CATEGORY_QUERY = """
UPDATE categories  SET last_level =  ?
WHERE ID = ?;                    
"""

# get all last level category 
SELECT_ALL_LAST_LEVEL_CATEGORIES_QUERY = """
SELECT * FROM categories
WHERE last_level = 1                   
"""

# ************PRODUCT*************

# create products table
CREATE_PRODUCT_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cat_id INTEGER,
        title VARCHAR(255),
        price_sale INTEGER,
        sale INTEGER,
        price_regular INTEGER,
        rating FLOAT,
        reviewers INTEGER,
        url TEXT,
        img_url TEXT,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

# insert category into categories tables
INSERT_PRODUCT_QUERY = """
INSERT INTO products (
    cat_id,
    title,
    price_sale,
    sale,
    price_regular,
    rating,
    reviewers,
    url,
    img_url 
    )
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);                    
"""