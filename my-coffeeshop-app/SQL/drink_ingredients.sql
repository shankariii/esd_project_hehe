create schema drink_ingredients;

-- drop schema drink_ingredients;

use drink_ingredients;

create table drink_ingredients
(drink_ingredient_id int not null auto_increment,
drink_id int not null ,
ingredient varchar(255) not null,
quantity int not null,
unit varchar(15) not null,
constraint drink_ingredient_id_pk primary key (drink_ingredient_id));

insert into drink_ingredients (drink_ingredient_id, drink_id, ingredient, quantity, unit)
values 
	(1, 1, "Caramel Syrup", 2, 'ounces'),
	(2, 2, "Regular Milk", 100, 'ml');
    

select * from drink_ingredients;