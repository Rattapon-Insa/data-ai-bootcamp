## Data Exploration with BigQuery

### User
1. Summarize total user by traffice_source, gender and city
```
WITH CTE AS (
  SELECT
  events.id,
  events.user_id,
  events.sequence_number,
  events.session_id,
  events.created_at,
  events.ip_address,
  events.state,
  events.postal_code,
  events.browser,
  events.uri,
  events.event_type,
  users.id,
  users.first_name,
  users.last_name,
  users.email,
  users.age,
  users.gender,
  users.state,
  users.street_address,
  users.postal_code,
  users.city,
  users.country,
  users.latitude,
  users.longitude,
  users.traffic_source,
  users.created_at,
  users.user_geom
FROM
  `bigquery-public-data.thelook_ecommerce.events` AS events
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.users` AS users
ON
  events.user_id = users.id
)
SELECT
  traffic_source,
  gender,
  city,
  COUNT(user_id) AS total_users
FROM
  CTE
GROUP BY
  1,
  2,
  3;
```

### Product
2. Top 10 Average, min, max profit from each category
```
SELECT
  category,
  AVG(retail_price - cost) AS avg_profit,
  MIN(retail_price - cost) AS min_profit,
  MAX(retail_price - cost) AS max_profit
FROM
  `bigquery-public-data.thelook_ecommerce.products`
GROUP BY
  1
ORDER BY
  avg_profit DESC
LIMIT
  10;
```

### Order
3.1 For Shipped Orders, find average, min, max, lead time in hour before Shipped. Check status need to be 'Shipped' and lead time are higher than 0

```
SELECT
  AVG(EXTRACT(HOUR
    FROM (shipped_at - created_at))) AS avg_lead_time_hours,
  MIN(EXTRACT(HOUR
    FROM (shipped_at - created_at))) AS min_lead_time_hours,
  MAX(EXTRACT(HOUR
    FROM (shipped_at - created_at))) AS max_lead_time_hours
FROM
  `bigquery-public-data.thelook_ecommerce.order_items`
WHERE
  status = 'Shipped'
  AND EXTRACT(HOUR
  FROM (shipped_at - created_at)) > 0;
```

3.2 For each month, find total_revenue, total_items, total_purchasers, total_orders where the order not Cancelled or Returned. Please sort the result with month. Also noted that total revenue retail price multiply with num_of_item

```
SELECT
  EXTRACT(MONTH
  FROM
    order_items.created_at) AS month,
  SUM(order_items.sale_price * order_items.id) AS total_revenue,
  COUNT(order_items.id) AS total_items,
  COUNT(DISTINCT order_items.user_id) AS total_purchasers,
  COUNT(DISTINCT order_items.order_id) AS total_orders
FROM
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
WHERE
  order_items.status != 'Cancelled'
  AND order_items.status != 'Returned'
GROUP BY
  1
ORDER BY
  1;
```

3.3 For all order, find ratio of each order status per total order
```
SELECT
  orders.status,
  COUNT(orders.order_id) / (
  SELECT
    COUNT(*)
  FROM
    `bigquery-public-data.thelook_ecommerce.orders` AS orders ) AS ratio
FROM
  `bigquery-public-data.thelook_ecommerce.orders` AS orders
GROUP BY
  1;
```

3.4 Find Cancelled rate based on gender
```
SELECT
  orders.gender,
  SUM(CASE
      WHEN orders.status = 'Cancelled' THEN 1
      ELSE 0
  END
    ) / COUNT(orders.order_id) AS cancelled_rate
FROM
  `bigquery-public-data.thelook_ecommerce.orders` AS orders
GROUP BY
  1;
```

### Event

4.1 สรุปจำนวน event จาก trafic source , ทุก event_type, browser
```
SELECT
  traffic_source,
  event_type,
  browser,
  COUNT(*) AS total_event
FROM
  `bigquery-public-data.thelook_ecommerce.events`
GROUP BY
  traffic_source,
  event_type,
  browser;
```

4.2 count unique total users group by trafic source , country where user id is not empty
```
SELECT
  events.traffic_source,
  events.city,
  COUNT(DISTINCT events.user_id)
FROM
  `bigquery-public-data.thelook_ecommerce.events` AS events
WHERE
  events.user_id IS NOT NULL
GROUP BY
  1,
  2;
