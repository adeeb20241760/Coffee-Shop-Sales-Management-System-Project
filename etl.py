# Extarcting data from excel file
import pandas as pd
coffee_sales = pd.read_excel('Coffee Shop Sales.xlsx')

# Transforming data

## Removing null values
initial_row_count = len(coffee_sales)
coffee_sales = coffee_sales.dropna()
null_values_removed = initial_row_count - len(coffee_sales)

if null_values_removed > 0:
    print(f"Removed {null_values_removed} rows with null values.")
else:
    print("No null values found in the dataset.")    

## Removing Negative Values
intial_row_count = len(coffee_sales)
coffee_sales = coffee_sales[
    (coffee_sales['transaction_qty'] >= 0) & 
    (coffee_sales['unit_price'] >= 0) &
    (coffee_sales['transaction_id'] > 0) &
    (coffee_sales['store_id'] > 0) &
    (coffee_sales['product_id'] > 0)
]  
negative_values_removed = intial_row_count - len(coffee_sales)

if negative_values_removed > 0:
    print(f"Removed {negative_values_removed} rows with negative values.")
else:
    print("No negative values found in the dataset.")   

## Removing Duplicates
initial_row_count = len(coffee_sales)
coffee_sales = coffee_sales.drop_duplicates(subset=['transaction_id'])
duplicates_removed = initial_row_count - len(coffee_sales)

if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate rows.")
else:
    print("No duplicate rows found in the dataset.")

## Date & Time Formatting

coffee_sales['transaction_date'] = pd.to_datetime(coffee_sales['transaction_date'], format = '%Y-%m-%d')
coffee_sales['transaction_time'] = pd.to_datetime(coffee_sales['transaction_time'], format = '%H:%M:%S').dt.time
print("Date and Time columns formatted successfully.")    

## Splitting the dataframe to be turned into tables

### Transactions Table
transaction_df = coffee_sales[['transaction_id','transaction_date', 'transaction_time','transaction_qty','store_id', 'product_id', 'unit_price']].copy().sort_values(by='transaction_id').reset_index(drop=True)
print("Transactions table created successfully.")

### Products Table
product_df = coffee_sales[['product_id', 'product_category', 'product_type', 'product_detail']].copy().drop_duplicates(subset='product_id').sort_values(by='product_id').reset_index(drop=True)
print("Products table created successfully.")

### Stores Table
store_df = coffee_sales[['store_id','store_location']].copy().drop_duplicates(subset='store_id').sort_values(by='store_id').reset_index(drop=True)
print("Stores table created successfully.")

### Store_Products Table
store_product = coffee_sales[['store_id', 'product_id']].copy().drop_duplicates().sort_values(by=['store_id', 'product_id']).reset_index(drop=True)
#### Creating the 'base_price' column 
coffee_sales_grouped = coffee_sales.groupby(['store_id','product_id'])['unit_price'].max().reset_index()
store_product = store_product.merge(coffee_sales_grouped, on=['store_id', 'product_id'], how='left')
store_product.rename(columns={'unit_price': 'base_price'}, inplace=True)
print("Store_Products table created successfully.")

print("Data extraction and transformation completed successfully.")


