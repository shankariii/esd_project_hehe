-- phpMyAdmin SQL Dump
-- Database: `inventory`

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `inventory` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `inventory`;

-- Drop and recreate the table
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE IF NOT EXISTS `inventory` (
  `inventory_id` INT NOT NULL AUTO_INCREMENT,
  `ingredient_id` VARCHAR(64) NOT NULL,
  `available_quantity` FLOAT(2) NOT NULL,
  `unit` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`inventory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert sample inventory items
INSERT INTO `inventory` (`ingredient_id`, `available_quantity`, `unit`) VALUES
('1', 100.0, 'kg'),
('2', 150.0, 'kg'),
('3', 200.0, 'ml'),
('4', 300.0, 'ml'),
('5', 50.0, 'g'),
('6', 75.0, 'g');

COMMIT;
