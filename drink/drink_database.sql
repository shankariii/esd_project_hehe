create schema drink;

-- drop schema drink;

use drink;

create table drink_ingredients
(drink_ingredient_id int not null auto_increment,
drink_id int not null ,
ingredient_id int not null,
quantity int not null,
unit varchar(15) not null,
constraint drink_ingredient_id_pk primary key (drink_ingredient_id),
constraint drink_id_fk foreign key (drink_id) references drink_menu(drink_id));

create table drink_menu
(drink_id int not null auto_increment,
drink_name varchar(50) not null,
description varchar(255) not null,
price decimal(5, 2) not null,
image varchar(255),
prep_time_min decimal(5,2) not null,
constraint drink_id_pk primary key (drink_id));

create table customisation
(customisation_id int not null,
customisation_type varchar(10) not null,
name varchar(32) not null, 
price_diff decimal(4, 2) not null,
constraint customisation_id_pk primary key (customisation_id));

insert into drink_ingredients (drink_ingredient_id, drink_id, ingredient_id, quantity, unit)
values 
	(1, 1, 3, 2, 'ounces'),
	(2, 2, 4, 100, 'ml');
    
insert into drink_menu (drink_id, drink_name, description, price, image, prep_time_min)
values 
	(1, 'Espresso', 'A bold and concentrated shot of rich, aromatic coffee, perfect for those who love a strong caffeine kick.', 3.00, '/static/images/espresso.jpg', 2),
	(2, 'Latte', 'Smooth and creamy, this espresso-based drink is blended with steamed milk and topped with a light layer of foam for a balanced, velvety taste.', 4.50, '/static/images/latte.webp', 4),
    (3, 'Cappuccino', 'A classic favorite with equal parts espresso, steamed milk, and frothy foam, delivering a rich, robust flavor with a light, airy texture.', 4.00, '/static/images/cappuccino.jpg', 6),
    (4, 'Americano', 'A simple yet satisfying mix of espresso and hot water, creating a smooth, mellow coffee with a slightly lighter body than a traditional espresso.', 5.50, '/static/images/americano.jpg', 1);
    
insert into customisation (customisation_id, customisation_type, name, price_diff)
values 
	(1, 'S', 'Small', 0),
	(2, 'M', 'Oat Milk', 0.5),
    (3, 'S', 'Medium', 0.8),
    (4, 'A', 'Extra Shot', 1.0),
    (5, 'M', 'Normal Milk', 0);
    
select * from drink_ingredients;
select * from drink_menu;
select * from customisation;