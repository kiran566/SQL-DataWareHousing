/*
===============================================================================
Script: Direct Load All Bronze Layer Tables (MySQL)
===============================================================================
*/

USE dw_bronze;

-- Temporarily disable strict SQL mode to prevent warning escalation
SET SESSION sql_mode = '';

-- 1. Load CRM Customer Info
TRUNCATE TABLE crm_cust_info;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_crm/cust_info.csv'
INTO TABLE crm_cust_info
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(cst_id, cst_key, cst_firstname, cst_lastname, cst_marital_status, cst_gndr, cst_create_date);

-- 2. Load CRM Product Info
TRUNCATE TABLE crm_prd_info;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_crm/prd_info.csv'
INTO TABLE crm_prd_info
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(prd_id, prd_key, prd_nm, prd_cost, prd_line, prd_start_dt, prd_end_dt);

-- 3. Load CRM Sales Details
TRUNCATE TABLE crm_sales_details;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_crm/sales_details.csv'
INTO TABLE crm_sales_details
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(sls_ord_num, sls_prd_key, sls_cust_id, sls_order_dt, sls_ship_dt, sls_due_dt, sls_sales, sls_quantity, sls_price);

-- 4. Load ERP Location
TRUNCATE TABLE erp_loc_a101;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_erp/loc_a101.csv'
INTO TABLE erp_loc_a101
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(cid, cntry);

-- 5. Load ERP Customer
TRUNCATE TABLE erp_cust_az12;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_erp/cust_az12.csv'
INTO TABLE erp_cust_az12
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(cid, bdate, gen);

-- 6. Load ERP Product Category
TRUNCATE TABLE erp_px_cat_g1v2;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_erp/px_cat_g1v2.csv'
INTO TABLE erp_px_cat_g1v2
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id, cat, subcat, maintenance);


-- Verification: Check row counts across all Bronze tables


SELECT 'crm_cust_info' AS table_name, COUNT(*) AS record_count FROM dw_bronze.crm_cust_info
UNION ALL
SELECT 'crm_prd_info', COUNT(*) FROM dw_bronze.crm_prd_info
UNION ALL
SELECT 'crm_sales_details', COUNT(*) FROM dw_bronze.crm_sales_details
UNION ALL
SELECT 'erp_loc_a101', COUNT(*) FROM dw_bronze.erp_loc_a101
UNION ALL
SELECT 'erp_cust_az12', COUNT(*) FROM dw_bronze.erp_cust_az12
UNION ALL
SELECT 'erp_px_cat_g1v2', COUNT(*) FROM dw_bronze.erp_px_cat_g1v2;