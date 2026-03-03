-- Products
INSERT INTO dim_products (product_id, product_name, category, about_product)
SELECT DISTINCT
  product_id, product_name, category, about_product
FROM amazon_products
WHERE product_id IS NOT NULL
ON DUPLICATE KEY UPDATE
  product_name = VALUES(product_name),
  category = VALUES(category),
  about_product = VALUES(about_product);

-- Users
INSERT INTO dim_users (user_id, user_name)
SELECT DISTINCT
  user_id, user_name
FROM amazon_products
WHERE user_id IS NOT NULL
ON DUPLICATE KEY UPDATE
  user_name = VALUES(user_name);

-- Reviews
INSERT INTO dim_reviews (review_id, review_title, review_content)
SELECT DISTINCT
  review_id, review_title, review_content
FROM amazon_products
WHERE review_id IS NOT NULL
ON DUPLICATE KEY UPDATE
  review_title = VALUES(review_title),
  review_content = VALUES(review_content);
