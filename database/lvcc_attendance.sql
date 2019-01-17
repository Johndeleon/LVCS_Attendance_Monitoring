-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 16, 2019 at 08:05 AM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lvcc_attendance`
--

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `full_name` varchar(120) DEFAULT NULL,
  `year_level` varchar(20) DEFAULT NULL,
  `section` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `students_absences`
--

CREATE TABLE `students_absences` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `excuse` text,
  `date_absent` date DEFAULT NULL,
  `date_returned` date DEFAULT NULL,
  `days_absent` int(11) NOT NULL,
  `remarks` varchar(50) DEFAULT NULL,
  `created_at` date NOT NULL,
  `updated_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `students_tardiness`
--

CREATE TABLE `students_tardiness` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `tardiness_date` date NOT NULL,
  `tardiness_code` varchar(11) NOT NULL,
  `remarks` text NOT NULL,
  `created_at` date NOT NULL,
  `updated_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `students_tardiness`
--

-- --------------------------------------------------------

--
-- Table structure for table `tardiness_types`
--

CREATE TABLE `tardiness_types` (
  `id` int(11) NOT NULL,
  `code` varchar(5) NOT NULL,
  `title` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tardiness_types`
--

INSERT INTO `tardiness_types` (`id`, `code`, `title`) VALUES
(1, 'FB', 'Late from Break'),
(2, 'NS', 'No Slip pero Reported ng OSA'),
(3, 'FC', 'Late on Flag Ceremony'),
(4, 'RA', 'Refered to the Adviser'),
(5, 'CW', 'Checked with Late Slip'),
(6, 'X', 'Hindi dumaan sa OSA pero nasa list of Late Student'),
(7, 'R', 'Refered to the Guidance Office'),
(8, 'R X', 'Refered to the Guidance Office and Hindi dumaan sa OSA'),
(9, 'R FC', 'Referred to the Guidance Office and Late on Flag Ceremony'),
(10, 'R X', 'Refered to the Guidance Office and Hindi dumaan ng OSA pero nasa list of late students'),
(11, 'CW FC', 'Checked with Late Slip and Late on Flag Ceremony'),
(12, 'FC X', 'Late on Flag Ceremony and Hindi dumaan ng OSA pero nasa list of late students'),
(13, 'FC CW', 'Late on Flag Ceremony and Checked with Slip');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students_absences`
--
ALTER TABLE `students_absences`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students_tardiness`
--
ALTER TABLE `students_tardiness`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tardiness_types`
--
ALTER TABLE `tardiness_types`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3533;

--
-- AUTO_INCREMENT for table `students_absences`
--
ALTER TABLE `students_absences`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7586;

--
-- AUTO_INCREMENT for table `students_tardiness`
--
ALTER TABLE `students_tardiness`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6304;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
