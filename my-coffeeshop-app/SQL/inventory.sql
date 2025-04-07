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
-- Coffee Beans 
('Coffee Beans', 3500.00, 'g', '2025-03-30 07:15:00', -40.00),
('Coffee Beans', 3460.00, 'g', '2025-03-30 12:30:00', -30.00),
('Coffee Beans', 3400.00, 'g', '2025-03-31 08:00:00', -60.00),
('Coffee Beans', 3340.00, 'g', '2025-03-31 14:20:00', -40.00),
('Coffee Beans', 3270.00, 'g', '2025-04-01 09:45:00', -70.00),
('Coffee Beans', 3200.00, 'g', '2025-04-02 07:30:00', -50.00),
('Coffee Beans', 3150.00, 'g', '2025-04-02 16:00:00', -30.00),
('Coffee Beans', 3080.00, 'g', '2025-04-03 08:15:00', -70.00),
('Coffee Beans', 3000.00, 'g', '2025-04-04 10:30:00', -80.00),
('Coffee Beans', 2920.00, 'g', '2025-04-05 11:00:00', -60.00),
('Coffee Beans', 2860.00, 'g', '2025-04-05 18:30:00', -40.00),
('Coffee Beans', 2800.00, 'g', '2025-04-06 07:45:00', -60.00),
('Coffee Beans', 2740.00, 'g', '2025-04-06 12:45:00', -60.00),

-- Regular Milk 
('Regular Milk', 10000.00, 'ml', '2025-03-30 07:30:00', -200.00),
('Regular Milk', 9800.00, 'ml', '2025-03-30 13:45:00', -150.00),
('Regular Milk', 9600.00, 'ml', '2025-03-31 08:45:00', -250.00),
('Regular Milk', 9350.00, 'ml', '2025-04-01 09:00:00', -300.00),
('Regular Milk', 9050.00, 'ml', '2025-04-02 10:15:00', -200.00),
('Regular Milk', 8850.00, 'ml', '2025-04-03 11:30:00', -180.00),
('Regular Milk', 8600.00, 'ml', '2025-04-04 14:00:00', -250.00),
('Regular Milk', 8350.00, 'ml', '2025-04-05 09:30:00', -200.00),
('Regular Milk', 8150.00, 'ml', '2025-04-06 08:00:00', -150.00),
('Regular Milk', 8000.00, 'ml', '2025-04-06 12:00:00', -150.00),

-- Skim Milk
('Skim Milk', 4000.00, 'ml', '2025-03-30 08:15:00', -200.00), 
('Skim Milk', 3800.00, 'ml', '2025-03-31 11:30:00', -200.00),  
('Skim Milk', 3600.00, 'ml', '2025-04-02 14:00:00', -200.00),  
('Skim Milk', 3400.00, 'ml', '2025-04-04 09:45:00', -400.00),  
('Skim Milk', 3000.00, 'ml', '2025-04-06 10:30:00', -200.00),   

-- Almond Milk
('Almond Milk', 3000.00, 'ml', '2025-03-30 10:00:00', -200.00), 
('Almond Milk', 2800.00, 'ml', '2025-04-01 13:20:00', -200.00),  
('Almond Milk', 2600.00, 'ml', '2025-04-03 16:45:00', -200.00),  
('Almond Milk', 2400.00, 'ml', '2025-04-05 12:15:00', -400.00),  
('Almond Milk', 2000.00, 'ml', '2025-04-06 12:45:00', -400.00),  

-- Oat Milk
('Oat Milk', 5000.00, 'ml', '2025-03-30 09:30:00', -200.00), 
('Oat Milk', 4800.00, 'ml', '2025-03-31 15:00:00', -200.00),    
('Oat Milk', 4600.00, 'ml', '2025-04-02 10:30:00', -200.00),    
('Oat Milk', 4400.00, 'ml', '2025-04-04 17:30:00', -400.00),    
('Oat Milk', 4000.00, 'ml', '2025-04-06 11:45:00', -200.00),   

-- Soy Milk
('Soy Milk', 3500.00, 'ml', '2025-03-30 11:00:00', -200.00),
('Soy Milk', 3300.00, 'ml', '2025-04-01 14:10:00', -200.00),    
('Soy Milk', 3100.00, 'ml', '2025-04-03 12:40:00', -200.00),    
('Soy Milk', 2900.00, 'ml', '2025-04-05 15:20:00', -400.00),

-- Matcha Powder
('Matcha Powder', 200.00, 'g', '2025-03-30 11:00:00', -5.00),
('Matcha Powder', 195.00, 'g', '2025-03-31 15:00:00', -5.00),  
('Matcha Powder', 190.00, 'g', '2025-04-01 16:30:00', -5.00),   
('Matcha Powder', 185.00, 'g', '2025-04-03 12:00:00', -5.00),
('Matcha Powder', 180.00, 'g', '2025-04-04 13:45:00', -5.00),
('Matcha Powder', 175.00, 'g', '2025-04-05 16:45:00', -5.00),
('Matcha Powder', 170.00, 'g', '2025-04-05 10:20:00', -5.00),

