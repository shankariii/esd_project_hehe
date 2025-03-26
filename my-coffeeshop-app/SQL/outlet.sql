-- phpMyAdmin SQL Dump
-- Database: `outlet`

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `outlet` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `outlet`;

-- Drop and recreate the outlets table
DROP TABLE IF EXISTS `outlets`;
CREATE TABLE IF NOT EXISTS `outlets` (
  `outlet_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `address` TEXT NOT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  `contact_info` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`outlet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert sample data
INSERT INTO `outlets` (`name`, `address`, `latitude`, `longitude`, `contact_info`) VALUES
('Orchard Rd', '2 Orchard Turn, #B2 - 09, Singapore 238801', 1.30453350, 103.83167718, '62389283'),
('SMU', '70 Stamford Rd, #B1-25 Li Ka Shing Library, SMU 178901', 1.29643403, 103.84995523, '67239283'),
('Changi Airport', '80 Airport Blvd, Singapore Changi Airport, Singapore 819642', 1.364420, 103.991531, '65412345'),
('Tiong Bahru', '56 Eng Hoon St, Tiong Bahru Estate, Singapore 160056', 1.285364, 103.828412, '62224455'),
('Jurong East', '3 Gateway Drive, #01-18, Westgate, Singapore 608532', 1.333180, 103.742125, '68901234'),
('Tampines Hub', '1 Tampines Walk, Singapore 528523', 1.352083, 103.940415, '67894567'),
('Paya Lebar Quarter', '10 Paya Lebar Rd, #01-28, Singapore 409057', 1.317300, 103.892400, '63887766');

COMMIT;
