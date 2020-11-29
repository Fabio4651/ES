CREATE DATABASE  IF NOT EXISTS `lego` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `lego`;
-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: lego
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `conjuntos`
--

DROP TABLE IF EXISTS `conjuntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conjuntos` (
  `Referencia` varchar(45) NOT NULL,
  `idProduto` int(11) NOT NULL,
  `Nome` varchar(45) NOT NULL,
  `Preco` float NOT NULL,
  `N_pecas` int(11) NOT NULL,
  `Ano` year(4) NOT NULL,
  `Acessórios` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Referencia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conjuntos`
--

LOCK TABLES `conjuntos` WRITE;
/*!40000 ALTER TABLE `conjuntos` DISABLE KEYS */;
INSERT INTO `conjuntos` VALUES ('32asfaf65',1,'Deathstar',500,3000,2008,'Sim'),('asd2112aa',3,'Airport',80,1000,2010,'Sim');
/*!40000 ALTER TABLE `conjuntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empregados`
--

DROP TABLE IF EXISTS `empregados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empregados` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(45) NOT NULL,
  `Contacto` int(11) NOT NULL,
  `Morada` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empregados`
--

LOCK TABLES `empregados` WRITE;
/*!40000 ALTER TABLE `empregados` DISABLE KEYS */;
INSERT INTO `empregados` VALUES (1,'Zé Pedro',962358756,'Silves','zman@gmail.com'),(2,'Diogo Sila',912658347,'Portimão','dsila@outlook.pt'),(3,'Hugo',965874523,'Silves','hugo@gmail.com');
/*!40000 ALTER TABLE `empregados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encomendas`
--

DROP TABLE IF EXISTS `encomendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `encomendas` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `idVenda` int(11) NOT NULL,
  `Portes` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `idVenda_idx` (`idVenda`),
  CONSTRAINT `idVenda` FOREIGN KEY (`idVenda`) REFERENCES `vendas` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encomendas`
--

LOCK TABLES `encomendas` WRITE;
/*!40000 ALTER TABLE `encomendas` DISABLE KEYS */;
INSERT INTO `encomendas` VALUES (1,3,3.5);
/*!40000 ALTER TABLE `encomendas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fornecedores`
--

DROP TABLE IF EXISTS `fornecedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornecedores` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(45) NOT NULL,
  `NIF` int(11) NOT NULL,
  `Contacto` varchar(20) NOT NULL,
  `Pais` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedores`
--

LOCK TABLES `fornecedores` WRITE;
/*!40000 ALTER TABLE `fornecedores` DISABLE KEYS */;
INSERT INTO `fornecedores` VALUES (1,'Bricks do Norte',236524869,'282365475','Portugal'),(2,'QBricks',256359684,'33 256365891','Franca'),(3,'Noi siamo i soliti',256354789,'39 365217896','Italia');
/*!40000 ALTER TABLE `fornecedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `individuais`
--

DROP TABLE IF EXISTS `individuais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `individuais` (
  `Referencia` varchar(45) NOT NULL,
  `idProduto` int(11) NOT NULL,
  `Nome` varchar(45) NOT NULL,
  `Preco` float NOT NULL,
  `Ano` year(4) NOT NULL,
  `Medidas` varchar(50) DEFAULT NULL,
  `Categoria` varchar(50) NOT NULL,
  `Tema` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Referencia`),
  KEY `idProduto_idx` (`idProduto`),
  CONSTRAINT `idProduto` FOREIGN KEY (`idProduto`) REFERENCES `produtos` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `individuais`
--

LOCK TABLES `individuais` WRITE;
/*!40000 ALTER TABLE `individuais` DISABLE KEYS */;
INSERT INTO `individuais` VALUES ('afsaafsfsf',4,'Darth Vader Minifigure',3,1990,NULL,'Bonecos','Star Wars'),('at24566af',2,'Woodie minifigure',2,2004,NULL,'Bonecos','ToyStory');
/*!40000 ALTER TABLE `individuais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performance`
--

DROP TABLE IF EXISTS `performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performance` (
  `ID_empregado` int(11) NOT NULL,
  `Total_vendas` decimal(6,2) NOT NULL,
  `Media` decimal(6,2) NOT NULL,
  PRIMARY KEY (`ID_empregado`),
  KEY `ID_empregado_idx` (`ID_empregado`),
  CONSTRAINT `ID_empr` FOREIGN KEY (`ID_empregado`) REFERENCES `empregados` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performance`
--

LOCK TABLES `performance` WRITE;
/*!40000 ALTER TABLE `performance` DISABLE KEYS */;
INSERT INTO `performance` VALUES (1,93.00,46.50),(2,30.00,30.00),(3,35.00,35.00);
/*!40000 ALTER TABLE `performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(45) NOT NULL,
  `Tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Deathstar','Conjuntos'),(2,'Buzzlightyear','Pecas_Individuais'),(3,'Airport','Conjuntos'),(4,'Darth Vader Minifigure','Pecas_Individuais'),(5,'roda','Pecas_Individuais'),(6,'Estação de Comboio','Conjuntos'),(7,'London Eye','Conjuntos'),(8,'Porche 911 (997)','Conjuntos'),(9,'Polícia','Pecas Individuais');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transportadora`
--

DROP TABLE IF EXISTS `transportadora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transportadora` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `Contacto` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportadora`
--

LOCK TABLES `transportadora` WRITE;
/*!40000 ALTER TABLE `transportadora` DISABLE KEYS */;
INSERT INTO `transportadora` VALUES (1,'DHL','portugal@dhl.com','282695476'),(2,'Chronopost','portugal@dpd.com','365249632');
/*!40000 ALTER TABLE `transportadora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendas`
--

DROP TABLE IF EXISTS `vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendas` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Total` float NOT NULL,
  `Data` date NOT NULL,
  `Hora` time NOT NULL,
  `Pagamento` varchar(45) NOT NULL,
  `Desconto` int(11) NOT NULL,
  `ID_empregado` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_empregado_idx` (`ID_empregado`),
  CONSTRAINT `ID_empregado` FOREIGN KEY (`ID_empregado`) REFERENCES `empregados` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas`
--

LOCK TABLES `vendas` WRITE;
/*!40000 ALTER TABLE `vendas` DISABLE KEYS */;
INSERT INTO `vendas` VALUES (1,50,'2018-05-21','14:36:00','Numerario',0,1),(2,27,'2019-02-11','15:21:00','Multibanco',0,2),(3,134,'2020-03-30','19:20:00','Multibanco',10,1),(4,50,'2020-03-02','14:30:03','Multibanco',0,1),(5,50,'2020-03-02','17:13:03','Numerario',0,1),(6,50,'2020-03-02','17:13:03','Numerario',0,3),(7,60,'2020-03-02','17:33:03','Numerario',0,3),(8,30,'2020-08-16','12:45:36','Multibanco',10,2),(9,50,'2020-02-12','16:23:00','Numerario',0,1),(10,43,'2020-05-23','11:12:00','Multibanco',0,1),(11,35,'2019-03-06','20:13:00','Numerario',10,3);
/*!40000 ALTER TABLE `vendas` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `TVendas_BEFORE_INSERT` BEFORE INSERT ON `vendas` FOR EACH ROW BEGIN
DECLARE num_linha INTEGER;
DECLARE total_linha INTEGER;

SELECT COUNT(*) INTO total_linha
FROM vendas
WHERE ID_empregado=NEW.ID_empregado;
SELECT COUNT(*) INTO num_linha
FROM performance
WHERE ID_empregado=NEW.ID_empregado;
IF num_linha > 0 THEN
UPDATE performance
SET Total_vendas = NEW.total+Total_vendas,
media=Total_vendas/(num_linha+1) WHERE ID_empregado=NEW.ID_empregado;
ELSE
INSERT INTO performance(ID_empregado,Total_vendas,media) VALUES (NEW.ID_empregado,NEW.total,NEW.total);
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping events for database 'lego'
--

--
-- Dumping routines for database 'lego'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_insert_venda` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_venda`(id INT, v_valor DECIMAL(6,2), v_data DATE, v_hora TIME, v_pag char, v_desc int, e_id INT)
BEGIN
IF (e_id = NULL) THEN
INSERT INTO vendas(ID, Total, Data, Hora, Pagamento, Desconto, ID_empregado) VALUES(id, v_valor, v_hora, v_pag, v_desc, e_id);
 ELSE SELECT "É necessário indicar o ID do empregado." AS Msg;
END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-27 15:57:12
