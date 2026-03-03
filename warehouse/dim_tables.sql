CREATE TABLE IF NOT EXISTS dim_products (
  product_key INT AUTO_INCREMENT PRIMARY KEY,
  product_id VARCHAR(100) NOT NULL,
  product_name TEXT,
  category VARCHAR(255),
  about_product TEXT,
  UNIQUE KEY uq_dim_products_product_id (product_id)
);

CREATE TABLE IF NOT EXISTS dim_users (
  user_key BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  user_name TEXT,
  UNIQUE KEY uq_dim_users_user_id (user_id)
);

CREATE TABLE IF NOT EXISTS dim_reviews (
  review_key BIGINT AUTO_INCREMENT PRIMARY KEY,
  review_id VARCHAR(255) NOT NULL,
  review_title TEXT,
  review_content TEXT,
  UNIQUE KEY uq_dim_reviews_review_id (review_id)
);


