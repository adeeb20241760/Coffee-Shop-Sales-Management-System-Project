# Extarcting data from excel file
import pandas as pd
coffee_sales = pd.read_excel('C:\\Users\\Adeeb\\Desktop\\Coffee-Shop-Sales-Management-System-Project\\Coffee Shop Sales.xlsx')

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
numeric_columns = coffee_sales.select_dtypes(include=['number']).columns
numeric_columns

for column in numeric_columns:
    negative_values = coffee_sales[coffee_sales[column] < 0 ]
    if not negative_values.empty:
        print(f"Negative Values found in column {column}:")

coffee_sales = coffee_sales[(coffee_sales[numeric_columns] >= 0).all(axis=1)]    
print("Negative values removed from the dataset.")   

## Removing Duplicates
initial_row_count = shape(coffee_sales)[0]
coffee_sales = coffee_sales.drop_duplicates()
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
