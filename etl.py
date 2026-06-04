# Extarcting data from excel file
import pandas as pd
coffee_sales = pd.read_excel('C:\\Users\\Adeeb\\Desktop\\Coffee-Shop-Sales-Management-System-Project\\Coffee Shop Sales.xlsx')

# Transforming data

# Null Values
print(coffee_sales.isnull().sum())

# Negative values 
negative_qty = (coffee_sales['transaction_qty'] < 0).any()
negative_price = (coffee_sales['unit_price'] < 0).any()
negative_transaction_id = (coffee_sales['transaction_id'] < 0).any()
negative_store_id = (coffee_sales['store_id'] < 0).any()
negative_product_id = (coffee_sales['product_id'] < 0).any()
print(f"Negative values in 'transaction_qty'? {negative_qty}")
print(f"Negative values in 'unit_price'? {negative_price}") 
print(f"Negative values in 'transaction_id'? {negative_transaction_id}")
print(f"Negative values in 'store_id'? {negative_store_id}")
print(f"Negative values in 'product_id'? {negative_product_id}")