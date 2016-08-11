# Host: 10.66.144.145  (Version 5.6.23-log)
# Date: 2016-08-11 11:00:52
# Generator: MySQL-Front 5.3  (Build 5.31)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "cvm_info"
#

DROP TABLE IF EXISTS `cvm_info`;
CREATE TABLE `cvm_info` (
  `number` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL,
  `instanceName` varchar(128) NOT NULL,
  `lanIp` varchar(64) NOT NULL,
  `wanIpSet` varchar(256) NOT NULL,
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deadlineTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `projectId` int(11) NOT NULL,
  `osid` varchar(64) NOT NULL,
  `zoneId` int(11) NOT NULL,
  PRIMARY KEY (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "cvm_info"
#

INSERT INTO `cvm_info` VALUES (1,'1','LDZW-Publicsvr-AND-001','10.104.51.27','119.29.114.203','2016-07-13 11:02:47','2016-07-14 11:02:19',1,'2',2),(2,'2','LDZW-Publicsvr-AND-002','10.104.32.168','119.29.80.23','2016-07-13 11:02:47','2016-07-14 11:02:19',1,'2',2);
