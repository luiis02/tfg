-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: database:3306
-- Tiempo de generación: 29-04-2024 a las 16:02:06
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tfg`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cartas`
--

CREATE TABLE `cartas` (
  `id` int NOT NULL,
  `nombre` varchar(32) NOT NULL,
  `usuario` varchar(32) NOT NULL,
  `indice` int DEFAULT '0',
  `status` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `cartas`
--

INSERT INTO `cartas` (`id`, `nombre`, `usuario`, `indice`, `status`) VALUES
(4, 'Desayunos', 'root', 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intents`
--

CREATE TABLE `intents` (
  `indice_apoyo` int NOT NULL,
  `id` int NOT NULL,
  `tag` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Tipo` int NOT NULL,
  `Texto` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `intents`
--

INSERT INTO `intents` (`indice_apoyo`, `id`, `tag`, `Tipo`, `Texto`) VALUES
(2, 1, 'agradecimientos', 0, 'Gracias'),
(2, 2, 'agradecimientos', 0, 'Muchas gracias'),
(2, 3, 'agradecimientos', 0, 'Gracias por tu ayuda'),
(2, 4, 'agradecimientos', 1, 'De nada'),
(2, 5, 'agradecimientos', 1, 'No hay de que'),
(2, 6, 'agradecimientos', 1, 'Estoy para ayudarte'),
(2, 7, 'camarero', 0, 'camarero'),
(2, 8, 'camarero', 0, 'puede venir un camarero?'),
(2, 9, 'camarero', 0, 'necesito un camarero'),
(2, 10, 'camarero', 0, 'camarero por favor'),
(2, 11, 'camarero', 0, 'solicitar camarero'),
(2, 12, 'camarero', 0, 'necesito ayuda'),
(2, 13, 'camarero', 0, 'mesero'),
(2, 14, 'camarero', 0, 'mesera'),
(2, 15, 'camarero', 0, 'puede venir un mesero?'),
(2, 16, 'camarero', 0, 'necesito que me atiendan presencialmente'),
(2, 17, 'camarero', 0, 'atencion real'),
(2, 18, 'camarero', 1, 'Un camarero vendra enseguida'),
(2, 19, 'camarero', 1, 'Claro, en un momento llega el camarero'),
(2, 20, 'camarero', 1, 'El camarero ha sido avisado'),
(2, 21, 'pagar', 0, 'Cuanto es?'),
(2, 22, 'pagar', 0, 'Cuanto tengo que pagar?'),
(2, 23, 'pagar', 0, 'Quiero pagar'),
(2, 24, 'pagar', 0, 'Quiero la cuenta'),
(2, 25, 'pagar', 0, 'La cuenta por favor'),
(2, 26, 'pagar', 0, 'Puedo pagar?'),
(2, 27, 'pagar', 0, 'Pagar'),
(2, 28, 'pagar', 0, 'La multa por favor'),
(2, 29, 'pagar', 1, 'Claro, enseguida le traigo la cuenta'),
(2, 30, 'pagar', 1, 'Un momento, le traigo la cuenta'),
(2, 31, 'pedir', 0, 'Quiero'),
(2, 32, 'pedir', 0, 'Me gustaria'),
(2, 33, 'pedir', 0, 'Deseo'),
(2, 34, 'pedir', 0, 'Necesito'),
(2, 35, 'pedir', 0, 'Quiero pedir'),
(2, 36, 'pedir', 0, 'Me gustaria pedir'),
(2, 37, 'pedir', 0, 'Ponme'),
(2, 38, 'pedir', 0, 'Dame'),
(2, 39, 'pedir', 0, 'Traeme'),
(2, 40, 'pedir', 0, 'Quiero ordenar'),
(2, 41, 'pedir', 0, 'Quiero hacer un pedido'),
(2, 42, 'pedir', 0, 'Quiero hacer un encargo'),
(2, 43, 'pedir', 0, 'Anota'),
(2, 44, 'pedir', 1, 'Pedido anotado'),
(2, 45, 'pedir', 1, 'Pedido recibido'),
(2, 46, 'pedir', 1, 'Recibido en cocina'),
(2, 47, 'despedida', 0, 'Adios'),
(2, 48, 'despedida', 0, 'Hasta luego'),
(2, 49, 'despedida', 0, 'Hasta pronto'),
(2, 50, 'despedida', 0, 'Nos vemos'),
(2, 51, 'despedida', 0, 'Chao'),
(2, 52, 'despedida', 0, 'Bye'),
(2, 53, 'despedida', 1, 'Adios, que tengas un buen dia'),
(2, 54, 'despedida', 1, 'Hasta luego, cuidate'),
(2, 55, 'despedida', 1, 'Nos vemos, gracias por tu visita'),
(2, 56, 'saludos', 0, 'Hi'),
(2, 57, 'saludos', 0, 'Hey'),
(2, 58, 'saludos', 0, 'Hola'),
(2, 59, 'saludos', 0, 'Hola que tal'),
(2, 60, 'saludos', 0, 'Buenos dias'),
(2, 61, 'saludos', 0, 'Buenas tardes'),
(2, 62, 'saludos', 0, 'Buenas noches'),
(2, 63, 'saludos', 0, 'Saludos'),
(2, 64, 'saludos', 1, 'Hey :-)'),
(2, 65, 'saludos', 1, 'Hola, en que te puedo ayudar'),
(2, 66, 'saludos', 1, 'Bienvenido, ¿en que puedo ayudarte?'),
(2, 67, 'saludos', 1, 'Estoy encantado de poder ayudarte');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mesas`
--

CREATE TABLE `mesas` (
  `id` int NOT NULL,
  `id_establecimiento` int DEFAULT NULL,
  `numero_mesa` int DEFAULT NULL,
  `img_qr` longblob
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_activos`
--

CREATE TABLE `pedidos_activos` (
  `id` int NOT NULL,
  `usuario` varchar(32) NOT NULL,
  `mesa` int NOT NULL,
  `plato` varchar(32) NOT NULL,
  `cantidad` int NOT NULL,
  `precio` float NOT NULL,
  `fecha` datetime NOT NULL,
  `categoria` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_historicos`
--

CREATE TABLE `pedidos_historicos` (
  `id` int NOT NULL,
  `usuario` varchar(32) NOT NULL,
  `mesa` int NOT NULL,
  `plato` varchar(32) NOT NULL,
  `cantidad` int NOT NULL,
  `precio` float NOT NULL,
  `fecha` datetime NOT NULL,
  `fecha_cierre` datetime DEFAULT NULL,
  `categoria` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `pedidos_historicos`
--

INSERT INTO `pedidos_historicos` (`id`, `usuario`, `mesa`, `plato`, `cantidad`, `precio`, `fecha`, `fecha_cierre`, `categoria`) VALUES
(1, 'root', 1, 'Fresa', 2, 1, '2024-04-15 19:31:13', '2024-04-15 19:32:58', 'Batidos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `platos`
--

CREATE TABLE `platos` (
  `id` int NOT NULL,
  `nombre` varchar(32) NOT NULL,
  `descripcion` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `usuario` varchar(32) NOT NULL,
  `carta` varchar(32) NOT NULL,
  `seccion` varchar(32) NOT NULL,
  `indice` int DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `precio` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `platos`
--

INSERT INTO `platos` (`id`, `nombre`, `descripcion`, `usuario`, `carta`, `seccion`, `indice`, `status`, `precio`) VALUES
(5, 'Fresa', 'None', 'root', 'Desayunos', 'Batidos', 0, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seccion`
--

CREATE TABLE `seccion` (
  `ID` int NOT NULL,
  `nombre` varchar(32) NOT NULL,
  `usuario` varchar(32) NOT NULL,
  `carta` varchar(32) NOT NULL,
  `indice` int NOT NULL,
  `status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `seccion`
--

INSERT INTO `seccion` (`ID`, `nombre`, `usuario`, `carta`, `indice`, `status`) VALUES
(5, 'Batidos', 'root', 'Desayunos', 0, 1),
(2, 'Bebidas con alcohol', 'root', 'Comidas', 2, 1),
(1, 'Bebidas sin alcohol', 'root', 'Comidas', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int NOT NULL,
  `nombre` varchar(32) NOT NULL,
  `apellido` varchar(32) NOT NULL,
  `establecimiento` varchar(32) NOT NULL,
  `provincia` varchar(32) NOT NULL,
  `email` varchar(64) NOT NULL,
  `passwd` longtext NOT NULL,
  `usuario` varchar(32) NOT NULL,
  `telefono` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `apellido`, `establecimiento`, `provincia`, `email`, `passwd`, `usuario`, `telefono`) VALUES
(1, 'Luis', 'Alcalde ', 'Bar Vilchez', 'Granada', 'luisalcaldegarcia.02@gmail.com', 'Calahonda1', 'root', 601103754);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_sin_confirmar`
--

CREATE TABLE `usuario_sin_confirmar` (
  `id` int NOT NULL,
  `nombre` varchar(32) NOT NULL,
  `apellido` varchar(32) NOT NULL,
  `establecimiento` varchar(32) NOT NULL,
  `provincia` varchar(32) NOT NULL,
  `email` varchar(64) NOT NULL,
  `passwd` longtext NOT NULL,
  `usuario` varchar(32) NOT NULL,
  `telefono` int NOT NULL,
  `codigo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cartas`
--
ALTER TABLE `cartas`
  ADD PRIMARY KEY (`nombre`,`usuario`),
  ADD UNIQUE KEY `ID` (`id`),
  ADD KEY `usuario` (`usuario`);

--
-- Indices de la tabla `intents`
--
ALTER TABLE `intents`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `mesas`
--
ALTER TABLE `mesas`
  ADD UNIQUE KEY `ID` (`id`);

--
-- Indices de la tabla `pedidos_activos`
--
ALTER TABLE `pedidos_activos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pedidos_historicos`
--
ALTER TABLE `pedidos_historicos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `platos`
--
ALTER TABLE `platos`
  ADD PRIMARY KEY (`nombre`,`usuario`,`carta`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indices de la tabla `seccion`
--
ALTER TABLE `seccion`
  ADD PRIMARY KEY (`nombre`,`usuario`,`carta`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `usuario` (`usuario`),
  ADD UNIQUE KEY `telefono` (`telefono`);

--
-- Indices de la tabla `usuario_sin_confirmar`
--
ALTER TABLE `usuario_sin_confirmar`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `usuario` (`usuario`),
  ADD UNIQUE KEY `telefono` (`telefono`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cartas`
--
ALTER TABLE `cartas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `intents`
--
ALTER TABLE `intents`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT de la tabla `mesas`
--
ALTER TABLE `mesas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `pedidos_activos`
--
ALTER TABLE `pedidos_activos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `pedidos_historicos`
--
ALTER TABLE `pedidos_historicos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `platos`
--
ALTER TABLE `platos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `seccion`
--
ALTER TABLE `seccion`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuario_sin_confirmar`
--
ALTER TABLE `usuario_sin_confirmar`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cartas`
--
ALTER TABLE `cartas`
  ADD CONSTRAINT `cartas_ibfk_1` FOREIGN KEY (`usuario`) REFERENCES `usuario` (`usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
