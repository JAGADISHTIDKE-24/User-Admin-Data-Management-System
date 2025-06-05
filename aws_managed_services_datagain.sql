use vendor_portal;

SET SQL_SAFE_UPDATES = 0;

show tables;
truncate table managed_services;

# dummy table
select * from managed_service;

create table if not exists managed_services(
timestamp	date,
`Email Address`	varchar(255),
ocr	varchar(25),
`bill ref code`	varchar(200),
`track id`	varchar(200),
`Annotation ID`	longtext,
`document type`	varchar(100),
`matched payee id`	varchar(200),
`payer`	varchar(255),
`review`	varchar(10),
`Bill lines`	int(11),
`payee name`	text,
`invoice`	bigint(20),
`Invoice Date`	longtext,
`Invoice Due Date`	longtext,
`terms`	text,
po	text,
`tax amt`	decimal(10,2),
`total amt`	decimal(10,2),
currency	varchar(10),
`foreign language`	varchar(15),
`Quality analyst`	varchar(50),
`invoice pages`	int(11),
`Multiple payees`	varchar(15),
Comments	longtext,
`pst to ist`	time,
`us date`	date,
`ind date`	date,
`IND Time`	longtext,
team	text,
Agent	varchar(20),
`Unique id`	tinytext,
priority	varchar(50),
month	varchar(25),
hour	int(11),
EMEA	varchar(25));

desc managed_services;
select * from managed_services limit 10;
select count(*) as total_count from managed_services;