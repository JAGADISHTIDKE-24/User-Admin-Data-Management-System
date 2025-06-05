use vendor_portal;

create table if not exists audit_logs(
login_id	int(11),
user_email	varchar(255),
name	varchar(255),
role	enum('admin','user'),
action	enum('login','logout'),
login_time	datetime,
logout_time	datetime);

desc audit_logs;