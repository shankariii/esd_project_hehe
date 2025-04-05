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


