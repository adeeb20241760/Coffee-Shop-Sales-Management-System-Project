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

