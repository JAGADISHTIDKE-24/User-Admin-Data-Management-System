use vendor_portal;

show tables;
SET SQL_SAFE_UPDATES = 0;

CREATE TABLE IF NOT EXISTS payee_support_quality (
  `Timestamp` DATETIME,
  `Email Address` VARCHAR(200),
  `Agent Name` VARCHAR(200),
  `Payer` VARCHAR(100),
  `Ticket Link` VARCHAR(100),
  `Queue` VARCHAR(70),
  `Assigned Ticket Status` VARCHAR(40),
  `Agent Solved` VARCHAR(20),
  `Solved Opportunity` INT,
  `Incorrect Info` INT,
  `Incomplete Info` INT,
  `FCR` INT,
  `DBR Tagging` INT,
  `Grammatical Errors` INT,
  `Apology / Sympathy` INT,
  `Opening / Closing` INT,
  `Fatal` VARCHAR(20),
  `Fatal Parameters` VARCHAR(20),
  `Query` VARCHAR(50),
  `Comments` TEXT
);


desc payee_support_quality;
select * from payee_support_quality limit 10;
select count(*) as total_count from payee_support_quality;
truncate table payee_support_quality;