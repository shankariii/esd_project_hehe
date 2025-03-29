create schema customisation;

-- drop schema customisation;

use customisation;

create table customisation
(customisation_id int not null,
customisation_type varchar(10) not null,
name varchar(32) not null, 
price_diff decimal(4, 2) not null,
constraint customisation_id_pk primary key (customisation_id));

    
insert into customisation (customisation_id, customisation_type, name, price_diff)
values 
	(1, "S", "Small", 0.00),
	(2, "S", "Medium", 0.50),
	(3, "S", "Large", 0.80),
	(4, "M", "Regular", 0.00),
	(5, "M", "Skim", 0.00),
	(6, "M", "Almond", 0.75),
	(7, "M", "Oat", 0.75),
	(8, "M", "Soy", 0.75),
	(9, "A", "Vanilla Syrup", 0.50),
	(10, "A", "Caramel Syrup", 0.50),
	(11, "A", "Hazelnut Syrup", 0.50),
	(12, "A", "Whipped Cream", 0.50),
	(13, "A", "Chocolate Sprinkles", 0.25);


select * from customisation;