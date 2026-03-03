INSERT INTO fact_amazon_sales (
  product_key,
  user_key,
  review_key,
  discount_price,
  actual_price,
  discount_percentage,
  rating,
  rating_count
)
SELECT
  p.product_key,
  u.user_key,
  r.review_key,
  ap.discounted_price,
  ap.actual_price,
  ap.discount_percentage,
  ap.rating,
  ap.rating_count
FROM amazon_products ap
JOIN dim_products p
  ON ap.product_id = p.product_id
LEFT JOIN dim_users u
  ON ap.user_id = u.user_id
LEFT JOIN dim_reviews r
  ON ap.review_id = r.review_id;