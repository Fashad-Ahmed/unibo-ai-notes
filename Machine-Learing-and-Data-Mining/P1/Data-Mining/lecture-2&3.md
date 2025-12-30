Based on the presentation "Machine Learning and Data Mining - DFM - Example," here is a slide-by-slide explanation of the case study for a company called "RetailCo."

### **Part 1: The Context & Problem (Slides 1–5)**

* **Slide 1: Title Slide**
This slide introduces the course topic, "Machine Learning and Data Mining," specifically focusing on an example of the **Dimensional Fact Model (DFM)**.


* **Slide 2: Outline**
This sets the agenda for the presentation, covering the story (problem), management requirements, the DWH structure, the final deliverables, data mart schemas, and next steps.


* **Slide 3: The Story - Why RetailCo Needs a Data Warehouse**
This introduces the subject, **RetailCo**, a national chain with hundreds of stores.


* 
**The Problem:** Currently, each store runs its own operational systems (sales, inventory, loyalty).


* 
**The Chaos:** Data is fragmented, inconsistent, and designed only for transactions, not analysis. Different stores may even use different software.




* **Slide 4: Challenges Faced by Management**
This details the specific pain points resulting from the fragmented data:
* 
**Fragmented Information:** Sales reports do not match across channels.


* 
**Slow Decision-Making:** IT must manually reconcile spreadsheets.


* 
**Missed Opportunities:** Managers cannot react quickly to demand.


* 
**Limited Forecasting:** This leads to overstocking or stockouts.




* **Slide 5: The Solution - Build a Data Warehouse**
The proposed solution is to build a centralized, historical repository (Data Warehouse). This will enable **OLAP analysis** and **data mining** to uncover trends, customer behaviors, and performance indicators.



---

### **Part 2: Requirements (Slides 6–8)**

* **Slide 6: Outline**
Transition slide moving to the "Requirements from Management" section.


* **Slide 7: High-Level Management Requirements**
This lists what Executives and Directors need:
* A "unified view of the business" (one version of the truth).


* Strategic KPIs like revenue growth and market basket analysis.


* Customer insights regarding loyalty and churn.


* Forecasting for sales and inventory.




* **Slide 8: Medium-Level Management Requirements**
This lists what Regional Managers need:
* 
**Sales Monitoring:** Daily/weekly views across regions.


* 
**Inventory Control:** Tracking turnover and slow-moving items.


* 
**Promotions Analysis:** Measuring the effectiveness of campaigns.


* 
**Supply Chain & Service:** Monitoring supplier performance and customer satisfaction.





---

### **Part 3: Structure & Modeling (Slides 9–14)**

* **Slide 9: Outline**
Transition slide moving to "Data Warehouse Structure - Dimensional Fact Model".


* **Slide 10: Dimensional Fact Model (DFM) Approach**
The project will use DFM because it ensures clarity for stakeholders and provides intuitive hierarchies for analysis.


* **Slide 11: Facts - Core Measurable Events**
The model identifies three core "Facts" to track:
* 
**Sales Fact:** Measures include Quantity, Revenue, and Profit at the transaction level.


* 
**Inventory Fact:** Measures stock levels and turnover at a daily snapshot level.


* 
**Promotion Fact:** Measures cost and ROI per promotion event.




* **Slide 12: Dimensions - Perspectives for Analysis**
The model identifies the "Dimensions" (perspectives) used to slice the data:
* 
**Time:** Day to Year hierarchies.


* 
**Product:** Hierarchy includes Brand, Category, and Department.


* 
**Store:** Hierarchy includes City, Region, and Country.


* 
**Customer, Promotion, and Supplier:** Additional dimensions for segmentation and logistics.




* **Slide 13: Sales Fact Schema - Example**
This shows a preliminary schema connecting the **Sales Fact** (center) to dimensions like Time, Product, Store, Customer, and Promotion.


* **Slide 14: Benefits of the Star Schema**
Explains why this structure is useful:
* 
**Additivity:** Measures like revenue can be summed up.


* 
**Historical Analysis:** Supported by time hierarchies.


* 
**Flexibility:** Allows slicing-and-dicing data.





---

### **Part 4: Deliverables & Detailed Schemas (Slides 15–24)**

* **Slides 15-16: Final Deliverable**
The goal is a retail DWH designed around Sales, Inventory, and Promotions that provides a scalable BI platform for decision-making.


