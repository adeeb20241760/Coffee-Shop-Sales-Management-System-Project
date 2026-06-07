# Extarcting data from excel file
import pandas as pd
coffee_sales = pd.read_excel('Coffee Shop Sales.xlsx')

# Transforming data

## Removing null values
from numpy import shape
initial_row_count = shape(coffee_sales)[0] 
coffee_sales = coffee_sales.dropna()
null_values_removed = initial_row_count - shape(coffee_sales)[0]

if null_values_removed > 0:
    print(f"Removed {null_values_removed} rows with null values.")
else:
    print("No null values found in the dataset.")    

## Removing Negative Values
intial_row_count = shape(coffee_sales)[0]
coffee_sales = coffee_sales[
    (coffee_sales['transaction_qty'] >= 0) & 
    (coffee_sales['unit_price'] >= 0) &
    (coffee_sales['transaction_id'] > 0) &
    (coffee_sales['store_id'] > 0) &
    (coffee_sales['product_id'] > 0)
]  
negative_values_removed = intial_row_count - shape(coffee_sales)[0]

if negative_values_removed > 0:
    print(f"Removed {negative_values_removed} rows with negative values.")
else:
    print("No negative values found in the dataset.")   
    
## Removing Duplicates
initial_row_count = shape(coffee_sales)[0]
coffee_sales = coffee_sales.drop_duplicates(subset=['transaction_id'])
duplicates_removed = initial_row_count - shape(coffee_sales)[0]

if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate rows.")
else:
    print("No duplicate rows found in the dataset.")

## Date & Time Formatting

coffee_sales['transaction_date'] = pd.to_datetime(coffee_sales['transaction_date'], format = '%Y-%m-%d')
coffee_sales['transaction_time'] = pd.to_datetime(coffee_sales['transaction_time'], format = '%H:%M:%S').dt.time
print("Date and Time columns formatted successfully.")    

print("Data extraction and transformation completed successfully.")
