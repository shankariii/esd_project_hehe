create schema payment_log;

-- drop schema payment_log;

use payment_log;

create table payment_log
(payment_log_id int not null auto_increment,
user_id int not null ,
order_id int not null,
amount float not null,
-- currency varchar(15) not null,
payment_method varchar(20) not null,
transaction_id varchar(15) unique not null,
payment_status varchar(20) not null,
created_at timestamp default current_timestamp,
constraint payment_log_id_pk primary key (payment_log_id));

insert into payment_log (user_id, order_id, amount, payment_method, transaction_id, payment_status, created_at) 
values 
(1, 1001, 10,'Credit Card', 'TXN123456', 'Completed', NOW()),
(2, 1002, 15,'PayPal', 'TXN123457', 'Pending', NOW()),
(3, 1003, 20,'Debit Card', 'TXN123458', 'Failed', NOW()),
(4, 1004, 30,'Google Pay', 'TXN123459', 'Completed', NOW()),
(5, 1005, 25,'Apple Pay', 'TXN123460', 'Refunded', NOW());
-- (1, 1001, 10, 'USD', 'Credit Card', 'TXN123456', 'Completed', NOW()),
-- (2, 1002, 15, 'USD', 'PayPal', 'TXN123457', 'Pending', NOW()),
-- (3, 1003, 20, 'EUR', 'Debit Card', 'TXN123458', 'Failed', NOW()),
-- (4, 1004, 30, 'GBP', 'Google Pay', 'TXN123459', 'Completed', NOW()),
-- (5, 1005, 25, 'USD', 'Apple Pay', 'TXN123460', 'Refunded', NOW());

select * from payment_log