```

### Distribution Centers

5 Summary product category in each DC name
```
WITH
  CTE AS (
  SELECT
    products.id,
    products.cost,
    products.category,
    products.name,
    products.brand,
    products.retail_price,
    products.department,
    products.sku,
    distribution_centers.id,
    distribution_centers.name AS distribution_centers_name,
    distribution_centers.latitude,
    distribution_centers.longitude,
    distribution_centers.distribution_center_geom
  FROM
    `bigquery-public-data.thelook_ecommerce.products` AS products
  INNER JOIN
    `bigquery-public-data.thelook_ecommerce.distribution_centers` AS distribution_centers
  ON
    products.distribution_center_id = distribution_centers.id )
SELECT
  t1.distribution_centers_name AS name,
  t1.category
FROM
  CTE AS t1
GROUP BY
  1,
  2;
```

### Order Items and Product

6.1 Total sale volume by category where order status is Cancelled or Returned. sort by highest total_sale_volume
```
WITH CTE AS (
  SELECT
  products.id,
  products.cost,
  products.category,
  products.name,
  products.brand,
  products.retail_price,
  products.department,
  products.sku,
  products.distribution_center_id,
  order_items.id,
  order_items.order_id,
  order_items.user_id,
  order_items.product_id,
  order_items.inventory_item_id,
  order_items.status,
  order_items.created_at,
  order_items.shipped_at,
  order_items.delivered_at,
  order_items.returned_at,
  order_items.sale_price
FROM
  `bigquery-public-data.thelook_ecommerce.products` AS products
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
ON
  products.id = order_items.product_id
)
SELECT
  category,
  SUM(sale_price) AS total_sale_volume
FROM
  CTE AS t1
WHERE
  t1.status = 'Cancelled'
  OR t1.status = 'Returned'
GROUP BY
  1
ORDER BY
  total_sale_volume DESC;
```

6.2 product sales

```
WITH CTE AS (
  SELECT
  products.id,
  products.cost,
  products.category,
  products.name,
  products.brand,
  products.retail_price,
  products.department,
  products.sku,
  products.distribution_center_id,
  order_items.id,
  order_items.order_id,
  order_items.user_id,
  order_items.product_id,
  order_items.inventory_item_id,
  order_items.status,
  order_items.created_at,
  order_items.shipped_at,
  order_items.delivered_at,
  order_items.returned_at,
  order_items.sale_price
FROM
  `bigquery-public-data.thelook_ecommerce.products` AS products
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
ON
  products.id = order_items.product_id
)
SELECT
  t1.category,
  SUM(t1.sale_price) AS total_sales
FROM
  CTE AS t1
GROUP BY
  1;
```

6.3 brand total sale volume
```
WITH CTE AS (
  SELECT
  products.id,
  products.cost,
  products.category,
  products.name,
  products.brand,
  products.retail_price,
  products.department,
  products.sku,
  products.distribution_center_id,
  order_items.id,
  order_items.order_id,
  order_items.user_id,
  order_items.product_id,
  order_items.inventory_item_id,
  order_items.status,
  order_items.created_at,
  order_items.shipped_at,
  order_items.delivered_at,
  order_items.returned_at,
  order_items.sale_price
FROM
  `bigquery-public-data.thelook_ecommerce.products` AS products
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
ON
  products.id = order_items.product_id
)
SELECT
  t1.brand,
  SUM(t1.sale_price) AS total_sales
FROM
  CTE AS t1
GROUP BY
  1;
```

6.4 Analyze which product category have order sale volume and frequency
```
WITH CTE AS (
  SELECT
  products.id,
  products.cost,
  products.category,
  products.name,
  products.brand,
  products.retail_price,
  products.department,
  products.sku,
  products.distribution_center_id,
  order_items.id,
  order_items.order_id,
  order_items.user_id,
  order_items.product_id,
  order_items.inventory_item_id,
  order_items.status,
  order_items.created_at,
  order_items.shipped_at,
  order_items.delivered_at,
  order_items.returned_at,
  order_items.sale_price
FROM
  `bigquery-public-data.thelook_ecommerce.products` AS products
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
ON
  products.id = order_items.product_id
)
SELECT
  category,
  COUNT(DISTINCT order_id) AS order_count,
  SUM(sale_price) AS total_sale_volume
FROM
  CTE
GROUP BY
  1
ORDER BY
  order_count DESC;
