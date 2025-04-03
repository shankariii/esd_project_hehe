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

    # Coffee Beans
    ('Coffee Beans', 1500.0, 'g', '2025-03-27 10:00:00', -60.0),
    ('Coffee Beans', 1440.0, 'g', '2025-03-28 12:00:00', -50.0),
    ('Coffee Beans', 1390.0, 'g', '2025-03-29 09:00:00', -40.0),
    ('Coffee Beans', 1350.0, 'g', '2025-03-29 17:00:00', -30.0),
    ('Coffee Beans', 1320.0, 'g', '2025-03-30 11:00:00', -55.0),
    ('Coffee Beans', 1265.0, 'g', '2025-03-31 15:00:00', -45.0),
    ('Coffee Beans', 1220.0, 'g', '2025-04-01 08:00:00', -35.0),
    ('Coffee Beans', 1185.0, 'g', '2025-04-02 13:00:00', -65.0),
    ('Coffee Beans', 1120.0, 'g', '2025-04-03 09:00:00', -40.0),

    # Almond Milk
    ('Almond Milk', 1250.0, 'ml', '2025-03-27 08:00:00', -25.0),
    ('Almond Milk', 1225.0, 'ml', '2025-03-28 09:00:00', -30.0),
    ('Almond Milk', 1195.0, 'ml', '2025-03-29 11:00:00', -20.0),
    ('Almond Milk', 1175.0, 'ml', '2025-03-30 07:00:00', -15.0),
    ('Almond Milk', 1160.0, 'ml', '2025-03-30 18:00:00', -10.0),
    ('Almond Milk', 1150.0, 'ml', '2025-03-31 10:00:00', -25.0),
    ('Almond Milk', 1125.0, 'ml', '2025-04-01 14:00:00', -10.0),
    ('Almond Milk', 1115.0, 'ml', '2025-04-02 08:00:00', -10.0),
    ('Almond Milk', 1105.0, 'ml', '2025-04-03 10:00:00', -20.0)
