CREATE TABLE Amazon_sales AS
SELECT 
	product_id,
    discounted_price,
    actual_price
    discounted_percentage,
    rating,
    rating_count,
    user_id,
    review_id
FROM amazon_products;