* **Slide 17: Outline**
Transition slide to "Data Marts - DFM schemas".


* **Slide 18: Sales Data Mart - DFM (Basic)**
A high-level visual diagram of the Sales Data Mart. The **Sales Fact** is central, connected to Product, Time, Store, Customer, and Promotion dimensions.


* **Slide 19: Inventory Snapshot Data Mart - DFM (Basic)**
A high-level diagram for Inventory. The **Inventory Snapshot Fact** connects to Time, Product, Supplier, and Store.


* **Slide 20: Promotion Effect Data Mart - DFM (Basic)**
A high-level diagram for Promotions. The **Promotion Effect Fact** connects to Promo Time, Product, Promotion, and Store.


* **Slide 21: Sales Data Mart - Conformed Star (Detailed)**
A detailed schema for Sales.
* 
**Hierarchies:** Shows detailed paths (e.g., ).


* 
**Measures:** Defines Quantity, Revenue, and Profit as **flow** measures.


* 
**Additivity:** Notes that flow measures sum over all dimensions.




* **Slide 22: Inventory Snapshot - Periodic Snapshot (Detailed)**
A detailed schema for Inventory.
* 
**Measures:** Tracks On-hand Qty and Stockout Flag.


* 
**Aggregation Rule:** Level measures (like quantity on hand) use **AVG/MIN/MAX** over time, but **SUM** across non-temporal dimensions.




* **Slide 23: Promotion Effect - Event Fact (Detailed)**
A detailed schema for Promotions.
* 
**Measures:** Tracks Campaign Cost, Lift in Revenue, and ROI.


* 
**Note:** Algebraic measures like **ROI** require support measures (Revenue Lift, Cost) to be calculated correctly.




* **Slide 24: Legend & Modeling Notes**
Provides the key to reading the previous diagrams:
* 
**Orange:** Facts (quantitative measures).


* 
**Blue:** Dimensions (analysis axes).


* 
**Conformed Dimensions:** Dimensions like Product and Store are reused across different data marts.


* 
**Additivity Rules:** Explains that Flow measures sum everywhere, Level measures average over time, and Unit measures (ROI) should generally not be summed.





---

### **Part 5: Next Steps (Slides 25–27)**

* **Slide 25: Outline**
Transition slide to "Next Steps".


* **Slide 26: Next Steps for Implementation**
Lists the necessary actions for deployment:
* 
**ETL Process:** Define extraction and cleansing.


* 
**Data Governance:** Establish quality standards.


* 
**Infrastructure & Tools:** Select cloud/hybrid tech and BI tools (e.g., Power BI).


* 
**Rollout & Training:** Start with sales/inventory marts and train staff.




* **Slide 27: Conclusion**
Visualizes the transformation from "Fragmented Operational Data" (Chaos) to an "Integrated Data Warehouse" that empowers Executives, Managers, and Analysts.



---


In the **Dimensional Fact Model (DFM)**, the structure is designed to be intuitive for both technical teams and business managers by organizing data around specific business events.

### **Important Elements of DFM**

The DFM is a graphical formalism that uses several core building blocks to represent a multidimensional database:

* **Facts**: These are the central focus of the analysis, representing a business process or event (e.g., a "Sale" or "Inventory Snapshot").
* **Measures**: These are numerical properties of a fact that can be quantified and aggregated (e.g., *Revenue*, *Quantity Sold*, or *Profit*).
* **Dimensions**: These are the coordinates or "perspectives" used to analyze a fact (e.g., *Time*, *Product*, or *Store*).
* **Hierarchies**: These exist within dimensions to allow for "drill-down" analysis. For example, a Time dimension might follow a hierarchy of .
* **Dimensional Attributes**: Descriptive properties within a hierarchy (e.g., *Brand* or *Category* for a product).

---

### **What is the "Grain"?**

The **Grain** is perhaps the most critical definition in a data warehouse because it specifies exactly **what a single row in a fact table represents**.

* **The Level of Detail**: It determines the "finest level of detail" available for analysis. A "finer" grain provides more detail (e.g., every individual transaction line), while a "coarser" grain is more summarized (e.g., daily totals per store).
* **Consistency**: Declaring the grain upfront ensures that all dimensions and measures are consistent; you cannot mix different levels of detail (like a daily total and a single transaction) in the same fact table.

#### **Examples of Grains from your Case Study:**

