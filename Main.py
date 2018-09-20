import csv
from pprint import pprint
from datetime import datetime
from decimal import Decimal

with open('products_short.csv', 'r') as fp:
    reader = csv.reader(fp)
    products = [l for l in reader]
    _products = products
    
    #Creates a dict from data in "products"
    products = [{
        '_invoice' : p[0],
        'stock_code' : p[1],
        'description' : p[2],
        '_quantity' : p[3],
        '_invoice_date' : p[4],
        '_price' : p[5],
        '_customer_id' : p[6],
        'country' : p[7]
    } for p in products]
    

    #convert _invoice from string to integer and put in new key invoice
    [product.update({
        'invoice' : int(product['_invoice'])
    }) for product in products]  
    
    #convert _invoice_date to datetime object and put in new key invoice_date
    [product.update({
        'invoice_date' : datetime.strptime(product['_invoice_date'], '%m/%d/%y %H:%M')
    }) for product in products]
    
    #generate a list of countries in which products are sold
    print(set([product['country'] for product in products]))
    
    #parse _price and _quantity into valid numeric formats and put into new keys
    [product.update({
        'price' : Decimal(product['_price']),
        'quantity' : int(product['_quantity'])
    }) for product in products]
    
    #create a total which is price * quantity and put in in total key
    [product.update({
        'total' : product['price'] * product['quantity']
    }) for product in products]
    
    #return the product "total" spent per country
    def total_per_country(products, country):
        return sum([product['total'] for product in products if product['country'] == country])
        
    #Implements a function "search_by" that receives a list of products and a number of dynamic search params
    def search_by(products, date_lt=None, country=None, stock_code_char=None):
        #receives a product and returns true/false based on default arg params
        def passes_test(p):
            if date_lt and product['invoice_date'] >= date_lt:
                return False
            if country and product['country'] != country:
                return False
            if stock_code_char and not product['stock_code'].endswith(stock_code_char):
                return False
            return True
            
        return [product for product in products if passes_test(p)]
    
    
    
    # pprint(products)
    # pprint(search_by(products, date_lt=datetime(2010, 12, 1, 8, 28)))
    pprint(search_by(products, country='United Kingdom', stock_code_char='A'))