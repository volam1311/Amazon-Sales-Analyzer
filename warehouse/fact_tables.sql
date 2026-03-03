CREATE TABLE IF NOT EXISTS fact_amazon_sales (
  fact_key BIGINT AUTO_INCREMENT PRIMARY KEY,

  product_key INT NOT NULL,
  user_key BIGINT NULL,
  review_key BIGINT NULL,

  discounted_price DECIMAL(12,2) NULL,
  actual_price DECIMAL(12,2) NULL,
  discounted_percentage DECIMAL(6,2) NULL,
  rating DECIMAL(4,2) NULL,
  rating_count INT NULL,

  CONSTRAINT fk_fact_product FOREIGN KEY (product_key) REFERENCES dim_products(product_key),
  CONSTRAINT fk_fact_user FOREIGN KEY (user_key) REFERENCES dim_users(user_key),
  CONSTRAINT fk_fact_review FOREIGN KEY (review_key) REFERENCES dim_reviews(review_key)
);
