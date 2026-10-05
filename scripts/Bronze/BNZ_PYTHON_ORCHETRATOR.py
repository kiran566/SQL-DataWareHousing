import mysql.connector
import logging
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "0714",
    "database": "datawarehouse_bronze"
}


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )


# ============================================================
# START AUDIT RECORD
# ============================================================

def start_audit(cursor, table_name):

    cursor.execute("""
        INSERT INTO etl_load_log
        (
            table_name,
            load_type,
            start_time,
            status
        )
        VALUES (%s, %s, %s, %s)
    """, (
        table_name,
        "FULL",
        datetime.now(),
        "STARTED"
    ))

    return cursor.lastrowid


# ============================================================
# MARK AUDIT SUCCESS
# ============================================================

def mark_success(cursor, load_id, rows_loaded):

    cursor.execute("""
        UPDATE etl_load_log
        SET
            end_time = %s,
            rows_loaded = %s,
            status = %s
        WHERE load_id = %s
    """, (
        datetime.now(),
        rows_loaded,
        "SUCCESS",
        load_id
    ))


# ============================================================
# MARK AUDIT FAILURE
# ============================================================

def mark_failed(cursor, load_id, error_message):

    cursor.execute("""
        UPDATE etl_load_log
        SET
            end_time = %s,
            status = %s,
            error_message = %s
        WHERE load_id = %s
    """, (
        datetime.now(),
        "FAILED",
        str(error_message),
        load_id
    ))


# ============================================================
# LOAD ONE BRONZE TABLE
# ============================================================

def load_table(cursor, table_name, load_sql):

    load_id = start_audit(cursor, table_name)

    logger.info(f"Starting FULL load: {table_name}")

    try:

        # ----------------------------------------------------
        # Step 1: Remove previous Bronze data
        # ----------------------------------------------------

        cursor.execute(
            f"TRUNCATE TABLE {table_name}"
        )

        logger.info(
            f"Truncated table: {table_name}"
        )

        # ----------------------------------------------------
        # Step 2: Load source CSV
        # ----------------------------------------------------

        cursor.execute(load_sql)

        # ----------------------------------------------------
        # Step 3: Validate row count
        # ----------------------------------------------------

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        rows_loaded = cursor.fetchone()[0]

        # ----------------------------------------------------
        # Step 4: Update audit table
        # ----------------------------------------------------

        mark_success(
            cursor,
            load_id,
            rows_loaded
        )

        logger.info(
            f"Completed FULL load: "
            f"{table_name} | rows={rows_loaded}"
        )

        return True

    except Exception as e:

        mark_failed(
            cursor,
            load_id,
            e
        )

        logger.error(
            f"FAILED: {table_name} | error={e}"
        )

        raise


# ============================================================
# 1. CRM CUSTOMER INFO
# ============================================================

CRM_CUSTOMER_LOAD = """
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_crm/cust_info.csv'
INTO TABLE crm_cust_info
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
(
    @cst_id,
    cst_key,
    cst_firstname,
    cst_lastname,
    cst_marital_status,
    cst_gndr,
    @cst_create_date
)
SET
    cst_id = NULLIF(@cst_id, ''),
    cst_create_date = NULLIF(@cst_create_date, '')
"""


# ============================================================
# 2. CRM PRODUCT INFO
# ============================================================

CRM_PRODUCT_LOAD = """
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_crm/prd_info.csv'
INTO TABLE crm_prd_info
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
(
    @prd_id,
    prd_key,
    prd_nm,
    @prd_cost,
    prd_line,
    @prd_start_dt,
    @prd_end_dt
)
SET
    prd_id = NULLIF(@prd_id, ''),
    prd_cost = NULLIF(@prd_cost, ''),
    prd_start_dt = NULLIF(@prd_start_dt, ''),
    prd_end_dt = NULLIF(@prd_end_dt, '')
"""


# ============================================================
# 3. CRM SALES DETAILS
# ============================================================

CRM_SALES_LOAD = """
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_crm/sales_details.csv'
INTO TABLE crm_sales_details
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
(
    sls_ord_num,
    sls_prd_key,
    @sls_cust_id,
    @sls_order_dt,
    @sls_ship_dt,
    @sls_due_dt,
    @sls_sales,
    @sls_quantity,
    @sls_price
)
SET
    sls_cust_id = NULLIF(@sls_cust_id, ''),
    sls_order_dt = NULLIF(@sls_order_dt, ''),
    sls_ship_dt = NULLIF(@sls_ship_dt, ''),
    sls_due_dt = NULLIF(@sls_due_dt, ''),
    sls_sales = NULLIF(@sls_sales, ''),
    sls_quantity = NULLIF(@sls_quantity, ''),
    sls_price = NULLIF(@sls_price, '')
"""


# ============================================================
# 4. ERP LOCATION
# ============================================================

ERP_LOCATION_LOAD = """
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_erp/loc_a101.csv'
INTO TABLE erp_loc_a101
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
(
    cid,
    cntry
)
"""


# ============================================================
# 5. ERP CUSTOMER
# ============================================================

ERP_CUSTOMER_LOAD = """
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_erp/cust_az12.csv'
INTO TABLE erp_cust_az12
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 LINES
(
    cid,
    @bdate,
    @gen
)
SET
    bdate = NULLIF(@bdate, ''),
    gen = NULLIF(@gen, '')
"""


# ============================================================
# 6. ERP PRODUCT CATEGORY
# ============================================================

ERP_CATEGORY_LOAD = """
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/datasets/source_erp/px_cat_g1v2.csv'
INTO TABLE erp_px_cat_g1v2
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
(
    id,
    cat,
    subcat,
    maintenance
)
"""


# ============================================================
# BRONZE ETL ORCHESTRATOR
# ============================================================

def main():

    conn = None
    cursor = None

    try:

        logger.info("==============================================")
        logger.info("Starting Bronze Data Ingestion")
        logger.info("==============================================")

        # ----------------------------------------------------
        # Connect to MySQL
        # ----------------------------------------------------

        conn = get_connection()

        cursor = conn.cursor()

        logger.info(
            "Connected to MySQL successfully"
        )

        # ====================================================
        # CRM
        # ====================================================

        load_table(
            cursor,
            "crm_cust_info",
            CRM_CUSTOMER_LOAD
        )

        conn.commit()


        load_table(
            cursor,
            "crm_prd_info",
            CRM_PRODUCT_LOAD
        )

        conn.commit()


        load_table(
            cursor,
            "crm_sales_details",
            CRM_SALES_LOAD
        )

        conn.commit()


        # ====================================================
        # ERP
        # ====================================================

        load_table(
            cursor,
            "erp_loc_a101",
            ERP_LOCATION_LOAD
        )

        conn.commit()


        load_table(
            cursor,
            "erp_cust_az12",
            ERP_CUSTOMER_LOAD
        )

        conn.commit()


        load_table(
            cursor,
            "erp_px_cat_g1v2",
            ERP_CATEGORY_LOAD
        )

        conn.commit()


        # ====================================================
        # FINAL SUCCESS
        # ====================================================

        logger.info("==============================================")
        logger.info("Bronze Data Ingestion Completed Successfully")
        logger.info("==============================================")


    except Exception as e:

        logger.error(
            f"Bronze ETL failed: {e}"
        )

        if conn:
            conn.rollback()


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        logger.info(
            "MySQL connection closed"
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()