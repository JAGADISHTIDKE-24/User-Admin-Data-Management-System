use vendor_portal;

desc implementation_DBR;
desc managed_services;

create table if not exists payee_support(
Timestamp date,
`Email Address` varchar(100),
Auxes varchar(50),
Queue varchar(50),
`Ticket Link` varchar(100),
Payer varchar(150),
Payee varchar(100),
`Ticket Origin Timestamp` varchar(100),
`Assigned Ticket Status` varchar(100),
Query varchar(100),
`Ticket History` varchar(100),
`Aphub Status` varchar(100),
`Payer Ticket` varchar(100),
`Account Located` varchar(100),
`Managed By` varchar(75),
`Zendesk User` varchar(90),
`DBR Timestamp` varchar(100) ,
Agent varchar(50),	
`Ticket Link 2` text,
Accuracy varchar(50),
Observations varchar(255),
`PST to IST` time,
`US Date` date,
`IND Date` date,
`IND Time` longtext,
`Agent 2` varchar(25),
Month varchar(10),
Week int ,
Hourly int);

select * from payee_support limit 10;
truncate table payee_support;