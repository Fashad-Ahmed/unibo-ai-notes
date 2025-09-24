### OLTP

OLTP is short for Online Transaction Processing. It refers to a type of database system designed to handle high volumes of real-time transactions and manage daily business operations, such as online banking, e-commerce, and airline reservations. OLTP systems are optimized for fast response times, data integrity, and processing thousands of concurrent transactions, ensuring that data is accurate and up-to-date. 
Key Characteristics of OLTP Systems
Real-time Transactions: OLTP systems process many transactions at the same time, with rapid, millisecond-level response times. 
High Volume: They are built to handle a massive number of transactions, often from many users concurrently. 
Data Integrity: These systems maintain data accuracy and atomicity, meaning a transaction is either completed successfully or fails entirely, never in an intermediate state. 
Day-to-Day Operations: OLTP is used for operational tasks like checking bank balances, making purchases, or updating inventory. 
Simplified Queries: The queries in an OLTP system are generally simple, focused on retrieving or modifying individual data records. 
Data Design: OLTP databases use a normalized format and are designed for capturing and storing detailed data for business operations. 


### OLAP

Online analytical processing (OLAP) is software technology you can use to analyze business data from different points of view. Organizations collect and store data from multiple data sources, such as websites, applications, smart meters, and internal systems. OLAP combines and groups this data into categories to provide actionable insights for strategic planning. For example, a retailer stores data about all the products it sells, such as color, size, cost, and location. The retailer also collects customer purchase data, such as the name of the items ordered and total sales value, in a different system. OLAP combines the datasets to answer questions such as which color products are more popular or how product placement impacts sales.

Online analytical processing (OLAP) helps organizations process and benefit from a growing amount of digital information. Some benefits of OLAP include the following.

Faster decision making
Businesses use OLAP to make quick and accurate decisions to remain competitive in a fast-paced economy. Performing analytical queries on multiple relational databases is time consuming because the computer system searches through multiple data tables. On the other hand, OLAP systems precalculate and integrate data so business analysts can generate reports faster when needed.

Non-technical user support
OLAP systems make complex data analysis easier for non-technical business users. Business users can create complex analytical calculations and generate reports instead of learning how to operate databases.

Integrated data view
OLAP provides a unified platform for marketing, finance, production, and other business units. Managers and decision makers can see the bigger picture and effectively solve problems. They can perform what-if analysis, which shows the impact of decisions taken by one department on other areas of the business.

##### What is OLAP architecture?
Online analytical processing (OLAP) systems store multidimensional data by representing information in more than two dimensions, or categories. Two-dimensional data involves columns and rows, but multidimensional data has multiple characteristics. For example, multidimensional data for product sales might consist of the following dimensions:

Product type
Location
Time
Data engineers build a multidimensional OLAP system that consists of the following elements. 

Data warehouse
A data warehouse collects information from different sources, including applications, files, and databases. It processes the information using various tools so that the data is ready for analytical purposes. For example, the data warehouse might collect information from a relational database that stores data in tables of rows and columns. 

ETL tools 
Extract, transform, and load (ETL) tools are database processes that automatically retrieve, change, and prepare the data to a format fit for analytical purposes. Data warehouses use ETL to convert and standardize information from various sources before making it available to OLAP tools.

OLAP server 
An OLAP server is the underlying machine that powers the OLAP system. It uses ETL tools to transform information in the relational databases and prepare them for OLAP operations. 

OLAP database
An OLAP database is a separate database that connects to the data warehouse. Data engineers sometimes use an OLAP database to prevent the data warehouse from being burdened by OLAP analysis. They also use an OLAP database to make it easier to create OLAP data models.

OLAP cubes
A data cube is a model representing a multidimensional array of information. While it’s easier to visualize it as a three-dimensional data model, most data cubes have more than three dimensions. An OLAP cube, or hypercube, is the term for data cubes in an OLAP system. OLAP cubes are rigid because you can't change the dimensions and underlying data once you model it. For example, if you add the warehouse dimension to a cube with product, location, and time dimensions, you have to remodel the entire cube. 

OLAP analytic tools
Business analysts use OLAP tools to interact with the OLAP cube. They perform operations such as slicing, dicing, and pivoting to gain deeper insights into specific information within the OLAP cube. 


<img width="1456" height="1022" alt="image" src="https://github.com/user-attachments/assets/33b49c50-88b0-418c-932e-254be7553ced" />
