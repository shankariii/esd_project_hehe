CREATE DATABASE IF NOT EXISTS `inventory` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `inventory`;

DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    ingredient VARCHAR(64) NOT NULL,
    available_quantity FLOAT(10,2) NOT NULL,
    unit VARCHAR(32) NOT NULL,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    change_in_quantity FLOAT(10,2) DEFAULT 0.00
);

INSERT INTO inventory (ingredient, available_quantity, unit, date_time, change_in_quantity) VALUES

    # Coffee Beans w restock
    ('Coffee Beans', 1200.0, 'g', '2025-03-28 07:00:00', -50.0),  # Morning batch brew
    ('Coffee Beans', 1150.0, 'g', '2025-03-28 10:00:00', -35.0),  # Mid-morning orders
    ('Coffee Beans', 1115.0, 'g', '2025-03-28 13:00:00', -45.0),  # Lunch rush
    ('Coffee Beans', 1070.0, 'g', '2025-03-28 16:00:00', -25.0),  # Afternoon lull
    ('Coffee Beans', 1045.0, 'g', '2025-03-29 08:00:00', -60.0),  # Weekend morning rush
    ('Coffee Beans', 985.0, 'g', '2025-03-29 12:00:00', -55.0),  # Weekend lunch
    ('Coffee Beans', 930.0, 'g', '2025-03-29 17:00:00', -30.0),  # Late afternoon
    ('Coffee Beans', 900.0, 'g', '2025-03-30 09:00:00', -40.0),  # Sunday morning
    ('Coffee Beans', 860.0, 'g', '2025-03-30 13:00:00', -35.0),  # Sunday lunch
    ('Coffee Beans', 825.0, 'g', '2025-03-31 07:30:00', -50.0),  # Monday morning
    ('Coffee Beans', 775.0, 'g', '2025-03-31 11:00:00', -40.0),  # Mid-morning
    ('Coffee Beans', 735.0, 'g', '2025-04-01 08:30:00', -45.0),  # Tuesday morning
    ('Coffee Beans', 690.0, 'g', '2025-04-01 12:30:00', -30.0),  # Lunch
    ('Coffee Beans', 660.0, 'g', '2025-04-02 09:30:00', -35.0),  # Wednesday morning
    ('Coffee Beans', 625.0, 'g', '2025-04-02 14:30:00', -25.0),  # Afternoon
    ('Coffee Beans', 1525.0, 'g', '2025-04-03 07:45:00', 900.0),  # **RESTOCK!**
    ('Coffee Beans', 1485.0, 'g', '2025-04-03 11:30:00', -40.0),  # Mid-morning
    ('Coffee Beans', 1425.0, 'g', '2025-04-04 07:15:00', -55.0),  # Friday morning

    #Regular Milk need restock
    ('Regular Milk', 4300.0, 'ml', '2025-03-29 11:00:00', -200.0),
    ('Regular Milk', 4100.0, 'ml', '2025-03-30 07:00:00', -150.0),
    ('Regular Milk', 3950.0, 'ml', '2025-03-30 18:00:00', -100.0),
    ('Regular Milk', 3850.0, 'ml', '2025-03-31 10:00:00', -250.0),
    ('Regular Milk', 3600.0, 'ml', '2025-04-01 14:00:00', -100.0),
    ('Regular Milk', 3500.0, 'ml', '2025-04-02 08:00:00', -100.0),
    ('Regular Milk', 3400.0, 'ml', '2025-04-03 10:00:00', -200.0),
    ('Regular Milk', 3200.0, 'ml', '2025-04-04 07:35:00', -200.0),
    ('Regular Milk', 3000.0, 'ml', '2025-04-04 07:56:00', -200.0),

    # Chocolate Sprinkles 
    ('Chocolate Sprinkles', 250.0, 'g', '2025-03-28 14:00:00', -2.0),
    ('Chocolate Sprinkles', 248.0, 'g', '2025-03-29 10:30:00', -3.0),
    ('Chocolate Sprinkles', 245.0, 'g', '2025-03-29 16:45:00', -1.0),
    ('Chocolate Sprinkles', 244.0, 'g', '2025-03-30 12:15:00', -5.0),
    ('Chocolate Sprinkles', 239.0, 'g', '2025-03-31 09:45:00', -2.0),
    ('Chocolate Sprinkles', 237.0, 'g', '2025-04-01 11:00:00', -3.0),
    ('Chocolate Sprinkles', 234.0, 'g', '2025-04-02 15:30:00', -1.0),
    ('Chocolate Sprinkles', 233.0, 'g', '2025-04-03 13:00:00', -4.0),
    ('Chocolate Sprinkles', 229.0, 'g', '2025-04-04 07:40:00', -1.0),

    # Caramel Syrup need restock
    ('Caramel Syrup', 1500.0, 'ml', '2025-03-29 13:45:00', -50.0),
    ('Caramel Syrup', 1450.0, 'ml', '2025-03-30 09:15:00', -75.0),
    ('Caramel Syrup', 1375.0, 'ml', '2025-03-30 19:30:00', -25.0),
    ('Caramel Syrup', 1350.0, 'ml', '2025-03-31 14:45:00', -100.0),
    ('Caramel Syrup', 1250.0, 'ml', '2025-04-01 16:00:00', -60.0),
    ('Caramel Syrup', 1190.0, 'ml', '2025-04-02 10:15:00', -40.0),
    ('Caramel Syrup', 1150.0, 'ml', '2025-04-03 11:30:00', -80.0),
    ('Caramel Syrup', 1070.0, 'ml', '2025-04-04 07:45:00', -30.0),
    ('Caramel Syrup', 1040.0, 'ml', '2025-04-04 08:00:00', -10.0);

    # Matcha Powder
    ('Matcha Powder', 1000.0, 'g', '2025-03-29 07:15:00', -5.0),
    ('Matcha Powder', 995.0, 'g', '2025-03-29 18:30:00', -15.0),
    ('Matcha Powder', 980.0, 'g', '2025-03-30 08:00:00', -25.0),
    ('Matcha Powder', 955.0, 'g', '2025-03-30 12:30:00', -25.0),
    ('Matcha Powder', 930.0, 'g', '2025-03-31 11:15:00', -10.0),
    ('Matcha Powder', 920.0, 'g', '2025-04-01 16:00:00', -5.0),
    ('Matcha Powder', 915.0, 'g', '2025-04-02 09:00:00', -40.0),
    ('Matcha Powder', 875.0, 'g', '2025-04-03 13:00:00', -5.0),
    ('Matcha Powder', 870.0, 'g', '2025-04-04 15:15:00', -5.0),
    ('Matcha Powder', 865.0, 'g', '2025-04-05 08:00:00', -10.0),
    ('Matcha Powder', 855.0, 'g', '2025-04-05 19:15:00', -10.0);

    # Sugar Syrup
    ('Sugar Syrup', 3000.0, 'ml', '2025-03-29 07:45:00', -100.0),
    ('Sugar Syrup', 2900.0, 'ml', '2025-03-30 12:30:00', -120.0),
    ('Sugar Syrup', 2780.0, 'ml', '2025-03-31 16:45:00', -90.0),
    ('Sugar Syrup', 2690.0, 'ml', '2025-04-01 08:15:00', -110.0),
    ('Sugar Syrup', 2580.0, 'ml', '2025-04-02 14:00:00', -150.0),
    ('Sugar Syrup', 2430.0, 'ml', '2025-04-03 10:30:00', -80.0),
    ('Sugar Syrup', 2350.0, 'ml', '2025-04-04 18:45:00', -60.0),
    ('Sugar Syrup', 2290.0, 'ml', '2025-04-05 09:30:00', -70.0),
    ('Sugar Syrup', 2220.0, 'ml', '2025-04-05 15:15:00', -90.0);

    # Chocolate Syrup
    ('Chocolate Syrup', 2000.0, 'ml', '2025-03-29 08:30:00', -60.0),
    ('Chocolate Syrup', 1940.0, 'ml', '2025-03-30 10:45:00', -80.0),
    ('Chocolate Syrup', 1860.0, 'ml', '2025-03-31 15:00:00', -90.0),
    ('Chocolate Syrup', 1770.0, 'ml', '2025-04-01 09:00:00', -70.0),
    ('Chocolate Syrup', 1700.0, 'ml', '2025-04-02 11:15:00', -50.0),
    ('Chocolate Syrup', 1650.0, 'ml', '2025-04-03 13:45:00', -100.0),
    ('Chocolate Syrup', 1550.0, 'ml', '2025-04-04 17:30:00', -40.0),
    ('Chocolate Syrup', 1510.0, 'ml', '2025-04-05 07:15:00', -20.0),
    ('Chocolate Syrup', 1490.0, 'ml', '2025-04-05 18:00:00', -30.0);

    # Skim Milk
    ('Skim Milk', 3000.0, 'ml', '2025-03-29 09:00:00', -150.0),
    ('Skim Milk', 2850.0, 'ml', '2025-03-30 08:45:00', -200.0),
    ('Skim Milk', 2650.0, 'ml', '2025-03-30 17:30:00', -100.0),
    ('Skim Milk', 2550.0, 'ml', '2025-03-31 11:30:00', -180.0),
    ('Skim Milk', 2370.0, 'ml', '2025-04-01 13:15:00', -120.0),
    ('Skim Milk', 2250.0, 'ml', '2025-04-02 09:30:00', -100.0),
    ('Skim Milk', 2150.0, 'ml', '2025-04-03 11:00:00', -150.0),
    ('Skim Milk', 2000.0, 'ml', '2025-04-04 08:15:00', -150.0),
    ('Skim Milk', 1850.0, 'ml', '2025-04-04 08:45:00', -100.0);

    # Almond Milk
    ('Almond Milk', 2500.0, 'ml', '2025-03-29 10:30:00', -100.0),
    ('Almond Milk', 2400.0, 'ml', '2025-03-30 09:00:00', -120.0),
    ('Almond Milk', 2280.0, 'ml', '2025-03-30 16:15:00', -80.0),
    ('Almond Milk', 2200.0, 'ml', '2025-03-31 12:00:00', -150.0),
    ('Almond Milk', 2050.0, 'ml', '2025-04-01 14:45:00', -100.0),
    ('Almond Milk', 1950.0, 'ml', '2025-04-02 07:30:00', -90.0),
    ('Almond Milk', 1860.0, 'ml', '2025-04-03 10:45:00', -110.0),
    ('Almond Milk', 1750.0, 'ml', '2025-04-04 08:20:00', -130.0),
    ('Almond Milk', 1620.0, 'ml', '2025-04-04 17:50:00', -70.0);

    # Oat Milk
    ('Oat Milk', 2800.0, 'ml', '2025-03-29 07:30:00', -100.0),
    ('Oat Milk', 2700.0, 'ml', '2025-03-30 11:00:00', -120.0),
    ('Oat Milk', 2580.0, 'ml', '2025-03-30 15:30:00', -90.0),
    ('Oat Milk', 2490.0, 'ml', '2025-03-31 09:45:00', -140.0),
    ('Oat Milk', 2350.0, 'ml', '2025-04-01 13:30:00', -100.0),
    ('Oat Milk', 2250.0, 'ml', '2025-04-02 08:20:00', -100.0),
    ('Oat Milk', 2150.0, 'ml', '2025-04-03 12:15:00', -150.0),
    ('Oat Milk', 2000.0, 'ml', '2025-04-04 07:40:00', -100.0),
    ('Oat Milk', 1900.0, 'ml', '2025-04-04 18:00:00', -80.0);
    
    # Soy Milk
    ('Soy Milk', 2600.0, 'ml', '2025-03-29 08:00:00', -120.0),
    ('Soy Milk', 2480.0, 'ml', '2025-03-30 10:15:00', -130.0),
    ('Soy Milk', 2350.0, 'ml', '2025-03-30 17:00:00', -90.0),
    ('Soy Milk', 2260.0, 'ml', '2025-03-31 13:00:00', -160.0),
    ('Soy Milk', 2100.0, 'ml', '2025-04-01 09:30:00', -100.0),
    ('Soy Milk', 2000.0, 'ml', '2025-04-02 07:45:00', -90.0),
    ('Soy Milk', 1910.0, 'ml', '2025-04-03 14:15:00', -110.0),
    ('Soy Milk', 1800.0, 'ml', '2025-04-04 08:10:00', -100.0),
    ('Soy Milk', 1700.0, 'ml', '2025-04-04 18:30:00', -80.0);
    
    # Vanilla Syrup
    ('Vanilla Syrup', 1800.0, 'ml', '2025-03-29 07:50:00', -60.0),
    ('Vanilla Syrup', 1740.0, 'ml', '2025-03-30 09:20:00', -90.0),
    ('Vanilla Syrup', 1650.0, 'ml', '2025-03-30 16:45:00', -50.0),
    ('Vanilla Syrup', 1600.0, 'ml', '2025-03-31 11:10:00', -100.0),
    ('Vanilla Syrup', 1500.0, 'ml', '2025-04-01 15:30:00', -80.0),
    ('Vanilla Syrup', 1420.0, 'ml', '2025-04-02 08:40:00', -70.0),
    ('Vanilla Syrup', 1350.0, 'ml', '2025-04-03 12:30:00', -90.0),
    ('Vanilla Syrup', 1260.0, 'ml', '2025-04-04 07:25:00', -60.0),
    ('Vanilla Syrup', 1200.0, 'ml', '2025-04-04 17:20:00', -40.0)


    # Hazelnut Syrup
    ('Hazelnut Syrup', 1600.0, 'ml', '2025-03-29 10:15:00', -70.0),
    ('Hazelnut Syrup', 1530.0, 'ml', '2025-03-30 08:10:00', -90.0),
    ('Hazelnut Syrup', 1440.0, 'ml', '2025-03-30 17:10:00', -60.0),
    ('Hazelnut Syrup', 1380.0, 'ml', '2025-03-31 12:45:00', -80.0),
    ('Hazelnut Syrup', 1300.0, 'ml', '2025-04-01 14:10:00', -100.0),
    ('Hazelnut Syrup', 1200.0, 'ml', '2025-04-02 07:20:00', -50.0),
    ('Hazelnut Syrup', 1150.0, 'ml', '2025-04-03 13:30:00', -70.0),
    ('Hazelnut Syrup', 1080.0, 'ml', '2025-04-04 09:00:00', -60.0),
    ('Hazelnut Syrup', 1020.0, 'ml', '2025-04-05 08:50:00', -40.0),
    ('Hazelnut Syrup', 980.0, 'ml', '2025-04-05 16:10:00', -30.0);

    # Whipped Cream
    ('Whipped Cream', 1200.0, 'g', '2025-04-01 08:00:00', -10.0),
    ('Whipped Cream', 1185.0, 'g', '2025-04-01 15:30:00', -20.0),
    ('Whipped Cream', 1160.0, 'g', '2025-04-02 09:00:00', -30.0),
    ('Whipped Cream', 1130.0, 'g', '2025-04-02 14:00:00', -35.0),
    ('Whipped Cream', 1095.0, 'g', '2025-04-03 11:00:00', -15.0),
    ('Whipped Cream', 1080.0, 'g', '2025-04-04 12:30:00', -10.0),
    ('Whipped Cream', 1060.0, 'g', '2025-04-05 07:00:00', -40.0),
    ('Whipped Cream', 1020.0, 'g', '2025-04-06 08:00:00', -15.0),
    ('Whipped Cream', 1010.0, 'g', '2025-04-06 14:30:00', -10.0),
    ('Whipped Cream', 1000.0, 'g', '2025-04-07 10:00:00', -20.0),
    ('Whipped Cream', 980.0, 'g', '2025-04-07 18:00:00', -15.0);
