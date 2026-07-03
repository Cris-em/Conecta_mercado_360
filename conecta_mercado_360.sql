-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-07-2026 a las 14:02:19
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `conecta_mercado_360`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_pedido`
--

CREATE TABLE `detalles_pedido` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_pedido`
--

INSERT INTO `detalles_pedido` (`id`, `pedido_id`, `producto_id`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 1, 2, 28.00),
(2, 2, 1, 1, 28.00),
(3, 3, 1, 2, 28.00),
(4, 4, 1, 1, 28.00),
(5, 5, 1, 1, 28.00),
(6, 6, 2, 1, 22.00),
(7, 7, 71, 1, 20.00),
(8, 8, 2, 1, 22.00),
(9, 9, 1, 1, 28.00),
(10, 10, 73, 1, 200.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `locales`
--

CREATE TABLE `locales` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen_local` varchar(255) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `locales`
--

INSERT INTO `locales` (`id`, `nombre`, `descripcion`, `imagen_local`, `usuario_id`) VALUES
(1, 'Frutas y Legumbres El Chule', 'Las frutas y verduras más frescas del mercado.', '/static/imagenes/verduleria.jpeg', NULL),
(2, 'Carnicería y Tocinería La Nueva', 'Bistec, costilla, espinazo, lomo, pierna, chicharrón y longaniza.', '/static/imagenes/carniceria.jpeg', NULL),
(3, 'Pollería Esmeralda', 'Pollo entero, pechuga, pierna y muslo, retazo. Local 79.', '/static/imagenes/polleria.jpeg', NULL),
(4, 'Cremería Morales', 'La mejor cremería con queso Oaxaca, Panela, Manchego y más.', '/static/imagenes/cremeria morales.jpeg', NULL),
(5, 'Abarrotes y Semillas N134', 'Semillas, especias y la mejor canasta básica.', '/static/imagenes/abarrotes.jpeg', NULL),
(6, 'Tortillería Maria Isabel', '100% maíz, calidad e higiene, peso exacto.', '/static/imagenes/tortilleria.jpeg', NULL),
(7, 'Papelería y Copias', 'Útiles escolares, copias, impresiones y material de oficina.', '/static/imagenes/papeleria.jpeg', NULL),
(8, 'Tlapalería y Material Eléctrico DREAMS', 'Venta de materiales eléctricos y de construcción.', '/static/imagenes/materiasprimas.jpeg', NULL),
(9, 'Exp. de Pan Kitty', 'Pan dulce, bolillo, y deliciosos pastelillos.', '/static/imagenes/panaderia.jpeg', NULL),
(10, '\"GALLETITAS EL JACIEL\"', 'Ricas galletas recien horneadas', '/static/uploads/local_1782731169.jpg', 6),
(11, 'Pollos asados', 'Ricos pollos calientitos', '/static/uploads/local_1782734302.jpg', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'Pendiente',
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id`, `usuario_id`, `fecha`, `estado`, `total`) VALUES
(1, 4, '2026-06-29 00:45:18', 'Pendiente de pago', 56.00),
(2, 4, '2026-06-29 00:45:54', 'Pagado', 28.00),
(3, 4, '2026-06-29 00:51:03', 'Pendiente de pago', 56.00),
(4, 4, '2026-06-29 00:56:23', 'Pendiente de pago', 28.00),
(5, 4, '2026-06-29 03:15:24', 'Pendiente de pago', 28.00),
(6, 4, '2026-06-29 03:16:19', 'Pagado', 22.00),
(7, 4, '2026-06-29 11:08:13', 'Pagado', 20.00),
(8, 7, '2026-06-29 11:54:43', 'Pendiente de pago', 22.00),
(9, 7, '2026-06-29 11:55:29', 'Pagado', 28.00),
(10, 7, '2026-06-29 12:00:50', 'Pagado', 200.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles_comprador`
--

CREATE TABLE `perfiles_comprador` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perfiles_comprador`
--

INSERT INTO `perfiles_comprador` (`id`, `usuario_id`, `direccion`, `telefono`, `metodo_pago`, `nombre`) VALUES
(1, 3, '', '5569830693', 'Tarjeta de crédito/débito', NULL),
(2, 4, 'Mariano Rivapalacio N.7', '5570857593', 'Tarjeta de crédito/débito', 'Laura Gonzales Herrera'),
(3, 7, 'Mariano Rivapalacio N.7', '5570857593', 'Tarjeta de crédito/débito', 'Laura Gonzales Herrera');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles_vendedor`
--

CREATE TABLE `perfiles_vendedor` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `nombre_negocio` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perfiles_vendedor`
--

INSERT INTO `perfiles_vendedor` (`id`, `usuario_id`, `nombre_negocio`, `descripcion`, `ubicacion`, `telefono`, `nombre`) VALUES
(1, 5, '', '', 'Mercado Melchor Ocampo, frente Cecytem Chimalhuacán 1', '', NULL),
(2, 6, 'Sintaxxys IA', '', '', '5569830693', 'Juan Sebastian ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `local_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `categoria` varchar(50) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` decimal(10,2) DEFAULT 0.00,
  `unidad` varchar(20) DEFAULT 'kg',
  `imagen_url` varchar(255) DEFAULT NULL,
  `video_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `local_id`, `nombre`, `descripcion`, `categoria`, `precio`, `stock`, `unidad`, `imagen_url`, `video_url`) VALUES
(1, 1, 'Jitomate Saladet', '1 kg', 'verduras', 28.00, 2.00, 'kg', '/static/imagenes/Jitomate Saladet.jpg', NULL),
(2, 1, 'Cebolla Blanca', '1 kg', 'verduras', 22.00, 8.00, 'kg', '/static/imagenes/Cebolla blanca (1).jpg', NULL),
(19, 2, 'Bistec de Res', '1 kg (Aguayón)', 'carnes', 180.00, 10.00, 'kg', '/static/imagenes/Bandeja de carne de res fileteada (1).jpg', NULL),
(20, 2, 'Molida de Res', '1 kg', 'carnes', 165.00, 10.00, 'kg', '/static/imagenes/molida de res.jpg', NULL),
(28, 3, 'Pechuga de Pollo', '1 kg entera', 'carnes', 115.00, 10.00, 'kg', '/static/imagenes/pechuga de pollo.jpg', NULL),
(29, 3, 'Milanesa de Pollo', '1 kg aplanada', 'carnes', 130.00, 10.00, 'kg', '/static/imagenes/milanesa de pollo.jpg', NULL),
(71, 10, 'CHIKIS', '', 'Granos y semillas', 20.00, 39.00, 'kg', '/static/uploads/prod_1782731218.jpg', ''),
(73, 10, 'Pollo', 'Rico pollo rostizado,habanero y demas', 'Carnes', 200.00, 49.00, 'pza', '/static/uploads/prod_1782734364.jpg', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` enum('comprador','vendedor','admin') DEFAULT 'comprador',
  `foto_perfil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `contrasena`, `rol`, `foto_perfil`) VALUES
(1, 'Comprador Test', 'comprador@test.com', 'scrypt:32768:8:1$...', 'comprador', NULL),
(2, 'Vendedor Test', 'vendedor@test.com', 'scrypt:32768:8:1$...', 'vendedor', NULL),
(3, 'Cristian Salvador Martinez', 'samc090207hmclrra1@soycecytem.mx', 'scrypt:32768:8:1$20j69OOZkmI6z8bc$ae2558a34314c99db033d9bdbd10cd9bc888e5cfdd3650a24d10e39c3b4e7057a15254854441b6c2776d708f93055a7a22a9aac16d0a74bdd8390923e9cd931c', 'comprador', '/static/uploads/comprador_1782684923.jpg'),
(4, 'Laura Gonzales Herrera', 'cristiansalvadormartinez9@gmail.com', 'scrypt:32768:8:1$Io3ef7lNSIjHVznK$87b91b59f83392381bff9120b0da6f6e10fe4e736b93a08cd9365c48eb14cfb52f5d1369ff0c037d9a612f702de1eb3748018206e235f8a055308e4b9fc49d8e', 'comprador', '/static/uploads/comprador_1782701574.jpg'),
(5, '', '', 'scrypt:32768:8:1$CUwwC63LZkqXyu9D$119b2c4dae443c0c8b8d0266cb520f67c846e2242f737346115de877469cc8fd2ece9202f7a30a4dfc958f1d7de874b94a0e8d3a84516292b5a0809236cbd3a1', 'vendedor', '/static/uploads/vendedor_1782698350.jpg'),
(6, 'Juan Sebastian ', 'cristofermartinez@gmail.com', 'scrypt:32768:8:1$QdlRGpIOwL7yg9nV$6b96b4fd4e5a1f18f9463517c728eb7d1e7a18f8e86134c7207dbbac10d3a78fdeb87500dac899665c24bcc832e559e1831319feff00b81e5fe02f9ff98bb56b', 'vendedor', '/static/uploads/vendedor_1782734522.png'),
(7, 'Laura Gonzales Herrera', 'mariajose9@gmail.com', 'scrypt:32768:8:1$bPsEu3sHCnUD2p2t$ab8d6948c3be610e0a752a0ebf5fe15713cb434911424030788549ff9e92bee74b97e5da92bd3a0c4375ebad04a5205f997435bfad21257504441d2950b65bae', 'comprador', '/static/uploads/comprador_1782734239.png'),
(8, 'Admin Principal', 'admin@conecta.com', 'scrypt:32768:8:1$bs0MoOyL6iSh6fbr$d50e963f00f432774592caf5a4be9a7e329f0f261db94592102407a4f61ae30830696bab81e49f947a42752830b4e04098917ef055a23c802c41062bb1969280', 'admin', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `locales`
--
ALTER TABLE `locales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `perfiles_comprador`
--
ALTER TABLE `perfiles_comprador`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `perfiles_vendedor`
--
ALTER TABLE `perfiles_vendedor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `local_id` (`local_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `locales`
--
ALTER TABLE `locales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `perfiles_comprador`
--
ALTER TABLE `perfiles_comprador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `perfiles_vendedor`
--
ALTER TABLE `perfiles_vendedor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD CONSTRAINT `detalles_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `detalles_pedido_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `locales`
--
ALTER TABLE `locales`
  ADD CONSTRAINT `locales_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `perfiles_comprador`
--
ALTER TABLE `perfiles_comprador`
  ADD CONSTRAINT `perfiles_comprador_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `perfiles_vendedor`
--
ALTER TABLE `perfiles_vendedor`
  ADD CONSTRAINT `perfiles_vendedor_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