-- Sugar Syrup (15ml per matcha drink - paired with matcha powder data)
('Sugar Syrup', 800.00, 'ml', '2025-03-30 11:00:00', -15.00),
('Sugar Syrup', 785.00, 'ml', '2025-03-31 15:00:00', -15.00),  
('Sugar Syrup', 770.00, 'ml', '2025-04-01 16:30:00', -15.00),    
('Sugar Syrup', 755.00, 'ml', '2025-04-03 12:00:00', -15.00),    
('Sugar Syrup', 740.00, 'ml', '2025-04-04 13:45:00', -15.00),    
('Sugar Syrup', 725.00, 'ml', '2025-04-05 16:45:00', -15.00),  
('Sugar Syrup', 710.00, 'ml', '2025-04-06 10:20:00', -15.00), 

-- Chocolate Syrup 
('Chocolate Syrup', 1000.00, 'ml', '2025-03-30 09:00:00', -60.00),  
('Chocolate Syrup', 940.00, 'ml', '2025-03-30 14:30:00', -45.00), 
('Chocolate Syrup', 895.00, 'ml', '2025-03-31 10:30:00', -60.00),
('Chocolate Syrup', 835.00, 'ml', '2025-04-01 13:15:00', -60.00),
('Chocolate Syrup', 775.00, 'ml', '2025-04-02 11:20:00', -45.00), 
('Chocolate Syrup', 730.00, 'ml', '2025-04-03 08:45:00', -60.00),
('Chocolate Syrup', 670.00, 'ml', '2025-04-04 16:00:00', -45.00), 
('Chocolate Syrup', 625.00, 'ml', '2025-04-05 11:20:00', -60.00),
('Chocolate Syrup', 565.00, 'ml', '2025-04-06 10:15:00', -45.00),
('Chocolate Syrup', 520.00, 'ml', '2025-04-06 13:15:00', -45.00),


-- Whipped Cream
('Whipped Cream', 500.00, 'g', '2025-03-30 08:00:00', -20.00),  
('Whipped Cream', 480.00, 'g', '2025-03-30 12:00:00', -40.00), 
('Whipped Cream', 440.00, 'g', '2025-03-31 14:00:00', -40.00),  
('Whipped Cream', 400.00, 'g', '2025-04-01 14:30:00', -40.00), 
('Whipped Cream', 360.00, 'g', '2025-04-02 09:45:00', -40.00), 
('Whipped Cream', 320.00, 'g', '2025-04-03 10:00:00', -40.00), 
('Whipped Cream', 280.00, 'g', '2025-04-04 17:00:00', -60.00), 
('Whipped Cream', 220.00, 'g', '2025-04-05 13:15:00', -80.00),   
('Whipped Cream', 140.00, 'g', '2025-04-06 09:45:00', -40.00),   
('Whipped Cream', 100.00, 'g', '2025-04-06 13:30:00', -20.00),

-- Vanilla Syrup
('Vanilla Syrup', 750.00, 'ml', '2025-03-30 08:30:00', -45.00),
('Vanilla Syrup', 705.00, 'ml', '2025-03-31 11:45:00', -30.00),
('Vanilla Syrup', 675.00, 'ml', '2025-04-01 15:20:00', -45.00),
('Vanilla Syrup', 630.00, 'ml', '2025-04-03 09:30:00', -30.00),
('Vanilla Syrup', 600.00, 'ml', '2025-04-04 12:15:00', -45.00),
('Vanilla Syrup', 555.00, 'ml', '2025-04-05 14:50:00', -60.00),
('Vanilla Syrup', 495.00, 'ml', '2025-04-06 11:50:00', -60.00),


-- Caramel Syrup
('Caramel Syrup', 600.00, 'ml', '2025-03-30 10:15:00', -30.00),
('Caramel Syrup', 570.00, 'ml', '2025-03-31 13:30:00', -45.00),
('Caramel Syrup', 525.00, 'ml', '2025-04-02 08:20:00', -30.00),
('Caramel Syrup', 495.00, 'ml', '2025-04-03 14:10:00', -45.00),
('Caramel Syrup', 450.00, 'ml', '2025-04-05 10:40:00', -60.00),
('Caramel Syrup', 390.00, 'ml', '2025-04-06 10:45:00', -60.00),

-- Chocolate Sprinkles
('Chocolate Sprinkles', 200.00, 'g', '2025-03-30 11:30:00', -4.00),  
('Chocolate Sprinkles', 196.00, 'g', '2025-03-31 09:15:00', -8.00),   
('Chocolate Sprinkles', 188.00, 'g', '2025-03-31 16:45:00', -4.00),  
('Chocolate Sprinkles', 184.00, 'g', '2025-04-02 10:50:00', -8.00),  
('Chocolate Sprinkles', 176.00, 'g', '2025-04-03 14:20:00', -4.00),  
('Chocolate Sprinkles', 172.00, 'g', '2025-04-04 15:30:00', -12.00),  
('Chocolate Sprinkles', 160.00, 'g', '2025-04-05 12:20:00', -16.00), 
('Chocolate Sprinkles', 144.00, 'g', '2025-04-06 10:00:00', -8.00),  
('Chocolate Sprinkles', 136.00, 'g', '2025-04-06 12:30:00', -4.00);

select * from inventory where date_time < '2025-04-07';