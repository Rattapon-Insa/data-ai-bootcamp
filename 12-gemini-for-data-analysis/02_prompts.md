# BigQuery Casvas Prompt for Data Analysis

## ALL TABLES:
1. distribution_centers: Information about various distribution centers
2. events: Records of events, possibly related to website visits, customer interactions
3. inventory_items: Details about items in the inventory, possibly including quantities and locations.
4. order_items: Information about items included in orders.
5. orders: Details about customer orders, including order dates, statuses, and associated users.
6. products: Information about products, such as names, descriptions, and prices.
7. users: Details about users, including customer information.

## Orders
Prompts:
| Query Prompt | Visualization Prompts |
| - | - |
| Find Cancelled rate based on gender | -|
| For all order, find ratio of each order status per total order | Stacked bar chart by month |
| For each month, find total_revenue, total_items, total_purchasers, total_orders where the order not Cancelled or Returned. Please sort the result with month. Also noted that total revenue retail price multiply with num_of_item | Line chart by month |
|For Shipped Orders, find average, min, max, lead time in hour before Shipped. Check status need to be 'Shipped' and lead time are higher than 0| - |

## Distribution Centers
- Summary product category in each DC

## Events
- count unique total users group by trafic source , country where user id is not empty
- สรุปจำนวน event จาก trafic source , ทุก event_type, browser

## Products
| Query Prompt | Visualization Prompts |
| - | - |
|Top 10 Average, min, max profit from each category |Bar chrat|

## User
| Query Prompt | Visualization Prompts |
| - | - |
| Summarize total user by traffice_source, gender and city |-|

## Order Items + Product 
| Query Prompt | Visualization Prompts |
| - | - |
| Analyze which product category have order sale volume and frequency | - |
| brand total sale volume| - |
| Total sale volume by category where order status is Cancelled or Returned. sort by highest total sale volume | - |


### References:
- Medium: https://medium.com/@chisomnnamani/the-look-e-commerce-data-analysis-28342b8da868