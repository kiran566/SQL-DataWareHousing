
-- Create Databases for Architecture (MySQL)
-- ===================================================
-- Script Purpose:
--     This script sets up three databases representing the medallion
--     architecture layers: 'DataWarehouse_bronze', 'DataWarehouse_silver', 
--     and 'DataWarehouse_gold'. If they already exist, they are dropped 
--     and recreated from scratch.
-- bronze layer ingestion from source
 
drop database if exists dw_bronze;
create database dw_bronze;

-- silver layer for trsnsformation 

drop database if exists dw_silver;
create database dw_silver;

-- gold layer for actual bi data 
drop database if exists dw_gold;
create database dw_gold;


show  databases;