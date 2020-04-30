-- MySQL dump 10.16  Distrib 10.1.44-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ompdb
-- ------------------------------------------------------
-- Server version	10.1.44-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'Editors'),(1,'Moderators');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (2,1,1),(6,1,2),(7,1,3),(8,1,4),(12,1,5),(13,1,6),(14,1,7),(1,2,1),(3,2,2),(4,2,3),(5,2,4),(9,2,5),(10,2,6),(11,2,7);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=162 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can access Wagtail admin',3,'access_admin'),(2,'Can add document',4,'add_document'),(3,'Can change document',4,'change_document'),(4,'Can delete document',4,'delete_document'),(5,'Can add image',5,'add_image'),(6,'Can change image',5,'change_image'),(7,'Can delete image',5,'delete_image'),(8,'Can add home page',2,'add_homepage'),(9,'Can change home page',2,'change_homepage'),(10,'Can delete home page',2,'delete_homepage'),(11,'Can view home page',2,'view_homepage'),(12,'Can add 2C2P Settings',6,'add_settings2c2p'),(13,'Can change 2C2P Settings',6,'change_settings2c2p'),(14,'Can delete 2C2P Settings',6,'delete_settings2c2p'),(15,'Can view 2C2P Settings',6,'view_settings2c2p'),(16,'Can add global settings',7,'add_globalsettings'),(17,'Can change global settings',7,'change_globalsettings'),(18,'Can delete global settings',7,'delete_globalsettings'),(19,'Can view global settings',7,'view_globalsettings'),(20,'Can add admin emails',8,'add_adminemails'),(21,'Can change admin emails',8,'change_adminemails'),(22,'Can delete admin emails',8,'delete_adminemails'),(23,'Can view admin emails',8,'view_adminemails'),(24,'Can add donation',9,'add_donation'),(25,'Can change donation',9,'change_donation'),(26,'Can delete donation',9,'delete_donation'),(27,'Can view donation',9,'view_donation'),(28,'Can add donation form',10,'add_donationform'),(29,'Can change donation form',10,'change_donationform'),(30,'Can delete donation form',10,'delete_donationform'),(31,'Can view donation form',10,'view_donationform'),(32,'Can add payment gateway',11,'add_paymentgateway'),(33,'Can change payment gateway',11,'change_paymentgateway'),(34,'Can delete payment gateway',11,'delete_paymentgateway'),(35,'Can view payment gateway',11,'view_paymentgateway'),(36,'Can add more form field',12,'add_moreformfield'),(37,'Can change more form field',12,'change_moreformfield'),(38,'Can delete more form field',12,'delete_moreformfield'),(39,'Can view more form field',12,'view_moreformfield'),(40,'Can add donor',13,'add_donor'),(41,'Can change donor',13,'change_donor'),(42,'Can delete donor',13,'delete_donor'),(43,'Can view donor',13,'view_donor'),(44,'Can add donation meta',14,'add_donationmeta'),(45,'Can change donation meta',14,'change_donationmeta'),(46,'Can delete donation meta',14,'delete_donationmeta'),(47,'Can view donation meta',14,'view_donationmeta'),(48,'Can add amount step',15,'add_amountstep'),(49,'Can change amount step',15,'change_amountstep'),(50,'Can delete amount step',15,'delete_amountstep'),(51,'Can view amount step',15,'view_amountstep'),(52,'Can add form submission',16,'add_formsubmission'),(53,'Can change form submission',16,'change_formsubmission'),(54,'Can delete form submission',16,'delete_formsubmission'),(55,'Can view form submission',16,'view_formsubmission'),(56,'Can add redirect',17,'add_redirect'),(57,'Can change redirect',17,'change_redirect'),(58,'Can delete redirect',17,'delete_redirect'),(59,'Can view redirect',17,'view_redirect'),(60,'Can add embed',18,'add_embed'),(61,'Can change embed',18,'change_embed'),(62,'Can delete embed',18,'delete_embed'),(63,'Can view embed',18,'view_embed'),(64,'Can add user profile',19,'add_userprofile'),(65,'Can change user profile',19,'change_userprofile'),(66,'Can delete user profile',19,'delete_userprofile'),(67,'Can view user profile',19,'view_userprofile'),(68,'Can view document',4,'view_document'),(69,'Can view image',5,'view_image'),(70,'Can add rendition',20,'add_rendition'),(71,'Can change rendition',20,'change_rendition'),(72,'Can delete rendition',20,'delete_rendition'),(73,'Can view rendition',20,'view_rendition'),(74,'Can add query',21,'add_query'),(75,'Can change query',21,'change_query'),(76,'Can delete query',21,'delete_query'),(77,'Can view query',21,'view_query'),(78,'Can add Query Daily Hits',22,'add_querydailyhits'),(79,'Can change Query Daily Hits',22,'change_querydailyhits'),(80,'Can delete Query Daily Hits',22,'delete_querydailyhits'),(81,'Can view Query Daily Hits',22,'view_querydailyhits'),(82,'Can add page',1,'add_page'),(83,'Can change page',1,'change_page'),(84,'Can delete page',1,'delete_page'),(85,'Can view page',1,'view_page'),(86,'Can add group page permission',23,'add_grouppagepermission'),(87,'Can change group page permission',23,'change_grouppagepermission'),(88,'Can delete group page permission',23,'delete_grouppagepermission'),(89,'Can view group page permission',23,'view_grouppagepermission'),(90,'Can add page revision',24,'add_pagerevision'),(91,'Can change page revision',24,'change_pagerevision'),(92,'Can delete page revision',24,'delete_pagerevision'),(93,'Can view page revision',24,'view_pagerevision'),(94,'Can add page view restriction',25,'add_pageviewrestriction'),(95,'Can change page view restriction',25,'change_pageviewrestriction'),(96,'Can delete page view restriction',25,'delete_pageviewrestriction'),(97,'Can view page view restriction',25,'view_pageviewrestriction'),(98,'Can add site',26,'add_site'),(99,'Can change site',26,'change_site'),(100,'Can delete site',26,'delete_site'),(101,'Can view site',26,'view_site'),(102,'Can add collection',27,'add_collection'),(103,'Can change collection',27,'change_collection'),(104,'Can delete collection',27,'delete_collection'),(105,'Can view collection',27,'view_collection'),(106,'Can add group collection permission',28,'add_groupcollectionpermission'),(107,'Can change group collection permission',28,'change_groupcollectionpermission'),(108,'Can delete group collection permission',28,'delete_groupcollectionpermission'),(109,'Can view group collection permission',28,'view_groupcollectionpermission'),(110,'Can add collection view restriction',29,'add_collectionviewrestriction'),(111,'Can change collection view restriction',29,'change_collectionviewrestriction'),(112,'Can delete collection view restriction',29,'delete_collectionviewrestriction'),(113,'Can view collection view restriction',29,'view_collectionviewrestriction'),(114,'Can add Tag',30,'add_tag'),(115,'Can change Tag',30,'change_tag'),(116,'Can delete Tag',30,'delete_tag'),(117,'Can view Tag',30,'view_tag'),(118,'Can add Tagged Item',31,'add_taggeditem'),(119,'Can change Tagged Item',31,'change_taggeditem'),(120,'Can delete Tagged Item',31,'delete_taggeditem'),(121,'Can view Tagged Item',31,'view_taggeditem'),(122,'Can add user',32,'add_user'),(123,'Can change user',32,'change_user'),(124,'Can delete user',32,'delete_user'),(125,'Can view user',32,'view_user'),(126,'Can add log entry',33,'add_logentry'),(127,'Can change log entry',33,'change_logentry'),(128,'Can delete log entry',33,'delete_logentry'),(129,'Can view log entry',33,'view_logentry'),(130,'Can add permission',34,'add_permission'),(131,'Can change permission',34,'change_permission'),(132,'Can delete permission',34,'delete_permission'),(133,'Can view permission',34,'view_permission'),(134,'Can add group',35,'add_group'),(135,'Can change group',35,'change_group'),(136,'Can delete group',35,'delete_group'),(137,'Can view group',35,'view_group'),(138,'Can add content type',36,'add_contenttype'),(139,'Can change content type',36,'change_contenttype'),(140,'Can delete content type',36,'delete_contenttype'),(141,'Can view content type',36,'view_contenttype'),(142,'Can add session',37,'add_session'),(143,'Can change session',37,'change_session'),(144,'Can delete session',37,'delete_session'),(145,'Can view session',37,'view_session'),(146,'Can add donation meta field',38,'add_donationmetafield'),(147,'Can change donation meta field',38,'change_donationmetafield'),(148,'Can delete donation meta field',38,'delete_donationmetafield'),(149,'Can view donation meta field',38,'view_donationmetafield'),(150,'Can add donor meta',39,'add_donormeta'),(151,'Can change donor meta',39,'change_donormeta'),(152,'Can delete donor meta',39,'delete_donormeta'),(153,'Can view donor meta',39,'view_donormeta'),(154,'Can add donor meta field',40,'add_donormetafield'),(155,'Can change donor meta field',40,'change_donormetafield'),(156,'Can delete donor meta field',40,'delete_donormetafield'),(157,'Can view donor meta field',40,'view_donormetafield'),(158,'Can add appearance settings',41,'add_appearancesettings'),(159,'Can change appearance settings',41,'change_appearancesettings'),(160,'Can delete appearance settings',41,'delete_appearancesettings'),(161,'Can view appearance settings',41,'view_appearancesettings');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_user_user`
--

