-- ====================================================================
-- PHASE 1: DATABASE SETUP
-- ====================================================================

-- Create databases for each layer of the Medallion Architecture
-- WE ARE IMPLEMETING FULL LOAD THAT WHY WE ARE DROPIN IF DB ALREADY PRESENT-

-- FOR BRONZE LAYER--- DATA INGESTION FORM SOURCE
DROP DATABASE IF EXISTS DataWarehouse_Bronze;
CREATE DATABASE DataWarehouse_Bronze;


 --  FOR SILVER LAYER --- DATA PREPROCESSING
DROP DATABASE IF EXISTS DataWarehouse_Silver;
CREATE DATABASE DataWarehouse_Silver;

-- GOLD LAYER -- DATA WAREHOUSING (BI)
DROP DATABASE IF EXISTS DataWarehouse_Gold;
CREATE DATABASE DataWarehouse_Gold;

SHOW DATABASES;
