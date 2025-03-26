create schema drink_menu;

-- drop schema drink_menu;

use drink_menu;

create table drink_menu
(drink_id int not null auto_increment,
drink_name varchar(50) not null,
description varchar(255) not null,
price decimal(5, 2) not null,
image varchar(255),
prep_time_min decimal(5,2) not null,
available varchar(10) not null,
constraint drink_id_pk primary key (drink_id));
    
insert into drink_menu (drink_id, drink_name, description, price, image, prep_time_min, available)
values 
	(1, 'Espresso', 'A bold and concentrated shot of rich, aromatic coffee, perfect for those who love a strong caffeine kick.', 3.00, '/static/images/espresso.jpg', 2, 'Yes'),
	(2, 'Latte', 'Smooth and creamy, this espresso-based drink is blended with steamed milk and topped with a light layer of foam for a balanced, velvety taste.', 4.50, '/static/images/latte.webp', 4, 'Yes'),
    (3, 'Cappuccino', 'A classic favorite with equal parts espresso, steamed milk, and frothy foam, delivering a rich, robust flavor with a light, airy texture.', 4.00, '/static/images/cappuccino.jpg', 6, 'Yes'),
    (4, 'Americano', 'A simple yet satisfying mix of espresso and hot water, creating a smooth, mellow coffee with a slightly lighter body than a traditional espresso.', 5.50, '/static/images/americano.jpg', 1, 'Yes');
    
    
select * from drink_menu;