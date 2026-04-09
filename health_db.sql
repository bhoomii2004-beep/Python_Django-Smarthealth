-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 09, 2026 at 07:06 AM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `health_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment_tb`
--

CREATE TABLE IF NOT EXISTS `appointment_tb` (
  `a_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `s_id` int(11) NOT NULL,
  `a_title` varchar(100) NOT NULL,
  `a_symptoms` text NOT NULL,
  `a_date` date NOT NULL,
  `a_fees` double NOT NULL,
  `a_remarks` text,
  `a_status` enum('Pending','Approved','Cancel') NOT NULL,
  `a_cdate` datetime NOT NULL,
  `a_udate` datetime NOT NULL,
  PRIMARY KEY (`a_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

--
-- Dumping data for table `appointment_tb`
--

INSERT INTO `appointment_tb` (`a_id`, `u_id`, `d_id`, `s_id`, `a_title`, `a_symptoms`, `a_date`, `a_fees`, `a_remarks`, `a_status`, `a_cdate`, `a_udate`) VALUES
(1, 1, 1, 1, 'Chest Discomfort Evaluation', 'Burning sensation in chest', '2026-04-07', 1000, NULL, 'Approved', '2026-04-06 21:40:13', '2026-04-07 12:25:26'),
(2, 1, 2, 2, 'Skin Allergy Consultation', 'Red itchy patches on skin', '2026-04-08', 1000, NULL, 'Pending', '2026-04-07 13:11:12', '2026-04-07 13:11:12'),
(3, 3, 3, 3, 'Headache Evaluation', 'Continuous throbbing pain on one side of head', '2026-04-08', 1000, NULL, 'Cancel', '2026-04-07 13:15:39', '2026-04-07 13:51:24'),
(4, 3, 4, 4, 'Back Pain Consultation', 'Lower back stiffness after sitting', '2026-04-08', 1000, NULL, 'Pending', '2026-04-07 13:17:03', '2026-04-07 13:17:03'),
(5, 2, 5, 5, 'Lung Health Check', 'Persistent dry cough', '2026-04-08', 1000, NULL, 'Pending', '2026-04-07 13:19:43', '2026-04-07 13:19:43'),
(6, 2, 1, 1, 'Breathlessness Assessment', 'Difficulty breathing while walking', '2026-04-08', 1000, NULL, 'Approved', '2026-04-07 13:20:48', '2026-04-07 13:25:10'),
(7, 3, 1, 1, 'Heart Rhythm Check', 'Fluttering sensation in chest', '2026-04-15', 1000, NULL, 'Approved', '2026-04-07 13:43:18', '2026-04-07 13:43:31'),
(8, 1, 3, 3, 'Memory Review Visit', 'Difficulty recalling recent events', '2026-04-16', 1000, NULL, 'Pending', '2026-04-07 13:47:16', '2026-04-07 13:47:16'),
(9, 2, 3, 3, 'Sleep Disturbance Consultation', 'Trouble sleeping at night', '2026-04-15', 1000, NULL, 'Approved', '2026-04-07 13:48:32', '2026-04-07 13:51:33');

-- --------------------------------------------------------

--
-- Table structure for table `bill_tb`
--

CREATE TABLE IF NOT EXISTS `bill_tb` (
  `b_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `b_type` enum('Appointment','Treatment') NOT NULL,
  `b_bill_id` int(11) NOT NULL,
  `b_amount` double NOT NULL,
  `u_smartcard` varchar(50) NOT NULL,
  `u_discount` varchar(20) NOT NULL,
  `b_total` double NOT NULL,
  `b_status` enum('Paid','Unpaid') NOT NULL,
  `b_cdate` datetime NOT NULL,
  `b_udate` datetime NOT NULL,
  PRIMARY KEY (`b_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `bill_tb`
--

INSERT INTO `bill_tb` (`b_id`, `u_id`, `d_id`, `b_type`, `b_bill_id`, `b_amount`, `u_smartcard`, `u_discount`, `b_total`, `b_status`, `b_cdate`, `b_udate`) VALUES
(1, 1, 1, 'Appointment', 1, 1000, '0002385446', '10', 900, 'Paid', '2026-04-07 13:59:01', '2026-04-07 13:59:01'),
(2, 3, 1, 'Appointment', 7, 1000, '0002377630', '5', 950, 'Paid', '2026-04-07 13:59:44', '2026-04-07 13:59:44'),
(3, 2, 1, 'Appointment', 6, 1000, '0007626802', '7', 930, 'Paid', '2026-04-07 14:00:13', '2026-04-07 14:00:13'),
(4, 2, 1, 'Treatment', 1, 2000, '0007626802', '7%', 1860, 'Paid', '2026-04-07 14:00:42', '2026-04-07 14:00:42'),
(5, 1, 1, 'Treatment', 2, 5000, '0002385446', '10%', 4500, 'Paid', '2026-04-07 14:01:18', '2026-04-07 14:01:18'),
(6, 3, 1, 'Treatment', 3, 3000, '0002377630', '5%', 2850, 'Paid', '2026-04-07 14:02:35', '2026-04-08 16:12:59'),
(7, 2, 3, 'Appointment', 9, 1000, '0007626802', '7', 930, 'Paid', '2026-04-07 14:17:58', '2026-04-07 14:17:58'),
(8, 2, 3, 'Treatment', 4, 3000, '0007626802', '7%', 2790, 'Paid', '2026-04-07 14:18:48', '2026-04-07 14:18:48');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_tb`
--

CREATE TABLE IF NOT EXISTS `doctor_tb` (
  `d_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` int(11) NOT NULL,
  `d_hospitalname` varchar(100) NOT NULL,
  `d_name` varchar(50) NOT NULL,
  `d_contact` bigint(20) NOT NULL,
  `d_address` text NOT NULL,
  `d_gender` enum('Male','Female') NOT NULL,
  `d_image` varchar(100) NOT NULL,
  `d_experience` text NOT NULL,
  `d_certificate` varchar(100) NOT NULL,
  `d_fees` double NOT NULL,
  `d_password` varchar(20) NOT NULL,
  `d_status` enum('Active','Deactive') NOT NULL,
  `d_cdate` datetime NOT NULL,
  `d_udate` datetime NOT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `doctor_tb`
--

INSERT INTO `doctor_tb` (`d_id`, `s_id`, `d_hospitalname`, `d_name`, `d_contact`, `d_address`, `d_gender`, `d_image`, `d_experience`, `d_certificate`, `d_fees`, `d_password`, `d_status`, `d_cdate`, `d_udate`) VALUES
(1, 1, 'LifeLine Hospital', 'Dr.Bhoomi  Prajapati', 7990370176, 'LifeLine Hospital, 3rd Floor, Shree Complex, Near SBI Bank,Gandhinagar , Gujarat – 364002, India', 'Female', 'bhoomi11_ScJeNWy.png', 'I have solid experience in cardiology, diagnosing and treating heart and blood vessel conditions with care. I use tools like ECG and echocardiography for accurate diagnosis and manage cases such as heart attacks, hypertension, and arrhythmias. I also perform procedures like angiography and angioplasty, ensuring the best care and long-term heart health for my patients.', 'certificate.jpg', 1000, '7990', 'Active', '2026-04-06 21:29:57', '2026-04-08 16:27:45'),
(2, 2, 'SkinCare Multispeciality Hospital', 'Dr.Smit Prajapati', 7990076496, '12, Sunrise Complex, CG Road, Ellisbridge, Ahmedabad, Gujarat – 380006', 'Male', 'dc2.png', 'I have strong experience in dermatology, specializing in the diagnosis and treatment of skin, hair, and nail conditions with care and accuracy. I manage cases such as acne, allergies, infections, and pigmentation disorders using modern diagnostic methods. I also perform procedures like skin biopsies and minor treatments when required. I am committed to providing effective treatment and long-term skin care for patients of all ages.', 'certificate_SM1i8uA.jpg', 1000, '12345', 'Active', '2026-04-07 09:12:24', '2026-04-07 13:03:46'),
(3, 3, 'BrainWave Neurology Centre', 'Dr.Ansh Patel', 7622941654, '1st Floor, Silver Point Complex, CG Road, Near Panchvati Circle, Ahmedabad, Gujarat – 380006, India', 'Male', 'ansh_TZXGP4T.jpeg', 'I have solid experience in neurology, treating conditions related to the brain and nervous system such as stroke, migraine, epilepsy, and neuropathy. I focus on accurate diagnosis, timely treatment, and continuous patient care for better neurological health. I also guide patients and families with proper counseling and rehabilitation support for long-term recovery. My practice emphasizes preventive care and patient education to help maintain optimal neurological function.', 'certificate_avuHbir.jpg', 1000, '1234', 'Active', '2026-04-07 09:36:49', '2026-04-07 14:21:04'),
(4, 4, 'BoneCare Orthopedic & Joint Hospital', 'Dr.Mahek Shah', 9998515040, '2nd Floor, Crystal Plaza, C.G. Road, Near Navrangpura Circle, Ahmedabad, Gujarat – 380009, India', 'Female', 'h5.jpg', 'I have extensive experience in orthopedics, specializing in the diagnosis, treatment, and management of bone, joint, and musculoskeletal disorders. I handle cases such as fractures, arthritis, sports injuries, spine disorders, and joint replacements. My approach combines advanced diagnostic techniques, surgical expertise, and rehabilitation planning to ensure complete recovery. I also focus on preventive care, patient education, and long-term mobility improvement for all my patients.', 'certificate_OV4ycee.jpg', 1000, '12345', 'Active', '2026-04-07 09:43:16', '2026-04-07 10:01:00'),
(5, 5, 'LifeHope Cancer Hospital', 'Dr.Krushi Shah', 7048707177, '2nd Floor, Sunrise Tower, Near Bus Stand, Kalol, Gandhinagar, Gujarat – 382721, India', 'Female', 'h6.jpg', 'I have extensive experience in oncology, specializing in the diagnosis, treatment, and management of various cancers. I handle cases including breast, lung, blood, and gastrointestinal cancers using advanced diagnostic techniques and personalized treatment plans. My approach includes chemotherapy, radiotherapy, surgical interventions, and patient counseling. I focus on providing compassionate care, guiding patients and families through every step of treatment, and supporting long-term recovery and quality of life.', 'certificate_nV30tDu.jpg', 1000, '12345', 'Active', '2026-04-07 09:49:23', '2026-04-07 09:56:06'),
(6, 1, 'LifeLine Hospital', 'Dr.Jinal Prajapati', 6351269520, 'LifeLine Hospital, 3rd Floor, Shree Complex, Near SBI Bank,Gandhinagar , Gujarat – 364002, India', 'Female', 'h3_rUMBBoR.jpg', 'I have solid experience in cardiology, diagnosing and treating heart and blood vessel conditions with care. I use tools like ECG and echocardiography for accurate diagnosis and manage cases such as heart attacks, hypertension, and arrhythmias. I also perform procedures like angiography and angioplasty, ensuring the best care and long-term heart health for my patients.', 'certificate.jpg', 1000, '12345', 'Active', '2026-04-06 21:29:57', '2026-04-07 13:01:51'),
(7, 2, 'SkinCare Multispeciality Hospital', 'Dr.Sahil Patel', 9925383471, '12, Sunrise Complex, CG Road, Ellisbridge, Ahmedabad, Gujarat – 380006', 'Male', 'h8_A6YNn69.jpg', 'I have strong experience in dermatology, specializing in the diagnosis and treatment of skin, hair, and nail conditions with care and accuracy. I manage cases such as acne, allergies, infections, and pigmentation disorders using modern diagnostic methods. I also perform procedures like skin biopsies and minor treatments when required. I am committed to providing effective treatment and long-term skin care for patients of all ages.', 'certificate_SM1i8uA.jpg', 1000, '12345', 'Active', '2026-04-07 09:12:24', '2026-04-07 13:02:57'),
(8, 3, 'BrainWave Neurology Centre', 'Dr.Harsh Patel', 9429991279, '1st Floor, Silver Point Complex, CG Road, Near Panchvati Circle, Ahmedabad, Gujarat – 380006, India', 'Male', 'h2_L7L8cu3.jpg', 'I have solid experience in neurology, treating conditions related to the brain and nervous system such as stroke, migraine, epilepsy, and neuropathy. I focus on accurate diagnosis, timely treatment, and continuous patient care for better neurological health. I also guide patients and families with proper counseling and rehabilitation support for long-term recovery. My practice emphasizes preventive care and patient education to help maintain optimal neurological function.', 'certificate_avuHbir.jpg', 1000, '12345', 'Active', '2026-04-07 09:36:49', '2026-04-07 12:59:33'),
(9, 4, 'BoneCare Orthopedic & Joint Hospital', 'Dr.Visha Paneria', 9586550636, '2nd Floor, Crystal Plaza, C.G. Road, Near Navrangpura Circle, Ahmedabad, Gujarat – 380009, India', 'Female', 'h1_c5wBuFr.jpg', 'I have extensive experience in orthopedics, specializing in the diagnosis, treatment, and management of bone, joint, and musculoskeletal disorders. I handle cases such as fractures, arthritis, sports injuries, spine disorders, and joint replacements. My approach combines advanced diagnostic techniques, surgical expertise, and rehabilitation planning to ensure complete recovery. I also focus on preventive care, patient education, and long-term mobility improvement for all my patients.', 'certificate_OV4ycee.jpg', 1000, '12345', 'Active', '2026-04-07 09:43:16', '2026-04-07 13:05:27'),
(10, 5, 'LifeHope Cancer Hospital', 'Dr.Komal Bihola', 8511204094, '2nd Floor, Sunrise Tower, Near Bus Stand, Kalol, Gandhinagar, Gujarat – 382721, India', 'Female', 'h4_z9AnE6N.jpg', 'I have extensive experience in oncology, specializing in the diagnosis, treatment, and management of various cancers. I handle cases including breast, lung, blood, and gastrointestinal cancers using advanced diagnostic techniques and personalized treatment plans. My approach includes chemotherapy, radiotherapy, surgical interventions, and patient counseling. I focus on providing compassionate care, guiding patients and families through every step of treatment, and supporting long-term recovery and quality of life.', 'certificate_nV30tDu.jpg', 1000, '12345', 'Active', '2026-04-07 09:49:23', '2026-04-07 13:07:27');

-- --------------------------------------------------------

--
-- Table structure for table `feedback_tb`
--

CREATE TABLE IF NOT EXISTS `feedback_tb` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `f_name` varchar(20) NOT NULL,
  `f_contact` bigint(20) NOT NULL,
  `f_message` text NOT NULL,
  `f_status` enum('Show','Hide') NOT NULL,
  `f_cdate` datetime NOT NULL,
  `f_udate` datetime NOT NULL,
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `feedback_tb`
--

INSERT INTO `feedback_tb` (`f_id`, `f_name`, `f_contact`, `f_message`, `f_status`, `f_cdate`, `f_udate`) VALUES
(1, 'Prajapati Bhoomika', 7990370176, 'Excellent treatment and very polite behavior. The doctor explained everything clearly and patiently.', 'Show', '2026-04-06 21:34:56', '2026-04-06 21:34:56'),
(2, 'Prajapati Smit', 7990076496, 'Quick registration process and smooth appointment system. Overall service was very well organized.', 'Show', '2026-04-07 09:21:56', '2026-04-07 09:21:56'),
(3, 'Prajapati Jinal', 6351269520, 'The treatment was effective, and I started feeling better within a few days.', 'Show', '2026-04-07 09:25:30', '2026-04-07 09:25:30'),
(4, 'Patel Ansh', 7622941654, 'Clear explanation about my condition and medicines helped me a lot.', 'Show', '2026-04-07 09:26:29', '2026-04-07 09:26:29'),
(5, 'Bihola Komal', 8733005198, 'Very caring approach and friendly behavior throughout the consultation.', 'Show', '2026-04-07 09:28:11', '2026-04-07 09:28:11');

-- --------------------------------------------------------

--
-- Table structure for table `login_tb`
--

CREATE TABLE IF NOT EXISTS `login_tb` (
  `l_id` int(11) NOT NULL AUTO_INCREMENT,
  `l_username` varchar(20) NOT NULL,
  `l_password` varchar(20) NOT NULL,
  `l_image` varchar(100) NOT NULL,
  `l_lastseen` datetime NOT NULL,
  PRIMARY KEY (`l_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `login_tb`
--

INSERT INTO `login_tb` (`l_id`, `l_username`, `l_password`, `l_image`, `l_lastseen`) VALUES
(1, 'admin', '12345', 'user.png', '2026-04-08 15:55:42');

-- --------------------------------------------------------

--
-- Table structure for table `specialization_tb`
--

CREATE TABLE IF NOT EXISTS `specialization_tb` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_name` varchar(20) NOT NULL,
  `s_image` varchar(100) NOT NULL,
  `s_status` enum('Active','Deactive') NOT NULL,
  `s_cdate` datetime NOT NULL,
  `s_udate` datetime NOT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `specialization_tb`
--

INSERT INTO `specialization_tb` (`s_id`, `s_name`, `s_image`, `s_status`, `s_cdate`, `s_udate`) VALUES
(1, 'Cardiology', 'cardiology.jpg', 'Active', '2026-04-06 21:11:39', '2026-04-06 21:11:39'),
(2, 'Dermatology', 'dermatology.jpg', 'Active', '2026-04-06 21:12:16', '2026-04-06 21:12:16'),
(3, 'Neurology', 'neurology.jpg', 'Active', '2026-04-06 21:12:43', '2026-04-06 21:12:43'),
(4, 'Orthopedics', 'orthopedic.webp', 'Active', '2026-04-06 21:13:16', '2026-04-06 21:13:16'),
(5, 'Oncology', 'oncology.webp', 'Active', '2026-04-06 21:13:42', '2026-04-06 21:13:42');

-- --------------------------------------------------------

--
-- Table structure for table `treatment_tb`
--

CREATE TABLE IF NOT EXISTS `treatment_tb` (
  `t_id` int(11) NOT NULL AUTO_INCREMENT,
  `a_id` int(11) NOT NULL,
  `u_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `t_title` varchar(100) NOT NULL,
  `t_treatment` text NOT NULL,
  `t_file` varchar(100) NOT NULL,
  `t_fees` double NOT NULL,
  `t_date` date NOT NULL,
  `t_cdate` datetime NOT NULL,
  `t_udate` datetime NOT NULL,
  PRIMARY KEY (`t_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `treatment_tb`
--

INSERT INTO `treatment_tb` (`t_id`, `a_id`, `u_id`, `d_id`, `t_title`, `t_treatment`, `t_file`, `t_fees`, `t_date`, `t_cdate`, `t_udate`) VALUES
(1, 6, 2, 1, 'Breathlessness Evaluation Treatment', 'Oxygen level and vital signs checked; basic cardiac assessment done. Prescribed supportive medicines, advised slow activity, breathing exercises, and follow-up if symptoms continue.', '21bca71_ZODptn5.pdf', 2000, '2026-04-08', '2026-04-07 13:38:04', '2026-04-08 14:56:57'),
(2, 1, 1, 1, 'Chest Discomfort Support', 'Initial checkup done and suitable medication given for comfort. Recommended simple diet, adequate rest, and review if the issue continues.', '21bca71_fj7jqo0.pdf', 5000, '2026-04-09', '2026-04-07 13:41:09', '2026-04-08 14:56:45'),
(3, 7, 3, 1, 'Heart Rhythm Observation', 'Patient assessed and pulse rhythm monitored. Basic evaluation completed and medication advised for symptom control. Recommended rest and follow-up if fluttering continues.', '21bca71_p6I8GtP.pdf', 3000, '2026-04-15', '2026-04-07 13:44:32', '2026-04-08 14:56:36'),
(4, 9, 2, 3, 'Sleep Disorder Support', 'Patient reviewed and simple sleep routine guidance provided. Medication recommended as needed with advice for follow-up if symptoms continue.', 'treatment_TBPASEF', 3000, '2026-04-15', '2026-04-07 13:54:26', '2026-04-07 13:54:26');

-- --------------------------------------------------------

--
-- Table structure for table `user_tb`
--

CREATE TABLE IF NOT EXISTS `user_tb` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_name` varchar(20) NOT NULL,
  `u_contact` bigint(20) NOT NULL,
  `u_address` text NOT NULL,
  `u_gender` enum('Male','Female','Other') NOT NULL,
  `u_image` varchar(100) NOT NULL,
  `u_idproof` varchar(100) NOT NULL,
  `u_income` varchar(100) NOT NULL,
  `u_dob` date NOT NULL,
  `u_bloodgroup` varchar(10) NOT NULL,
  `u_password` varchar(20) NOT NULL,
  `u_smartcard` varchar(50) NOT NULL,
  `u_discount` varchar(20) NOT NULL,
  `u_status` enum('Active','Deactive') NOT NULL,
  `u_cdate` datetime NOT NULL,
  `u_udate` datetime NOT NULL,
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `user_tb`
--

INSERT INTO `user_tb` (`u_id`, `u_name`, `u_contact`, `u_address`, `u_gender`, `u_image`, `u_idproof`, `u_income`, `u_dob`, `u_bloodgroup`, `u_password`, `u_smartcard`, `u_discount`, `u_status`, `u_cdate`, `u_udate`) VALUES
(1, 'Prajapati Bhoomika', 7990370176, 'Village : Jalund , Prajapati Vas , Gandhinagar - 382640', 'Female', 'bhoomi11_UwnurHJ.png', 'idproof.png', 'income.png', '2004-01-20', 'B+', '7990', '0002385446', '10', 'Active', '2026-04-06 14:43:55', '2026-04-08 16:22:49'),
(2, 'Prajapati Smit', 7990076496, '12, Om Residency, CG Road, Ellisbridge, Ahmedabad, Gujarat – 380006', 'Male', 'user_NKk2s5Y.png', 'idproof_wYUeBna.png', 'income_LHIuMlo.png', '2005-09-17', 'B - ', '12345', '0007626802', '7', 'Active', '2026-04-07 08:56:40', '2026-04-07 15:09:58'),
(3, 'Patel Ansh', 7622941654, '123, Sunrise Apartment, MG Road, Navrangpura, Ahmedabad, Gujarat – 380009', 'Male', 'ansh.jpeg', 'idproof_yO2m0cU.png', 'income_hhWPz39.png', '2004-01-28', 'A+', '1234', '0002377630', '5', 'Active', '2026-04-07 09:02:16', '2026-04-07 15:08:38');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
