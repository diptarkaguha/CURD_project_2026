show databases;
create database curd_1_db; ---creation of DATABASE

--table created for the dataentry tab name::cust_details
use curd_1_db;
create table cust_details (
	cust_id int primary key auto_increment,
    full_name varchar(100) not null,
    address varchar(500) not null,
    ph_no bigint not null,
    user_id varchar(50) not null ,
    user_pwd varchar(255) not null,
    created_at timestamp default current_timestamp
);

----insert statement used in the python code
INSERT INTO cust_details (full_name,address,ph_no,user_id,user_pwd) VALUES (%s, %s, %s, %s, %s);


----select statement used in python code
select * from cust_details WHERE user_id='{user_id_login}';


---update script
UPDATE cust_details SET address=%s WHERE user_id=%s;
UPDATE cust_details SET ph_no=%s WHERE user_id=%s;
UPDATE cust_details SET user_pwd=%s WHERE user_id=%s;



----delete statement used in python
delete from cust_details where user_id='{user_id_login}';