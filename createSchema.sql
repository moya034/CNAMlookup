CREATE TABLE `tblAnveoSearch` (
  `IdCol` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Number` varchar(45) NOT NULL,
  `InsertDate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdCol`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tblCallerID` (
  `IdCol` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Number` varchar(11) NOT NULL,
  `Type` varchar(45) NOT NULL,
  `InsertDate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdCol`)
) ENGINE=InnoDB AUTO_INCREMENT=378 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tblCallerIDoverride` (
  `Name` varchar(45) NOT NULL,
  `Number` varchar(45) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE ALGORITHM=UNDEFINED DEFINER=`CallerID`@`192.168.%.%` SQL SECURITY DEFINER VIEW `view_CallerID` AS select `tblCallerID`.`Name` AS `Name`,`tblCallerID`.`Number` AS `Number` from `tblCallerID` where (not(`tblCallerID`.`Number` in (select `tblCallerIDoverride`.`Number` from `tblCallerIDoverride`))) union select replace(`tblAnveoSearch`.`Name`,'NO ANVEO CNAM','NO CNAM') AS `Name`,`tblAnveoSearch`.`Number` AS `Number` from `tblAnveoSearch` where (not(`tblAnveoSearch`.`Number` in (select `tblCallerIDoverride`.`Number` from `tblCallerIDoverride`))) union select `tblCallerIDoverride`.`Name` AS `Name`,`tblCallerIDoverride`.`Number` AS `Number` from `tblCallerIDoverride`;