```

### BigQuery ML

7.1 Train a boosted tree classifier model in BigQuery to predict product categories based on age, gender, city, country, and traffic source by creating a model with CREATE OR REPLACE MODEL, specifying the target column as category, splitting data randomly with 20% for evaluation, and selecting relevant features from the dataset while ensuring data types are consistent.

```
CREATE OR REPLACE MODEL
  `airflow-demo-437509._b9e0c16f3d4adbfc14369851e36362f2e91e8a7a.boosted_tree_model` OPTIONS ( model_type = 'BOOSTED_TREE_CLASSIFIER',
    data_split_method = 'RANDOM',
    data_split_eval_fraction = 0.2,
    input_label_cols = ['category'],
    max_iterations = 100) AS
SELECT
  CAST(age AS FLOAT64) AS age,
  CASE
    WHEN gender = 'F' THEN 1
    ELSE 0
END
  AS gender,
  city,
  country,
  traffic_source,
  category
FROM (
  SELECT
    status,
    shipped_at,
    delivered_at,
    returned_at,
    sale_price,
    cost,
    category,
    name,
    brand,
    retail_price,
    department,
    sku,
    first_name,
    last_name,
    email,
    age,
    gender,
    state,
    street_address,
    postal_code,
    city,
    country,
    latitude,
    longitude,
    traffic_source
  FROM
    `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
  INNER JOIN
    `bigquery-public-data.thelook_ecommerce.products` AS products
  ON
    order_items.product_id = products.id
  INNER JOIN
    `bigquery-public-data.thelook_ecommerce.users` AS users
  ON
    order_items.user_id = users.id
  WHERE
    status = 'Shipped' );
```

7.2 Evaluate Model Performance
```
WITH CTE AS (
SELECT
  status,
  shipped_at,
  delivered_at,
  returned_at,
  sale_price,
  cost,
  category,
  name,
  brand,
  retail_price,
  department,
  sku,
  first_name,
  last_name,
  email,
  age,
  gender,
  state,
  street_address,
  postal_code,
  city,
  country,
  latitude,
  longitude,
  traffic_source
  FROM
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.products` AS products
ON
  order_items.product_id = products.id
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.users` AS users
ON
  order_items.user_id = users.id
WHERE
  status = 'Shipped'
)

SELECT
  *
FROM
  ML.EVALUATE(
    MODEL `airflow-demo-437509._b9e0c16f3d4adbfc14369851e36362f2e91e8a7a.boosted_tree_model`,
    (
      SELECT
        CAST(age AS FLOAT64) AS age,
        CASE WHEN gender = 'F' THEN 1 ELSE 0 END AS gender,
        city,
        country,
        traffic_source,
        category
      FROM
        CTE
      WHERE
        category IS NOT NULL
    )
  );
```

Key Evaluation Metrics:

Accuracy: The proportion of correctly predicted instances among all instances. It reflects the overall effectiveness of the model but may be misleading in imbalanced datasets.

Precision: The ratio of true positive predictions to the total predicted positives. It indicates the model's ability to avoid false positives.

Recall (Sensitivity): The ratio of true positive predictions to all actual positives. It measures the model's capability to identify all relevant instances.

F1 Score: The harmonic mean of precision and recall. It provides a balance between precision and recall, especially useful when dealing with uneven class distributions.

Log Loss: Evaluates the uncertainty of predictions by comparing the predicted probabilities against the actual class labels. Lower values indicate better model performance.

ROC AUC (Receiver Operating Characteristic - Area Under Curve): Represents the model's ability to distinguish between classes across various threshold settings. A higher AUC indicates better discriminative performance.
7.3 Inference Query for Boosted Tree Model

```
WITH CTE AS (
SELECT
  status,
  shipped_at,
  delivered_at,
  returned_at,
  sale_price,
  cost,
  category,
  name,
  brand,
  retail_price,
  department,
  sku,
  first_name,
  last_name,
  email,
  age,
  gender,
  state,
  street_address,
  postal_code,
  city,
  country,
  latitude,
  longitude,
  traffic_source
  FROM
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.products` AS products
ON
  order_items.product_id = products.id
INNER JOIN
  `bigquery-public-data.thelook_ecommerce.users` AS users
ON
  order_items.user_id = users.id
WHERE
  status = 'Shipped'
)

SELECT
  *
FROM
  ML.EVALUATE(
    MODEL `airflow-demo-437509._b9e0c16f3d4adbfc14369851e36362f2e91e8a7a.boosted_tree_model`,
    (
      SELECT
        CAST(age AS FLOAT64) AS age,
        CASE WHEN gender = 'F' THEN 1 ELSE 0 END AS gender,
        city,
        country,
        traffic_source,
        category
      FROM
        CTE
      WHERE
        category IS NOT NULL
    )
  );
```