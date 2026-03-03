CREATE TABLE DIM_Products AS
SELECT 
	product_id,
    product_name,
    category,
    about_product,
    img_link,
    product_link
FROM amazon_products;

CREATE TABLE DIM_Reviews AS
SELECT
	review_id,
    review_title,
    review_content
FROM amazon_products;

CREATE TABLE DIM_Users AS
SELECT
	user_id,
    user_name
FROM amazon_products;