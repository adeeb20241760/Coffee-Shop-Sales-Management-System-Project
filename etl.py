# Extarcting data from excel file
import pandas as pd
coffee_sales = pd.read_excel('C:\\Users\\Adeeb\\Desktop\\Coffee-Shop-Sales-Management-System-Project\\Coffee Shop Sales.xlsx')

# Transforming data

# Null Values
print(coffee_sales.isnull().sum())