DROP TABLE IF EXISTS `custom_user_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_user_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_email_verified` tinyint(1) NOT NULL,
  `opt_in_mailing_list` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_user_user`
--

LOCK TABLES `custom_user_user` WRITE;
/*!40000 ALTER TABLE `custom_user_user` DISABLE KEYS */;
INSERT INTO `custom_user_user` VALUES (1,'pbkdf2_sha256$180000$w41CXTQsjejF$Hx58sORVz7DLnLpgBt43gt3pIqD1dERci6PO/yq2Uic=','2020-04-28 11:56:25.807878',1,'Chun Fai','Hung',1,1,'2020-04-18 19:55:08.984268','franky@uxcodified.com',0,0),(2,'pbkdf2_sha256$180000$7AicYamFGhWe$/2zjXTACt8h+1MM9TlTIyKBmBJM7uUX3dg7HRVAF2gw=','2020-04-19 12:22:12.879274',0,'','',0,1,'2020-04-19 12:16:51.576594','abc@john.com',0,0),(3,'pbkdf2_sha256$180000$it92Jktv6JD9$9Z/LkkyoesuYyZQ1kpH1HPuWTxO+kKNSZJZSpCMgZYE=',NULL,0,'','',0,1,'2020-04-19 13:35:51.157294','def@john.com',0,0),(4,'pbkdf2_sha256$180000$cAduue4eMUEJ$UquQiTYc2/MuZTtAB7JW2ByDCCTLXaHaunrldZUJ3Sw=','2020-04-25 19:07:49.265279',0,'Fan','John',0,1,'2020-04-19 13:40:44.595340','gatoutahellweb@gmail.com',1,1),(5,'pbkdf2_sha256$180000$2mGbXm39Amr1$+kuUutbwOG3m3dwbG2C2h1HYL5kbsWEA0NrmsK2f/BY=','2020-04-19 17:44:02.904259',0,'','',0,1,'2020-04-19 17:43:19.438678','sage@john.com',0,0),(6,'pbkdf2_sha256$180000$6sTSUMw6lmFj$2eSZCbc+fZW6+j8v/1wn5tRwY0OYbdG2xU2A64FAj8M=','2020-04-19 19:39:53.317561',0,'','',0,1,'2020-04-19 19:39:14.607922','dash@john.com',0,0),(7,'pbkdf2_sha256$180000$jrwnUqN2Xhhz$FUm67xspsbagzNdCMMU2ou+DxyKd4wK+jpsvJUUtOTI=','2020-04-19 20:27:19.929373',0,'','',0,1,'2020-04-19 20:26:31.387304','lick@john.com',0,0),(8,'pbkdf2_sha256$180000$YAte8IWD4atz$u9zS8I4BbQqtSbTYYuKmv/p0JY03IRGXNDejmyXSZkk=','2020-04-27 12:09:33.036513',0,'Franky','Hung',0,1,'2020-04-19 20:33:12.049057','frankyhung93@gmail.com',1,0),(9,'pbkdf2_sha256$180000$n9Mm56inOxCl$XEX3ezjjPIh6oYRfvr21WliKRKpaWksF+GEo6RNPTBs=','2020-04-20 09:20:27.080306',0,'','',0,1,'2020-04-20 09:19:47.195730','https@john.com',0,0),(19,'pbkdf2_sha256$180000$LORjlyGdPQDa$7PoKy07wakfqpBT+J/zCxSr6rnhXSrze9q2VX1+LSxI=','2020-04-22 09:57:17.353960',0,'Retest','John',0,1,'2020-04-22 09:56:24.089641','retest@john.com',0,0),(20,'pbkdf2_sha256$180000$dUgUMzAKjyWD$bpGwllIigYUj6eB4qMIsAMp/1ug5G/5QDEfDu+YED+s=','2020-04-23 09:11:07.086216',0,'ROTK','John',0,1,'2020-04-23 09:10:31.275861','rotk@john.com',0,0),(21,'pbkdf2_sha256$180000$1FI6Zj9t9gUO$IC/BjrF5Bkyyvgws+OfLmGIPhoMXmXQC+OPiDi9cfQI=','2020-04-23 09:16:32.722562',0,'ROTK','Peter',0,1,'2020-04-23 09:16:14.303513','rotk@peter.com',0,0),(22,'pbkdf2_sha256$180000$HM3l131G9lJr$qYkciQPGLxNg5OIeAodGweQ+f6GSdBvFe1ALgermaPE=','2020-04-24 10:52:44.947335',0,'Drake','John',0,1,'2020-04-23 20:00:32.915114','drake@john.com',0,0),(23,'pbkdf2_sha256$180000$MXLmoOOQUEZj$jI4wFgPQaU9Uz12I08lLli1PMh1XFH3WPNWLXDGa+Eo=','2020-04-27 09:37:15.827649',0,'John','Smith',0,1,'2020-04-27 09:36:20.866257','johnsmith2@gmail.example',0,0),(24,'pbkdf2_sha256$180000$zWGcjzy8jOL8$TeE/Oi55d7wu4I2oOwB/juHR6z+2yE3pgzMpY3jSP4I=','2020-04-27 12:11:17.307798',0,'Deca','John',0,1,'2020-04-27 12:10:47.483875','deca@john.com',0,1);
/*!40000 ALTER TABLE `custom_user_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_user_user_groups`
--

DROP TABLE IF EXISTS `custom_user_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_user_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `custom_user_user_groups_user_id_group_id_fc2104d2_uniq` (`user_id`,`group_id`),
  KEY `custom_user_user_groups_group_id_dfde52bf_fk_auth_group_id` (`group_id`),
  CONSTRAINT `custom_user_user_groups_group_id_dfde52bf_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `custom_user_user_groups_user_id_f1071bc9_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_user_user_groups`
--

LOCK TABLES `custom_user_user_groups` WRITE;
/*!40000 ALTER TABLE `custom_user_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_user_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_user_user_user_permissions`
--

DROP TABLE IF EXISTS `custom_user_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_user_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `custom_user_user_user_pe_user_id_permission_id_2215a086_uniq` (`user_id`,`permission_id`),
  KEY `custom_user_user_use_permission_id_cb2d2b0f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `custom_user_user_use_permission_id_cb2d2b0f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `custom_user_user_use_user_id_65556ab9_fk_custom_us` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_user_user_user_permissions`
--

LOCK TABLES `custom_user_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `custom_user_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_user_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_custom_user_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (33,'admin','logentry'),(35,'auth','group'),(34,'auth','permission'),(36,'contenttypes','contenttype'),(32,'custom_user','user'),(15,'donations','amountstep'),(9,'donations','donation'),(10,'donations','donationform'),(14,'donations','donationmeta'),(38,'donations','donationmetafield'),(13,'donations','donor'),(39,'donations','donormeta'),(40,'donations','donormetafield'),(12,'donations','moreformfield'),(11,'donations','paymentgateway'),(2,'home','homepage'),(37,'sessions','session'),(8,'site_settings','adminemails'),(41,'site_settings','appearancesettings'),(7,'site_settings','globalsettings'),(6,'site_settings','settings2c2p'),(30,'taggit','tag'),(31,'taggit','taggeditem'),(3,'wagtailadmin','admin'),(27,'wagtailcore','collection'),(29,'wagtailcore','collectionviewrestriction'),(28,'wagtailcore','groupcollectionpermission'),(23,'wagtailcore','grouppagepermission'),(1,'wagtailcore','page'),(24,'wagtailcore','pagerevision'),(25,'wagtailcore','pageviewrestriction'),(26,'wagtailcore','site'),(4,'wagtaildocs','document'),(18,'wagtailembeds','embed'),(16,'wagtailforms','formsubmission'),(5,'wagtailimages','image'),(20,'wagtailimages','rendition'),(17,'wagtailredirects','redirect'),(21,'wagtailsearch','query'),(22,'wagtailsearch','querydailyhits'),(19,'wagtailusers','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-04-18 19:53:00.141303'),(2,'contenttypes','0002_remove_content_type_name','2020-04-18 19:53:00.380315'),(3,'auth','0001_initial','2020-04-18 19:53:00.624322'),(4,'auth','0002_alter_permission_name_max_length','2020-04-18 19:53:01.474577'),(5,'auth','0003_alter_user_email_max_length','2020-04-18 19:53:01.490380'),(6,'auth','0004_alter_user_username_opts','2020-04-18 19:53:01.526516'),(7,'auth','0005_alter_user_last_login_null','2020-04-18 19:53:01.533772'),(8,'auth','0006_require_contenttypes_0002','2020-04-18 19:53:01.538872'),(9,'auth','0007_alter_validators_add_error_messages','2020-04-18 19:53:01.553589'),(10,'auth','0008_alter_user_username_max_length','2020-04-18 19:53:01.563284'),(11,'auth','0009_alter_user_last_name_max_length','2020-04-18 19:53:01.572880'),(12,'auth','0010_alter_group_name_max_length','2020-04-18 19:53:01.756795'),(13,'auth','0011_update_proxy_permissions','2020-04-18 19:53:01.771436'),(14,'custom_user','0001_initial','2020-04-18 19:53:01.994277'),(15,'admin','0001_initial','2020-04-18 19:53:02.928216'),(16,'admin','0002_logentry_remove_auto_add','2020-04-18 19:53:03.313562'),(17,'admin','0003_logentry_add_action_flag_choices','2020-04-18 19:53:03.323498'),(18,'donations','0001_initial','2020-04-18 19:53:04.799507'),(19,'wagtailcore','0001_initial','2020-04-18 19:53:06.873750'),(20,'wagtailcore','0002_initial_data','2020-04-18 19:53:06.882281'),(21,'wagtailcore','0003_add_uniqueness_constraint_on_group_page_permission','2020-04-18 19:53:06.884814'),(22,'wagtailcore','0004_page_locked','2020-04-18 19:53:06.894581'),(23,'wagtailcore','0005_add_page_lock_permission_to_moderators','2020-04-18 19:53:06.904371'),(24,'wagtailcore','0006_add_lock_page_permission','2020-04-18 19:53:06.914063'),(25,'wagtailcore','0007_page_latest_revision_created_at','2020-04-18 19:53:06.923891'),(26,'wagtailcore','0008_populate_latest_revision_created_at','2020-04-18 19:53:06.933422'),(27,'wagtailcore','0009_remove_auto_now_add_from_pagerevision_created_at','2020-04-18 19:53:06.943603'),(28,'wagtailcore','0010_change_page_owner_to_null_on_delete','2020-04-18 19:53:06.953083'),(29,'wagtailcore','0011_page_first_published_at','2020-04-18 19:53:06.962651'),(30,'wagtailcore','0012_extend_page_slug_field','2020-04-18 19:53:06.972402'),(31,'wagtailcore','0013_update_golive_expire_help_text','2020-04-18 19:53:06.982069'),(32,'wagtailcore','0014_add_verbose_name','2020-04-18 19:53:06.991763'),(33,'wagtailcore','0015_add_more_verbose_names','2020-04-18 19:53:07.001499'),(34,'wagtailcore','0016_change_page_url_path_to_text_field','2020-04-18 19:53:07.011229'),(35,'wagtailcore','0017_change_edit_page_permission_description','2020-04-18 19:53:08.729657'),(36,'wagtailcore','0018_pagerevision_submitted_for_moderation_index','2020-04-18 19:53:08.787674'),(37,'wagtailcore','0019_verbose_names_cleanup','2020-04-18 19:53:08.848323'),(38,'wagtailcore','0020_add_index_on_page_first_published_at','2020-04-18 19:53:08.902381'),(39,'wagtailcore','0021_capitalizeverbose','2020-04-18 19:53:11.077629'),(40,'wagtailcore','0022_add_site_name','2020-04-18 19:53:11.223025'),(41,'wagtailcore','0023_alter_page_revision_on_delete_behaviour','2020-04-18 19:53:11.459909'),(42,'wagtailcore','0024_collection','2020-04-18 19:53:11.550849'),(43,'wagtailcore','0025_collection_initial_data','2020-04-18 19:53:11.583788'),(44,'wagtailcore','0026_group_collection_permission','2020-04-18 19:53:11.729415'),(45,'wagtailcore','0027_fix_collection_path_collation','2020-04-18 19:53:12.351544'),(46,'wagtailcore','0024_alter_page_content_type_on_delete_behaviour','2020-04-18 19:53:12.626363'),(47,'wagtailcore','0028_merge','2020-04-18 19:53:12.635894'),(48,'wagtailcore','0029_unicode_slugfield_dj19','2020-04-18 19:53:12.657495'),(49,'wagtailcore','0030_index_on_pagerevision_created_at','2020-04-18 19:53:12.714592'),(50,'wagtailcore','0031_add_page_view_restriction_types','2020-04-18 19:53:12.938230'),(51,'wagtailcore','0032_add_bulk_delete_page_permission','2020-04-18 19:53:13.390930'),(52,'wagtailcore','0033_remove_golive_expiry_help_text','2020-04-18 19:53:13.423119'),(53,'wagtailcore','0034_page_live_revision','2020-04-18 19:53:13.683692'),(54,'wagtailcore','0035_page_last_published_at','2020-04-18 19:53:13.879493'),(55,'wagtailcore','0036_populate_page_last_published_at','2020-04-18 19:53:13.913791'),(56,'wagtailcore','0037_set_page_owner_editable','2020-04-18 19:53:14.203744'),(57,'wagtailcore','0038_make_first_published_at_editable','2020-04-18 19:53:14.226160'),(58,'wagtailcore','0039_collectionviewrestriction','2020-04-18 19:53:14.809080'),(59,'wagtailcore','0040_page_draft_title','2020-04-18 19:53:15.659772'),(60,'home','0001_initial','2020-04-18 19:53:15.746253'),(61,'home','0002_create_homepage','2020-04-18 19:53:15.967566'),(62,'sessions','0001_initial','2020-04-18 19:53:16.049521'),(63,'wagtailcore','0041_group_collection_permissions_verbose_name_plural','2020-04-18 19:53:16.121173'),(64,'wagtailcore','0042_index_on_pagerevision_approved_go_live_at','2020-04-18 19:53:16.180234'),(65,'wagtailcore','0043_lock_fields','2020-04-18 19:53:16.625917'),(66,'wagtailcore','0044_add_unlock_grouppagepermission','2020-04-18 19:53:16.649316'),(67,'wagtailcore','0045_assign_unlock_grouppagepermission','2020-04-18 19:53:16.684013'),(68,'site_settings','0001_initial','2020-04-18 19:53:16.952210'),(69,'taggit','0001_initial','2020-04-18 19:53:17.741821'),(70,'taggit','0002_auto_20150616_2121','2020-04-18 19:53:18.293122'),(71,'taggit','0003_taggeditem_add_unique_index','2020-04-18 19:53:18.342247'),(72,'wagtailadmin','0001_create_admin_access_permissions','2020-04-18 19:53:18.392718'),(73,'wagtaildocs','0001_initial','2020-04-18 19:53:18.482691'),(74,'wagtaildocs','0002_initial_data','2020-04-18 19:53:18.735761'),(75,'wagtaildocs','0003_add_verbose_names','2020-04-18 19:53:18.973692'),(76,'wagtaildocs','0004_capitalizeverbose','2020-04-18 19:53:19.248605'),(77,'wagtaildocs','0005_document_collection','2020-04-18 19:53:19.467572'),(78,'wagtaildocs','0006_copy_document_permissions_to_collections','2020-04-18 19:53:19.533280'),(79,'wagtaildocs','0005_alter_uploaded_by_user_on_delete_action','2020-04-18 19:53:19.765997'),(80,'wagtaildocs','0007_merge','2020-04-18 19:53:19.775593'),(81,'wagtaildocs','0008_document_file_size','2020-04-18 19:53:19.905083'),(82,'wagtaildocs','0009_document_verbose_name_plural','2020-04-18 19:53:19.930696'),(83,'wagtaildocs','0010_document_file_hash','2020-04-18 19:53:20.062535'),(84,'wagtailembeds','0001_initial','2020-04-18 19:53:20.185023'),(85,'wagtailembeds','0002_add_verbose_names','2020-04-18 19:53:20.197582'),(86,'wagtailembeds','0003_capitalizeverbose','2020-04-18 19:53:20.206817'),(87,'wagtailembeds','0004_embed_verbose_name_plural','2020-04-18 19:53:20.216579'),(88,'wagtailembeds','0005_specify_thumbnail_url_max_length','2020-04-18 19:53:20.417194'),(89,'wagtailforms','0001_initial','2020-04-18 19:53:20.507409'),(90,'wagtailforms','0002_add_verbose_names','2020-04-18 19:53:20.712759'),(91,'wagtailforms','0003_capitalizeverbose','2020-04-18 19:53:20.732743'),(92,'wagtailforms','0004_add_verbose_name_plural','2020-04-18 19:53:20.744236'),(93,'wagtailimages','0001_initial','2020-04-18 19:53:21.074057'),(94,'wagtailimages','0002_initial_data','2020-04-18 19:53:21.082570'),(95,'wagtailimages','0003_fix_focal_point_fields','2020-04-18 19:53:21.085300'),(96,'wagtailimages','0004_make_focal_point_key_not_nullable','2020-04-18 19:53:21.095105'),(97,'wagtailimages','0005_make_filter_spec_unique','2020-04-18 19:53:21.104723'),(98,'wagtailimages','0006_add_verbose_names','2020-04-18 19:53:21.114425'),(99,'wagtailimages','0007_image_file_size','2020-04-18 19:53:21.124136'),(100,'wagtailimages','0008_image_created_at_index','2020-04-18 19:53:21.133929'),(101,'wagtailimages','0009_capitalizeverbose','2020-04-18 19:53:21.143562'),(102,'wagtailimages','0010_change_on_delete_behaviour','2020-04-18 19:53:21.153376'),(103,'wagtailimages','0011_image_collection','2020-04-18 19:53:21.162929'),(104,'wagtailimages','0012_copy_image_permissions_to_collections','2020-04-18 19:53:21.172623'),(105,'wagtailimages','0013_make_rendition_upload_callable','2020-04-18 19:53:21.182471'),(106,'wagtailimages','0014_add_filter_spec_field','2020-04-18 19:53:21.191993'),(107,'wagtailimages','0015_fill_filter_spec_field','2020-04-18 19:53:21.201889'),(108,'wagtailimages','0016_deprecate_rendition_filter_relation','2020-04-18 19:53:21.211810'),(109,'wagtailimages','0017_reduce_focal_point_key_max_length','2020-04-18 19:53:21.221451'),(110,'wagtailimages','0018_remove_rendition_filter','2020-04-18 19:53:21.231562'),(111,'wagtailimages','0019_delete_filter','2020-04-18 19:53:21.241839'),(112,'wagtailimages','0020_add-verbose-name','2020-04-18 19:53:21.251469'),(113,'wagtailimages','0021_image_file_hash','2020-04-18 19:53:21.260995'),(114,'wagtailredirects','0001_initial','2020-04-18 19:53:22.033651'),(115,'wagtailredirects','0002_add_verbose_names','2020-04-18 19:53:22.693828'),(116,'wagtailredirects','0003_make_site_field_editable','2020-04-18 19:53:22.944293'),(117,'wagtailredirects','0004_set_unique_on_path_and_site','2020-04-18 19:53:23.078391'),(118,'wagtailredirects','0005_capitalizeverbose','2020-04-18 19:53:23.687178'),(119,'wagtailredirects','0006_redirect_increase_max_length','2020-04-18 19:53:23.915294'),(120,'wagtailsearch','0001_initial','2020-04-18 19:53:24.420444'),(121,'wagtailsearch','0002_add_verbose_names','2020-04-18 19:53:25.065837'),(122,'wagtailsearch','0003_remove_editors_pick','2020-04-18 19:53:25.104929'),(123,'wagtailsearch','0004_querydailyhits_verbose_name_plural','2020-04-18 19:53:25.111280'),(124,'wagtailusers','0001_initial','2020-04-18 19:53:25.216840'),(125,'wagtailusers','0002_add_verbose_name_on_userprofile','2020-04-18 19:53:25.448113'),(126,'wagtailusers','0003_add_verbose_names','2020-04-18 19:53:25.463986'),(127,'wagtailusers','0004_capitalizeverbose','2020-04-18 19:53:25.520089'),(128,'wagtailusers','0005_make_related_name_wagtail_specific','2020-04-18 19:53:25.737007'),(129,'wagtailusers','0006_userprofile_prefered_language','2020-04-18 19:53:25.875609'),(130,'wagtailusers','0007_userprofile_current_time_zone','2020-04-18 19:53:25.996635'),(131,'wagtailusers','0008_userprofile_avatar','2020-04-18 19:53:26.127494'),(132,'wagtailusers','0009_userprofile_verbose_name_plural','2020-04-18 19:53:26.144471'),(133,'wagtailimages','0001_squashed_0021','2020-04-18 19:53:26.151030'),(134,'wagtailcore','0001_squashed_0016_change_page_url_path_to_text_field','2020-04-18 19:53:26.157669'),(135,'donations','0002_auto_20200419_1126','2020-04-19 11:26:46.695773'),(136,'home','0003_homepage_body','2020-04-21 09:25:44.936702'),(137,'home','0004_auto_20200421_0954','2020-04-21 09:54:14.564340'),(138,'home','0005_auto_20200421_1051','2020-04-21 10:51:11.394764'),(139,'home','0005_auto_20200421_1142','2020-04-21 11:42:30.836162'),(140,'home','0006_auto_20200421_1848','2020-04-21 18:48:52.024597'),(141,'home','0007_auto_20200421_1852','2020-04-21 18:52:10.979428'),(142,'home','0008_auto_20200421_1907','2020-04-21 19:07:11.911154'),(143,'home','0009_auto_20200422_0904','2020-04-22 09:04:10.559913'),(144,'home','0010_auto_20200422_0931','2020-04-22 09:31:05.093162'),(145,'home','0011_auto_20200422_0934','2020-04-22 09:34:36.794887'),(146,'home','0012_auto_20200422_1055','2020-04-22 10:55:47.464327'),(147,'home','0013_auto_20200422_1058','2020-04-22 10:58:16.582263'),(148,'home','0014_auto_20200422_1119','2020-04-22 11:19:14.629568'),(149,'home','0015_auto_20200422_1124','2020-04-22 11:24:21.710147'),(150,'home','0016_auto_20200422_1126','2020-04-22 11:26:22.283450'),(151,'home','0017_auto_20200422_1216','2020-04-22 12:16:20.572096'),(152,'site_settings','0002_appearancesettings','2020-04-22 14:50:04.229276'),(153,'home','0018_auto_20200422_1626','2020-04-22 16:26:27.975467'),(154,'donations','0003_auto_20200423_0855','2020-04-23 08:55:15.055384'),(155,'donations','0004_paymentgateway_frontend_label','2020-04-23 09:07:10.456976'),(156,'donations','0005_donationform_footer_text','2020-04-23 16:36:02.372276'),(157,'custom_user','0002_user_opt_in_mailing_list','2020-04-25 11:47:00.397264');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4m6m6s67by92hvp7krl9worwfh4wzmzk','MWZmZWY1NmM0YTI1YzJkOTViN2JkMmY1MmRiYjI2ZDk5ZjAwNjk2NTp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxOX0=','2020-05-03 20:02:01.474171'),('5ztqbt7rhk0ryd79u2xa9apc7aumj22n','ZmFiYTQyNGVhZGFkMjc4Mzg2ODI4NTQwMDkwNGJkYzM4ZTUxM2M3Yzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxNzUwOTBlYmIzZGFhYTVjMGY4YWE5YjA5OGM5MjlmZGI0YTk1N2NiIn0=','2020-05-11 09:27:47.250634'),('6i0rl6vrn1xrm3m5vjih5gnr3s2a6buv','OTBkODhiMjljYjczMmE5MjU2NzMzMjZhM2M0Yzk2YjIyYzY5NTUyZDp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxM30=','2020-05-03 18:55:09.130065'),('autnk1iu3p6ltcodayrkw94a9o0a1xfh','MDc4MWJkMmFhOGY1ZGY3YzExYjljY2QxZjkwMDIxZWM4NDgyNTE2MDp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0NSwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjdiZGQxNDI5MjhmZWQzNzE3OWYwNzlmNzMxNDlmZjY5MmY5OTEzM2EifQ==','2020-05-12 11:56:25.912009'),('b9d6x5k9m7klg5332v2wfocyy0u93z6c','ZTliOGZhM2ZkNzdiNGM3MDk2MzAyOTE2OGJhZjU3OGNiY2FmNjhlNTp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoyM30=','2020-05-04 09:12:24.736103'),('dsi3e4cryfqo8xn6oa37b1uvr90f9xdk','ZTI1ZjJmOWJlZjdmZDI4ODMxYWI1MjEyNTgzYmZlMTVjNTZmMWI5NDp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoyMn0=','2020-05-04 08:48:26.401595'),('e7ct25afnso3e2066cbk5fhrkebbak4g','OWM4ZmRiMzdlNzY1ZWI5ZWFhZTE3YWEzMWVkZmYzNjc0ODRjY2NiYjp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0MSwiX2F1dGhfdXNlcl9pZCI6IjIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYzQ4OGJjZmMyNGFkOTRmMTI5OTRkNDNjY2ZjZDkyNTZjMDQzN2Y0In0=','2020-05-11 09:37:15.946544'),('ev70cgfbfuff90unmvmx9mp07hawt02p','ZjI5NTViZjdlYmY5YTNjZjYxMzVkMmJmNzFjYzFlZWZkYjlkZTNkNzp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxNH0=','2020-05-03 19:01:09.569707'),('fuhkvf2ilsqaosxu8k1qfi071s7lnj4c','MGViMzkzZTI5ZTA5ZjUxMGUzYzk3YWJmNTI0ODIzOTJjNjhkNTYwODp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo1LCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYjExN2E0MWQyMDY4NjVjYzk3YjQwZDgzYzkyN2RkOGU1YTlmNmVhYiJ9','2020-05-03 12:17:24.981160'),('g3tpied39zagih4wekpqkdbxyj6iloi0','NzJiZTMxMzJkNjJkMzkzMGE4YzQ2ZWVlMTdiYzczZWMwOTJmYTI0MDp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0Nn0=','2020-05-12 11:46:07.883824'),('gcprfqqwaglu8zxadfg0dcz2s6e67520','ODBhMGM3MTA5MTBhZjM1OTRhYjhlZmVjZmRkMTJhMjE4MjJlMDQ2YTp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxMCwiX2F1dGhfdXNlcl9pZCI6IjUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhjOTI2ODQ2MGI3NjNjNzdiZTYzMTNiODYwODZiZDI2ZTNlZjcwMDAifQ==','2020-05-03 17:43:35.802500'),('hy9kurc26hpmnmpcfw6yab3w1xgjx7ih','OTY2ODBiMzg0NDJmZDU1OWIyMTVhMjZiMDdlOTcxOWM3YzQ3ZDAxNzp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0M30=','2020-05-11 12:09:33.023472'),('knqetn6x6gb3vv4ccip2xhlcljb21pvm','OGRhMGU3MjA5Njk4YTkyMzg2ZmNkODRmZDM3MTgwODk2MDc3OWQ4YTp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxMn0=','2020-05-03 18:47:41.843747'),('m3c7f1ojlsqjjz74l3m7ra9rg9as2ui1','NTg5ZDUxYzE1ZTc2NzAyZmFmYzVlZGFhNmQ4ZDgzOWVkM2NiNGZkNTp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0fQ==','2020-05-03 12:16:18.208911'),('n3x1fpuaf3ew2frevj3orbnq9o7f2zhn','NGU1M2I5YmIyNjg3ZGEzMTczN2U3ZDkwOTk0YWFjNGI3YWY5ZGU4Nzp7InRoYW5reW91LWRvbmF0aW9uLWlkIjozfQ==','2020-05-03 12:05:39.020576'),('pmejxqv08zlmh5ev5m1p4h6ew6dnjobm','NjRkZDQxM2RhMTBlNWVhMzI0ODY3NTAxOGJmN2Y3OGVkZDIzZTA4MDp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxNX0=','2020-05-03 19:03:55.416685'),('q4y9azcbxeoibv690cr58kvi9oio81u6','NDY3OWQ0ZjdiZWFhZDIxMzg0NjdjZWJjMTllMDFlNTAzNDVmMzAxMzp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0MH0=','2020-05-11 09:31:42.872614'),('s5b0fplsd7kztp8lyllklyci3ncerpr3','MmYzODMzZDg3YWIyNWQ4MDhlZGZlOGMxZmEzZjc4ZjI4NmJkMmMwMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3YmRkMTQyOTI4ZmVkMzcxNzlmMDc5ZjczMTQ5ZmY2OTJmOTkxMzNhIiwid2FndGFpbC1wcmV2aWV3LTMiOlsiY3NyZm1pZGRsZXdhcmV0b2tlbj13TDZwalNRYmY2aW5lYk90NWlZNXlGMGdQNDJBeUl6cGlseHZyR3I0akU3anVYeWNLaHFNZ3hOYU9iS0Y0ZjhzJm5leHQ9JnRpdGxlPUhvbWUmYm9keS1jb3VudD02JmJvZHktMC1kZWxldGVkPSZib2R5LTAtb3JkZXI9MCZib2R5LTAtdHlwZT1mdWxsX3dpZHRoX3NlY3Rpb24mYm9keS0wLWlkPSZib2R5LTAtdmFsdWUtd2lkdGhfY3NzPWNvbnRhaW5lci10aWdodCZib2R5LTAtdmFsdWUtYmFja2dyb3VuZF9jb2xvcl9jc3M9YmctcHJpbWFyeSZib2R5LTAtdmFsdWUtY29udGVudC1jb3VudD0xJmJvZHktMC12YWx1ZS1jb250ZW50LTAtZGVsZXRlZD0mYm9keS0wLXZhbHVlLWNvbnRlbnQtMC1vcmRlcj0wJmJvZHktMC12YWx1ZS1jb250ZW50LTAtdHlwZT1zaW5nbGVfY29sdW1uX3JvdyZib2R5LTAtdmFsdWUtY29udGVudC0wLWlkPSZib2R5LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWFsaWdubWVudF9jc3M9Y29sdW1uLWhvcnotYWxpZ24tY2VudGVyJmJvZHktMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC1jb3VudD0yJmJvZHktMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLWRlbGV0ZWQ9JmJvZHktMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtdHlwZT1oZWFkaW5nX2Jsb2NrJmJvZHktMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLWlkPSZib2R5LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1oZWFkaW5nX3NpemU9aDEmYm9keS0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtaGVhZGluZ190ZXh0PUhlbGxvK3RoaXMraXMrYStibG9jayZib2R5LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS1kZWxldGVkPSZib2R5LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS1vcmRlcj0xJmJvZHktMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0xLXR5cGU9dGV4dF9ibG9jayZib2R5LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS1pZD0mYm9keS0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtdmFsdWU9JTdCJTIyYmxvY2tzJTIyJTNBJTVCJTdCJTIya2V5JTIyJTNBJTIyenQ3NW0lMjIlMkMlMjJ0ZXh0JTIyJTNBJTIyVGV4dCtjb250ZW50JTIyJTJDJTIydHlwZSUyMiUzQSUyMnVuc3R5bGVkJTIyJTJDJTIyZGVwdGglMjIlM0EwJTJDJTIyaW5saW5lU3R5bGVSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJlbnRpdHlSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJkYXRhJTIyJTNBJTdCJTdEJTdEJTVEJTJDJTIyZW50aXR5TWFwJTIyJTNBJTdCJTdEJTdEJmJvZHktMS1kZWxldGVkPSZib2R5LTEtb3JkZXI9MSZib2R5LTEtdHlwZT1mdWxsX3dpZHRoX2ltYWdlJmJvZHktMS1pZD1iM2JhYWRhYS05NTRmLTQzNGUtYTBkZS1jOGJhZTZlMTJiN2EmYm9keS0xLXZhbHVlLWJhbm5lcj00JmJvZHktMi1kZWxldGVkPSZib2R5LTItb3JkZXI9MiZib2R5LTItdHlwZT1mdWxsX3dpZHRoX3NlY3Rpb24mYm9keS0yLWlkPTBkYmIxNjQ1LWUxNzQtNDIwNS04ZGViLWFiZDIwZWI1OWI1NSZib2R5LTItdmFsdWUtd2lkdGhfY3NzPWNvbnRhaW5lci10aWdodCZib2R5LTItdmFsdWUtYmFja2dyb3VuZF9jb2xvcl9jc3M9JmJvZHktMi12YWx1ZS1jb250ZW50LWNvdW50PTImYm9keS0yLXZhbHVlLWNvbnRlbnQtMC1kZWxldGVkPSZib2R5LTItdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS0yLXZhbHVlLWNvbnRlbnQtMC10eXBlPXNpbmdsZV9jb2x1bW5fcm93JmJvZHktMi12YWx1ZS1jb250ZW50LTAtaWQ9NjIwOGYzNjUtYmRiNS00NmMxLTlkNTItYzUzMzcxYTNjZWU0JmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtYWxpZ25tZW50X2Nzcz1jb2x1bW4taG9yei1hbGlnbi1jZW50ZXImYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LWNvdW50PTQmYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtZGVsZXRlZD0mYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtb3JkZXI9MCZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC10eXBlPWhlYWRpbmdfYmxvY2smYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtaWQ9YjU3ZTI5ZWMtYjczZS00Y2QzLWI5YjktY2M1MDI3MWZlNjUxJmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWhlYWRpbmdfc2l6ZT1oMSZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1oZWFkaW5nX3RleHQ9U3VwcG9ydCtIb25nK0tvbmcrRnJlZStQcmVzcyZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS1kZWxldGVkPSZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS1vcmRlcj0xJmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0xLXR5cGU9dGV4dF9ibG9jayZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS1pZD00ZjkxYjM3Mi00MzM5LTQ1MDEtYWIyMS0wMjdlZGEyZWQ3YWYmYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtdmFsdWU9JTdCJTIyYmxvY2tzJTIyJTNBJTVCJTdCJTIya2V5JTIyJTNBJTIydmlvMWwlMjIlMkMlMjJ0ZXh0JTIyJTNBJTIyV2hpbHN0K0VuZ2xpc2gtbGFuZ3VhZ2Uram91cm5hbGlzbStpbitIb25nK0tvbmcrY2FuK2JlK3RvdWdoK2FuZCtleHBlbnNpdmUlMkMrc3VwcG9ydGluZyt1cytuZWVkbiVFMiU4MCU5OXQrYmUlMjErSW4ranVzdCthK2NvdXBsZStvZittaW51dGVzJTJDK3lvdStjYW4rZW5zdXJlK291citpbmRlcGVuZGVuY2UrYW5kK2hlbHArc2FmZWd1YXJkK3ByZXNzK2ZyZWVkb20rd2l0aCthK2RvbmF0aW9uK3RvK0hLRlAuJTIyJTJDJTIydHlwZSUyMiUzQSUyMnVuc3R5bGVkJTIyJTJDJTIyZGVwdGglMjIlM0EwJTJDJTIyaW5saW5lU3R5bGVSYW5nZXMlMjIlM0ElNUIlN0IlMjJvZmZzZXQlMjIlM0ExMzElMkMlMjJsZW5ndGglMjIlM0E4OCUyQyUyMnN0eWxlJTIyJTNBJTIyQk9MRCUyMiU3RCU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmRhdGElMjIlM0ElN0IlN0QlN0QlNUQlMkMlMjJlbnRpdHlNYXAlMjIlM0ElN0IlN0QlN0QmYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTItZGVsZXRlZD0mYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTItb3JkZXI9MiZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMi10eXBlPXRleHRfYmxvY2smYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTItaWQ9YTg3OTcyYTYtN2QxYy00MjU1LWJhZDgtMDYzZWEwODY2NDIyJmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0yLXZhbHVlPSU3QiUyMmJsb2NrcyUyMiUzQSU1QiU3QiUyMmtleSUyMiUzQSUyMmFlbHRiJTIyJTJDJTIydGV4dCUyMiUzQSUyMk5vdC1mb3ItcHJvZml0JTJDK3J1bitieStqb3VybmFsaXN0cythbmQrY29tcGxldGVseStpbmRlcGVuZGVudCUyQyt0aGUrSEtGUCt0ZWFtK3JlbGllcytvbityZWFkZXJzK3RvK2tlZXArdXMrZ29pbmcrYW5kK3RvK2hlbHArc2FmZWd1YXJkK3ByZXNzK2ZyZWVkb20uK0xlYXJuK21vcmUrYWJvdXQrb3VyK2FjaGlldmVtZW50cytpbitvdXIrbGF0ZXN0K0FubnVhbCtSZXBvcnQuK091citUcmFuc3BhcmVuY3krUmVwb3J0K3Nob3dzK2hvdytjYXJlZnVsbHkrd2Urc3BlbmQrZXZlcnkrY2VudC4lMjIlMkMlMjJ0eXBlJTIyJTNBJTIydW5zdHlsZWQlMjIlMkMlMjJkZXB0aCUyMiUzQTAlMkMlMjJpbmxpbmVTdHlsZVJhbmdlcyUyMiUzQSU1QiU3QiUyMm9mZnNldCUyMiUzQTAlMkMlMjJsZW5ndGglMjIlM0E2MSUyQyUyMnN0eWxlJTIyJTNBJTIyQk9MRCUyMiU3RCU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmRhdGElMjIlM0ElN0IlN0QlN0QlNUQlMkMlMjJlbnRpdHlNYXAlMjIlM0ElN0IlN0QlN0QmYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtZGVsZXRlZD0mYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtb3JkZXI9MyZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy10eXBlPWJ1dHRvbnNfYmxvY2smYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtaWQ9Zjk3OWQyNDMtOGU1NC00YjBjLWIwOTItYTY3ZWI1NGQ0YTZlJmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLWNvdW50PTImYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMC1kZWxldGVkPSZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0wLW9yZGVyPTAmYm9keS0yLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMC12YWx1ZS1idXR0b25fdGV4dD1Eb25hdGUrdG8rSEtGUCZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0wLXZhbHVlLWJ1dHRvbl9saW5rPWh0dHBzJTNBJTJGJTJGZ2l2ZWh5YnJpZC5zeXRlcy5uZXQlMkZkb25hdGlvbnMlMkZvbmV0aW1lLWRvbmF0aW9uJmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTAtdmFsdWUtdGFyZ2V0X3dpbmRvdz1fc2VsZiZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0xLWRlbGV0ZWQ9JmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTEtb3JkZXI9MSZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0xLXZhbHVlLWJ1dHRvbl90ZXh0PTEyK3dheXMrdG8rc3VwcG9ydCZib2R5LTItdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0xLXZhbHVlLWJ1dHRvbl9saW5rPWh0dHBzJTNBJTJGJTJGZ2l2ZWh5YnJpZC5zeXRlcy5uZXQlMkZkb25hdGlvbnMlMkZvbmV0aW1lLWRvbmF0aW9uJmJvZHktMi12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTEtdmFsdWUtdGFyZ2V0X3dpbmRvdz1fc2VsZiZib2R5LTItdmFsdWUtY29udGVudC0xLWRlbGV0ZWQ9JmJvZHktMi12YWx1ZS1jb250ZW50LTEtb3JkZXI9MSZib2R5LTItdmFsdWUtY29udGVudC0xLXR5cGU9c2luZ2xlX2NvbHVtbl9yb3cmYm9keS0yLXZhbHVlLWNvbnRlbnQtMS1pZD0xMDI4Y2UzYy0wM2ZhLTQ1OTItYWFmYy0wMTEyYmZlY2UyYjQmYm9keS0yLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1hbGlnbm1lbnRfY3NzPWNvbHVtbi1ob3J6LWFsaWduLWNlbnRlciZib2R5LTItdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtY291bnQ9MSZib2R5LTItdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtMC1kZWxldGVkPSZib2R5LTItdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtMC1vcmRlcj0wJmJvZHktMi12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29udGVudC0wLXR5cGU9aHRtbF9ibG9jayZib2R5LTItdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtMC1pZD03ZWU2MzdiNy02YWE3LTQ3NjctOTdmMS1kMjRmNTYwZDcwYTEmYm9keS0yLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdmFsdWU9JTNDaWZyYW1lK3dpZHRoJTNEJTIyNzk0JTIyK2hlaWdodCUzRCUyMjQ2NiUyMitzcmMlM0QlMjJodHRwcyUzQSUyRiUyRnd3dy55b3V0dWJlLmNvbSUyRmVtYmVkJTJGSWhPTXpXRlpySXclMjIrZnJhbWVib3JkZXIlM0QlMjIwJTIyK2FsbG93JTNEJTIyYWNjZWxlcm9tZXRlciUzQithdXRvcGxheSUzQitlbmNyeXB0ZWQtbWVkaWElM0IrZ3lyb3Njb3BlJTNCK3BpY3R1cmUtaW4tcGljdHVyZSUyMithbGxvd2Z1bGxzY3JlZW4lM0UlM0MlMkZpZnJhbWUlM0UmYm9keS0zLWRlbGV0ZWQ9JmJvZHktMy1vcmRlcj0zJmJvZHktMy10eXBlPWZ1bGxfd2lkdGhfc2VjdGlvbiZib2R5LTMtaWQ9MWJkOTc4OTEtODE2MS00NjE2LWIwMzQtZmQ1YzU5M2Q3NzU4JmJvZHktMy12YWx1ZS13aWR0aF9jc3M9Y29udGFpbmVyJmJvZHktMy12YWx1ZS1iYWNrZ3JvdW5kX2NvbG9yX2Nzcz1iZy1wcmltYXJ5LWxpZ2h0JmJvZHktMy12YWx1ZS1jb250ZW50LWNvdW50PTImYm9keS0zLXZhbHVlLWNvbnRlbnQtMC1kZWxldGVkPSZib2R5LTMtdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS0zLXZhbHVlLWNvbnRlbnQtMC10eXBlPXNpbmdsZV9jb2x1bW5fcm93JmJvZHktMy12YWx1ZS1jb250ZW50LTAtaWQ9MzQ3MGFiY2MtOGQxYy00NzAzLWJjYTktOGQ4ZWVkOTMxYTVhJmJvZHktMy12YWx1ZS1jb250ZW50LTAtdmFsdWUtYWxpZ25tZW50X2Nzcz1jb2x1bW4taG9yei1hbGlnbi1jZW50ZXImYm9keS0zLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LWNvdW50PTEmYm9keS0zLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtZGVsZXRlZD0mYm9keS0zLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtb3JkZXI9MCZib2R5LTMtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC10eXBlPWhlYWRpbmdfYmxvY2smYm9keS0zLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtaWQ9NDI1NjM3NmUtNjU1NS00N2QxLThhOWEtNTFlMDkyNDBhZWMzJmJvZHktMy12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWhlYWRpbmdfc2l6ZT1oMSZib2R5LTMtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1oZWFkaW5nX3RleHQ9V2h5K3RydXN0K3VzJTNGJmJvZHktMy12YWx1ZS1jb250ZW50LTEtZGVsZXRlZD0mYm9keS0zLXZhbHVlLWNvbnRlbnQtMS1vcmRlcj0xJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdHlwZT10d29fY29sdW1uX3JvdyZib2R5LTMtdmFsdWUtY29udGVudC0xLWlkPTYxMzk1NjAwLWQzNGYtNDU2ZS05YTAyLTQ1NGE1OWNkNmM3MyZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWFsaWdubWVudF9jc3M9Y29sdW1uLWhvcnotYWxpZ24tc3RhcnQmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS1jb3VudD00JmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMC1kZWxldGVkPSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTAtb3JkZXI9MCZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTAtdHlwZT1oZWFkaW5nX2Jsb2NrJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMC1pZD0wZTE0ZWNiMi01YTJlLTQ2ZWUtYTQwYi02MTYzNzkzZWQ2NDcmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS0wLXZhbHVlLWhlYWRpbmdfc2l6ZT1oNCZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTAtdmFsdWUtaGVhZGluZ190ZXh0PUltbXVuZSt0bytjZW5zb3JzaGlwJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMS1kZWxldGVkPSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTEtb3JkZXI9MSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTEtdHlwZT10ZXh0X2Jsb2NrJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMS1pZD1kYzlkNjAwZS01NmY0LTRmNDYtYmI3My1iMTBlNmM5MGYzNTUmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS0xLXZhbHVlPSU3QiUyMmJsb2NrcyUyMiUzQSU1QiU3QiUyMmtleSUyMiUzQSUyMndvbmxwJTIyJTJDJTIydGV4dCUyMiUzQSUyMkhLRlAraXMrYW5zd2VyYWJsZStvbmx5K3RvK3JlYWRlcnMrJUUyJTgwJTkzK3dlK2hhdmUrbm8raW52ZXN0b3JzJTJDK25vK3NoYXJlaG9sZGVycyUyQytubyt0eWNvb25zJTJDK25vK21haW5sYW5kK293bmVycytvcit1bWJyZWxsYStjb21wYW55K2JlaGluZCt1cy4rT3VyK2luZGVwZW5kZW5jZSttZWFucyt3ZSthcmUrZnVsbHkrcmVzaXN0YW50K3RvK2NlbnNvcnNoaXArYW5kK3NlbGYtY2Vuc29yc2hpcC4lMjIlMkMlMjJ0eXBlJTIyJTNBJTIydW5zdHlsZWQlMjIlMkMlMjJkZXB0aCUyMiUzQTAlMkMlMjJpbmxpbmVTdHlsZVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmRhdGElMjIlM0ElN0IlN0QlN0QlNUQlMkMlMjJlbnRpdHlNYXAlMjIlM0ElN0IlN0QlN0QmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS0yLWRlbGV0ZWQ9JmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMi1vcmRlcj0yJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMi10eXBlPWhlYWRpbmdfYmxvY2smYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS0yLWlkPTMyZjM3Mjk4LTBlZWYtNDRiMC04ODFiLTFiZTk5MTdjNmE4MSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTItdmFsdWUtaGVhZGluZ19zaXplPWg0JmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMi12YWx1ZS1oZWFkaW5nX3RleHQ9VHJhbnNwYXJlbnQrJTI2K2VmZmljaWVudCZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTMtZGVsZXRlZD0mYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS0zLW9yZGVyPTMmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMS0zLXR5cGU9dGV4dF9ibG9jayZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8xLTMtaWQ9ZWVmN2RlOTUtMzE4MC00ZWY1LWIzZTAtMDAxMWFjZjVlMGUxJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzEtMy12YWx1ZT0lN0IlMjJibG9ja3MlMjIlM0ElNUIlN0IlMjJrZXklMjIlM0ElMjI3MndqbSUyMiUyQyUyMnRleHQlMjIlM0ElMjJXZSthcmUrdGhlK2NpdHklRTIlODAlOTlzK21vc3QrdHJhbnNwYXJlbnQrbmV3cytvdXRsZXQrJUUyJTgwJTkzK3dlK3VuZGVyZ28rYW4rZXh0ZXJuYWwrYXVkaXQrZWFjaCt5ZWFyK2FuZCtwdWJsaXNoK2FuK2FubnVhbCtUcmFuc3BhcmVuY3krUmVwb3J0Lis4NCtwZXIrY2VudCtvZitpbmNvbWUrY29tZXMrZnJvbStkb25hdGlvbnMlMkMrd2hpbHN0KzgxK3BlcitjZW50K29mK3NwZW5kaW5nK2dvZXMrc2ltcGx5K3Rvd2FyZHMrcGF5aW5nK2pvdXJuYWxpc3RzLitUZWFtd29yayUyQythdXRvbWF0aW9uJTJDK3BhcnRuZXJzaGlwcythbmQrdGhlK3VzZStvZitmcmVlK2RpZ2l0YWwrdG9vbHMra2VlcCtvdXIrY29zdHMrZG93bi4lMjIlMkMlMjJ0eXBlJTIyJTNBJTIydW5zdHlsZWQlMjIlMkMlMjJkZXB0aCUyMiUzQTAlMkMlMjJpbmxpbmVTdHlsZVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmRhdGElMjIlM0ElN0IlN0QlN0QlNUQlMkMlMjJlbnRpdHlNYXAlMjIlM0ElN0IlN0QlN0QmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi1jb3VudD00JmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMC1kZWxldGVkPSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTAtb3JkZXI9MCZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTAtdHlwZT1oZWFkaW5nX2Jsb2NrJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMC1pZD1lODlhY2YzZi02NmJkLTQ3ODktYjdlMy1kZDVkMzdjNTkxNzImYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi0wLXZhbHVlLWhlYWRpbmdfc2l6ZT1oNCZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTAtdmFsdWUtaGVhZGluZ190ZXh0PU5vbi1wcm9maXQrbW9kZWwmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi0xLWRlbGV0ZWQ9JmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMS1vcmRlcj0xJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMS10eXBlPXRleHRfYmxvY2smYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi0xLWlkPTMwOTk0ZjQwLTkyZTctNDM4MS1iOWQyLTRlMTc4ZTk2ZGI4MSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTEtdmFsdWU9JTdCJTIyYmxvY2tzJTIyJTNBJTVCJTdCJTIya2V5JTIyJTNBJTIyaXdlejUlMjIlMkMlMjJ0ZXh0JTIyJTNBJTIyQXMrYStub24tcHJvZml0JTJDK2xpbWl0ZWQrYnkrZ3VhcmFudGVlK2NvbXBhbnklMkMrYW55K3N1cnBsdXMrd2UrbWFrZStpcytyZWN5Y2xlZCtiYWNrK2ludG8rdGhlK2NvbXBhbnkuK1dlK2FyZStydW4rYnkram91cm5hbGlzdHMrYW5kK2ltbXVuZSt0bytjb21tZXJjaWFsK2FuZCtwb2xpdGljYWwrcHJlc3N1cmUuJTIyJTJDJTIydHlwZSUyMiUzQSUyMnVuc3R5bGVkJTIyJTJDJTIyZGVwdGglMjIlM0EwJTJDJTIyaW5saW5lU3R5bGVSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJlbnRpdHlSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJkYXRhJTIyJTNBJTdCJTdEJTdEJTVEJTJDJTIyZW50aXR5TWFwJTIyJTNBJTdCJTdEJTdEJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMi1kZWxldGVkPSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTItb3JkZXI9MiZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTItdHlwZT1oZWFkaW5nX2Jsb2NrJmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMi1pZD1lZTY3Y2JkMi0yYWQ5LTQxNDEtYjc4OC0xZDAzYzQ0YTdmZjImYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi0yLXZhbHVlLWhlYWRpbmdfc2l6ZT1oNCZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTItdmFsdWUtaGVhZGluZ190ZXh0PUFjY3VyYXRlKyUyNithY2NvdW50YWJsZSZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTMtZGVsZXRlZD0mYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi0zLW9yZGVyPTMmYm9keS0zLXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb2x1bW5fMi0zLXR5cGU9dGV4dF9ibG9jayZib2R5LTMtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbHVtbl8yLTMtaWQ9OGNjZDk0NTctM2FiNS00YTU2LTllYmEtMTg1ZTkzYTEwNDc1JmJvZHktMy12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29sdW1uXzItMy12YWx1ZT0lN0IlMjJibG9ja3MlMjIlM0ElNUIlN0IlMjJrZXklMjIlM0ElMjI1ZDF0bSUyMiUyQyUyMnRleHQlMjIlM0ElMjJXZStlbnN1cmUrZXZlcnl0aGluZyt3ZStwdWJsaXNoK2luY2x1ZGVzK2ErYmFsYW5jZStvZit2aWV3cG9pbnRzK2luK29yZGVyK3RvK2F2b2lkK2FueStiaWFzLitBbGwrZmFjdHMlMkMrcXVvdGVzK2FuZCtmaWd1cmVzK2FyZStwcm9wZXJseSthdHRyaWJ1dGVkK3RvK3RoZStzb3VyY2UlMkMrb2Z0ZW4rd2l0aCtsaW5rcyt0byt0aGUrb3JpZ2luYWwrbWF0ZXJpYWwuK091citvd24rb3BpbmlvbnMrYXJlK2tlcHQrb3V0K29mK291citjb3B5JTJDK3doaWxzdCt3ZSthY3QrcXVpY2tseSthbmQrdHJhbnNwYXJlbnRseSt0bytjb3JyZWN0K2Vycm9ycy4rSEtGUCthdm9pZHMrc2Vuc2F0aW9uYWxpc20rYW5kK2NsaWNrYmFpdCUyQythbmQrY2xlYXJseSttYXJrcytwYWlkLWZvcitjb250ZW50K2FzKyVFMiU4MCU5Q3Nwb25zb3JlZC4lRTIlODAlOUQrQWNjdXJhY3krYW5kK2ZhaXJuZXNzK2FyZStvdXIrdG9wK3ByaW9yaXRpZXMuJTIyJTJDJTIydHlwZSUyMiUzQSUyMnVuc3R5bGVkJTIyJTJDJTIyZGVwdGglMjIlM0EwJTJDJTIyaW5saW5lU3R5bGVSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJlbnRpdHlSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJkYXRhJTIyJTNBJTdCJTdEJTdEJTVEJTJDJTIyZW50aXR5TWFwJTIyJTNBJTdCJTdEJTdEJmJvZHktNC1kZWxldGVkPSZib2R5LTQtb3JkZXI9NCZib2R5LTQtdHlwZT1mdWxsX3dpZHRoX3NlY3Rpb24mYm9keS00LWlkPWY2NGIwY2E1LTZiNWUtNDA4ZC1hNTU0LWUyMWU5MGRkMjJlMyZib2R5LTQtdmFsdWUtd2lkdGhfY3NzPWNvbnRhaW5lci10aWdodCZib2R5LTQtdmFsdWUtYmFja2dyb3VuZF9jb2xvcl9jc3M9JmJvZHktNC12YWx1ZS1jb250ZW50LWNvdW50PTImYm9keS00LXZhbHVlLWNvbnRlbnQtMC1kZWxldGVkPSZib2R5LTQtdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS00LXZhbHVlLWNvbnRlbnQtMC10eXBlPXNpbmdsZV9jb2x1bW5fcm93JmJvZHktNC12YWx1ZS1jb250ZW50LTAtaWQ9MGY1MjI0OTYtNmM2ZS00YTg1LWI5M2QtOTY0YjU3ZTY1ZjMxJmJvZHktNC12YWx1ZS1jb250ZW50LTAtdmFsdWUtYWxpZ25tZW50X2Nzcz1jb2x1bW4taG9yei1hbGlnbi1jZW50ZXImYm9keS00LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LWNvdW50PTEmYm9keS00LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtZGVsZXRlZD0mYm9keS00LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtb3JkZXI9MCZib2R5LTQtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC10eXBlPWhlYWRpbmdfYmxvY2smYm9keS00LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtaWQ9MzExMTVjODItY2JhNS00NGVkLWJkOTUtNzVhYjliNjNlNWRjJmJvZHktNC12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLXZhbHVlLWhlYWRpbmdfc2l6ZT1oMSZib2R5LTQtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1oZWFkaW5nX3RleHQ9RkFRJmJvZHktNC12YWx1ZS1jb250ZW50LTEtZGVsZXRlZD0mYm9keS00LXZhbHVlLWNvbnRlbnQtMS1vcmRlcj0xJmJvZHktNC12YWx1ZS1jb250ZW50LTEtdHlwZT1zaW5nbGVfY29sdW1uX3JvdyZib2R5LTQtdmFsdWUtY29udGVudC0xLWlkPTUwOWI4MDU4LWU4YmItNDIzZC04MmVhLTJjOTEwOWE3NWY2OCZib2R5LTQtdmFsdWUtY29udGVudC0xLXZhbHVlLWFsaWdubWVudF9jc3M9Y29sdW1uLWhvcnotYWxpZ24tY2VudGVyJmJvZHktNC12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29udGVudC1jb3VudD0xJmJvZHktNC12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29udGVudC0wLWRlbGV0ZWQ9JmJvZHktNC12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdHlwZT1hY2NvcmRpb25fYmxvY2smYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtaWQ9NDViODRhYTQtODIzNC00ODVlLWFiMzMtNTU2YTQwOTI2MGFiJmJvZHktNC12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWl0ZW1zLWNvdW50PTImYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtaXRlbXMtMC1kZWxldGVkPSZib2R5LTQtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1pdGVtcy0wLW9yZGVyPTAmYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtaXRlbXMtMC12YWx1ZS1pdGVtX3RpdGxlPUkrbWFkZSthK3JlY3VycmluZyUyRnJlZ3VsYXIrZG9uYXRpb24uK0hvdytjYW4rSStjaGFuZ2Urb3IrY2FuY2VsK2l0JTNGJmJvZHktNC12YWx1ZS1jb250ZW50LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWl0ZW1zLTAtdmFsdWUtaXRlbV9jb250ZW50PSU3QiUyMmJsb2NrcyUyMiUzQSU1QiU3QiUyMmtleSUyMiUzQSUyMnIyZzEzJTIyJTJDJTIydGV4dCUyMiUzQSUyMllvdSttYXkrY2FuY2VsK3lvdXIrbW9udGhseStkb25hdGlvbithdCthbnkrdGltZStieStlbWFpbGluZytkb25hdGlvbnMlNDBob25na29uZ2ZwLmNvbSslRTIlODAlOTMrd2UrYWltK3RvK3Jlc3BvbmQrd2l0aGluKzEtMitidXNpbmVzcytkYXlzLitGcm9tK3RoZStlbWFpbCthZGRyZXNzK3lvdStzZXQrdXAreW91cityZWN1cnJpbmcrZG9uYXRpb24lMkMrc2ltcGx5K3N0YXRlKyVFMiU4MCU5Q0NBTkNFTCVFMiU4MCU5RCtpbit0aGUrc3ViamVjdCtsaW5lLislMjhXZStjYW5ub3QrY2hhbmdlK3lvdXIrcGF5bWVudCtkZXRhaWxzK29yK2Ftb3VudCslRTIlODAlOTMrcGxlYXNlK2NhbmNlbCt5b3VyK3JlZ3VsYXIrcGF5bWVudCthbmQrc2V0K3VwK2ErbmV3K29uZS4lMjkrSWYreW91K2RvbmF0ZWQrdmlhK1BheVBhbCUyQyt5b3UrbWF5K2NhbmNlbCUyRmFkanVzdCt0aGUrcGF5bWVudCt5b3Vyc2VsZi4lMjIlMkMlMjJ0eXBlJTIyJTNBJTIydW5zdHlsZWQlMjIlMkMlMjJkZXB0aCUyMiUzQTAlMkMlMjJpbmxpbmVTdHlsZVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmRhdGElMjIlM0ElN0IlN0QlN0QlNUQlMkMlMjJlbnRpdHlNYXAlMjIlM0ElN0IlN0QlN0QmYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtaXRlbXMtMS1kZWxldGVkPSZib2R5LTQtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1pdGVtcy0xLW9yZGVyPTEmYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtaXRlbXMtMS12YWx1ZS1pdGVtX3RpdGxlPVdpbGwreW91K3NoYXJlK29yK3NlbGwrbXkrcGVyc29uYWwraW5mb3JtYXRpb24lM0YmYm9keS00LXZhbHVlLWNvbnRlbnQtMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtaXRlbXMtMS12YWx1ZS1pdGVtX2NvbnRlbnQ9JTdCJTIyYmxvY2tzJTIyJTNBJTVCJTdCJTIya2V5JTIyJTNBJTIybzIyeHYlMjIlMkMlMjJ0ZXh0JTIyJTNBJTIyWW91K21heStjYW5jZWwreW91cittb250aGx5K2RvbmF0aW9uK2F0K2FueSt0aW1lK2J5K2VtYWlsaW5nK2RvbmF0aW9ucyU0MGhvbmdrb25nZnAuY29tKyVFMiU4MCU5Myt3ZSthaW0rdG8rcmVzcG9uZCt3aXRoaW4rMS0yK2J1c2luZXNzK2RheXMuK0Zyb20rdGhlK2VtYWlsK2FkZHJlc3MreW91K3NldCt1cCt5b3VyK3JlY3VycmluZytkb25hdGlvbiUyQytzaW1wbHkrc3RhdGUrJUUyJTgwJTlDQ0FOQ0VMJUUyJTgwJTlEK2luK3RoZStzdWJqZWN0K2xpbmUuKyUyOFdlK2Nhbm5vdCtjaGFuZ2UreW91citwYXltZW50K2RldGFpbHMrb3IrYW1vdW50KyVFMiU4MCU5MytwbGVhc2UrY2FuY2VsK3lvdXIrcmVndWxhcitwYXltZW50K2FuZCtzZXQrdXArYStuZXcrb25lLiUyOStJZit5b3UrZG9uYXRlZCt2aWErUGF5UGFsJTJDK3lvdSttYXkrY2FuY2VsJTJGYWRqdXN0K3RoZStwYXltZW50K3lvdXJzZWxmLiUyMiUyQyUyMnR5cGUlMjIlM0ElMjJ1bnN0eWxlZCUyMiUyQyUyMmRlcHRoJTIyJTNBMCUyQyUyMmlubGluZVN0eWxlUmFuZ2VzJTIyJTNBJTVCJTVEJTJDJTIyZW50aXR5UmFuZ2VzJTIyJTNBJTVCJTVEJTJDJTIyZGF0YSUyMiUzQSU3QiU3RCU3RCU1RCUyQyUyMmVudGl0eU1hcCUyMiUzQSU3QiU3RCU3RCZib2R5LTQtdmFsdWUtY29udGVudC0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1mb290ZXI9JTdCJTIyYmxvY2tzJTIyJTNBJTVCJTdCJTIya2V5JTIyJTNBJTIyeWVwOHolMjIlMkMlMjJ0ZXh0JTIyJTNBJTIyRGlkbiVFMiU4MCU5OXQrZmluZCt0aGUrYW5zd2VyK3lvdSt3ZXJlK2xvb2tpbmcrZm9yJTNGK0NvbnRhY3QrdXMlMjIlMkMlMjJ0eXBlJTIyJTNBJTIydW5zdHlsZWQlMjIlMkMlMjJkZXB0aCUyMiUzQTAlMkMlMjJpbmxpbmVTdHlsZVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU3QiUyMm9mZnNldCUyMiUzQTQ1JTJDJTIybGVuZ3RoJTIyJTNBMTAlMkMlMjJrZXklMjIlM0EwJTdEJTVEJTJDJTIyZGF0YSUyMiUzQSU3QiU3RCU3RCU1RCUyQyUyMmVudGl0eU1hcCUyMiUzQSU3QiUyMjAlMjIlM0ElN0IlMjJ0eXBlJTIyJTNBJTIyTElOSyUyMiUyQyUyMm11dGFiaWxpdHklMjIlM0ElMjJNVVRBQkxFJTIyJTJDJTIyZGF0YSUyMiUzQSU3QiUyMnVybCUyMiUzQSUyMmh0dHBzJTNBJTJGJTJGZ2l2ZWh5YnJpZC5zeXRlcy5uZXQlMkZjb250YWN0LXVzJTIyJTdEJTdEJTdEJTdEJmJvZHktNS1kZWxldGVkPSZib2R5LTUtb3JkZXI9NSZib2R5LTUtdHlwZT1mdWxsX3dpZHRoX3NlY3Rpb24mYm9keS01LWlkPTkxOWYwZDlmLTA1YzMtNDM5Yi05OTExLTE5YzZmMWFkNjc3NSZib2R5LTUtdmFsdWUtd2lkdGhfY3NzPWNvbnRhaW5lci10aWdodCZib2R5LTUtdmFsdWUtYmFja2dyb3VuZF9jb2xvcl9jc3M9YmctcHJpbWFyeSZib2R5LTUtdmFsdWUtY29udGVudC1jb3VudD0xJmJvZHktNS12YWx1ZS1jb250ZW50LTAtZGVsZXRlZD0mYm9keS01LXZhbHVlLWNvbnRlbnQtMC1vcmRlcj0wJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdHlwZT1zaW5nbGVfY29sdW1uX3JvdyZib2R5LTUtdmFsdWUtY29udGVudC0wLWlkPWI0OWJjY2MwLTI2ZGMtNDg0Ny04NjZjLTIzMDVmNmFlMmRmYyZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWFsaWdubWVudF9jc3M9Y29sdW1uLWhvcnotYWxpZ24tY2VudGVyJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC1jb3VudD00JmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLWRlbGV0ZWQ9JmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtdHlwZT1oZWFkaW5nX2Jsb2NrJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLWlkPTAwM2I4MGQ1LTdhYjYtNDNiMS04Mzc3LWVkNTU2NDViMmUzMiZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1oZWFkaW5nX3NpemU9aDEmYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtaGVhZGluZ190ZXh0PURvbmF0ZStOb3crdG8rSG9uZytLb25nK0ZyZWUrUHJlc3MmYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtZGVsZXRlZD0mYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtb3JkZXI9MSZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS10eXBlPXRleHRfYmxvY2smYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtaWQ9NTNmMDgwZTAtZDMzMi00NjNhLWI0NTktOTY3YmNjZWU3MmMwJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0xLXZhbHVlPSU3QiUyMmJsb2NrcyUyMiUzQSU1QiU3QiUyMmtleSUyMiUzQSUyMnNxNHYyJTIyJTJDJTIydGV4dCUyMiUzQSUyMlRoZStIS0ZQK3RlYW0rcmVsaWVzK29uK3JlYWRlcnMrdG8ra2VlcCt1cytnb2luZythbmQrdG8raGVscCtzYWZlZ3VhcmQrcHJlc3MrZnJlZWRvbS4rWW91K2NhbitlbnN1cmUrb3VyK2luZGVwZW5kZW5jZSthbmQraGVscCtzYWZlZ3VhcmQrcHJlc3MrZnJlZWRvbSt3aXRoK2ErZG9uYXRpb24rdG8rSEtGUC4lMjIlMkMlMjJ0eXBlJTIyJTNBJTIydW5zdHlsZWQlMjIlMkMlMjJkZXB0aCUyMiUzQTAlMkMlMjJpbmxpbmVTdHlsZVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmVudGl0eVJhbmdlcyUyMiUzQSU1QiU1RCUyQyUyMmRhdGElMjIlM0ElN0IlN0QlN0QlNUQlMkMlMjJlbnRpdHlNYXAlMjIlM0ElN0IlN0QlN0QmYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTItZGVsZXRlZD0mYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTItb3JkZXI9MiZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMi10eXBlPXBhZ2VicmVha2VyX2Jsb2NrJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0yLWlkPWZkZTMxODQ0LTczZDItNDQ5Zi05MTkxLTBiMDJkZjE3YWQ0NiZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMi12YWx1ZS13aWR0aF9jc3M9dy0xJTJGMiZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy1kZWxldGVkPSZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy1vcmRlcj0zJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXR5cGU9YnV0dG9uc19ibG9jayZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy1pZD0yMjI1ZWUwNi1hYjFlLTQ1ZmQtYmVhMi1jYzA3OWVkMzA1NGYmYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtY291bnQ9MSZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0wLWRlbGV0ZWQ9JmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTAtb3JkZXI9MCZib2R5LTUtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0wLXZhbHVlLWJ1dHRvbl90ZXh0PURvbmF0ZStOb3cmYm9keS01LXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMC12YWx1ZS1idXR0b25fbGluaz1odHRwcyUzQSUyRiUyRmdpdmVoeWJyaWQuc3l0ZXMubmV0JTJGZG9uYXRlJmJvZHktNS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTAtdmFsdWUtdGFyZ2V0X3dpbmRvdz1fc2VsZiZzbHVnPWhvbWUmc2VvX3RpdGxlPSZzZWFyY2hfZGVzY3JpcHRpb249JmdvX2xpdmVfYXQ9JmV4cGlyZV9hdD0iLDE1ODc5Nzc1MzcuOTYwMjQ0XX0=','2020-05-11 08:52:17.972030'),('syc2d033lc3r6ee92usgjbp88wph3mca','Mzk2MDcxNGNlMDVhODY1ZDQ5NmQyMDIzYTAwOGRmYmY2MjA2MzI2Mjp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxOH0=','2020-05-03 19:43:29.831411'),('u9h47uy9mqbkif4d4ecaxrmv203qhw8y','MDIyZTM1ZTM0Mzk0YzdmZTJmZDM1YjUxNTM0ZmVjOTYyZGQ3NDk2Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3YmRkMTQyOTI4ZmVkMzcxNzlmMDc5ZjczMTQ5ZmY2OTJmOTkxMzNhIiwid2FndGFpbC1wcmV2aWV3LTMiOlsiY3NyZm1pZGRsZXdhcmV0b2tlbj1HY2VVZ2luTFNNdWJ4NnVXYjBMa0U0ejNIcGRjOU5lYzZ2ZjViYVZyN1dqa0d3N3Z1UW5pWEltbW1telNyRHNHJm5leHQ9JnRpdGxlPUhvbWUmYm9keS1jb3VudD0yJmJvZHktMC1kZWxldGVkPSZib2R5LTAtb3JkZXI9MCZib2R5LTAtdHlwZT1mdWxsX3dpZHRoX2ltYWdlJmJvZHktMC1pZD1iM2JhYWRhYS05NTRmLTQzNGUtYTBkZS1jOGJhZTZlMTJiN2EmYm9keS0wLXZhbHVlLWJhbm5lcj00JmJvZHktMS1kZWxldGVkPSZib2R5LTEtb3JkZXI9MSZib2R5LTEtdHlwZT1mdWxsX3dpZHRoX3NlY3Rpb24mYm9keS0xLWlkPTBkYmIxNjQ1LWUxNzQtNDIwNS04ZGViLWFiZDIwZWI1OWI1NSZib2R5LTEtdmFsdWUtd2lkdGhfY3NzPWNvbnRhaW5lciZib2R5LTEtdmFsdWUtY29udGVudC1jb3VudD0xJmJvZHktMS12YWx1ZS1jb250ZW50LTAtZGVsZXRlZD0mYm9keS0xLXZhbHVlLWNvbnRlbnQtMC1vcmRlcj0wJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdHlwZT1zaW5nbGVfY29sdW1uX3JvdyZib2R5LTEtdmFsdWUtY29udGVudC0wLWlkPSZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWFsaWdubWVudF9jc3M9cmljaHRleHQtY2VudGVyJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC1jb3VudD00JmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLWRlbGV0ZWQ9JmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLW9yZGVyPTAmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtdHlwZT1oZWFkaW5nX2Jsb2NrJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0wLWlkPSZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1oZWFkaW5nX3NpemU9aDImYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTAtdmFsdWUtaGVhZGluZ190ZXh0PVN1cHBvcnQrSG9uZytLb25nK0ZyZWUrUHJlc3MmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtZGVsZXRlZD0mYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtb3JkZXI9MSZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMS10eXBlPXRleHRfYmxvY2smYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTEtaWQ9JmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0xLXZhbHVlPSU3QiUyMmJsb2NrcyUyMiUzQSU1QiU3QiUyMmtleSUyMiUzQSUyMnQ3c2w5JTIyJTJDJTIydGV4dCUyMiUzQSUyMldoaWxzdCtFbmdsaXNoLWxhbmd1YWdlK2pvdXJuYWxpc20raW4rSG9uZytLb25nK2NhbitiZSt0b3VnaCthbmQrZXhwZW5zaXZlJTJDK3N1cHBvcnRpbmcrdXMrbmVlZG4lRTIlODAlOTl0K2JlJTIxK0luK2p1c3QrYStjb3VwbGUrb2YrbWludXRlcyUyQyt5b3UrY2FuK2Vuc3VyZStvdXIraW5kZXBlbmRlbmNlK2FuZCtoZWxwK3NhZmVndWFyZCtwcmVzcytmcmVlZG9tK3dpdGgrYStkb25hdGlvbit0bytIS0ZQLiUyMiUyQyUyMnR5cGUlMjIlM0ElMjJ1bnN0eWxlZCUyMiUyQyUyMmRlcHRoJTIyJTNBMCUyQyUyMmlubGluZVN0eWxlUmFuZ2VzJTIyJTNBJTVCJTdCJTIyb2Zmc2V0JTIyJTNBMTMxJTJDJTIybGVuZ3RoJTIyJTNBODglMkMlMjJzdHlsZSUyMiUzQSUyMkJPTEQlMjIlN0QlNUQlMkMlMjJlbnRpdHlSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJkYXRhJTIyJTNBJTdCJTdEJTdEJTVEJTJDJTIyZW50aXR5TWFwJTIyJTNBJTdCJTdEJTdEJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0yLWRlbGV0ZWQ9JmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0yLW9yZGVyPTImYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTItdHlwZT10ZXh0X2Jsb2NrJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0yLWlkPSZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMi12YWx1ZT0lN0IlMjJibG9ja3MlMjIlM0ElNUIlN0IlMjJrZXklMjIlM0ElMjJqZmh4cSUyMiUyQyUyMnRleHQlMjIlM0ElMjJOb3QtZm9yLXByb2ZpdCUyQytydW4rYnkram91cm5hbGlzdHMrYW5kK2NvbXBsZXRlbHkraW5kZXBlbmRlbnQlMkMrdGhlK0hLRlArdGVhbStyZWxpZXMrb24rcmVhZGVycyt0bytrZWVwK3VzK2dvaW5nK2FuZCt0bytoZWxwK3NhZmVndWFyZCtwcmVzcytmcmVlZG9tLitMZWFybittb3JlK2Fib3V0K291cithY2hpZXZlbWVudHMraW4rb3VyK2xhdGVzdCtBbm51YWwrUmVwb3J0LitPdXIrVHJhbnNwYXJlbmN5K1JlcG9ydCtzaG93cytob3crY2FyZWZ1bGx5K3dlK3NwZW5kK2V2ZXJ5K2NlbnQuJTIyJTJDJTIydHlwZSUyMiUzQSUyMnVuc3R5bGVkJTIyJTJDJTIyZGVwdGglMjIlM0EwJTJDJTIyaW5saW5lU3R5bGVSYW5nZXMlMjIlM0ElNUIlN0IlMjJvZmZzZXQlMjIlM0EwJTJDJTIybGVuZ3RoJTIyJTNBNjElMkMlMjJzdHlsZSUyMiUzQSUyMkJPTEQlMjIlN0QlNUQlMkMlMjJlbnRpdHlSYW5nZXMlMjIlM0ElNUIlNUQlMkMlMjJkYXRhJTIyJTNBJTdCJTdEJTdEJTVEJTJDJTIyZW50aXR5TWFwJTIyJTNBJTdCJTdEJTdEJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLWRlbGV0ZWQ9JmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLW9yZGVyPTMmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdHlwZT1idXR0b25zX2Jsb2NrJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLWlkPSZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS1jb3VudD0yJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTAtZGVsZXRlZD0mYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMC1vcmRlcj0wJmJvZHktMS12YWx1ZS1jb250ZW50LTAtdmFsdWUtY29udGVudC0zLXZhbHVlLTAtdmFsdWUtYnV0dG9uX3RleHQ9RG9uYXRlK3RvK0hLRlAmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMC12YWx1ZS1idXR0b25fbGluaz1odHRwcyUzQSUyRiUyRmdpdmVoeWJyaWQuc3l0ZXMubmV0JTJGZG9uYXRpb25zJTJGb25ldGltZS1kb25hdGlvbiZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0wLXZhbHVlLXRhcmdldF93aW5kb3c9X3NlbGYmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMS1kZWxldGVkPSZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0xLW9yZGVyPTEmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMS12YWx1ZS1idXR0b25fdGV4dD0xMit3YXlzK3RvK3N1cHBvcnQmYm9keS0xLXZhbHVlLWNvbnRlbnQtMC12YWx1ZS1jb250ZW50LTMtdmFsdWUtMS12YWx1ZS1idXR0b25fbGluaz1odHRwcyUzQSUyRiUyRmdpdmVoeWJyaWQuc3l0ZXMubmV0JTJGZG9uYXRpb25zJTJGb25ldGltZS1kb25hdGlvbiZib2R5LTEtdmFsdWUtY29udGVudC0wLXZhbHVlLWNvbnRlbnQtMy12YWx1ZS0xLXZhbHVlLXRhcmdldF93aW5kb3c9X3NlbGYmc2x1Zz1ob21lJnNlb190aXRsZT0mc2VhcmNoX2Rlc2NyaXB0aW9uPSZnb19saXZlX2F0PSZleHBpcmVfYXQ9IiwxNTg3NTQ1MTAzLjIyODkyOThdfQ==','2020-05-06 08:45:03.349253'),('vw2w9mnkybud7po1tt554s70szu6no41','ZjdlY2ZmNzJiYjUzZTUxYmVmN2FkNDJiNGE3NTJmOGVhYjQ2ODFmNDp7InRoYW5reW91LWRvbmF0aW9uLWlkIjoxNn0=','2020-05-03 19:31:03.106817'),('wa1oyg2x3zowe0dos0dzqo4n6cwvkb39','ZGU2MzAxNjFhMzdhMDEzYzQ3NTZhMDk1NjkxODIyYjQ0YjJlNjFmODp7Il9hdXRoX3VzZXJfaWQiOiIxOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjFiMDg2MzkyMDk1NWYyY2Y4ODQyYjE2NmNhMTk5NzBjZTljNGEzOSJ9','2020-05-04 21:02:07.205246'),('xd2qvy0xd0ore1smqzqjhfy67bfisdx6','NGNiNDY4Yzk4NDUwNTdmZTZiZTI0NGUyNGQwMDI4ZmQ2YThjN2RmZjp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo0MiwiX2F1dGhfdXNlcl9pZCI6IjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE3NTA5MGViYjNkYWFhNWMwZjhhYTliMDk4YzkyOWZkYjRhOTU3Y2IifQ==','2020-05-11 09:54:07.890850'),('yhi2kd062cgeq0fmn4ce77n08j3gdw4v','NDEzZTFhZTJlNzY3Yzg1MGJhZDYyOWY2NGJkM2U4OGZiNzE5ZDk0MTp7InRoYW5reW91LWRvbmF0aW9uLWlkIjo4LCJfYXV0aF91c2VyX2lkIjoiNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzkzNmIxNjAyYTAzODhlYWExYjhmNDA5ODQ1ODIyNmFlNTg1OTZiNiJ9','2020-05-03 13:45:21.150177');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_amountstep`
--