| Fact Table | Declared Grain |
| --- | --- |
| **Sales Fact** | One line item per transaction |
| **Inventory Fact** | One product-store per day (Daily Snapshot) |
| **Promotion Fact** | One promotion-event per product per store |



A **star schema** is a data modeling technique used in **data warehouses** and **BI systems** to organize data for fast, simple querying.

---

## What it is

It’s called a *star* because the structure looks like one:

* **One central fact table**
* **Multiple surrounding dimension tables**
* The fact table connects to each dimension via **foreign keys**
* Dimension tables are **not connected to each other**

```
        Time
          |
Product — Fact_Sales — Customer
          |
        Store
```

---

## Components

### 1. Fact Table (center)

Contains:

* **Measures** (numeric, aggregatable values)

  * e.g. `sales_amount`, `quantity`, `profit`
* **Foreign keys** to dimension tables

Example:

```
Fact_Sales
-----------
date_id
product_id
customer_id
store_id
sales_amount
quantity
```

---

### 2. Dimension Tables (edges)

Contain:

* **Descriptive attributes**
* Usually **denormalized**
* Used for filtering, grouping, and labeling

Example:

```
Dim_Product
-----------
product_id
product_name
category
brand
```

---

## Example (Retail)

* **Fact table**: `Fact_Sales`
* **Dimensions**:

  * `Dim_Date`
  * `Dim_Product`
  * `Dim_Customer`
  * `Dim_Store`

Typical query:

> Total sales by product category and month

Star schema makes this fast and readable.

---

## Advantages

✅ Simple to understand
✅ Faster queries (fewer joins)
✅ Ideal for OLAP and reporting
✅ Works well with BI tools (Power BI, Tableau, Looker)

---

## Disadvantages

❌ Data redundancy in dimensions
❌ Less flexible for very complex relationships
❌ Not ideal for highly normalized transactional systems (OLTP)

---

## Star Schema vs Snowflake Schema

| Star Schema             | Snowflake Schema      |
| ----------------------- | --------------------- |
| Denormalized dimensions | Normalized dimensions |
| Simpler                 | More complex          |
| Faster queries          | More joins            |
| More storage            | Less storage          |

---


A **snowflake schema** is a data warehouse modeling technique that’s an extension of the **star schema**, where **dimension tables are normalized into multiple related tables**. The structure resembles a **snowflake** due to its branching shape.

---

## What it is

* **Fact table** in the center
* **Dimensions split into sub-dimensions**
* More **joins** than a star schema
* Reduced **data redundancy**

```
             Dim_Year
                |
Dim_Month — Dim_Date — Fact_Sales — Dim_Product
                                |
                           Dim_Category
                                |
                           Dim_Department
```

---

## Components

### 1. Fact Table

Contains:

* **Measures** (numeric values)
* **Foreign keys** to dimension tables

Example:

```
Fact_Sales
-----------
date_id
product_id
store_id
sales_amount
quantity
```

---

### 2. Dimension Tables (Normalized)

Dimensions are broken into multiple tables to remove redundancy.

Example (Product dimension):

```
Dim_Product
-----------
product_id
product_name
category_id

Dim_Category
------------
category_id
category_name
department_id

Dim_Department
--------------
department_id
department_name
```

---

## Example Query

> Total sales by department

This requires more joins than a star schema:

```sql
SELECT d.department_name, SUM(f.sales_amount)
FROM Fact_Sales f
JOIN Dim_Product p ON f.product_id = p.product_id
JOIN Dim_Category c ON p.category_id = c.category_id
JOIN Dim_Department d ON c.department_id = d.department_id
GROUP BY d.department_name;
```

---

## Advantages

✅ Reduced data redundancy
✅ Smaller dimension tables
✅ Easier to maintain hierarchical dimensions
✅ Better data integrity

---

## Disadvantages

❌ More complex queries
❌ Slower performance due to many joins
❌ Harder for business users to understand
❌ Less BI-tool friendly than star schema

---

## Snowflake vs Star Schema

| Snowflake Schema      | Star Schema             |
| --------------------- | ----------------------- |
| Normalized dimensions | Denormalized dimensions |
| Less storage          | More storage            |
| More joins            | Fewer joins             |
| Slower queries        | Faster queries          |
| More complex          | Simpler                 |

---

## When to use Snowflake Schema

✔ Large dimensions with clear hierarchies
✔ Storage optimization is critical
✔ Strong data governance needs
✔ Dimensions change frequently

---




