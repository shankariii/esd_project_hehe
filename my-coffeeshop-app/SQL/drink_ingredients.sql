DROP SCHEMA IF EXISTS drink_ingredients;

create schema drink_ingredients;

use drink_ingredients;

create table drink_ingredients
(drink_ingredient_id int not null,
drink_id int,
ingredient varchar(255) not null,
quantity int not null,
unit varchar(15) not null,
constraint drink_ingredient_id_pk primary key (drink_ingredient_id));

insert into drink_ingredients (drink_ingredient_id, drink_id, ingredient, quantity, unit)
values 
	-- Espresso (Drink ID 1)
    (16, 1, 'Coffee Beans', 10, 'g'),

    -- Latte (Drink ID 2)
    (16, 2, 'Coffee Beans', 1, 'shot'),

    -- Cappuccino (Drink ID 3)
    (16, 3, 'Coffee Beans', 1, 'shot'),

    -- Americano (Drink ID 4)
	(16, 4, 'Coffee Beans', 10, 'g'),

    -- Iced Matcha Latte (Drink ID 5)
    (24, 5, 'Matcha Powder', 5, 'g'),
	(20, 5, 'Sugar Syrup', 1, 'tbsp'),

    -- Iced Chocolate (Drink ID 6)
    (26, 6, 'Chocolate Syrup', 2, 'tbsp'),

	-- no drink ids
	(104, NULL, 'Regular Milk', 200, 'ml'),
	(105, NULL, 'Skim Milk', 200, 'ml'),
	(106, NULL, 'Almond Milk', 200, 'ml'),
	(107, NULL, 'Oat Milk', 200, 'ml'),
	(108, NULL, 'Soy Milk', 200, 'ml'),
	(109, NULL, 'Vanilla Syrup', 2, 'tbsp'),
	(110, NULL, 'Caramel Syrup', 2, 'tbsp'),
	(111, NULL, 'Hazelnut Syrup', 2, 'tbsp'),
	(112, NULL, 'Whipped Cream', 20, 'g'),
	(113, NULL, 'Chocolate Sprinkles', 4, 'g');
    

select * from drink_ingredients;