DROP TABLE IF EXISTS `donations_amountstep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_amountstep` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `step` double NOT NULL,
  `form_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `donations_amountstep_form_id_step_91e3c5b7_uniq` (`form_id`,`step`),
  KEY `donations_amountstep_form_id_c712e4ed` (`form_id`),
  CONSTRAINT `donations_amountstep_form_id_c712e4ed_fk_donations` FOREIGN KEY (`form_id`) REFERENCES `donations_donationform` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_amountstep`
--

LOCK TABLES `donations_amountstep` WRITE;
/*!40000 ALTER TABLE `donations_amountstep` DISABLE KEYS */;
INSERT INTO `donations_amountstep` VALUES (4,12,1),(5,24,1),(6,36,1),(1,8,2),(2,18,2),(3,28,2);
/*!40000 ALTER TABLE `donations_amountstep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donation`
--

DROP TABLE IF EXISTS `donations_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(255) NOT NULL,
  `donation_amount` double NOT NULL,
  `is_recurring` tinyint(1) NOT NULL,
  `currency` varchar(20) NOT NULL,
  `is_create_account` tinyint(1) NOT NULL,
  `payment_status` varchar(255) NOT NULL,
  `recurring_status` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `donor_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `gateway_id` int(11) NOT NULL,
  `parent_donation_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`),
  KEY `donations_donation_donor_id_25b1f2bc_fk_donations_donor_id` (`donor_id`),
  KEY `donations_donation_form_id_799bcd7f_fk_donations_donationform_id` (`form_id`),
  KEY `donations_donation_gateway_id_a66d38dc_fk_donations` (`gateway_id`),
  KEY `donations_donation_parent_donation_id_b8c48105_fk_donations` (`parent_donation_id`),
  CONSTRAINT `donations_donation_donor_id_25b1f2bc_fk_donations_donor_id` FOREIGN KEY (`donor_id`) REFERENCES `donations_donor` (`id`),
  CONSTRAINT `donations_donation_form_id_799bcd7f_fk_donations_donationform_id` FOREIGN KEY (`form_id`) REFERENCES `donations_donationform` (`id`),
  CONSTRAINT `donations_donation_gateway_id_a66d38dc_fk_donations` FOREIGN KEY (`gateway_id`) REFERENCES `donations_paymentgateway` (`id`),
  CONSTRAINT `donations_donation_parent_donation_id_b8c48105_fk_donations` FOREIGN KEY (`parent_donation_id`) REFERENCES `donations_donation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donation`
--

LOCK TABLES `donations_donation` WRITE;
/*!40000 ALTER TABLE `donations_donation` DISABLE KEYS */;
INSERT INTO `donations_donation` VALUES (3,'3b9721b9ce58730f6ea0',15,0,'MYR',0,'complete','non-recurring','2020-04-19 12:04:51.426913','2020-04-19 12:05:38.982247',0,3,1,1,NULL),(4,'1b51b16d50323408068f',15,0,'MYR',0,'complete','non-recurring','2020-04-19 12:15:30.136071','2020-04-19 12:16:18.175887',0,3,1,1,NULL),(5,'5feb415bfa19ad6d0f2a',15,0,'MYR',1,'complete','non-recurring','2020-04-19 12:16:51.748806','2020-04-19 12:17:24.532986',0,3,1,1,NULL),(6,'04c5f406d266b7fba606',15,0,'MYR',0,'complete','non-recurring','2020-04-19 12:21:27.038716','2020-04-19 12:22:12.608458',0,3,1,1,NULL),(7,'414c3444981c936706a1',8,1,'MYR',1,'pending','non-recurring','2020-04-19 13:35:51.315616','2020-04-19 13:35:51.315651',0,4,2,1,NULL),(8,'761454737764bc6c3560',8,1,'MYR',1,'complete','on-going','2020-04-19 13:40:44.753064','2020-04-19 19:31:40.264460',0,5,2,1,NULL),(9,'be65b58e19b879a057ce',18,1,'MYR',0,'complete','on-going','2020-04-19 13:46:22.180212','2020-04-19 13:46:42.244022',0,5,2,1,NULL),(10,'2d39c61d8cbae52a24d0',15,0,'MYR',1,'complete','non-recurring','2020-04-19 17:43:19.601841','2020-04-19 17:43:35.367003',0,6,1,1,NULL),(11,'1ad28e3b24c3efed687e',8,1,'MYR',0,'complete','on-going','2020-04-19 17:43:47.047264','2020-04-19 17:44:02.606452',0,6,2,1,NULL),(12,'cea923fe6b4ecba96a59',15,0,'MYR',0,'complete','non-recurring','2020-04-19 18:45:25.726658','2020-04-19 18:47:41.828146',0,7,1,1,NULL),(13,'81a7e14e2c9f5eeedd13',15,0,'MYR',0,'complete','non-recurring','2020-04-19 18:51:23.409860','2020-04-19 18:55:09.080789',0,8,1,1,NULL),(14,'d0675b68fb788bcbbb03',15,0,'MYR',0,'complete','non-recurring','2020-04-19 18:56:39.234877','2020-04-19 18:56:58.885897',0,9,1,1,NULL),(15,'35414e0846d742e75c9e',15,0,'MYR',0,'complete','non-recurring','2020-04-19 19:01:39.052443','2020-04-19 19:02:12.976573',0,10,1,1,NULL),(16,'95e5150d9d8a931e35c3',15,0,'MYR',0,'complete','non-recurring','2020-04-19 19:13:22.040796','2020-04-19 19:13:37.409438',0,11,1,1,NULL),(17,'bc53cfe7fdebc067c596',15,0,'MYR',1,'complete','non-recurring','2020-04-19 19:39:14.773560','2020-04-19 19:39:32.238172',0,12,1,1,NULL),(20,'3c5528c74b9e7a763a25',8,1,'MYR',1,'complete','on-going','2020-04-19 20:26:31.542658','2020-04-19 20:26:58.145537',0,15,2,1,NULL),(21,'c48d0ad11c8385b1c484',8,1,'MYR',1,'complete','on-going','2020-04-19 20:33:12.199747','2020-04-19 20:33:30.318184',0,16,2,1,NULL),(22,'218f38715fe279df05fa',15,0,'MYR',0,'cancelled','non-recurring','2020-04-20 08:47:55.024299','2020-04-20 08:48:12.720178',0,17,1,1,NULL),(23,'f70b2b8463e680fec1f3',15,0,'MYR',0,'complete','non-recurring','2020-04-20 09:12:02.216508','2020-04-20 09:12:16.224265',0,18,1,1,NULL),(24,'ac416dcffe677a152983',8,1,'MYR',1,'complete','on-going','2020-04-20 09:19:47.365717','2020-04-20 09:19:59.759469',0,19,2,1,NULL),(29,'bad12eced149f10509c4',8,1,'MYR',1,'complete','on-going','2020-04-20 12:14:58.068830','2020-04-20 12:15:12.796154',0,24,2,1,NULL),(33,'696584cb5a16b24dd4c1',15,0,'MYR',1,'complete','non-recurring','2020-04-20 18:20:00.584537','2020-04-20 18:20:16.901444',0,28,1,1,NULL),(34,'d4b1d9c5197ac6f5f854',8,1,'MYR',1,'complete','on-going','2020-04-22 09:56:24.248469','2020-04-22 09:57:13.176097',0,29,2,1,NULL),(35,'c438f5bcab00f0a0add3',12,0,'MYR',1,'complete','non-recurring','2020-04-23 09:10:31.445220','2020-04-23 09:11:04.792703',0,30,1,1,NULL),(36,'63b6bf7d6f70b9b16974',24,1,'MYR',1,'complete','on-going','2020-04-23 09:16:14.463822','2020-04-23 09:16:30.210158',0,31,1,1,NULL),(37,'353a227cbd949fc43dc4',12,0,'MYR',0,'pending','non-recurring','2020-04-23 19:53:46.460242','2020-04-23 19:53:46.460275',0,32,1,1,NULL),(38,'b0147d39ee4e0dcdb758',12,0,'MYR',0,'pending','non-recurring','2020-04-23 19:58:14.648531','2020-04-23 19:58:14.648564',0,32,1,1,NULL),(39,'9087841d9180a2e1cb0c',24,0,'MYR',1,'complete','non-recurring','2020-04-23 20:00:33.085305','2020-04-23 20:01:33.123880',0,33,1,1,NULL),(40,'8aecf133f438b7063952',12,1,'MYR',0,'complete','on-going','2020-04-27 09:28:14.678332','2020-04-27 09:31:34.424036',0,34,1,1,NULL),(41,'533a7f28d2a8e161d5e8',12,1,'MYR',1,'complete','on-going','2020-04-27 09:36:21.032424','2020-04-27 09:37:14.887296',0,35,1,1,NULL),(42,'2d78920b4cd48060a53b',12,0,'MYR',0,'cancelled','non-recurring','2020-04-27 09:50:13.795150','2020-04-27 09:54:02.463907',0,16,1,1,NULL),(43,'e08adfe9ac247fbe9e52',12,0,'MYR',0,'complete','non-recurring','2020-04-27 12:09:13.205849','2020-04-27 12:09:39.379520',0,16,1,1,NULL),(44,'1184258a8369793ca119',24,0,'MYR',1,'complete','non-recurring','2020-04-27 12:10:47.654110','2020-04-27 12:11:02.236282',0,36,1,1,NULL),(45,'35b255b5e7c18558d195',12,0,'MYR',0,'cancelled','non-recurring','2020-04-28 11:38:14.046459','2020-04-28 11:43:36.426607',0,37,1,1,NULL),(46,'337e0412709ea025c057',12,1,'MYR',0,'complete','on-going','2020-04-28 11:45:51.947575','2020-04-28 11:46:06.543828',0,38,1,1,NULL);
/*!40000 ALTER TABLE `donations_donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donationform`
--

DROP TABLE IF EXISTS `donations_donationform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donationform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `amount_type` varchar(20) NOT NULL,
  `fixed_amount` double DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `footer_text` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donationform`
--

LOCK TABLES `donations_donationform` WRITE;
/*!40000 ALTER TABLE `donations_donationform` DISABLE KEYS */;
INSERT INTO `donations_donationform` VALUES (1,'Primary Donation Form','the usually used / most often used form','stepped',15,'2020-04-18 20:00:44.362396','2020-04-23 16:37:51.628469',0,1,'<p>By proceeding you are agreeing to our Terms and Conditions. You can cancel your donation at any time by logging in, or if you do not create an account, by emailing us directly at <a href=\"mailto:donations@hongkongfp.com\">donations@hongkongfp.com</a>.</p>'),(2,'Secondary Donation Form','','stepped',NULL,'2020-04-18 20:01:54.123154','2020-04-23 09:00:26.419328',0,0,'');
/*!40000 ALTER TABLE `donations_donationform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donationform_allowed_gateways`
--

DROP TABLE IF EXISTS `donations_donationform_allowed_gateways`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donationform_allowed_gateways` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `donationform_id` int(11) NOT NULL,
  `paymentgateway_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `donations_donationform_a_donationform_id_paymentg_e9960a65_uniq` (`donationform_id`,`paymentgateway_id`),
  KEY `donations_donationfo_paymentgateway_id_a67166e1_fk_donations` (`paymentgateway_id`),
  CONSTRAINT `donations_donationfo_donationform_id_f4b7c3a9_fk_donations` FOREIGN KEY (`donationform_id`) REFERENCES `donations_donationform` (`id`),
  CONSTRAINT `donations_donationfo_paymentgateway_id_a67166e1_fk_donations` FOREIGN KEY (`paymentgateway_id`) REFERENCES `donations_paymentgateway` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donationform_allowed_gateways`
--

LOCK TABLES `donations_donationform_allowed_gateways` WRITE;
/*!40000 ALTER TABLE `donations_donationform_allowed_gateways` DISABLE KEYS */;
INSERT INTO `donations_donationform_allowed_gateways` VALUES (1,1,1),(4,1,2),(2,2,1),(3,2,2);
/*!40000 ALTER TABLE `donations_donationform_allowed_gateways` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donationmeta`
--

DROP TABLE IF EXISTS `donations_donationmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donationmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_key` varchar(255) NOT NULL,
  `field_value` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `donation_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `donations_donationmeta_donation_id_a62cc807` (`donation_id`),
  CONSTRAINT `donations_donationme_donation_id_a62cc807_fk_donations` FOREIGN KEY (`donation_id`) REFERENCES `donations_donation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donationmeta`
--

LOCK TABLES `donations_donationmeta` WRITE;
/*!40000 ALTER TABLE `donations_donationmeta` DISABLE KEYS */;
INSERT INTO `donations_donationmeta` VALUES (5,'feedback','','2020-04-19 12:04:51.435785','2020-04-19 12:04:51.435815',0,3),(6,'hash_value','7c1b94305c656e28425cc234b5cca13f9f7bfcf240f06f00b6f6e495c3b40bf6','2020-04-19 12:04:51.446841','2020-04-19 12:04:51.446870',0,3),(7,'checkHash','86d8eab1b21852d447a6710e1b49160c1200892674536f62fc32beb0dad2df42','2020-04-19 12:05:09.881255','2020-04-19 12:05:09.881285',0,3),(8,'checkHash','86d8eab1b21852d447a6710e1b49160c1200892674536f62fc32beb0dad2df42','2020-04-19 12:05:38.991015','2020-04-19 12:05:38.991090',0,3),(9,'feedback','','2020-04-19 12:15:30.155183','2020-04-19 12:15:30.155222',0,4),(10,'hash_value','51818177033c1746c7c000ab8312c49de3a639fdf717e60d4cc34ad2d9bb05cb','2020-04-19 12:15:30.165832','2020-04-19 12:15:30.165858',0,4),(11,'checkHash','8c55b0120e74dd98566b2aff8b5817dce82fd14846abb95284efd9b4c6faaeac','2020-04-19 12:16:08.488260','2020-04-19 12:16:08.488289',0,4),(12,'checkHash','8c55b0120e74dd98566b2aff8b5817dce82fd14846abb95284efd9b4c6faaeac','2020-04-19 12:16:18.186451','2020-04-19 12:16:18.186480',0,4),(13,'feedback','','2020-04-19 12:16:51.769377','2020-04-19 12:16:51.769418',0,5),(14,'hash_value','03b4755b94b238a0b619825a47091889d40d80c14570545b36db4f68c2667d25','2020-04-19 12:16:51.780323','2020-04-19 12:16:51.780351',0,5),(15,'checkHash','5638a8acade283954abb96cf1a104cf16458eb747c5a997a55242eeb44ab7ccb','2020-04-19 12:17:13.759077','2020-04-19 12:17:13.759119',0,5),(16,'checkHash','5638a8acade283954abb96cf1a104cf16458eb747c5a997a55242eeb44ab7ccb','2020-04-19 12:17:24.536948','2020-04-19 12:17:24.536977',0,5),(17,'feedback','This payment is real quickckck','2020-04-19 12:21:27.053075','2020-04-19 12:21:27.053117',0,6),(18,'hash_value','f3b793d14bd19d108e9c45d448a2ad1d7d9f8b0c6edabe83f7a12b1ee1d7b539','2020-04-19 12:21:27.058370','2020-04-19 12:21:27.058397',0,6),(19,'checkHash','7013dd0b69226a9fd1bd7b2d9c9c89f1f528f780c818844c214f6330c289a58e','2020-04-19 12:22:04.072245','2020-04-19 12:22:04.072280',0,6),(20,'checkHash','7013dd0b69226a9fd1bd7b2d9c9c89f1f528f780c818844c214f6330c289a58e','2020-04-19 12:22:12.611745','2020-04-19 12:22:12.611778',0,6),(21,'feedback','Hold on tihgt','2020-04-19 13:35:51.335873','2020-04-19 13:35:51.335912',0,7),(22,'feedback','Cool Aid','2020-04-19 13:40:44.762036','2020-04-19 13:40:44.762067',0,8),(23,'order_prefix','P889a9bdb1d385d','2020-04-19 13:40:44.791182','2020-04-19 13:40:44.791220',0,8),(24,'hash_value','3b8d2ed34c393e37f096e81c5061035d4a36d51f77395724be14a544d0c53eab','2020-04-19 13:40:44.793603','2020-04-19 13:40:44.793630',0,8),(25,'checkHash','dd6801c3dfc0350bb3a57d1d0d94a543daa60e5d9ca7852aaa4ac58ab98624a3','2020-04-19 13:41:06.487484','2020-04-19 13:41:06.487512',0,8),(26,'recurring_unique_id','138206','2020-04-19 13:41:06.507004','2020-04-19 13:41:06.507071',0,8),(27,'checkHash','dd6801c3dfc0350bb3a57d1d0d94a543daa60e5d9ca7852aaa4ac58ab98624a3','2020-04-19 13:45:20.533749','2020-04-19 13:45:20.533778',0,8),(28,'recurring_unique_id','138206','2020-04-19 13:45:20.542904','2020-04-19 13:45:20.542932',0,8),(29,'feedback','My second offer, Cheers','2020-04-19 13:46:22.194784','2020-04-19 13:46:22.194816',0,9),(30,'order_prefix','P0fadb9d0940ef0','2020-04-19 13:46:22.219314','2020-04-19 13:46:22.219345',0,9),(31,'hash_value','e29ce46d32687e37d162e16fab1ddbd0357d38e18f4904b08eef54f51d274afe','2020-04-19 13:46:22.224408','2020-04-19 13:46:22.224439',0,9),(32,'checkHash','89836cb39f09480c7c9b0ae307901a0f3d5be1da82037c5c38bd7e02a63c4239','2020-04-19 13:46:38.944067','2020-04-19 13:46:38.944095',0,9),(33,'recurring_unique_id','138207','2020-04-19 13:46:38.953849','2020-04-19 13:46:38.953876',0,9),(34,'checkHash','89836cb39f09480c7c9b0ae307901a0f3d5be1da82037c5c38bd7e02a63c4239','2020-04-19 13:46:42.253710','2020-04-19 13:46:42.253738',0,9),(35,'recurring_unique_id','138207','2020-04-19 13:46:42.263505','2020-04-19 13:46:42.263531',0,9),(36,'feedback','','2020-04-19 17:43:19.628476','2020-04-19 17:43:19.628513',0,10),(37,'hash_value','5c69a235df9f3fe97116166242c86526e17aa9aa3c30f4578fc3bb08f1dcfddd','2020-04-19 17:43:19.640364','2020-04-19 17:43:19.640394',0,10),(38,'checkHash','cc85e285b3748772610c530dd09c3f9f75002ee4b57ba3d78a582e455a5f0aae','2020-04-19 17:43:34.176732','2020-04-19 17:43:34.176772',0,10),(39,'checkHash','cc85e285b3748772610c530dd09c3f9f75002ee4b57ba3d78a582e455a5f0aae','2020-04-19 17:43:35.379241','2020-04-19 17:43:35.379270',0,10),(40,'feedback','','2020-04-19 17:43:47.061556','2020-04-19 17:43:47.061588',0,11),(41,'order_prefix','P5749c9cc450e0e','2020-04-19 17:43:47.090574','2020-04-19 17:43:47.090602',0,11),(42,'hash_value','6057b97d72fc172ab3e4705228b56ddc151b6318c109e2db374768a66afbff5f','2020-04-19 17:43:47.092765','2020-04-19 17:43:47.092795',0,11),(43,'checkHash','3e755136e82efda06bf5151264e90d1bd5908c980bf2c3eddeba6b60223113d7','2020-04-19 17:44:01.100804','2020-04-19 17:44:01.100844',0,11),(44,'recurring_unique_id','138208','2020-04-19 17:44:01.129880','2020-04-19 17:44:01.129925',0,11),(45,'checkHash','3e755136e82efda06bf5151264e90d1bd5908c980bf2c3eddeba6b60223113d7','2020-04-19 17:44:02.618880','2020-04-19 17:44:02.618945',0,11),(46,'recurring_unique_id','138208','2020-04-19 17:44:02.628437','2020-04-19 17:44:02.628465',0,11),(47,'feedback','','2020-04-19 18:45:25.746067','2020-04-19 18:45:25.746107',0,12),(48,'hash_value','19d19c7de588eb9aa2f91cd4e54f0c8c2d9b4387413c995d7def322c0a2fe583','2020-04-19 18:45:25.757358','2020-04-19 18:45:25.757392',0,12),(49,'checkHash','f7f67f9dedaefc0747023f7e38c9422b5a6e4fda49fec7def675a7f17976c8c7','2020-04-19 18:45:44.392210','2020-04-19 18:45:44.392238',0,12),(50,'checkHash','f7f67f9dedaefc0747023f7e38c9422b5a6e4fda49fec7def675a7f17976c8c7','2020-04-19 18:47:41.831882','2020-04-19 18:47:41.831911',0,12),(51,'feedback','','2020-04-19 18:51:23.437302','2020-04-19 18:51:23.437346',0,13),(52,'hash_value','673062aa1df8ccca0b921942f25b609954fdbd23a132513574b81701c97af93a','2020-04-19 18:51:23.449326','2020-04-19 18:51:23.449355',0,13),(53,'checkHash','618524cffb78f9fcb9bdd174fe7a68c365d745cd99d8a548f0dd4c60c8dda651','2020-04-19 18:51:40.097620','2020-04-19 18:51:40.097660',0,13),(54,'checkHash','618524cffb78f9fcb9bdd174fe7a68c365d745cd99d8a548f0dd4c60c8dda651','2020-04-19 18:55:09.085280','2020-04-19 18:55:09.085312',0,13),(55,'feedback','','2020-04-19 18:56:39.254279','2020-04-19 18:56:39.254320',0,14),(56,'hash_value','d7f56f0511110b13ced33628687b37223dedc3eb897eac55dc756f5384380e09','2020-04-19 18:56:39.265303','2020-04-19 18:56:39.265332',0,14),(57,'checkHash','8eb99c6a441387222dc09344aef0a8087f7415f9ac81614bb610e60d148030c1','2020-04-19 18:56:58.891146','2020-04-19 18:56:58.891177',0,14),(58,'feedback','','2020-04-19 19:01:39.061305','2020-04-19 19:01:39.061333',0,15),(59,'hash_value','6886cb985195e20ac2dbfc34a35daf68e9ad0191f3b427d29d1a580e98f77d19','2020-04-19 19:01:39.072576','2020-04-19 19:01:39.072606',0,15),(60,'checkHash','b6310a3cc231be77b68a69aaaa5bbe63f439fdc4a0164766ce0b117f1f585136','2020-04-19 19:02:12.985928','2020-04-19 19:02:12.985957',0,15),(61,'feedback','','2020-04-19 19:13:22.061885','2020-04-19 19:13:22.061930',0,16),(62,'hash_value','7c0b85b6a3349919df8f0a95b12dcb3600c4da1b679a32f0466c26e5548c8727','2020-04-19 19:13:22.072597','2020-04-19 19:13:22.072627',0,16),(63,'checkHash','364cdfbd372e144cf46a81c5a03f2cf714a329f96060264f8aa0ad6f8443d52c','2020-04-19 19:13:37.413555','2020-04-19 19:13:37.413583',0,16),(64,'checkHash','f4b139c4c138627ba727d754302fc63c5f37a4be8161dd652a91ecc7b8fb2602','2020-04-19 19:31:40.269035','2020-04-19 19:31:40.269064',0,8),(65,'recurring_unique_id','138206','2020-04-19 19:31:40.278363','2020-04-19 19:31:40.278390',0,8),(66,'feedback','','2020-04-19 19:39:14.787924','2020-04-19 19:39:14.787953',0,17),(67,'hash_value','7b306b7a736263bdef4d74581aeb01abf7ac455cc39063cffa1d5cf4aeef7f56','2020-04-19 19:39:14.798959','2020-04-19 19:39:14.798999',0,17),(68,'checkHash','08c2fef74b85471db18876435c3be14ce29f1884745338ab2a930edb0a6b13c9','2020-04-19 19:39:32.241983','2020-04-19 19:39:32.242010',0,17),(75,'feedback','','2020-04-19 20:26:31.561822','2020-04-19 20:26:31.561855',0,20),(76,'order_prefix','P6eb17961371ca4','2020-04-19 20:26:31.590964','2020-04-19 20:26:31.591000',0,20),(77,'hash_value','fcb9b58d1cc9377381eac552dc25778d880ecc60fedffc97971365c7950f26a3','2020-04-19 20:26:31.602849','2020-04-19 20:26:31.602876',0,20),(78,'checkHash','56bbaf3dff38ff33daa5ce6473395b49c6f8dcddd6373b16639f7dbfa138497f','2020-04-19 20:26:58.150447','2020-04-19 20:26:58.150474',0,20),(79,'recurring_unique_id','138209','2020-04-19 20:26:58.158778','2020-04-19 20:26:58.158808',0,20),(80,'feedback','','2020-04-19 20:33:12.219373','2020-04-19 20:33:12.219418',0,21),(81,'order_prefix','Paad570974581cf','2020-04-19 20:33:12.232432','2020-04-19 20:33:12.232462',0,21),(82,'hash_value','304c2145cf6c35bd90be2698ce3fb0375bbdb3ce1dba3a259bb2aaf155965afb','2020-04-19 20:33:12.237447','2020-04-19 20:33:12.237476',0,21),(83,'checkHash','6079c513251791507245e9517b502f5fa6941b53fb754289ee663d61c37c1724','2020-04-19 20:33:30.327205','2020-04-19 20:33:30.327235',0,21),(84,'recurring_unique_id','138210','2020-04-19 20:33:30.336851','2020-04-19 20:33:30.336881',0,21),(85,'feedback','','2020-04-20 08:47:55.057552','2020-04-20 08:47:55.057596',0,22),(86,'hash_value','3f24aba46e6d35573ac64f720669b578f6aa1d1b38a06b189eea60b95066e366','2020-04-20 08:47:55.063509','2020-04-20 08:47:55.063539',0,22),(87,'checkHash','f32ed621df5c6b1385277b57077bf30f01eb227132e158b5945baf13dcb28d67','2020-04-20 08:48:12.730622','2020-04-20 08:48:12.730659',0,22),(88,'feedback','','2020-04-20 09:12:02.235770','2020-04-20 09:12:02.235807',0,23),(89,'hash_value','a664e8b3dc71bd891fe92c152c229e3b86c8a27fe38b8a42941edcde70706539','2020-04-20 09:12:02.279483','2020-04-20 09:12:02.279524',0,23),(90,'checkHash','4fece9945bcd8f8e09b5a46e601383aa98858aad1c3117c5491dbeff85409083','2020-04-20 09:12:16.236756','2020-04-20 09:12:16.236786',0,23),(91,'feedback','','2020-04-20 09:19:47.369599','2020-04-20 09:19:47.369627',0,24),(92,'order_prefix','Pe8fff6e958997d','2020-04-20 09:19:47.399727','2020-04-20 09:19:47.399757',0,24),(93,'hash_value','9d1b2201125bf567cf0fbc0ac78a9dbdf1cb67355c07e01517ca865b7052713c','2020-04-20 09:19:47.411579','2020-04-20 09:19:47.411606',0,24),(94,'checkHash','dba994efede0877cabb77496897b667735fde3000a5e7d8635dd418151989096','2020-04-20 09:19:59.763175','2020-04-20 09:19:59.763201',0,24),(95,'recurring_unique_id','138214','2020-04-20 09:19:59.772451','2020-04-20 09:19:59.772476',0,24),(110,'feedback','','2020-04-20 12:14:58.078490','2020-04-20 12:14:58.078522',0,29),(111,'order_prefix','Pb02e22dce99cf7','2020-04-20 12:14:58.091991','2020-04-20 12:14:58.092019',0,29),(112,'hash_value','e93a4c6cff78e224630e1e41d5132d50ee06d3d233584d72c5273b3cbca74de7','2020-04-20 12:14:58.095948','2020-04-20 12:14:58.095974',0,29),(113,'checkHash','d74a17b02163442bfe61ff66fff99710cd38f91205ce13c7290e45d95836465b','2020-04-20 12:15:12.799581','2020-04-20 12:15:12.799609',0,29),(114,'recurring_unique_id','138218','2020-04-20 12:15:12.819187','2020-04-20 12:15:12.819217',0,29),(124,'feedback','','2020-04-20 18:20:00.599031','2020-04-20 18:20:00.599085',0,33),(125,'hash_value','94b3ac090285f858f3df3a674dd1a2ba34f70874ff89ed74e7cb7817990403ad','2020-04-20 18:20:00.612178','2020-04-20 18:20:00.612208',0,33),(126,'checkHash','b1965d43b4b8a614e6f6e3a0d3f55573160f6bd30dff15871d5a6dbf3ff987be','2020-04-20 18:20:16.904772','2020-04-20 18:20:16.904800',0,33),(127,'feedback','','2020-04-22 09:56:24.258037','2020-04-22 09:56:24.258068',0,34),(128,'order_prefix','P01b49400000d46','2020-04-22 09:56:24.288741','2020-04-22 09:56:24.288775',0,34),(129,'hash_value','a19b97c447c7d4a29e6b04d996a57092d1485835de3a23a8e64669ecc4e6feb7','2020-04-22 09:56:24.291352','2020-04-22 09:56:24.291379',0,34),(130,'checkHash','966510903fb64c6599e8d7f6baf43d8142aa688f20520d386505296aba5c6300','2020-04-22 09:57:13.188661','2020-04-22 09:57:13.188695',0,34),(131,'recurring_unique_id','138223','2020-04-22 09:57:13.198326','2020-04-22 09:57:13.198359',0,34),(132,'hash_value','1dae4b1e19dc54a75e9b361cefcef314f0bb96550f73b9853de56471ea5ac67c','2020-04-23 09:10:31.501614','2020-04-23 09:10:31.501656',0,35),(133,'checkHash','9e72cb2dae5cf08243f197e40502c54537b6b0ba6c541a121b29d28f6657a68a','2020-04-23 09:11:04.812549','2020-04-23 09:11:04.812580',0,35),(134,'order_prefix','P0b361e8500e626','2020-04-23 09:16:14.477719','2020-04-23 09:16:14.477747',0,36),(135,'hash_value','45359db8c55d4df9612300148dfe15f6678ad3fe87f0ecb845cf2f3f0337b8c5','2020-04-23 09:16:14.481272','2020-04-23 09:16:14.481299',0,36),(136,'checkHash','87fbcb203f40f654e3e78a37064aa91db9e05c6884b400d678775678c04ddd51','2020-04-23 09:16:30.214241','2020-04-23 09:16:30.214270',0,36),(137,'recurring_unique_id','138240','2020-04-23 09:16:30.222553','2020-04-23 09:16:30.222591',0,36),(138,'hash_value','18b0a06c2a1cc648905196c61fdbab8e0a080a3314516ee78bf71e1095951b78','2020-04-23 19:53:46.525668','2020-04-23 19:53:46.525709',0,37),(139,'hash_value','10b5703ccb8b31084b3d0a3bbf8ef572560afea72826fd58d6a21d3b837810b6','2020-04-23 19:58:14.695959','2020-04-23 19:58:14.696004',0,38),(140,'hash_value','8079cd2fddfd20b4193c777ee7faf43a2a8372e413a1ea66ae703a59841ad52e','2020-04-23 20:00:33.130928','2020-04-23 20:00:33.130971',0,39),(141,'checkHash','49dc78ba339be231dcdd31412af356871a9603df10ad497c3b9339fed9a05deb','2020-04-23 20:01:33.128005','2020-04-23 20:01:33.128040',0,39),(142,'order_prefix','P61a4f748ebecf9','2020-04-27 09:28:14.711247','2020-04-27 09:28:14.711284',0,40),(143,'hash_value','0f34956d65158eb3c2bdfd61f5ce0124bbdd250fd81c5d48a4055904222eedf2','2020-04-27 09:28:14.714823','2020-04-27 09:28:14.714850',0,40),(144,'checkHash','dc5d4caab7e07330be752de63c815a9202e6fdc770bf8445f19ab6f5e98f8bfc','2020-04-27 09:31:34.436443','2020-04-27 09:31:34.436482',0,40),(145,'recurring_unique_id','138314','2020-04-27 09:31:34.445653','2020-04-27 09:31:34.445685',0,40),(146,'order_prefix','P1159671e4b3579','2020-04-27 09:36:21.047805','2020-04-27 09:36:21.047840',0,41),(147,'hash_value','f8c8fa6b9086b2b3a9da3f2c3f7a827bd94b87d285859ce29fb07d1f75ac94f4','2020-04-27 09:36:21.050159','2020-04-27 09:36:21.050188',0,41),(148,'checkHash','5a38e4e96574b5fc1bcc855eedb68b35007eb8dc3a6202692a926e6ae743c5d9','2020-04-27 09:37:14.893014','2020-04-27 09:37:14.893043',0,41),(149,'recurring_unique_id','138315','2020-04-27 09:37:14.912623','2020-04-27 09:37:14.912653',0,41),(150,'hash_value','2544c56ba94492f24fe2cbed08e416ff8c8512730565d540f8020ebb06791106','2020-04-27 09:50:13.802723','2020-04-27 09:50:13.802751',0,42),(151,'checkHash','f4789ac19f77bc09940ab318caed29ec1b1accdb3975c29a6d7fdedf3b2d50cc','2020-04-27 09:54:02.467271','2020-04-27 09:54:02.467298',0,42),(152,'order_prefix','Pd264ba42b800d9','2020-04-28 11:45:52.002222','2020-04-28 11:45:52.002262',0,46),(153,'recurring_unique_id','138359','2020-04-28 11:46:06.548090','2020-04-28 11:46:06.548131',0,46);
/*!40000 ALTER TABLE `donations_donationmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donationmetafield`
--

DROP TABLE IF EXISTS `donations_donationmetafield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donationmetafield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_order` int(11) DEFAULT NULL,
  `label` varchar(255) NOT NULL,
  `field_type` varchar(16) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `choices` longtext NOT NULL,
  `default_value` varchar(255) NOT NULL,
  `help_text` varchar(255) NOT NULL,
  `form_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `donations_donationmetafield_form_id_1b7f9321` (`form_id`),
  CONSTRAINT `donations_donationme_form_id_1b7f9321_fk_donations` FOREIGN KEY (`form_id`) REFERENCES `donations_donationform` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donationmetafield`
--

LOCK TABLES `donations_donationmetafield` WRITE;
/*!40000 ALTER TABLE `donations_donationmetafield` DISABLE KEYS */;
INSERT INTO `donations_donationmetafield` VALUES (2,0,'Feedback','multiline',0,'','','any feedbacks or comments for us?',2);
/*!40000 ALTER TABLE `donations_donationmetafield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donor`
--

DROP TABLE IF EXISTS `donations_donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `opt_in_mailing_list` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `linked_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `donations_donor_email_008150ad_uniq` (`email`),
  KEY `donations_donor_linked_user_id_bc79f4b2_fk_custom_user_user_id` (`linked_user_id`),
  CONSTRAINT `donations_donor_linked_user_id_bc79f4b2_fk_custom_user_user_id` FOREIGN KEY (`linked_user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donor`
--

LOCK TABLES `donations_donor` WRITE;
/*!40000 ALTER TABLE `donations_donor` DISABLE KEYS */;
INSERT INTO `donations_donor` VALUES (3,'ABC','John','abc@john.com',0,'2020-04-19 12:04:51.412312','2020-04-19 12:16:51.733139',0,2),(4,'DEF','John','def@john.com',1,'2020-04-19 13:35:51.134734','2020-04-19 13:35:51.300643',0,3),(5,'fan','john','fan@john.com',0,'2020-04-19 13:40:44.582708','2020-04-19 13:40:44.737611',0,4),(6,'Sage','John','sage@john.com',1,'2020-04-19 17:43:19.416109','2020-04-19 17:43:19.585073',0,5),(7,'Tesla','John','tesla@john.com',0,'2020-04-19 18:45:25.712039','2020-04-19 18:45:25.712083',0,NULL),(8,'Titan','John','titan@john.com',0,'2020-04-19 18:51:23.372936','2020-04-19 18:51:23.372970',0,NULL),(9,'Crocs','John','crocs@john.com',0,'2020-04-19 18:56:39.219818','2020-04-19 18:56:39.219850',0,NULL),(10,'Shame','John','shame@john.com',0,'2020-04-19 19:01:39.015984','2020-04-19 19:01:39.016019',0,NULL),(11,'Zed','John','zed@john.com',0,'2020-04-19 19:13:22.026768','2020-04-19 19:13:22.026813',0,NULL),(12,'Dash','John','dash@john.com',1,'2020-04-19 19:39:14.595675','2020-04-19 19:39:14.758928',0,6),(15,'Lick','John','lick@john.com',0,'2020-04-19 20:26:31.364543','2020-04-19 20:26:31.536910',0,7),(16,'Franky','John','frankyhung93@gmail.com',0,'2020-04-19 20:33:12.036839','2020-04-25 19:27:28.899444',0,8),(17,'Eco','John','eco@john.com',0,'2020-04-20 08:47:55.000703','2020-04-20 08:47:55.000743',0,NULL),(18,'Return','John','return@john.com',0,'2020-04-20 09:12:02.200587','2020-04-20 09:12:02.200624',0,NULL),(19,'Https','John','https@john.com',0,'2020-04-20 09:19:47.183633','2020-04-20 09:19:47.350865',0,9),(24,'Gat','John','gatoutahellweb@gmail.com',0,'2020-04-20 12:14:57.903604','2020-04-25 10:56:30.692893',0,4),(28,'Yahoo','John','frankyhung93@yahoo.com.hk',0,'2020-04-20 18:20:00.391916','2020-04-20 21:03:36.172837',0,NULL),(29,'Retest','John','retest@john.com',0,'2020-04-22 09:56:24.077099','2020-04-22 09:56:24.236380',0,19),(30,'ROTK','John','rotk@john.com',0,'2020-04-23 09:10:31.260775','2020-04-23 09:10:31.432262',0,20),(31,'ROTK','Peter','rotk@peter.com',0,'2020-04-23 09:16:14.299799','2020-04-23 09:16:14.452078',0,21),(32,'Hi','John','hi@john.com',0,'2020-04-23 19:53:46.444024','2020-04-23 19:58:14.643273',0,NULL),(33,'Drake','John','drake@john.com',1,'2020-04-23 20:00:32.911160','2020-04-23 20:00:33.073097',0,22),(34,'John','Smith','johnsmith@gmail.example',0,'2020-04-27 09:28:14.652793','2020-04-27 09:28:14.652838',0,NULL),(35,'John','Smith','johnsmith2@gmail.example',0,'2020-04-27 09:36:20.862644','2020-04-27 09:36:21.020567',0,23),(36,'Deca','John','deca@john.com',1,'2020-04-27 12:10:47.479800','2020-04-27 12:10:47.632638',0,24),(37,'Franky','Hung','franky@uxcodified.com',0,'0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000',0,1),(38,'what','john','what@john.com',1,'2020-04-28 11:45:51.942791','2020-04-28 11:45:51.942830',0,NULL);
/*!40000 ALTER TABLE `donations_donor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donormeta`
--

DROP TABLE IF EXISTS `donations_donormeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donormeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_key` varchar(255) NOT NULL,
  `field_value` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `donor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `donations_donormeta_donor_id_cd7b6835` (`donor_id`),
  CONSTRAINT `donations_donormeta_donor_id_cd7b6835_fk_donations_donor_id` FOREIGN KEY (`donor_id`) REFERENCES `donations_donor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donormeta`
--

LOCK TABLES `donations_donormeta` WRITE;
/*!40000 ALTER TABLE `donations_donormeta` DISABLE KEYS */;
INSERT INTO `donations_donormeta` VALUES (3,'telephone','34952858','2020-04-19 12:04:51.416288','2020-04-19 12:16:51.563506',0,3),(4,'Other Name','ABCD John','2020-04-19 12:15:30.104353','2020-04-19 12:15:30.104381',0,3),(5,'telephone','98708798','2020-04-19 13:35:51.138704','2020-04-19 13:35:51.138733',0,4),(6,'telephone','898345743','2020-04-19 13:40:44.586971','2020-04-19 13:40:44.587000',0,5),(7,'telephone','98768765','2020-04-19 17:43:19.420357','2020-04-19 17:43:19.420385',0,6),(8,'telephone','0870987','2020-04-19 18:45:25.716143','2020-04-19 18:45:25.716178',0,7),(9,'telephone','34564567','2020-04-19 18:51:23.389255','2020-04-19 18:51:23.389298',0,8),(10,'telephone','456457345','2020-04-19 18:56:39.224495','2020-04-19 18:56:39.224525',0,9),(11,'telephone','43560985','2020-04-19 19:01:39.030695','2020-04-19 19:01:39.030732',0,10),(12,'telephone','3549685','2020-04-19 19:13:22.030755','2020-04-19 19:13:22.030791',0,11),(13,'telephone','88998888','2020-04-19 19:39:14.599827','2020-04-19 19:39:14.599856',0,12),(16,'telephone','84569354','2020-04-19 20:26:31.368679','2020-04-19 20:26:31.368709',0,15),(17,'telephone','3849502','2020-04-19 20:33:12.040778','2020-04-19 20:33:12.040808',0,16),(18,'telephone','4592843','2020-04-20 08:47:55.013843','2020-04-20 08:47:55.013890',0,17),(19,'telephone','2584295','2020-04-20 09:12:02.205437','2020-04-20 09:12:02.205469',0,18),(20,'telephone','2450348','2020-04-20 09:19:47.187641','2020-04-20 09:19:47.187675',0,19),(25,'telephone','34958347','2020-04-20 12:14:57.908167','2020-04-20 12:14:57.908198',0,24),(29,'telephone','348592348','2020-04-20 18:20:00.406699','2020-04-20 18:20:00.406736',0,28),(30,'telephone','93485279','2020-04-22 09:56:24.081496','2020-04-22 09:56:24.081526',0,29);
/*!40000 ALTER TABLE `donations_donormeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_donormetafield`
--

DROP TABLE IF EXISTS `donations_donormetafield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_donormetafield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_order` int(11) DEFAULT NULL,
  `label` varchar(255) NOT NULL,
  `field_type` varchar(16) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `choices` longtext NOT NULL,
  `default_value` varchar(255) NOT NULL,
  `help_text` varchar(255) NOT NULL,
  `form_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `donations_donormetafield_form_id_0c16e1eb` (`form_id`),
  CONSTRAINT `donations_donormetaf_form_id_0c16e1eb_fk_donations` FOREIGN KEY (`form_id`) REFERENCES `donations_donationform` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_donormetafield`
--

LOCK TABLES `donations_donormetafield` WRITE;
/*!40000 ALTER TABLE `donations_donormetafield` DISABLE KEYS */;
INSERT INTO `donations_donormetafield` VALUES (2,0,'Telephone','singleline',1,'','','enter your contact number',2);
/*!40000 ALTER TABLE `donations_donormetafield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donations_paymentgateway`
--

DROP TABLE IF EXISTS `donations_paymentgateway`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donations_paymentgateway` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `list_order` int(11) NOT NULL,
  `frontend_label` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donations_paymentgateway`
--

LOCK TABLES `donations_paymentgateway` WRITE;
/*!40000 ALTER TABLE `donations_paymentgateway` DISABLE KEYS */;
INSERT INTO `donations_paymentgateway` VALUES (1,'2C2P',0,'Credit Card'),(2,'PayPal',1,'PayPal');
/*!40000 ALTER TABLE `donations_paymentgateway` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `home_homepage`
--

DROP TABLE IF EXISTS `home_homepage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_homepage` (
  `page_ptr_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  PRIMARY KEY (`page_ptr_id`),
  CONSTRAINT `home_homepage_page_ptr_id_e5b77cf7_fk_wagtailcore_page_id` FOREIGN KEY (`page_ptr_id`) REFERENCES `wagtailcore_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_homepage`
--

LOCK TABLES `home_homepage` WRITE;
/*!40000 ALTER TABLE `home_homepage` DISABLE KEYS */;
INSERT INTO `home_homepage` VALUES (3,'[{\"type\": \"full_width_image\", \"value\": {\"banner\": 4}, \"id\": \"b3baadaa-954f-434e-a0de-c8bae6e12b7a\"}, {\"type\": \"full_width_section\", \"value\": {\"width_css\": \"container-tight\", \"background_color_css\": \"\", \"content\": [{\"type\": \"single_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-center\", \"content\": [{\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h1\", \"heading_text\": \"Support Hong Kong Free Press\"}, \"id\": \"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\"}, {\"type\": \"text_block\", \"value\": \"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\", \"id\": \"4f91b372-4339-4501-ab21-027eda2ed7af\"}, {\"type\": \"text_block\", \"value\": \"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\", \"id\": \"a87972a6-7d1c-4255-bad8-063ea0866422\"}, {\"type\": \"buttons_block\", \"value\": [{\"button_text\": \"Donate to HKFP\", \"button_link\": \"https://givehybrid.sytes.net/donations/donate\", \"target_window\": \"_self\"}, {\"button_text\": \"12 ways to support\", \"button_link\": \"https://givehybrid.sytes.net/donations/donate\", \"target_window\": \"_self\"}], \"id\": \"f979d243-8e54-4b0c-b092-a67eb54d4a6e\"}]}, \"id\": \"6208f365-bdb5-46c1-9d52-c53371a3cee4\"}, {\"type\": \"single_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-center\", \"content\": [{\"type\": \"html_block\", \"value\": \"<iframe width=\\\"794\\\" height=\\\"466\\\" src=\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\" frameborder=\\\"0\\\" allow=\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\" allowfullscreen></iframe>\", \"id\": \"7ee637b7-6aa7-4767-97f1-d24f560d70a1\"}]}, \"id\": \"1028ce3c-03fa-4592-aafc-0112bfece2b4\"}]}, \"id\": \"0dbb1645-e174-4205-8deb-abd20eb59b55\"}, {\"type\": \"full_width_section\", \"value\": {\"width_css\": \"container\", \"background_color_css\": \"bg-primary-light\", \"content\": [{\"type\": \"single_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-center\", \"content\": [{\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h1\", \"heading_text\": \"Why trust us?\"}, \"id\": \"4256376e-6555-47d1-8a9a-51e09240aec3\"}]}, \"id\": \"3470abcc-8d1c-4703-bca9-8d8eed931a5a\"}, {\"type\": \"two_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-start\", \"column_1\": [{\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h4\", \"heading_text\": \"Immune to censorship\"}, \"id\": \"0e14ecb2-5a2e-46ee-a40b-6163793ed647\"}, {\"type\": \"text_block\", \"value\": \"<p>HKFP is answerable only to readers \\u2013 we have no investors, no shareholders, no tycoons, no mainland owners or umbrella company behind us. Our independence means we are fully resistant to censorship and self-censorship.</p>\", \"id\": \"dc9d600e-56f4-4f46-bb73-b10e6c90f355\"}, {\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h4\", \"heading_text\": \"Transparent & efficient\"}, \"id\": \"32f37298-0eef-44b0-881b-1be9917c6a81\"}, {\"type\": \"text_block\", \"value\": \"<p>We are the city\\u2019s most transparent news outlet \\u2013 we undergo an external audit each year and publish an annual Transparency Report. 84 per cent of income comes from donations, whilst 81 per cent of spending goes simply towards paying journalists. Teamwork, automation, partnerships and the use of free digital tools keep our costs down.</p>\", \"id\": \"eef7de95-3180-4ef5-b3e0-0011acf5e0e1\"}], \"column_2\": [{\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h4\", \"heading_text\": \"Non-profit model\"}, \"id\": \"e89acf3f-66bd-4789-b7e3-dd5d37c59172\"}, {\"type\": \"text_block\", \"value\": \"<p>As a non-profit, limited by guarantee company, any surplus we make is recycled back into the company. We are run by journalists and immune to commercial and political pressure.</p>\", \"id\": \"30994f40-92e7-4381-b9d2-4e178e96db81\"}, {\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h4\", \"heading_text\": \"Accurate & accountable\"}, \"id\": \"ee67cbd2-2ad9-4141-b788-1d03c44a7ff2\"}, {\"type\": \"text_block\", \"value\": \"<p>We ensure everything we publish includes a balance of viewpoints in order to avoid any bias. All facts, quotes and figures are properly attributed to the source, often with links to the original material. Our own opinions are kept out of our copy, whilst we act quickly and transparently to correct errors. HKFP avoids sensationalism and clickbait, and clearly marks paid-for content as \\u201csponsored.\\u201d Accuracy and fairness are our top priorities.</p>\", \"id\": \"8ccd9457-3ab5-4a56-9eba-185e93a10475\"}]}, \"id\": \"61395600-d34f-456e-9a02-454a59cd6c73\"}]}, \"id\": \"1bd97891-8161-4616-b034-fd5c593d7758\"}, {\"type\": \"full_width_section\", \"value\": {\"width_css\": \"container-tight\", \"background_color_css\": \"\", \"content\": [{\"type\": \"single_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-center\", \"content\": [{\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h1\", \"heading_text\": \"FAQ\"}, \"id\": \"31115c82-cba5-44ed-bd95-75ab9b63e5dc\"}]}, \"id\": \"0f522496-6c6e-4a85-b93d-964b57e65f31\"}, {\"type\": \"single_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-center\", \"content\": [{\"type\": \"accordion_block\", \"value\": {\"items\": [{\"item_title\": \"I made a recurring/regular donation. How can I change or cancel it?\", \"item_content\": \"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\u201cCANCEL\\u201d in the subject line. (We cannot change your payment details or amount \\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\"}, {\"item_title\": \"Will you share or sell my personal information?\", \"item_content\": \"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\u201cCANCEL\\u201d in the subject line. (We cannot change your payment details or amount \\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\"}], \"footer\": \"<p>Didn\\u2019t find the answer you were looking for? <a href=\\\"https://givehybrid.sytes.net/contact-us\\\">Contact us</a></p>\"}, \"id\": \"45b84aa4-8234-485e-ab33-556a409260ab\"}]}, \"id\": \"509b8058-e8bb-423d-82ea-2c9109a75f68\"}]}, \"id\": \"f64b0ca5-6b5e-408d-a554-e21e90dd22e3\"}, {\"type\": \"full_width_section\", \"value\": {\"width_css\": \"container-tight\", \"background_color_css\": \"bg-primary\", \"content\": [{\"type\": \"single_column_row\", \"value\": {\"alignment_css\": \"column-horz-align-center\", \"content\": [{\"type\": \"heading_block\", \"value\": {\"heading_size\": \"h1\", \"heading_text\": \"Donate Now to Hong Kong Free Press\"}, \"id\": \"003b80d5-7ab6-43b1-8377-ed55645b2e32\"}, {\"type\": \"text_block\", \"value\": \"<p>The HKFP team relies on readers to keep us going and to help safeguard press freedom. You can ensure our independence and help safeguard press freedom with a donation to HKFP.</p>\", \"id\": \"53f080e0-d332-463a-b459-967bccee72c0\"}, {\"type\": \"pagebreaker_block\", \"value\": {\"width_css\": \"w-1/2\"}, \"id\": \"fde31844-73d2-449f-9191-0b02df17ad46\"}, {\"type\": \"buttons_block\", \"value\": [{\"button_text\": \"Donate Now\", \"button_link\": \"https://givehybrid.sytes.net/donations/donate\", \"target_window\": \"_self\"}], \"id\": \"2225ee06-ab1e-45fd-bea2-cc079ed3054f\"}]}, \"id\": \"b49bccc0-26dc-4847-866c-2305f6ae2dfc\"}]}, \"id\": \"919f0d9f-05c3-439b-9911-19c6f1ad6775\"}]');
/*!40000 ALTER TABLE `home_homepage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_settings_adminemails`
--

DROP TABLE IF EXISTS `site_settings_adminemails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_settings_adminemails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `setting_parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `site_settings_adminemails_setting_parent_id_f6d97634` (`setting_parent_id`),
  CONSTRAINT `site_settings_admine_setting_parent_id_f6d97634_fk_site_sett` FOREIGN KEY (`setting_parent_id`) REFERENCES `site_settings_globalsettings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_settings_adminemails`
--

LOCK TABLES `site_settings_adminemails` WRITE;
/*!40000 ALTER TABLE `site_settings_adminemails` DISABLE KEYS */;
INSERT INTO `site_settings_adminemails` VALUES (1,'franky@Diffractive','franky@diffractive.io',1);
/*!40000 ALTER TABLE `site_settings_adminemails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_settings_appearancesettings`
--

DROP TABLE IF EXISTS `site_settings_appearancesettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_settings_appearancesettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand_logo_id` int(11) DEFAULT NULL,
  `site_id` int(11) NOT NULL,
  `site_icon_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`),
  KEY `site_settings_appear_brand_logo_id_e0ceee2e_fk_wagtailim` (`brand_logo_id`),
  KEY `site_settings_appear_site_icon_id_e469f820_fk_wagtailim` (`site_icon_id`),
  CONSTRAINT `site_settings_appear_brand_logo_id_e0ceee2e_fk_wagtailim` FOREIGN KEY (`brand_logo_id`) REFERENCES `wagtailimages_image` (`id`),
  CONSTRAINT `site_settings_appear_site_icon_id_e469f820_fk_wagtailim` FOREIGN KEY (`site_icon_id`) REFERENCES `wagtailimages_image` (`id`),
  CONSTRAINT `site_settings_appear_site_id_4d4b0c3a_fk_wagtailco` FOREIGN KEY (`site_id`) REFERENCES `wagtailcore_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_settings_appearancesettings`
--

LOCK TABLES `site_settings_appearancesettings` WRITE;
/*!40000 ALTER TABLE `site_settings_appearancesettings` DISABLE KEYS */;
INSERT INTO `site_settings_appearancesettings` VALUES (1,5,2,6);
/*!40000 ALTER TABLE `site_settings_appearancesettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_settings_globalsettings`
--

DROP TABLE IF EXISTS `site_settings_globalsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_settings_globalsettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_mode` tinyint(1) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`),
  CONSTRAINT `site_settings_global_site_id_2a80fe87_fk_wagtailco` FOREIGN KEY (`site_id`) REFERENCES `wagtailcore_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_settings_globalsettings`
--

LOCK TABLES `site_settings_globalsettings` WRITE;
/*!40000 ALTER TABLE `site_settings_globalsettings` DISABLE KEYS */;
INSERT INTO `site_settings_globalsettings` VALUES (1,1,'MYR',2);
/*!40000 ALTER TABLE `site_settings_globalsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_settings_settings2c2p`
--

DROP TABLE IF EXISTS `site_settings_settings2c2p`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_settings_settings2c2p` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `merchant_id` varchar(255) DEFAULT NULL,
  `secret_key` varchar(255) DEFAULT NULL,
  `log_filename` varchar(255) DEFAULT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`),
  CONSTRAINT `site_settings_settin_site_id_e1050dda_fk_wagtailco` FOREIGN KEY (`site_id`) REFERENCES `wagtailcore_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_settings_settings2c2p`
--

LOCK TABLES `site_settings_settings2c2p` WRITE;
/*!40000 ALTER TABLE `site_settings_settings2c2p` DISABLE KEYS */;
INSERT INTO `site_settings_settings2c2p` VALUES (1,'458458000000453','021BB08D8E7650D9AE7AA2D8EA0C1A3AF133B03597C5DE17F509F06DFFC3BD19','mypgw.log',2);
/*!40000 ALTER TABLE `site_settings_settings2c2p` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taggit_tag`
--

DROP TABLE IF EXISTS `taggit_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taggit_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taggit_tag`
--

LOCK TABLES `taggit_tag` WRITE;
/*!40000 ALTER TABLE `taggit_tag` DISABLE KEYS */;
INSERT INTO `taggit_tag` VALUES (1,'startup','startup'),(2,'mug','mug'),(3,'memes','memes'),(4,'banner','banner'),(5,'brand','brand');
/*!40000 ALTER TABLE `taggit_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taggit_taggeditem`
--

DROP TABLE IF EXISTS `taggit_taggeditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taggit_taggeditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taggit_taggeditem_content_type_id_object_id_tag_id_4bb97a8e_uniq` (`content_type_id`,`object_id`,`tag_id`),
  KEY `taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id` (`tag_id`),
  KEY `taggit_taggeditem_object_id_e2d7d1df` (`object_id`),
  KEY `taggit_taggeditem_content_type_id_object_id_196cc965_idx` (`content_type_id`,`object_id`),
  CONSTRAINT `taggit_taggeditem_content_type_id_9957a03c_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `taggit_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taggit_taggeditem`
--

LOCK TABLES `taggit_taggeditem` WRITE;
/*!40000 ALTER TABLE `taggit_taggeditem` DISABLE KEYS */;
INSERT INTO `taggit_taggeditem` VALUES (1,1,4,1),(2,1,5,2),(3,2,5,3),(4,3,5,3),(5,4,5,4),(6,5,5,5),(7,6,5,5);
/*!40000 ALTER TABLE `taggit_taggeditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_collection`
--

DROP TABLE IF EXISTS `wagtailcore_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) NOT NULL,
  `depth` int(10) unsigned NOT NULL,
  `numchild` int(10) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_collection`
--

LOCK TABLES `wagtailcore_collection` WRITE;
/*!40000 ALTER TABLE `wagtailcore_collection` DISABLE KEYS */;
INSERT INTO `wagtailcore_collection` VALUES (1,'0001',1,0,'Root');
/*!40000 ALTER TABLE `wagtailcore_collection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_collectionviewrestriction`
--

DROP TABLE IF EXISTS `wagtailcore_collectionviewrestriction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_collectionviewrestriction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `restriction_type` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `collection_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtailcore_collecti_collection_id_761908ec_fk_wagtailco` (`collection_id`),
  CONSTRAINT `wagtailcore_collecti_collection_id_761908ec_fk_wagtailco` FOREIGN KEY (`collection_id`) REFERENCES `wagtailcore_collection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_collectionviewrestriction`
--

LOCK TABLES `wagtailcore_collectionviewrestriction` WRITE;
/*!40000 ALTER TABLE `wagtailcore_collectionviewrestriction` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailcore_collectionviewrestriction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_collectionviewrestriction_groups`
--

DROP TABLE IF EXISTS `wagtailcore_collectionviewrestriction_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_collectionviewrestriction_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `collectionviewrestriction_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailcore_collectionvi_collectionviewrestrictio_988995ae_uniq` (`collectionviewrestriction_id`,`group_id`),
  KEY `wagtailcore_collecti_group_id_1823f2a3_fk_auth_grou` (`group_id`),
  CONSTRAINT `wagtailcore_collecti_collectionviewrestri_47320efd_fk_wagtailco` FOREIGN KEY (`collectionviewrestriction_id`) REFERENCES `wagtailcore_collectionviewrestriction` (`id`),
  CONSTRAINT `wagtailcore_collecti_group_id_1823f2a3_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_collectionviewrestriction_groups`
--

LOCK TABLES `wagtailcore_collectionviewrestriction_groups` WRITE;
/*!40000 ALTER TABLE `wagtailcore_collectionviewrestriction_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailcore_collectionviewrestriction_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_groupcollectionpermission`
--

DROP TABLE IF EXISTS `wagtailcore_groupcollectionpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_groupcollectionpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `collection_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailcore_groupcollect_group_id_collection_id_p_a21cefe9_uniq` (`group_id`,`collection_id`,`permission_id`),
  KEY `wagtailcore_groupcol_collection_id_5423575a_fk_wagtailco` (`collection_id`),
  KEY `wagtailcore_groupcol_permission_id_1b626275_fk_auth_perm` (`permission_id`),
  CONSTRAINT `wagtailcore_groupcol_collection_id_5423575a_fk_wagtailco` FOREIGN KEY (`collection_id`) REFERENCES `wagtailcore_collection` (`id`),
  CONSTRAINT `wagtailcore_groupcol_group_id_05d61460_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `wagtailcore_groupcol_permission_id_1b626275_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_groupcollectionpermission`
--

LOCK TABLES `wagtailcore_groupcollectionpermission` WRITE;
/*!40000 ALTER TABLE `wagtailcore_groupcollectionpermission` DISABLE KEYS */;
INSERT INTO `wagtailcore_groupcollectionpermission` VALUES (2,1,1,2),(4,1,1,3),(6,1,1,5),(8,1,1,6),(1,1,2,2),(3,1,2,3),(5,1,2,5),(7,1,2,6);
/*!40000 ALTER TABLE `wagtailcore_groupcollectionpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_grouppagepermission`
--

DROP TABLE IF EXISTS `wagtailcore_grouppagepermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_grouppagepermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_type` varchar(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailcore_grouppageper_group_id_page_id_permiss_0898bdf8_uniq` (`group_id`,`page_id`,`permission_type`),
  KEY `wagtailcore_grouppag_page_id_710b114a_fk_wagtailco` (`page_id`),
  CONSTRAINT `wagtailcore_grouppag_group_id_fc07e671_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `wagtailcore_grouppag_page_id_710b114a_fk_wagtailco` FOREIGN KEY (`page_id`) REFERENCES `wagtailcore_page` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_grouppagepermission`
--

LOCK TABLES `wagtailcore_grouppagepermission` WRITE;
/*!40000 ALTER TABLE `wagtailcore_grouppagepermission` DISABLE KEYS */;
INSERT INTO `wagtailcore_grouppagepermission` VALUES (1,'add',1,1),(2,'edit',1,1),(6,'lock',1,1),(3,'publish',1,1),(7,'unlock',1,1),(4,'add',2,1),(5,'edit',2,1);
/*!40000 ALTER TABLE `wagtailcore_grouppagepermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_page`
--

DROP TABLE IF EXISTS `wagtailcore_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) NOT NULL,
  `depth` int(10) unsigned NOT NULL,
  `numchild` int(10) unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `live` tinyint(1) NOT NULL,
  `has_unpublished_changes` tinyint(1) NOT NULL,
  `url_path` longtext NOT NULL,
  `seo_title` varchar(255) NOT NULL,
  `show_in_menus` tinyint(1) NOT NULL,
  `search_description` longtext NOT NULL,
  `go_live_at` datetime(6) DEFAULT NULL,
  `expire_at` datetime(6) DEFAULT NULL,
  `expired` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `locked` tinyint(1) NOT NULL,
  `latest_revision_created_at` datetime(6) DEFAULT NULL,
  `first_published_at` datetime(6) DEFAULT NULL,
  `live_revision_id` int(11) DEFAULT NULL,
  `last_published_at` datetime(6) DEFAULT NULL,
  `draft_title` varchar(255) NOT NULL,
  `locked_at` datetime(6) DEFAULT NULL,
  `locked_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`),
  KEY `wagtailcore_page_slug_e7c11b8f` (`slug`),
  KEY `wagtailcore_page_first_published_at_2b5dd637` (`first_published_at`),
  KEY `wagtailcore_page_content_type_id_c28424df_fk_django_co` (`content_type_id`),
  KEY `wagtailcore_page_live_revision_id_930bd822_fk_wagtailco` (`live_revision_id`),
  KEY `wagtailcore_page_owner_id_fbf7c332_fk_custom_user_user_id` (`owner_id`),
  KEY `wagtailcore_page_locked_by_id_bcb86245_fk_custom_user_user_id` (`locked_by_id`),
  CONSTRAINT `wagtailcore_page_content_type_id_c28424df_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `wagtailcore_page_live_revision_id_930bd822_fk_wagtailco` FOREIGN KEY (`live_revision_id`) REFERENCES `wagtailcore_pagerevision` (`id`),
  CONSTRAINT `wagtailcore_page_locked_by_id_bcb86245_fk_custom_user_user_id` FOREIGN KEY (`locked_by_id`) REFERENCES `custom_user_user` (`id`),
  CONSTRAINT `wagtailcore_page_owner_id_fbf7c332_fk_custom_user_user_id` FOREIGN KEY (`owner_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_page`
--

LOCK TABLES `wagtailcore_page` WRITE;
/*!40000 ALTER TABLE `wagtailcore_page` DISABLE KEYS */;
INSERT INTO `wagtailcore_page` VALUES (1,'0001',1,1,'Root','root',1,0,'/','',0,'',NULL,NULL,0,1,NULL,0,NULL,NULL,NULL,NULL,'Root',NULL,NULL),(3,'00010001',2,0,'Home','home',1,0,'/home/','',0,'',NULL,NULL,0,2,NULL,0,'2020-04-27 08:55:44.276343','2020-04-21 09:26:28.295647',27,'2020-04-27 08:55:44.330549','Home',NULL,NULL);
/*!40000 ALTER TABLE `wagtailcore_page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_pagerevision`
--

DROP TABLE IF EXISTS `wagtailcore_pagerevision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_pagerevision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submitted_for_moderation` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `content_json` longtext NOT NULL,
  `approved_go_live_at` datetime(6) DEFAULT NULL,
  `page_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtailcore_pagerevision_submitted_for_moderation_c682e44c` (`submitted_for_moderation`),
  KEY `wagtailcore_pagerevision_page_id_d421cc1d_fk_wagtailcore_page_id` (`page_id`),
  KEY `wagtailcore_pagerevision_user_id_2409d2f4_fk_custom_user_user_id` (`user_id`),
  KEY `wagtailcore_pagerevision_created_at_66954e3b` (`created_at`),
  KEY `wagtailcore_pagerevision_approved_go_live_at_e56afc67` (`approved_go_live_at`),
  CONSTRAINT `wagtailcore_pagerevision_page_id_d421cc1d_fk_wagtailcore_page_id` FOREIGN KEY (`page_id`) REFERENCES `wagtailcore_page` (`id`),
  CONSTRAINT `wagtailcore_pagerevision_user_id_2409d2f4_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_pagerevision`
--

LOCK TABLES `wagtailcore_pagerevision` WRITE;
/*!40000 ALTER TABLE `wagtailcore_pagerevision` DISABLE KEYS */;
INSERT INTO `wagtailcore_pagerevision` VALUES (1,0,'2020-04-21 09:26:28.264263','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": null, \"last_published_at\": null, \"latest_revision_created_at\": null, \"live_revision\": null, \"body\": \"<p>Slam Dunk</p><p>Oh Hi Mark</p>\"}',NULL,3,1),(2,0,'2020-04-21 09:30:57.973140','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T09:26:28.295Z\", \"latest_revision_created_at\": \"2020-04-21T09:26:28.264Z\", \"live_revision\": 1, \"body\": \"<h2>Slam Dunk</h2><h3>Oh Hi Mark</h3><ol><li>stupid</li><li>sandwich</li><li>beaches</li></ol><ul><li>Nope we don&#x27;t do that here</li><li>Yes we offer so much</li></ul><p></p><hr/><p></p><p></p><embed embedtype=\\\"media\\\" url=\\\"https://www.youtube.com/watch?v=YsjGFO3HpOE&amp;list=PLViEDKrLI53mc9qcUUP6xolWnQsS02xD8&amp;index=11\\\"/><p><a id=\\\"1\\\" linktype=\\\"document\\\">test doc</a></p><p></p><embed alt=\\\"test img\\\" embedtype=\\\"image\\\" format=\\\"fullwidth\\\" id=\\\"1\\\"/><p></p>\"}',NULL,3,1),(3,0,'2020-04-21 09:57:37.321162','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T09:30:58.008Z\", \"latest_revision_created_at\": \"2020-04-21T09:30:57.973Z\", \"live_revision\": 2, \"body\": \"[{\\\"type\\\": \\\"heading\\\", \\\"value\\\": \\\"Wholesome Memes\\\", \\\"id\\\": \\\"4dfd4eb6-5837-446b-9bdb-53908db783d0\\\"}, {\\\"type\\\": \\\"image\\\", \\\"value\\\": 2, \\\"id\\\": \\\"9115b16c-2726-4879-9827-57dfea5038f9\\\"}, {\\\"type\\\": \\\"paragraph\\\", \\\"value\\\": \\\"<p><b>Everyone needs someone to lean on sometimes, even penguins</b></p>\\\", \\\"id\\\": \\\"0b97eaa6-6039-4772-b642-ab2c802a2917\\\"}, {\\\"type\\\": \\\"image\\\", \\\"value\\\": 3, \\\"id\\\": \\\"c87e32fc-f22e-4640-b723-fc063c63701b\\\"}, {\\\"type\\\": \\\"paragraph\\\", \\\"value\\\": \\\"<p>Most wholesome dad ever</p>\\\", \\\"id\\\": \\\"fc9ca8bd-fe14-463b-9fac-5ac7925cdd86\\\"}]\"}',NULL,3,1),(4,0,'2020-04-21 10:57:52.236958','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T09:57:37.356Z\", \"latest_revision_created_at\": \"2020-04-21T09:57:37.321Z\", \"live_revision\": 3, \"body\": \"[{\\\"type\\\": \\\"full_width_images\\\", \\\"value\\\": 4, \\\"id\\\": \\\"1d832f9c-34d5-482b-bb6f-71897c5cf786\\\"}, {\\\"type\\\": \\\"raw_html\\\", \\\"value\\\": \\\"<p>Just some raw p tags lying around</p>\\\\r\\\\n<h2>Raw H2 here!</h2>\\\", \\\"id\\\": \\\"c6956281-5b59-4bf7-86d2-9c1b5cb7ebd2\\\"}]\"}',NULL,3,1),(5,0,'2020-04-21 11:42:54.540030','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T10:57:52.273Z\", \"latest_revision_created_at\": \"2020-04-21T10:57:52.236Z\", \"live_revision\": 4, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"6c6c140f-0447-4762-a394-fe1650d8d7a8\\\"}, {\\\"type\\\": \\\"raw_html\\\", \\\"value\\\": \\\"<p>Just some raw p tags lying around</p>\\\\r\\\\n<h2>Raw H2 here!</h2>\\\", \\\"id\\\": \\\"c6956281-5b59-4bf7-86d2-9c1b5cb7ebd2\\\"}]\"}',NULL,3,1),(6,0,'2020-04-21 11:52:02.353641','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T11:42:54.576Z\", \"latest_revision_created_at\": \"2020-04-21T11:42:54.540Z\", \"live_revision\": 5, \"body\": \"[{\\\"type\\\": \\\"raw_html\\\", \\\"value\\\": \\\"sdfadsf\\\", \\\"id\\\": \\\"854848eb-31b8-42d1-b774-249b4c2bfcaf\\\"}]\"}',NULL,3,1),(7,0,'2020-04-21 11:52:25.989195','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T11:52:02.388Z\", \"latest_revision_created_at\": \"2020-04-21T11:52:02.353Z\", \"live_revision\": 6, \"body\": \"[{\\\"type\\\": \\\"raw_html\\\", \\\"value\\\": \\\"sdfadsf\\\", \\\"id\\\": \\\"854848eb-31b8-42d1-b774-249b4c2bfcaf\\\"}, {\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}]\"}',NULL,3,1),(8,0,'2020-04-21 18:53:29.652126','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T11:52:26.023Z\", \"latest_revision_created_at\": \"2020-04-21T11:52:25.989Z\", \"live_revision\": 7, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"two_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"flex flex-col items-center\\\", \\\"column_1\\\": \\\"<p><b>Lorem Ipsum</b> is simply dummy text of the printing and  typesetting industry. Lorem Ipsum has been the industry&#x27;s standard dummy  text ever since the 1500s, when an unknown printer took a galley of  type and scrambled it to make a type specimen book. It has survived not  only five centuries, but also the leap into electronic typesetting,  remaining essentially unchanged. It was popularised in the 1960s with  the release of Letraset sheets containing Lorem Ipsum passages, and more  recently with desktop publishing software like Aldus PageMaker  including versions of Lorem Ipsum.</p>\\\", \\\"column_2\\\": \\\"<p></p><embed alt=\\\\\\\"Penguins\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"2\\\\\\\"/><p></p><p>It is a long established fact that a reader will be distracted by the  readable content of a page when looking at its layout. The point of  using Lorem Ipsum is that it has a more-or-less normal distribution of  letters, as opposed to using &#x27;Content here, content here&#x27;, making it  look like readable English. Many desktop publishing packages and web  page editors now use Lorem Ipsum as their default model text, and a  search for &#x27;lorem ipsum&#x27; will uncover many web sites still in their  infancy. Various versions have evolved over the years, sometimes by  accident, sometimes on purpose (injected humour and the like).</p>\\\"}, \\\"id\\\": \\\"36295ddf-07b8-4024-b67a-9ee5fb450a01\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(9,0,'2020-04-21 19:09:02.794277','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T18:53:29.688Z\", \"latest_revision_created_at\": \"2020-04-21T18:53:29.652Z\", \"live_revision\": 8, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"two_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-center\\\", \\\"column_1\\\": \\\"<p><b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&#x27;s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>\\\", \\\"column_2\\\": \\\"<p></p><embed alt=\\\\\\\"Penguins\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"2\\\\\\\"/><p></p><p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using &#x27;Content here, content here&#x27;, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for &#x27;lorem ipsum&#x27; will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).</p>\\\"}, \\\"id\\\": \\\"36295ddf-07b8-4024-b67a-9ee5fb450a01\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(10,0,'2020-04-21 19:52:56.018343','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T19:09:02.828Z\", \"latest_revision_created_at\": \"2020-04-21T19:09:02.794Z\", \"live_revision\": 9, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-center\\\", \\\"content\\\": \\\"<ol><li>Boom box</li><li>Boom Box</li><li>BooM BooX</li></ol>\\\"}, \\\"id\\\": \\\"3094c3ed-1889-458f-91cb-cb042500990a\\\"}, {\\\"type\\\": \\\"two_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-center\\\", \\\"column_1\\\": \\\"<p><b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&#x27;s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>\\\", \\\"column_2\\\": \\\"<p></p><embed alt=\\\\\\\"Penguins\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"2\\\\\\\"/><p></p><p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using &#x27;Content here, content here&#x27;, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for &#x27;lorem ipsum&#x27; will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).</p>\\\"}, \\\"id\\\": \\\"36295ddf-07b8-4024-b67a-9ee5fb450a01\\\"}, {\\\"type\\\": \\\"three_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-end\\\", \\\"column_1\\\": \\\"<p>Damn COol</p>\\\", \\\"column_2\\\": \\\"<p>Soo good</p>\\\", \\\"column_3\\\": \\\"<p>Hi Mark</p><p></p><embed alt=\\\\\\\"test img\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"1\\\\\\\"/><p></p>\\\"}, \\\"id\\\": \\\"9dd0eaea-8f61-46a3-b65b-d2da94a46a9a\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(11,0,'2020-04-21 20:16:40.863411','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T19:52:56.052Z\", \"latest_revision_created_at\": \"2020-04-21T19:52:56.018Z\", \"live_revision\": 10, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-start\\\", \\\"content\\\": \\\"<ol><li>Boom box</li><li>Boom Box</li><li>BooM BooX</li></ol>\\\"}, \\\"id\\\": \\\"3094c3ed-1889-458f-91cb-cb042500990a\\\"}, {\\\"type\\\": \\\"two_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-center\\\", \\\"column_1\\\": \\\"<p><b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&#x27;s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>\\\", \\\"column_2\\\": \\\"<p></p><embed alt=\\\\\\\"Penguins\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"2\\\\\\\"/><p></p><p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using &#x27;Content here, content here&#x27;, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for &#x27;lorem ipsum&#x27; will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).</p>\\\"}, \\\"id\\\": \\\"36295ddf-07b8-4024-b67a-9ee5fb450a01\\\"}, {\\\"type\\\": \\\"three_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-end\\\", \\\"column_1\\\": \\\"<p>Damn COol</p>\\\", \\\"column_2\\\": \\\"<p>Soo good</p>\\\", \\\"column_3\\\": \\\"<p>Hi Mark</p><p></p><embed alt=\\\\\\\"test img\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"1\\\\\\\"/><p></p>\\\"}, \\\"id\\\": \\\"9dd0eaea-8f61-46a3-b65b-d2da94a46a9a\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(12,0,'2020-04-21 20:26:56.789715','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T20:16:40.899Z\", \"latest_revision_created_at\": \"2020-04-21T20:16:40.863Z\", \"live_revision\": 11, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-start\\\", \\\"content\\\": \\\"<ol><li>Boom box</li><li>Boom Box</li><li>BooM BooX</li></ol>\\\"}, \\\"id\\\": \\\"3094c3ed-1889-458f-91cb-cb042500990a\\\"}, {\\\"type\\\": \\\"two_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-center\\\", \\\"column_1\\\": \\\"<p><b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&#x27;s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>\\\", \\\"column_2\\\": \\\"<p></p><embed alt=\\\\\\\"Penguins\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"2\\\\\\\"/><p></p><p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using &#x27;Content here, content here&#x27;, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for &#x27;lorem ipsum&#x27; will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).</p>\\\"}, \\\"id\\\": \\\"36295ddf-07b8-4024-b67a-9ee5fb450a01\\\"}, {\\\"type\\\": \\\"three_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-end\\\", \\\"column_1\\\": \\\"<p>Damn COol</p>\\\", \\\"column_2\\\": \\\"<p>Soo good</p>\\\", \\\"column_3\\\": \\\"<p>Hi Mark</p><p></p><embed alt=\\\\\\\"test img\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"1\\\\\\\"/><p></p>\\\"}, \\\"id\\\": \\\"9dd0eaea-8f61-46a3-b65b-d2da94a46a9a\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(13,0,'2020-04-22 06:55:22.450603','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-21T20:26:56.835Z\", \"latest_revision_created_at\": \"2020-04-21T20:26:56.789Z\", \"live_revision\": 12, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-start\\\", \\\"content\\\": \\\"<h2>I love coding</h2><h3>i love newstream</h3><h4>i like waffles</h4>\\\"}, \\\"id\\\": \\\"3094c3ed-1889-458f-91cb-cb042500990a\\\"}, {\\\"type\\\": \\\"two_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-center\\\", \\\"column_1\\\": \\\"<p><b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&#x27;s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>\\\", \\\"column_2\\\": \\\"<p></p><embed alt=\\\\\\\"Penguins\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"2\\\\\\\"/><p></p><p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using &#x27;Content here, content here&#x27;, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for &#x27;lorem ipsum&#x27; will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).</p>\\\"}, \\\"id\\\": \\\"36295ddf-07b8-4024-b67a-9ee5fb450a01\\\"}, {\\\"type\\\": \\\"three_column_block\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"richtext-end\\\", \\\"column_1\\\": \\\"<p>Damn COol</p>\\\", \\\"column_2\\\": \\\"<p>Soo good</p>\\\", \\\"column_3\\\": \\\"<p>Hi Mark</p><p></p><embed alt=\\\\\\\"test img\\\\\\\" embedtype=\\\\\\\"image\\\\\\\" format=\\\\\\\"fullwidth\\\\\\\" id=\\\\\\\"1\\\\\\\"/><p></p>\\\"}, \\\"id\\\": \\\"9dd0eaea-8f61-46a3-b65b-d2da94a46a9a\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(14,0,'2020-04-22 09:05:54.756907','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T06:55:22.494Z\", \"latest_revision_created_at\": \"2020-04-22T06:55:22.450Z\", \"live_revision\": 13, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h2\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.<br/></p><p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(15,0,'2020-04-22 09:15:29.372445','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T09:05:54.799Z\", \"latest_revision_created_at\": \"2020-04-22T09:05:54.756Z\", \"live_revision\": 14, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h2\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.<br/></p><p></p><p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(16,0,'2020-04-22 09:19:02.567130','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T09:15:29.409Z\", \"latest_revision_created_at\": \"2020-04-22T09:15:29.372Z\", \"live_revision\": 15, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h2\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(17,0,'2020-04-22 09:28:53.121315','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T09:19:02.604Z\", \"latest_revision_created_at\": \"2020-04-22T09:19:02.567Z\", \"live_revision\": 16, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(18,0,'2020-04-22 09:31:24.792087','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T09:28:53.156Z\", \"latest_revision_created_at\": \"2020-04-22T09:28:53.121Z\", \"live_revision\": 17, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(19,0,'2020-04-22 09:34:54.729101','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T09:31:24.845Z\", \"latest_revision_created_at\": \"2020-04-22T09:31:24.792Z\", \"live_revision\": 18, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"two_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"column_1\\\": [{\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Just testing this stuff.</p>\\\", \\\"id\\\": \\\"b49ff5cd-2cfa-46ec-958f-138089b123d3\\\"}], \\\"column_2\\\": [{\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Another test for this stuff.</p><p>Heey another line is here.</p>\\\", \\\"id\\\": \\\"6e6c6baf-9e2e-4d14-876d-33ea7bd34b5b\\\"}]}, \\\"id\\\": \\\"9ff7e29e-0c38-46fc-a19b-3b559ba080dc\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(20,0,'2020-04-22 10:52:13.466053','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T09:34:54.765Z\", \"latest_revision_created_at\": \"2020-04-22T09:34:54.729Z\", \"live_revision\": 19, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p></p><embed embedtype=\\\\\\\"media\\\\\\\" url=\\\\\\\"https://www.youtube.com/watch?v=IhOMzWFZrIw\\\\\\\"/><p></p>\\\", \\\"id\\\": \\\"14275e47-2521-45cf-9408-76af45a02e3c\\\"}]}, \\\"id\\\": \\\"4a825fde-e3d5-431d-bcfc-fc943719b0d4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(21,0,'2020-04-22 10:55:04.590937','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T10:52:13.501Z\", \"latest_revision_created_at\": \"2020-04-22T10:52:13.466Z\", \"live_revision\": 20, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(22,0,'2020-04-22 10:56:35.921294','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T10:55:04.633Z\", \"latest_revision_created_at\": \"2020-04-22T10:55:04.590Z\", \"live_revision\": 21, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"html_block\\\", \\\"value\\\": \\\"<iframe width=\\\\\\\"794\\\\\\\" height=\\\\\\\"466\\\\\\\" src=\\\\\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\\\\\" frameborder=\\\\\\\"0\\\\\\\" allow=\\\\\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\\\\\" allowfullscreen></iframe>\\\", \\\"id\\\": \\\"7ee637b7-6aa7-4767-97f1-d24f560d70a1\\\"}]}, \\\"id\\\": \\\"1028ce3c-03fa-4592-aafc-0112bfece2b4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}]\"}',NULL,3,1),(23,0,'2020-04-22 11:23:47.409680','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T10:56:35.965Z\", \"latest_revision_created_at\": \"2020-04-22T10:56:35.921Z\", \"live_revision\": 22, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"bg-primary\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"html_block\\\", \\\"value\\\": \\\"<iframe width=\\\\\\\"794\\\\\\\" height=\\\\\\\"466\\\\\\\" src=\\\\\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\\\\\" frameborder=\\\\\\\"0\\\\\\\" allow=\\\\\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\\\\\" allowfullscreen></iframe>\\\", \\\"id\\\": \\\"7ee637b7-6aa7-4767-97f1-d24f560d70a1\\\"}]}, \\\"id\\\": \\\"1028ce3c-03fa-4592-aafc-0112bfece2b4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"background_color_css\\\": \\\"bg-primary-light\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Why trust us?\\\"}, \\\"id\\\": \\\"4256376e-6555-47d1-8a9a-51e09240aec3\\\"}]}, \\\"id\\\": \\\"3470abcc-8d1c-4703-bca9-8d8eed931a5a\\\"}, {\\\"type\\\": \\\"two_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-start\\\", \\\"column_1\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Immune to censorship\\\"}, \\\"id\\\": \\\"0e14ecb2-5a2e-46ee-a40b-6163793ed647\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>HKFP is answerable only to readers \\\\u2013 we have no investors, no shareholders, no tycoons, no mainland owners or umbrella company behind us. Our independence means we are fully resistant to censorship and self-censorship.</p>\\\", \\\"id\\\": \\\"dc9d600e-56f4-4f46-bb73-b10e6c90f355\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Transparent & efficient\\\"}, \\\"id\\\": \\\"32f37298-0eef-44b0-881b-1be9917c6a81\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We are the city\\\\u2019s most transparent news outlet \\\\u2013 we undergo an external audit each year and publish an annual Transparency Report. 84 per cent of income comes from donations, whilst 81 per cent of spending goes simply towards paying journalists. Teamwork, automation, partnerships and the use of free digital tools keep our costs down.</p>\\\", \\\"id\\\": \\\"eef7de95-3180-4ef5-b3e0-0011acf5e0e1\\\"}], \\\"column_2\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Non-profit model\\\"}, \\\"id\\\": \\\"e89acf3f-66bd-4789-b7e3-dd5d37c59172\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>As a non-profit, limited by guarantee company, any surplus we make is recycled back into the company. We are run by journalists and immune to commercial and political pressure.</p>\\\", \\\"id\\\": \\\"30994f40-92e7-4381-b9d2-4e178e96db81\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Accurate & accountable\\\"}, \\\"id\\\": \\\"ee67cbd2-2ad9-4141-b788-1d03c44a7ff2\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We ensure everything we publish includes a balance of viewpoints in order to avoid any bias. All facts, quotes and figures are properly attributed to the source, often with links to the original material. Our own opinions are kept out of our copy, whilst we act quickly and transparently to correct errors. HKFP avoids sensationalism and clickbait, and clearly marks paid-for content as \\\\u201csponsored.\\\\u201d Accuracy and fairness are our top priorities.</p>\\\", \\\"id\\\": \\\"8ccd9457-3ab5-4a56-9eba-185e93a10475\\\"}]}, \\\"id\\\": \\\"61395600-d34f-456e-9a02-454a59cd6c73\\\"}]}, \\\"id\\\": \\\"1bd97891-8161-4616-b034-fd5c593d7758\\\"}]\"}',NULL,3,1),(24,0,'2020-04-22 11:26:39.449772','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T11:23:47.462Z\", \"latest_revision_created_at\": \"2020-04-22T11:23:47.409Z\", \"live_revision\": 23, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"html_block\\\", \\\"value\\\": \\\"<iframe width=\\\\\\\"794\\\\\\\" height=\\\\\\\"466\\\\\\\" src=\\\\\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\\\\\" frameborder=\\\\\\\"0\\\\\\\" allow=\\\\\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\\\\\" allowfullscreen></iframe>\\\", \\\"id\\\": \\\"7ee637b7-6aa7-4767-97f1-d24f560d70a1\\\"}]}, \\\"id\\\": \\\"1028ce3c-03fa-4592-aafc-0112bfece2b4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"background_color_css\\\": \\\"bg-primary-light\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Why trust us?\\\"}, \\\"id\\\": \\\"4256376e-6555-47d1-8a9a-51e09240aec3\\\"}]}, \\\"id\\\": \\\"3470abcc-8d1c-4703-bca9-8d8eed931a5a\\\"}, {\\\"type\\\": \\\"two_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-start\\\", \\\"column_1\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Immune to censorship\\\"}, \\\"id\\\": \\\"0e14ecb2-5a2e-46ee-a40b-6163793ed647\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>HKFP is answerable only to readers \\\\u2013 we have no investors, no shareholders, no tycoons, no mainland owners or umbrella company behind us. Our independence means we are fully resistant to censorship and self-censorship.</p>\\\", \\\"id\\\": \\\"dc9d600e-56f4-4f46-bb73-b10e6c90f355\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Transparent & efficient\\\"}, \\\"id\\\": \\\"32f37298-0eef-44b0-881b-1be9917c6a81\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We are the city\\\\u2019s most transparent news outlet \\\\u2013 we undergo an external audit each year and publish an annual Transparency Report. 84 per cent of income comes from donations, whilst 81 per cent of spending goes simply towards paying journalists. Teamwork, automation, partnerships and the use of free digital tools keep our costs down.</p>\\\", \\\"id\\\": \\\"eef7de95-3180-4ef5-b3e0-0011acf5e0e1\\\"}], \\\"column_2\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Non-profit model\\\"}, \\\"id\\\": \\\"e89acf3f-66bd-4789-b7e3-dd5d37c59172\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>As a non-profit, limited by guarantee company, any surplus we make is recycled back into the company. We are run by journalists and immune to commercial and political pressure.</p>\\\", \\\"id\\\": \\\"30994f40-92e7-4381-b9d2-4e178e96db81\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Accurate & accountable\\\"}, \\\"id\\\": \\\"ee67cbd2-2ad9-4141-b788-1d03c44a7ff2\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We ensure everything we publish includes a balance of viewpoints in order to avoid any bias. All facts, quotes and figures are properly attributed to the source, often with links to the original material. Our own opinions are kept out of our copy, whilst we act quickly and transparently to correct errors. HKFP avoids sensationalism and clickbait, and clearly marks paid-for content as \\\\u201csponsored.\\\\u201d Accuracy and fairness are our top priorities.</p>\\\", \\\"id\\\": \\\"8ccd9457-3ab5-4a56-9eba-185e93a10475\\\"}]}, \\\"id\\\": \\\"61395600-d34f-456e-9a02-454a59cd6c73\\\"}]}, \\\"id\\\": \\\"1bd97891-8161-4616-b034-fd5c593d7758\\\"}]\"}',NULL,3,1),(25,0,'2020-04-22 12:19:17.565796','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T11:26:39.485Z\", \"latest_revision_created_at\": \"2020-04-22T11:26:39.449Z\", \"live_revision\": 24, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"html_block\\\", \\\"value\\\": \\\"<iframe width=\\\\\\\"794\\\\\\\" height=\\\\\\\"466\\\\\\\" src=\\\\\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\\\\\" frameborder=\\\\\\\"0\\\\\\\" allow=\\\\\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\\\\\" allowfullscreen></iframe>\\\", \\\"id\\\": \\\"7ee637b7-6aa7-4767-97f1-d24f560d70a1\\\"}]}, \\\"id\\\": \\\"1028ce3c-03fa-4592-aafc-0112bfece2b4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"background_color_css\\\": \\\"bg-primary-light\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Why trust us?\\\"}, \\\"id\\\": \\\"4256376e-6555-47d1-8a9a-51e09240aec3\\\"}]}, \\\"id\\\": \\\"3470abcc-8d1c-4703-bca9-8d8eed931a5a\\\"}, {\\\"type\\\": \\\"two_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-start\\\", \\\"column_1\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Immune to censorship\\\"}, \\\"id\\\": \\\"0e14ecb2-5a2e-46ee-a40b-6163793ed647\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>HKFP is answerable only to readers \\\\u2013 we have no investors, no shareholders, no tycoons, no mainland owners or umbrella company behind us. Our independence means we are fully resistant to censorship and self-censorship.</p>\\\", \\\"id\\\": \\\"dc9d600e-56f4-4f46-bb73-b10e6c90f355\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Transparent & efficient\\\"}, \\\"id\\\": \\\"32f37298-0eef-44b0-881b-1be9917c6a81\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We are the city\\\\u2019s most transparent news outlet \\\\u2013 we undergo an external audit each year and publish an annual Transparency Report. 84 per cent of income comes from donations, whilst 81 per cent of spending goes simply towards paying journalists. Teamwork, automation, partnerships and the use of free digital tools keep our costs down.</p>\\\", \\\"id\\\": \\\"eef7de95-3180-4ef5-b3e0-0011acf5e0e1\\\"}], \\\"column_2\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Non-profit model\\\"}, \\\"id\\\": \\\"e89acf3f-66bd-4789-b7e3-dd5d37c59172\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>As a non-profit, limited by guarantee company, any surplus we make is recycled back into the company. We are run by journalists and immune to commercial and political pressure.</p>\\\", \\\"id\\\": \\\"30994f40-92e7-4381-b9d2-4e178e96db81\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Accurate & accountable\\\"}, \\\"id\\\": \\\"ee67cbd2-2ad9-4141-b788-1d03c44a7ff2\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We ensure everything we publish includes a balance of viewpoints in order to avoid any bias. All facts, quotes and figures are properly attributed to the source, often with links to the original material. Our own opinions are kept out of our copy, whilst we act quickly and transparently to correct errors. HKFP avoids sensationalism and clickbait, and clearly marks paid-for content as \\\\u201csponsored.\\\\u201d Accuracy and fairness are our top priorities.</p>\\\", \\\"id\\\": \\\"8ccd9457-3ab5-4a56-9eba-185e93a10475\\\"}]}, \\\"id\\\": \\\"61395600-d34f-456e-9a02-454a59cd6c73\\\"}]}, \\\"id\\\": \\\"1bd97891-8161-4616-b034-fd5c593d7758\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"FAQ\\\"}, \\\"id\\\": \\\"31115c82-cba5-44ed-bd95-75ab9b63e5dc\\\"}]}, \\\"id\\\": \\\"0f522496-6c6e-4a85-b93d-964b57e65f31\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"accordion_block\\\", \\\"value\\\": {\\\"items\\\": [{\\\"item_title\\\": \\\"I made a recurring/regular donation. How can I change or cancel it?\\\", \\\"item_content\\\": \\\"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\\\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\\\u201cCANCEL\\\\u201d in the subject line. (We cannot change your payment details or amount \\\\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\\\"}, {\\\"item_title\\\": \\\"Will you share or sell my personal information?\\\", \\\"item_content\\\": \\\"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\\\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\\\u201cCANCEL\\\\u201d in the subject line. (We cannot change your payment details or amount \\\\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\\\"}], \\\"footer\\\": \\\"<p>Didn\\\\u2019t find the answer you were looking for?  <a href=\\\\\\\"https://givehybrid.sytes.net/contact-us\\\\\\\">Contact us</a></p>\\\"}, \\\"id\\\": \\\"45b84aa4-8234-485e-ab33-556a409260ab\\\"}]}, \\\"id\\\": \\\"509b8058-e8bb-423d-82ea-2c9109a75f68\\\"}]}, \\\"id\\\": \\\"f64b0ca5-6b5e-408d-a554-e21e90dd22e3\\\"}]\"}',NULL,3,1),(26,0,'2020-04-22 16:28:37.602292','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T12:19:17.610Z\", \"latest_revision_created_at\": \"2020-04-22T12:19:17.565Z\", \"live_revision\": 25, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/onetime-donation\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"html_block\\\", \\\"value\\\": \\\"<iframe width=\\\\\\\"794\\\\\\\" height=\\\\\\\"466\\\\\\\" src=\\\\\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\\\\\" frameborder=\\\\\\\"0\\\\\\\" allow=\\\\\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\\\\\" allowfullscreen></iframe>\\\", \\\"id\\\": \\\"7ee637b7-6aa7-4767-97f1-d24f560d70a1\\\"}]}, \\\"id\\\": \\\"1028ce3c-03fa-4592-aafc-0112bfece2b4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"background_color_css\\\": \\\"bg-primary-light\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Why trust us?\\\"}, \\\"id\\\": \\\"4256376e-6555-47d1-8a9a-51e09240aec3\\\"}]}, \\\"id\\\": \\\"3470abcc-8d1c-4703-bca9-8d8eed931a5a\\\"}, {\\\"type\\\": \\\"two_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-start\\\", \\\"column_1\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Immune to censorship\\\"}, \\\"id\\\": \\\"0e14ecb2-5a2e-46ee-a40b-6163793ed647\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>HKFP is answerable only to readers \\\\u2013 we have no investors, no shareholders, no tycoons, no mainland owners or umbrella company behind us. Our independence means we are fully resistant to censorship and self-censorship.</p>\\\", \\\"id\\\": \\\"dc9d600e-56f4-4f46-bb73-b10e6c90f355\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Transparent & efficient\\\"}, \\\"id\\\": \\\"32f37298-0eef-44b0-881b-1be9917c6a81\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We are the city\\\\u2019s most transparent news outlet \\\\u2013 we undergo an external audit each year and publish an annual Transparency Report. 84 per cent of income comes from donations, whilst 81 per cent of spending goes simply towards paying journalists. Teamwork, automation, partnerships and the use of free digital tools keep our costs down.</p>\\\", \\\"id\\\": \\\"eef7de95-3180-4ef5-b3e0-0011acf5e0e1\\\"}], \\\"column_2\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Non-profit model\\\"}, \\\"id\\\": \\\"e89acf3f-66bd-4789-b7e3-dd5d37c59172\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>As a non-profit, limited by guarantee company, any surplus we make is recycled back into the company. We are run by journalists and immune to commercial and political pressure.</p>\\\", \\\"id\\\": \\\"30994f40-92e7-4381-b9d2-4e178e96db81\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Accurate & accountable\\\"}, \\\"id\\\": \\\"ee67cbd2-2ad9-4141-b788-1d03c44a7ff2\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We ensure everything we publish includes a balance of viewpoints in order to avoid any bias. All facts, quotes and figures are properly attributed to the source, often with links to the original material. Our own opinions are kept out of our copy, whilst we act quickly and transparently to correct errors. HKFP avoids sensationalism and clickbait, and clearly marks paid-for content as \\\\u201csponsored.\\\\u201d Accuracy and fairness are our top priorities.</p>\\\", \\\"id\\\": \\\"8ccd9457-3ab5-4a56-9eba-185e93a10475\\\"}]}, \\\"id\\\": \\\"61395600-d34f-456e-9a02-454a59cd6c73\\\"}]}, \\\"id\\\": \\\"1bd97891-8161-4616-b034-fd5c593d7758\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"FAQ\\\"}, \\\"id\\\": \\\"31115c82-cba5-44ed-bd95-75ab9b63e5dc\\\"}]}, \\\"id\\\": \\\"0f522496-6c6e-4a85-b93d-964b57e65f31\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"accordion_block\\\", \\\"value\\\": {\\\"items\\\": [{\\\"item_title\\\": \\\"I made a recurring/regular donation. How can I change or cancel it?\\\", \\\"item_content\\\": \\\"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\\\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\\\u201cCANCEL\\\\u201d in the subject line. (We cannot change your payment details or amount \\\\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\\\"}, {\\\"item_title\\\": \\\"Will you share or sell my personal information?\\\", \\\"item_content\\\": \\\"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\\\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\\\u201cCANCEL\\\\u201d in the subject line. (We cannot change your payment details or amount \\\\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\\\"}], \\\"footer\\\": \\\"<p>Didn\\\\u2019t find the answer you were looking for? <a href=\\\\\\\"https://givehybrid.sytes.net/contact-us\\\\\\\">Contact us</a></p>\\\"}, \\\"id\\\": \\\"45b84aa4-8234-485e-ab33-556a409260ab\\\"}]}, \\\"id\\\": \\\"509b8058-e8bb-423d-82ea-2c9109a75f68\\\"}]}, \\\"id\\\": \\\"f64b0ca5-6b5e-408d-a554-e21e90dd22e3\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"bg-primary\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Donate Now to Hong Kong Free Press\\\"}, \\\"id\\\": \\\"003b80d5-7ab6-43b1-8377-ed55645b2e32\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>The HKFP team relies on readers to keep us going and to help safeguard press freedom. You can ensure our independence and help safeguard press freedom with a donation to HKFP.</p>\\\", \\\"id\\\": \\\"53f080e0-d332-463a-b459-967bccee72c0\\\"}, {\\\"type\\\": \\\"pagebreaker_block\\\", \\\"value\\\": {\\\"width_css\\\": \\\"w-1/2\\\"}, \\\"id\\\": \\\"fde31844-73d2-449f-9191-0b02df17ad46\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate Now\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donate\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"2225ee06-ab1e-45fd-bea2-cc079ed3054f\\\"}]}, \\\"id\\\": \\\"b49bccc0-26dc-4847-866c-2305f6ae2dfc\\\"}]}, \\\"id\\\": \\\"919f0d9f-05c3-439b-9911-19c6f1ad6775\\\"}]\"}',NULL,3,1),(27,0,'2020-04-27 08:55:44.276343','{\"pk\": 3, \"path\": \"00010001\", \"depth\": 2, \"numchild\": 0, \"title\": \"Home\", \"draft_title\": \"Home\", \"slug\": \"home\", \"content_type\": 2, \"live\": true, \"has_unpublished_changes\": false, \"url_path\": \"/home/\", \"owner\": null, \"seo_title\": \"\", \"show_in_menus\": false, \"search_description\": \"\", \"go_live_at\": null, \"expire_at\": null, \"expired\": false, \"locked\": false, \"locked_at\": null, \"locked_by\": null, \"first_published_at\": \"2020-04-21T09:26:28.295Z\", \"last_published_at\": \"2020-04-22T16:28:37.637Z\", \"latest_revision_created_at\": \"2020-04-22T16:28:37.602Z\", \"live_revision\": 26, \"body\": \"[{\\\"type\\\": \\\"full_width_image\\\", \\\"value\\\": {\\\"banner\\\": 4}, \\\"id\\\": \\\"b3baadaa-954f-434e-a0de-c8bae6e12b7a\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Support Hong Kong Free Press\\\"}, \\\"id\\\": \\\"b57e29ec-b73e-4cd3-b9b9-cc50271fe651\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>Whilst English-language journalism in Hong Kong can be tough and expensive, supporting us needn\\\\u2019t be! In just a couple of minutes, <b>you can ensure our independence and help safeguard press freedom with a donation to HKFP</b>.</p>\\\", \\\"id\\\": \\\"4f91b372-4339-4501-ab21-027eda2ed7af\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p><b>Not-for-profit, run by journalists and completely independent</b>, the HKFP team relies on readers to keep us going and to help safeguard press freedom. Learn more about our achievements in our latest Annual Report. Our Transparency Report shows how carefully we spend every cent.</p>\\\", \\\"id\\\": \\\"a87972a6-7d1c-4255-bad8-063ea0866422\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate to HKFP\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/donate\\\", \\\"target_window\\\": \\\"_self\\\"}, {\\\"button_text\\\": \\\"12 ways to support\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/donate\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"f979d243-8e54-4b0c-b092-a67eb54d4a6e\\\"}]}, \\\"id\\\": \\\"6208f365-bdb5-46c1-9d52-c53371a3cee4\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"html_block\\\", \\\"value\\\": \\\"<iframe width=\\\\\\\"794\\\\\\\" height=\\\\\\\"466\\\\\\\" src=\\\\\\\"https://www.youtube.com/embed/IhOMzWFZrIw\\\\\\\" frameborder=\\\\\\\"0\\\\\\\" allow=\\\\\\\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\\\\\\\" allowfullscreen></iframe>\\\", \\\"id\\\": \\\"7ee637b7-6aa7-4767-97f1-d24f560d70a1\\\"}]}, \\\"id\\\": \\\"1028ce3c-03fa-4592-aafc-0112bfece2b4\\\"}]}, \\\"id\\\": \\\"0dbb1645-e174-4205-8deb-abd20eb59b55\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container\\\", \\\"background_color_css\\\": \\\"bg-primary-light\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Why trust us?\\\"}, \\\"id\\\": \\\"4256376e-6555-47d1-8a9a-51e09240aec3\\\"}]}, \\\"id\\\": \\\"3470abcc-8d1c-4703-bca9-8d8eed931a5a\\\"}, {\\\"type\\\": \\\"two_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-start\\\", \\\"column_1\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Immune to censorship\\\"}, \\\"id\\\": \\\"0e14ecb2-5a2e-46ee-a40b-6163793ed647\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>HKFP is answerable only to readers \\\\u2013 we have no investors, no shareholders, no tycoons, no mainland owners or umbrella company behind us. Our independence means we are fully resistant to censorship and self-censorship.</p>\\\", \\\"id\\\": \\\"dc9d600e-56f4-4f46-bb73-b10e6c90f355\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Transparent & efficient\\\"}, \\\"id\\\": \\\"32f37298-0eef-44b0-881b-1be9917c6a81\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We are the city\\\\u2019s most transparent news outlet \\\\u2013 we undergo an external audit each year and publish an annual Transparency Report. 84 per cent of income comes from donations, whilst 81 per cent of spending goes simply towards paying journalists. Teamwork, automation, partnerships and the use of free digital tools keep our costs down.</p>\\\", \\\"id\\\": \\\"eef7de95-3180-4ef5-b3e0-0011acf5e0e1\\\"}], \\\"column_2\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Non-profit model\\\"}, \\\"id\\\": \\\"e89acf3f-66bd-4789-b7e3-dd5d37c59172\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>As a non-profit, limited by guarantee company, any surplus we make is recycled back into the company. We are run by journalists and immune to commercial and political pressure.</p>\\\", \\\"id\\\": \\\"30994f40-92e7-4381-b9d2-4e178e96db81\\\"}, {\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h4\\\", \\\"heading_text\\\": \\\"Accurate & accountable\\\"}, \\\"id\\\": \\\"ee67cbd2-2ad9-4141-b788-1d03c44a7ff2\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>We ensure everything we publish includes a balance of viewpoints in order to avoid any bias. All facts, quotes and figures are properly attributed to the source, often with links to the original material. Our own opinions are kept out of our copy, whilst we act quickly and transparently to correct errors. HKFP avoids sensationalism and clickbait, and clearly marks paid-for content as \\\\u201csponsored.\\\\u201d Accuracy and fairness are our top priorities.</p>\\\", \\\"id\\\": \\\"8ccd9457-3ab5-4a56-9eba-185e93a10475\\\"}]}, \\\"id\\\": \\\"61395600-d34f-456e-9a02-454a59cd6c73\\\"}]}, \\\"id\\\": \\\"1bd97891-8161-4616-b034-fd5c593d7758\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"FAQ\\\"}, \\\"id\\\": \\\"31115c82-cba5-44ed-bd95-75ab9b63e5dc\\\"}]}, \\\"id\\\": \\\"0f522496-6c6e-4a85-b93d-964b57e65f31\\\"}, {\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"accordion_block\\\", \\\"value\\\": {\\\"items\\\": [{\\\"item_title\\\": \\\"I made a recurring/regular donation. How can I change or cancel it?\\\", \\\"item_content\\\": \\\"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\\\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\\\u201cCANCEL\\\\u201d in the subject line. (We cannot change your payment details or amount \\\\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\\\"}, {\\\"item_title\\\": \\\"Will you share or sell my personal information?\\\", \\\"item_content\\\": \\\"<p>You may cancel your monthly donation at any time by emailing donations@hongkongfp.com \\\\u2013 we aim to respond within 1-2 business days. From the email address you set up your recurring donation, simply state \\\\u201cCANCEL\\\\u201d in the subject line. (We cannot change your payment details or amount \\\\u2013 please cancel your regular payment and set up a new one.) If you donated via PayPal, you may cancel/adjust the payment yourself.</p>\\\"}], \\\"footer\\\": \\\"<p>Didn\\\\u2019t find the answer you were looking for? <a href=\\\\\\\"https://givehybrid.sytes.net/contact-us\\\\\\\">Contact us</a></p>\\\"}, \\\"id\\\": \\\"45b84aa4-8234-485e-ab33-556a409260ab\\\"}]}, \\\"id\\\": \\\"509b8058-e8bb-423d-82ea-2c9109a75f68\\\"}]}, \\\"id\\\": \\\"f64b0ca5-6b5e-408d-a554-e21e90dd22e3\\\"}, {\\\"type\\\": \\\"full_width_section\\\", \\\"value\\\": {\\\"width_css\\\": \\\"container-tight\\\", \\\"background_color_css\\\": \\\"bg-primary\\\", \\\"content\\\": [{\\\"type\\\": \\\"single_column_row\\\", \\\"value\\\": {\\\"alignment_css\\\": \\\"column-horz-align-center\\\", \\\"content\\\": [{\\\"type\\\": \\\"heading_block\\\", \\\"value\\\": {\\\"heading_size\\\": \\\"h1\\\", \\\"heading_text\\\": \\\"Donate Now to Hong Kong Free Press\\\"}, \\\"id\\\": \\\"003b80d5-7ab6-43b1-8377-ed55645b2e32\\\"}, {\\\"type\\\": \\\"text_block\\\", \\\"value\\\": \\\"<p>The HKFP team relies on readers to keep us going and to help safeguard press freedom. You can ensure our independence and help safeguard press freedom with a donation to HKFP.</p>\\\", \\\"id\\\": \\\"53f080e0-d332-463a-b459-967bccee72c0\\\"}, {\\\"type\\\": \\\"pagebreaker_block\\\", \\\"value\\\": {\\\"width_css\\\": \\\"w-1/2\\\"}, \\\"id\\\": \\\"fde31844-73d2-449f-9191-0b02df17ad46\\\"}, {\\\"type\\\": \\\"buttons_block\\\", \\\"value\\\": [{\\\"button_text\\\": \\\"Donate Now\\\", \\\"button_link\\\": \\\"https://givehybrid.sytes.net/donations/donate\\\", \\\"target_window\\\": \\\"_self\\\"}], \\\"id\\\": \\\"2225ee06-ab1e-45fd-bea2-cc079ed3054f\\\"}]}, \\\"id\\\": \\\"b49bccc0-26dc-4847-866c-2305f6ae2dfc\\\"}]}, \\\"id\\\": \\\"919f0d9f-05c3-439b-9911-19c6f1ad6775\\\"}]\"}',NULL,3,1);
/*!40000 ALTER TABLE `wagtailcore_pagerevision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_pageviewrestriction`
--

DROP TABLE IF EXISTS `wagtailcore_pageviewrestriction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_pageviewrestriction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(255) NOT NULL,
  `page_id` int(11) NOT NULL,
  `restriction_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtailcore_pageview_page_id_15a8bea6_fk_wagtailco` (`page_id`),
  CONSTRAINT `wagtailcore_pageview_page_id_15a8bea6_fk_wagtailco` FOREIGN KEY (`page_id`) REFERENCES `wagtailcore_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_pageviewrestriction`
--

LOCK TABLES `wagtailcore_pageviewrestriction` WRITE;
/*!40000 ALTER TABLE `wagtailcore_pageviewrestriction` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailcore_pageviewrestriction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_pageviewrestriction_groups`
--

DROP TABLE IF EXISTS `wagtailcore_pageviewrestriction_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_pageviewrestriction_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pageviewrestriction_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailcore_pageviewrest_pageviewrestriction_id_g_d23f80bb_uniq` (`pageviewrestriction_id`,`group_id`),
  KEY `wagtailcore_pageview_group_id_6460f223_fk_auth_grou` (`group_id`),
  CONSTRAINT `wagtailcore_pageview_group_id_6460f223_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `wagtailcore_pageview_pageviewrestriction__f147a99a_fk_wagtailco` FOREIGN KEY (`pageviewrestriction_id`) REFERENCES `wagtailcore_pageviewrestriction` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_pageviewrestriction_groups`
--

LOCK TABLES `wagtailcore_pageviewrestriction_groups` WRITE;
/*!40000 ALTER TABLE `wagtailcore_pageviewrestriction_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailcore_pageviewrestriction_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailcore_site`
--

DROP TABLE IF EXISTS `wagtailcore_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailcore_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `port` int(11) NOT NULL,
  `is_default_site` tinyint(1) NOT NULL,
  `root_page_id` int(11) NOT NULL,
  `site_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailcore_site_hostname_port_2c626d70_uniq` (`hostname`,`port`),
  KEY `wagtailcore_site_hostname_96b20b46` (`hostname`),
  KEY `wagtailcore_site_root_page_id_e02fb95c_fk_wagtailcore_page_id` (`root_page_id`),
  CONSTRAINT `wagtailcore_site_root_page_id_e02fb95c_fk_wagtailcore_page_id` FOREIGN KEY (`root_page_id`) REFERENCES `wagtailcore_page` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailcore_site`
--

LOCK TABLES `wagtailcore_site` WRITE;
/*!40000 ALTER TABLE `wagtailcore_site` DISABLE KEYS */;
INSERT INTO `wagtailcore_site` VALUES (2,'localhost',80,1,3,'Newstream');
/*!40000 ALTER TABLE `wagtailcore_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtaildocs_document`
--

DROP TABLE IF EXISTS `wagtaildocs_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtaildocs_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `file` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `uploaded_by_user_id` int(11) DEFAULT NULL,
  `collection_id` int(11) NOT NULL,
  `file_size` int(10) unsigned DEFAULT NULL,
  `file_hash` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtaildocs_document_collection_id_23881625_fk_wagtailco` (`collection_id`),
  KEY `wagtaildocs_document_uploaded_by_user_id_17258b41_fk_custom_us` (`uploaded_by_user_id`),
  CONSTRAINT `wagtaildocs_document_collection_id_23881625_fk_wagtailco` FOREIGN KEY (`collection_id`) REFERENCES `wagtailcore_collection` (`id`),
  CONSTRAINT `wagtaildocs_document_uploaded_by_user_id_17258b41_fk_custom_us` FOREIGN KEY (`uploaded_by_user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtaildocs_document`
--

LOCK TABLES `wagtaildocs_document` WRITE;
/*!40000 ALTER TABLE `wagtaildocs_document` DISABLE KEYS */;
INSERT INTO `wagtaildocs_document` VALUES (1,'test doc','documents/draft_startup_intro.pdf','2020-04-21 09:30:18.880289',1,1,432906,'260095a69b5dc04f974cd7135d0c7a77960fc8af');
/*!40000 ALTER TABLE `wagtaildocs_document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailembeds_embed`
--

DROP TABLE IF EXISTS `wagtailembeds_embed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailembeds_embed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) NOT NULL,
  `max_width` smallint(6) DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `html` longtext NOT NULL,
  `title` longtext NOT NULL,
  `author_name` longtext NOT NULL,
  `provider_name` longtext NOT NULL,
  `thumbnail_url` varchar(255) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `last_updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailembeds_embed_url_max_width_8a2922d8_uniq` (`url`,`max_width`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailembeds_embed`
--

LOCK TABLES `wagtailembeds_embed` WRITE;
/*!40000 ALTER TABLE `wagtailembeds_embed` DISABLE KEYS */;
INSERT INTO `wagtailembeds_embed` VALUES (1,'https://www.youtube.com/watch?v=YsjGFO3HpOE&list=PLViEDKrLI53mc9qcUUP6xolWnQsS02xD8&index=11',NULL,'video','<iframe width=\"480\" height=\"270\" src=\"https://www.youtube.com/embed/videoseries?list=PLViEDKrLI53mc9qcUUP6xolWnQsS02xD8\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>','Bee Gees - You Should Be Dancing (Audio) [READY PLAYER ONE (2018) - SOUNDTRACK]','TV Series & Movie Soundtrack 3','YouTube','https://i.ytimg.com/vi/YsjGFO3HpOE/hqdefault.jpg',480,270,'2020-04-21 09:27:45.772803'),(2,'https://www.youtube.com/watch?v=IhOMzWFZrIw',NULL,'video','<iframe width=\"480\" height=\"270\" src=\"https://www.youtube.com/embed/IhOMzWFZrIw?feature=oembed\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>','Support Hong Kong Free Press: Non-profit, run by journalists, completely independent','Hong Kong Free Press','YouTube','https://i.ytimg.com/vi/IhOMzWFZrIw/hqdefault.jpg',480,270,'2020-04-22 10:52:06.652879');
/*!40000 ALTER TABLE `wagtailembeds_embed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailforms_formsubmission`
--

DROP TABLE IF EXISTS `wagtailforms_formsubmission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailforms_formsubmission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `form_data` longtext NOT NULL,
  `submit_time` datetime(6) NOT NULL,
  `page_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtailforms_formsub_page_id_e48e93e7_fk_wagtailco` (`page_id`),
  CONSTRAINT `wagtailforms_formsub_page_id_e48e93e7_fk_wagtailco` FOREIGN KEY (`page_id`) REFERENCES `wagtailcore_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailforms_formsubmission`
--

LOCK TABLES `wagtailforms_formsubmission` WRITE;
/*!40000 ALTER TABLE `wagtailforms_formsubmission` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailforms_formsubmission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailimages_image`
--

DROP TABLE IF EXISTS `wagtailimages_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailimages_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `file` varchar(100) NOT NULL,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `focal_point_x` int(10) unsigned DEFAULT NULL,
  `focal_point_y` int(10) unsigned DEFAULT NULL,
  `focal_point_width` int(10) unsigned DEFAULT NULL,
  `focal_point_height` int(10) unsigned DEFAULT NULL,
  `uploaded_by_user_id` int(11) DEFAULT NULL,
  `file_size` int(10) unsigned DEFAULT NULL,
  `collection_id` int(11) NOT NULL,
  `file_hash` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtailimages_image_uploaded_by_user_id_5d73dc75_fk_custom_us` (`uploaded_by_user_id`),
  KEY `wagtailimages_image_collection_id_c2f8af7e_fk_wagtailco` (`collection_id`),
  KEY `wagtailimages_image_created_at_86fa6cd4` (`created_at`),
  CONSTRAINT `wagtailimages_image_collection_id_c2f8af7e_fk_wagtailco` FOREIGN KEY (`collection_id`) REFERENCES `wagtailcore_collection` (`id`),
  CONSTRAINT `wagtailimages_image_uploaded_by_user_id_5d73dc75_fk_custom_us` FOREIGN KEY (`uploaded_by_user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailimages_image`
--

LOCK TABLES `wagtailimages_image` WRITE;
/*!40000 ALTER TABLE `wagtailimages_image` DISABLE KEYS */;
INSERT INTO `wagtailimages_image` VALUES (1,'test img','original_images/white-mug.png',400,400,'2020-04-21 09:30:42.773475',NULL,NULL,NULL,NULL,1,70713,1,'ae48bd720f2d8b8a5938912b7629663e80d80a5e'),(2,'Penguins','original_images/w7cm1noot3u41.png',365,545,'2020-04-21 09:55:54.528589',NULL,NULL,NULL,NULL,1,254964,1,'8b583d4c699ac5e363056e41d5e25785d82fe0b2'),(3,'Wholesome Dad','original_images/fg3mt8cyw3u41.jpg',960,940,'2020-04-21 09:57:16.848429',NULL,NULL,NULL,NULL,1,78635,1,'5866f8f7993b41b0127da77bd16c0b695d7d1d08'),(4,'Hero Banner','original_images/Banner.png',1440,450,'2020-04-21 10:57:16.648938',NULL,NULL,NULL,NULL,1,1229344,1,'b75ba97b7b4c9c77d08035b7f77e5f6df0d272aa'),(5,'Brand Logo','original_images/hkfp_site_logo.png',118,50,'2020-04-22 14:52:02.169226',NULL,NULL,NULL,NULL,1,1212,1,'88b90377123d21cab4e746f73321191641cbdb41'),(6,'Site Favicon','original_images/hkfp_favicon.png',324,286,'2020-04-22 14:53:50.513904',NULL,NULL,NULL,NULL,1,3041,1,'7b814f468b34d9af26078a4901579d06d1565365');
/*!40000 ALTER TABLE `wagtailimages_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailimages_rendition`
--

DROP TABLE IF EXISTS `wagtailimages_rendition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailimages_rendition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `focal_point_key` varchar(16) NOT NULL,
  `filter_spec` varchar(255) NOT NULL,
  `image_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailimages_rendition_image_id_filter_spec_foc_323c8fe0_uniq` (`image_id`,`filter_spec`,`focal_point_key`),
  KEY `wagtailimages_rendition_filter_spec_1cba3201` (`filter_spec`),
  CONSTRAINT `wagtailimages_rendit_image_id_3e1fd774_fk_wagtailim` FOREIGN KEY (`image_id`) REFERENCES `wagtailimages_image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailimages_rendition`
--

LOCK TABLES `wagtailimages_rendition` WRITE;
/*!40000 ALTER TABLE `wagtailimages_rendition` DISABLE KEYS */;
INSERT INTO `wagtailimages_rendition` VALUES (1,'images/white-mug.max-800x600.png',400,400,'','max-800x600',1),(2,'images/white-mug.width-800.png',400,400,'','width-800',1),(3,'images/white-mug.max-165x165.png',165,165,'','max-165x165',1),(4,'images/w7cm1noot3u41.max-165x165.png',110,165,'','max-165x165',2),(5,'images/fg3mt8cyw3u41.max-165x165.jpg',165,161,'','max-165x165',3),(6,'images/w7cm1noot3u41.original.png',365,545,'','original',2),(7,'images/fg3mt8cyw3u41.original.jpg',960,940,'','original',3),(8,'images/Banner.max-165x165.png',165,51,'','max-165x165',4),(9,'images/Banner.width-400.png',400,125,'','width-400',4),(10,'images/Banner.original.png',1440,450,'','original',4),(11,'images/w7cm1noot3u41.max-800x600.png',365,545,'','max-800x600',2),(12,'images/w7cm1noot3u41.width-800.png',365,545,'','width-800',2),(13,'images/hkfp_site_logo.max-165x165.png',118,50,'','max-165x165',5),(14,'images/hkfp_favicon.max-165x165.png',165,145,'','max-165x165',6),(15,'images/hkfp_favicon.max-32x32.png',32,28,'','max-32x32',6),(16,'images/hkfp_site_logo.max-120x120.png',118,50,'','max-120x120',5),(17,'images/hkfp_site_logo.max-70x70.png',70,29,'','max-70x70',5),(18,'images/hkfp_site_logo.max-80x80.png',80,33,'','max-80x80',5);
/*!40000 ALTER TABLE `wagtailimages_rendition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailredirects_redirect`
--

DROP TABLE IF EXISTS `wagtailredirects_redirect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailredirects_redirect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `old_path` varchar(255) NOT NULL,
  `is_permanent` tinyint(1) NOT NULL,
  `redirect_link` varchar(255) NOT NULL,
  `redirect_page_id` int(11) DEFAULT NULL,
  `site_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailredirects_redirect_old_path_site_id_783622d7_uniq` (`old_path`,`site_id`),
  KEY `wagtailredirects_redirect_old_path_bb35247b` (`old_path`),
  KEY `wagtailredirects_red_redirect_page_id_b5728a8f_fk_wagtailco` (`redirect_page_id`),
  KEY `wagtailredirects_red_site_id_780a0e1e_fk_wagtailco` (`site_id`),
  CONSTRAINT `wagtailredirects_red_redirect_page_id_b5728a8f_fk_wagtailco` FOREIGN KEY (`redirect_page_id`) REFERENCES `wagtailcore_page` (`id`),
  CONSTRAINT `wagtailredirects_red_site_id_780a0e1e_fk_wagtailco` FOREIGN KEY (`site_id`) REFERENCES `wagtailcore_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailredirects_redirect`
--

LOCK TABLES `wagtailredirects_redirect` WRITE;
/*!40000 ALTER TABLE `wagtailredirects_redirect` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailredirects_redirect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailsearch_editorspick`
--

DROP TABLE IF EXISTS `wagtailsearch_editorspick`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailsearch_editorspick` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_order` int(11) DEFAULT NULL,
  `description` longtext NOT NULL,
  `page_id` int(11) NOT NULL,
  `query_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wagtailsearch_editor_query_id_c6eee4a0_fk_wagtailse` (`query_id`),
  KEY `wagtailsearch_editor_page_id_28cbc274_fk_wagtailco` (`page_id`),
  CONSTRAINT `wagtailsearch_editor_page_id_28cbc274_fk_wagtailco` FOREIGN KEY (`page_id`) REFERENCES `wagtailcore_page` (`id`),
  CONSTRAINT `wagtailsearch_editor_query_id_c6eee4a0_fk_wagtailse` FOREIGN KEY (`query_id`) REFERENCES `wagtailsearch_query` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailsearch_editorspick`
--

LOCK TABLES `wagtailsearch_editorspick` WRITE;
/*!40000 ALTER TABLE `wagtailsearch_editorspick` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailsearch_editorspick` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailsearch_query`
--

DROP TABLE IF EXISTS `wagtailsearch_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailsearch_query` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `query_string` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `query_string` (`query_string`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailsearch_query`
--

LOCK TABLES `wagtailsearch_query` WRITE;
/*!40000 ALTER TABLE `wagtailsearch_query` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailsearch_query` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailsearch_querydailyhits`
--

DROP TABLE IF EXISTS `wagtailsearch_querydailyhits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailsearch_querydailyhits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `hits` int(11) NOT NULL,
  `query_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wagtailsearch_querydailyhits_query_id_date_1dd232e6_uniq` (`query_id`,`date`),
  CONSTRAINT `wagtailsearch_queryd_query_id_2185994b_fk_wagtailse` FOREIGN KEY (`query_id`) REFERENCES `wagtailsearch_query` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailsearch_querydailyhits`
--

LOCK TABLES `wagtailsearch_querydailyhits` WRITE;
/*!40000 ALTER TABLE `wagtailsearch_querydailyhits` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagtailsearch_querydailyhits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagtailusers_userprofile`
--

DROP TABLE IF EXISTS `wagtailusers_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wagtailusers_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submitted_notifications` tinyint(1) NOT NULL,
  `approved_notifications` tinyint(1) NOT NULL,
  `rejected_notifications` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `preferred_language` varchar(10) NOT NULL,
  `current_time_zone` varchar(40) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `wagtailusers_userprofile_user_id_59c92331_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagtailusers_userprofile`
--

LOCK TABLES `wagtailusers_userprofile` WRITE;
/*!40000 ALTER TABLE `wagtailusers_userprofile` DISABLE KEYS */;
INSERT INTO `wagtailusers_userprofile` VALUES (1,1,1,1,1,'','Asia/Hong_Kong','');
/*!40000 ALTER TABLE `wagtailusers_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-29  9:50:28
