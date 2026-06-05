# Coffee-Shop-Sales-Management-System-Project

A production-ready data engineering and interactive business intelligence platform designed to ingest, validate, profile, and analyze transactional retail logs for a multi-terminal coffee shop enterprise. This system moves raw, unrefined point-of-sale (POS) records through an automated Python ETL pipeline, enforces structural database integrity, and routes clean data to an insights framework.

---

## 📁 Repository Architecture & Layout

**Coffee-Shop-Sales-Management-System-Project**

├── Coffee Shop ER Diagram.drawio   Relational Database Entity Relationship Design

├── data_investigation.ipynb        EDA Sandbox Notebook used to design database architecture

├── etl.py                          Production Cleaning & Engineering Script

├── app.py                          Core Interactive Dashboard Application UI

├── schema.sql                      Relational Databse Schema Creation Script

├── README.md                       Documentation

└── requirements.txt                Fixed Framework Packaged Dependancies

## 🔍 Data Exploration & Database Architecture 

Before writing production data cleaning code, comprehensive data profiling was conducted within `data_investigation.ipynb` to aid in normalising the dataset & structure the Entity Relationship Diagram:

### Dataset Overview
For this project I took the following dataset of a fictitious coffee shop operating out of three NYC locations:
https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales/data 

•	transaction_id : Unique sequential ID representing an individual transaction

•	transaction_date : Date of the transaction (MM/DD/YY)

•	transaction_time : Timestamp of the transaction (HH:MM:SS)

•	transaction_qty : Quantity of items sold

•	store_id : Unique ID of the coffee shop where the transaction took place

•	store_location : Location of the coffee shop where the transaction took place

•	product_id : Unique ID of the product sold

•	unit_price : Retail price of the product sold

•	product_category : Description of the product category

•	product_type : Description of the product type

•	product_detail : Description of the product detail

### Oth Normal Form
<img width="956" height="214" alt="image" src="https://github.com/user-attachments/assets/24846f9e-e63d-4802-949b-f2e40878ce3d" />


### 1st Normal Form
#### The Globally Unique Identifier Finding
Exploratory Data Analysis (EDA) confirmed that **`transaction_id` is 100% globally unique** across every single record in the dataset:
Because every entry features an isolated, unique identifier, it is mathematically proven that **no true database row duplication errors exist**. 
Thus it can be utilised as a primary key.

##### Understanding Timestamp Collisions
Further EDA revealed occurrences where identical values are shared across `store_id`, `transaction_date`, `transaction_time`, and even `product_id`. 

<img width="1614" height="782" alt="image" src="https://github.com/user-attachments/assets/81f7dcad-4c3b-4a39-bbed-c117e1df3978" />


* **The Interpretation:** Because `transaction_id` remains perfectly unique during these collisions, these entries are verified as completely legitimate, high-velocity real-world events—such as split-second item scans or concurrent purchases fired across multiple active terminal registers. 
* **Engineering Impact:** Deleting these rows based on matching timestamps would result in catastrophic revenue recording loss. These records are intentionally preserved and routed directly to the dashboard insights engine.

#### Atomicity of Rows
EDA confirmed that all string columns (i.e store_location, product_category, product_type, product_detail) were atomic in nature containing no repeating groups.

#### Results
<img width="952" height="214" alt="image" src="https://github.com/user-attachments/assets/7c98d28c-cc3d-4673-a583-d5890e503612" />


### 2nd Normal Form
#### Partial Dependencies
Since the primary key consists of one component (i.e. transaction_id) there would be no partial dependencies as by default every no-key attribute depends on it.
Hence the data is already in 2nd Normal Form

### 3rd Normal Form
#### Transitive Dependancies
The following instances were identified and dealt with:

  `‘store_location’` is dependent on ‘store_id’ therefore a separate   `‘store’` entity was created.
  
  `‘product_type’`, `‘product_category’`, `‘product_detail’` are dependent on `‘product_id’` therefore a separate entity `‘product’` was created. 
  
  It was found that the `‘unit_price’` differed across the same product IDs and store IDs, hence it is fully dependant on `‘transaction_id’` and kept in the `‘transaction’` table. This is most likely due to discounts being offered at certain time periods or the use of loyalty scheme.
  <img width="546" height="306" alt="image" src="https://github.com/user-attachments/assets/f5450a51-fe70-4632-83ac-1a33190d9c4a" />


#### Results

`‘transaction’`

<img width="442" height="214" alt="image" src="https://github.com/user-attachments/assets/264a73f0-8a83-43c7-ab2c-b80e4d63f10e" />

`‘product’`

<img width="424" height="177" alt="image" src="https://github.com/user-attachments/assets/b9970c3d-7415-4374-b539-45713246ffbc" />

`‘store’`

<img width="258" height="371" alt="image" src="https://github.com/user-attachments/assets/50fd212d-3b28-41b3-a2d3-cd9498e5cb98" />


### Entity Relationship Modelling
After the normalisation process the further changes would be done to ensure a relational database structure that can be physically implemented.

#### Existing Problems and Solutions
A product can be offered in many stores, and a store can offer many products, hence there is a many-to-many relationship. To overcome this, a new link table ‘Store_Product’ will be created with ‘store_id’ and ‘product_id’ as a primary composite key.

While keeping ‘unit_price’ in the ‘Transaction’ table satisfies 3NF, from a business and practical standpoint it poses a flaw. When entering a new transaction, since every product doesn’t have a set price it will rely on the on the user (i.e. cashier) entering the unit every time which will cause numerous issues, such as forgetting the prices from over 80 different products, mistyping the price and it can be tedious leading to higher queue waiting times. Therefore it would be best to have a ‘base_price’ field which will show the default price for a product at a specific store, which will be stored separately in ‘Store_Product’, as well as the existing ‘unit_price’ product under ‘Transactions’. During a transaction once the user selects the product this default price will appear, however if there was a discount going on the user can enter it into a temporary box, which will calculate the new and this final price will be stored as the ‘unit_price’ under ‘Transactions’.

#### Entities

* **Transaction:** Describes the purchases made by customers at the coffee shops

* **Product:** Describes the different products offered at the coffee shops

* **Store:** Describes the different branches of coffee shops
   
* **Store_Product:** Describes and resolves the many-to-many relationship between the Product and Store entities.

#### Relational Constraints & Multiplicity Rules

The database schema enforces explicit real-world coffee shop operational rules directly at the engine level to maintain transactional accuracy:

* **Store_Product ──[1 : N]── Transaction**
  * *Constraint:* A specific store product can have zero historical sales records (e.g., a premium menu item that hasn't been ordered yet), while every transaction line item must map back to an authentic store-product pairing.

* **Product──[1 : N]── Store_Product**
  * *Constraint:* A product may not be availabe at any stores (e.g., a newly formulated coffee flavour), while a specific store product must map back to a single product occurrence.
    
* **Store ──[1 : N]── Store_Product** 
  * *Constraint:* A store can exist on the system without inventory items assigned to it (e.g., a newly opened branch before stock ingestion), but every tracked inventory item must map to exactly one valid store location.

### Entity Relationship Diagram
 <img width="979" height="650" alt="image" src="https://github.com/user-attachments/assets/d10ace83-29f1-4569-b195-272b5e605329" />


### Assumptions
•	A transaction can’t be stored unless a product has been included (business logic).

•	The newly added ‘base_price’ field is the maximum ‘unit_price’ price of a product at a specific store. Since any price lower than that can be considered discounted prices.

•	The determination, as well as tracking of discounts and customer loyalty schemes is beyond the scope of this system.





 
 




---
