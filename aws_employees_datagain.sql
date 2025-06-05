use vendor_portal;

create table if not exists employees(
employee_id	int(11),
employee_name	varchar(25),
email	varchar(25),
role	varchar(25),
password	varchar(25),
department	varchar(50));
select * from employees;
desc employees;