-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 01, 2025 at 05:38 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `payment_log`
--
CREATE DATABASE IF NOT EXISTS `payment_log` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `payment_log`;

-- --------------------------------------------------------

--
-- Table structure for table `payment_log`
--

DROP TABLE IF EXISTS `payment_log`;
CREATE TABLE IF NOT EXISTS `payment_log` (
  `payment_log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `order_id` int NOT NULL,
  `amount` float NOT NULL,
  `payment_id` varchar(15) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `outlet_id` int NOT NULL,
  PRIMARY KEY (`payment_log_id`),
  UNIQUE KEY `transaction_id` (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

use payment_log;

--
-- Dumping data for table `payment_log`
--

INSERT INTO `payment_log` (`payment_log_id`, `user_id`, `order_id`, `amount`, `payment_id`, `payment_status`, `created_at`, `outlet_id`) VALUES
(1, '1', 1001, 10, 'TXN123456', 'Completed', '2025-03-30 14:00:04', 0),
(2, '2', 1002, 15, 'TXN123457', 'Pending', '2025-03-30 14:00:04', 0),
(3, '3', 1003, 20, 'TXN123458', 'Failed', '2025-03-30 14:00:04', 0),
(4, '4', 1004, 30, 'TXN123459', 'Completed', '2025-03-30 14:00:04', 0),
(5, '5', 1005, 25, 'TXN123460', 'Refunded', '2025-03-30 14:00:04', 0),
(6, '0', 0, 23, 'pi_3R8kh4QRYfaB', 'pending', '2025-03-31 07:56:11', 2),
(7, '0', 0, 23, 'pi_3R8kkgQRYfaB', 'pending', '2025-03-31 07:59:55', 2),
(8, '0', 0, 23, 'pi_3R8ks9QRYfaB', 'pending', '2025-03-31 08:07:38', 2),
(9, '0', 0, 23, 'pi_3R8kvDQRYfaB', 'pending', '2025-03-31 08:10:48', 2),
(10, '0', 0, 23, 'pi_3R8kvIQRYfaB', 'pending', '2025-03-31 08:10:53', 2),
(11, '12332', 10042, 10.8, 'pi_3R8yHEQRYfaB', 'success', '2025-03-31 22:33:43', 7),
(12, '0', 10080, 23, 'pi_3R93ScQRYfaB', 'succeeded', '2025-04-01 03:58:44', 2),
(13, 'test24', 10080, 23, 'pi_3R97F4QRYfaB', 'succeeded', '2025-04-01 08:00:59', 2),
(14, 'test24', 10080, 23, 'pi_3R97JuQRYfaB', 'succeeded', '2025-04-01 08:06:02', 2),
(15, 'test24', 10082, 13.5, 'pi_3R97NoQRYfaB', 'succeeded', '2025-04-01 08:10:04', 6),
(16, 'test24', 10083, 4, 'pi_3R97VKQRYfaB', 'succeeded', '2025-04-01 08:17:50', 1),
(17, 'test24', 10084, 4, 'pi_3R97Z7QRYfaB', 'succeeded', '2025-04-01 08:21:44', 7),
(18, 'test24', 10084, 4, 'pi_3R97arQRYfaB', 'succeeded', '2025-04-01 08:23:27', 7),
(19, 'test24', 10085, 3, 'pi_3R97bTQRYfaB', 'succeeded', '2025-04-01 08:24:12', 3),
(20, 'test24', 10086, 22, 'pi_3R97hHQRYfaB', 'requires_payment_met', '2025-04-01 08:30:17', 3),
(22, 'test24', 10087, 10.25, 'pi_3R97qgQRYfaB', 'succeeded', '2025-04-01 08:39:48', 5),
(23, 'test24', 10083, 12.25, 'pi_3R97ysQRYfaB', 'succeeded', '2025-04-01 08:48:17', 1),
(24, 'test24', 10088, 13.8, 'pi_3R9859QRYfaB', 'succeeded', '2025-04-01 08:54:46', 3),
(25, 'test24', 10089, 4.5, 'pi_3R9868QRYfaB', 'requires_payment_met', '2025-04-01 08:55:51', 3),
(26, 'test24', 10089, 4.5, 'pi_3R988qQRYfaB', 'succeeded', '2025-04-01 08:58:37', 3),
(27, 'test24', 10083, 16.25, 'pi_3R98jVQRYfaB', 'succeeded', '2025-04-01 09:36:43', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
