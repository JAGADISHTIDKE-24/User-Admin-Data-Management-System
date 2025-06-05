USE VENDOR_PORTAL;
SET SQL_SAFE_UPDATES = 0;

create table  if not exists `implementation DBR`(
Timestamp DATE,
Task VARCHAR(100),
`QA Type` VARCHAR(100),
Deal VARCHAR(50),
`Request Type` VARCHAR(50),
IM VARCHAR(100),
`Rocketlane Name` TEXT ,
Location VARCHAR(100),
`Go Live Date` DATE,
`Received Date` DATE,
QA_Status varchar(50),	
Errors TEXT,
QA_Comments longtext,
Instance_Opportunity TEXT,
Instance_Payer varchar(50),
Instance_Status VARCHAR(30),
Currency VARCHAR(200),	
Instance_Comments varchar(200),
`Addon Entity`VARCHAR(100),
Addon_Payer VARCHAR(200),
Addon_Status VARCHAR(100),
Addon_Comments varchar(100),
GC_Payer VARCHAR(100),
GC_EMail TEXT,
`GC+Status` VARCHAR(100),
Defects INT(10),
`Email Address` VARCHAR(100) ,
`Salesforce Name` TEXT,
`OCR Vendor` VARCHAR(100),
`Deal Type` VARCHAR(100)
); 
DESC implementation_DBR;
select count(*) from implementation_DBR;
truncate table implementation_DBR;
select * from implementation_DBR;