DROP DATABASE IF EXISTS kraftboost;
CREATE DATABASE kraftboost;
USE kraftboost;

CREATE TABLE usuarios (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR (100) NOT NULL,
    apellidos VARCHAR (100) NOT NULL,
    email VARCHAR (150) NOT NULL UNIQUE,
    username VARCHAR (25) NOT NULL UNIQUE,
    telefono VARCHAR (20) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    password VARCHAR (255) NOT NULL,
	fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rol VARCHAR (50) NOT NULL
);

CREATE TABLE categorias (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR (100) NOT NULL,
    imagen VARCHAR (255) NOT NULL
);

CREATE TABLE marcas (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR (100) NOT NULL
);

CREATE TABLE productos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR (100) NOT NULL,
    stock INT UNSIGNED NOT NULL,
    precio DECIMAL (10,2) NOT NULL,
    id_categoria INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id),
    id_marca INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_marca) REFERENCES marcas(id),
    descripcion VARCHAR (255) NOT NULL,
    imagen VARCHAR (255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    ventas INT UNSIGNED DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE carrito (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    id_producto INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id),
    cantidad INT UNSIGNED NOT NULL,
    precio DECIMAL (10,2) NOT NULL
);

CREATE TABLE favoritos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    id_producto INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);

CREATE TABLE pedidos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    precio_total DECIMAL (10,2) NOT NULL,
    id_usuario INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre_destinatario VARCHAR (100) NOT NULL,
    domicilio VARCHAR (150) NOT NULL,
    localidad VARCHAR (150) NOT NULL,
    puerta INT UNSIGNED NOT NULL,
    codigo_postal INT UNSIGNED NOT NULL,
    enviado BOOLEAN NOT NULL
);

CREATE TABLE detalles_pedido (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id) ON DELETE CASCADE,
    id_producto INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE,
    cantidad INT UNSIGNED NOT NULL,
     precio DECIMAL (10,2) NOT NULL
);



-- Insertamos todas las marcas de la tienda
INSERT INTO marcas (nombre) VALUES
('domyos'),
('tunturi'),
('kraftboost'),
('corength'),
('maniak'),
('e-series');


-- Insertamos todas las categorias de la tienda
INSERT INTO categorias (nombre, imagen) VALUES
('barras', 'images/productos/barras/barra_exagonal.png'),
('bancos', 'images/productos/bancos/banco_multifuncion_domyos.png'),
('discos', 'images/productos/discos/disco_20kg_domyos.png'),
('mancuernas', 'images/productos/mancuernas/mancuerna_50kg_maniak.png'),
('accesorios', 'images/productos/accesorios/cinturon_lastre_corength.png'),
('bandas elasticas', 'images/productos/bandas elasticas/banda_60kg.png'),
('kettlebells', 'images/productos/kettlebells/kettlebell_32kg_tunturi.png'),
('estructuras', 'images/productos/estructuras/paralelas_kraftboost.png');


-- Barras (categoria 1, todos marca domyos)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Agarre Abierto Neutro', 50, 24.99, 1, 1, 'Agarre abierto neutro de hierro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/agarre_abierto_neutro.png'),
('Agarre con Cuerda', 50, 9.99, 1, 1, 'Agarre con cuerda. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/agarre_con_cuerda.png'),
('Agarre Estrecho Metal', 50, 19.99, 1, 1, 'Agarre estrecho de metal. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/agarre_estrecho_metal.png'),
('Agarre Gironda', 50, 19.99, 1, 1, 'Agarre gironda de hierro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/agarre_gironda.png'),
('Agarre Medio Neutro', 50, 39.99, 1, 1, 'Agarre medio neutro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/agarre_medio_neutro.png'),
('Agarre Unilateral Metálico', 50, 4.99, 1, 1, 'Agarre unilateral metálico. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/agarre_unilateral_metalico.png'),
('Barra Exagonal', 50, 29.99, 1, 1, 'Barra exagonal de hierro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/barra_exagonal.png'),
('Barra Olímpica', 50, 69.99, 1, 1, 'Barra Olímpica de hierro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/barra_olimpica.png'),
('Barra para Mancuernas', 50, 9.99, 1, 1, 'Barra para mancuernas de hierro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/barra_para_mancuernas.png'),
('Barra Z', 50, 29.99, 1, 1, 'Barra Z de hierro. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/barras/barra_z.png');


-- Bancos (categoria 2)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Banco con Soportes', 50, 99.99, 2, 2, 'Banco plano con soportes. Ideal para press de banca. Distribuido por la marca Tunturi.', 'images/productos/bancos/banco_con_soportes_tunturi.png'),
('Banco Inclinado Domyos', 50, 149.99, 2, 1, 'Banco inclinado. Ideal para press de banca inclinado. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/bancos/banco_inclinado_domyos.png'),
('Banco Inclinado Tunturi', 50, 99.99, 2, 2, 'Banco inclinado. Ideal para press de banca inclinado. Distribuido por la marca Tunturi.', 'images/productos/bancos/banco_inclinado_tunturi.png'),
('Banco Plano E-Series', 50, 199.99, 2, 6, 'Banco plano con soportes. Ideal para press de banca. Distribuido por la marca E-Series.', 'images/productos/bancos/banco_plano_e-series.png');


-- Discos (categoria 3)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Disco 1.25kg Goma', 50, 9.99, 3, 1, 'Disco de goma de 1.25 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_1.25kg_goma_domyos.png'),
('Disco 2.5kg Goma', 50, 14.99, 3, 1, 'Disco de goma de 2.5 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_2.5kg_goma_domyos.png'),
('Disco 5kg Goma', 50, 19.99, 3, 1, 'Disco de goma de 5 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_5kg_goma_domyos.png'),
('Disco 10kg Goma', 50, 24.99, 3, 1, 'Disco de goma de 10 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_10kg_goma_domyos.png'),
('Disco 20kg Goma', 50, 29.99, 3, 1, 'Disco de goma de 20 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_20kg_goma_domyos.png'),

('Disco 1kg Domyos', 50, 2.99, 3, 1, 'Disco de hierro de 1 kilogramo. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_1kg_domyos.png'),
('Disco 2kg Domyos', 50, 4.99, 3, 1, 'Disco de hierro de 2 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_2kg_domyos.png'),
('Disco 5kg Domyos', 50, 9.99, 3, 1, 'Disco de hierro de 5 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_5kg_domyos.png'),
('Disco 10kg', 50, 15.99, 3, 1, 'Disco de hierro de 10 kilogramos. Ideal para el entreno. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/discos/disco_10kg_domyos.png'),



('Disco 5kg Maniak', 50, 14.99, 3, 5, 'Disco de acero de 5 kilogramos. Ideal para el entreno. Distribuido por la marca Maniak.', 'images/productos/discos/disco_5kg_maniak.png'),
('Disco 10kg Maniak', 50, 19.99, 3, 5, 'Disco de acero de 10 kilogramos. Ideal para el entreno. Distribuido por la marca Maniak.', 'images/productos/discos/disco_10kg_maniak.png'),
('Disco 15kg Maniak', 50, 24.99, 3, 5, 'Disco de acero de 15 kilogramos. Ideal para el entreno. Distribuido por la marca Maniak.', 'images/productos/discos/disco_15kg_maniak.png'),
('Disco 20kg Maniak', 50, 34.99, 3, 5, 'Disco de acero de 20 kilogramos. Ideal para el entreno. Distribuido por la marca Maniak.', 'images/productos/discos/disco_20kg_maniak.png');






-- Mancuernas (categoria 4)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES

('Mancuerna 1kg Tunturi', 50, 0.99, 4, 2, 'Mancuerna de 1 kilogramo. Ideal para el entrenamiento casual. Distribuido por la marca Tunturi.', 'images/productos/mancuernas/mancuerna_1kg_tunturi.png'),
('Mancuerna 2kg Tunturi', 50, 1.99, 4, 2, 'Mancuerna de 2 kilogramos. Ideal para el entrenamiento casual. Distribuido por la marca Tunturi.', 'images/productos/mancuernas/mancuerna_2kg_tunturi.png'),
('Mancuerna 3kg Tunturi', 50, 2.99, 4, 2, 'Mancuerna de 3 kilogramos. Ideal para el entrenamiento casual. Distribuido por la marca Tunturi.', 'images/productos/mancuernas/mancuerna_3kg_tunturi.png'),
('Mancuerna 4kg Tunturi', 50, 3.99, 4, 2, 'Mancuerna de 4 kilogramos. Ideal para el entrenamiento casual. Distribuido por la marca Tunturi.', 'images/productos/mancuernas/mancuerna_4kg_tunturi.png'),
('Mancuerna 5kg Tunturi', 50, 4.99, 4, 2, 'Mancuerna de 5 kilogramos. Ideal para el entrenamiento casual. Distribuido por la marca Tunturi.', 'images/productos/mancuernas/mancuerna_5kg_tunturi.png'),



('Mancuerna 2.5kg Corength', 50, 4.99, 4, 4, 'Mancuerna de 2.5 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_2.5kg_corength.png'),
('Mancuerna 5kg Corength', 50, 9.99, 4, 4, 'Mancuerna de 5 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_5kg_corength.png'),
('Mancuerna 7.5kg Corength', 50, 14.99, 4, 4, 'Mancuerna de 7.5 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_7.5kg_corength.png'),
('Mancuerna 10kg Corength', 50, 19.99, 4, 4, 'Mancuerna de 10 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_10kg_corength.png'),
('Mancuerna 12kg Corength', 50, 24.99, 4, 4, 'Mancuerna de 12 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_12.5kg_corength.png'),
('Mancuerna 15kg Corength', 50, 29.99, 4, 4, 'Mancuerna de 15 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_15kg_corength.png'),
('Mancuerna 17.5kg Corength', 50, 34.99, 4, 4, 'Mancuerna de 17.5 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_17.5kg_corength.png'),
('Mancuerna 20kg Corength', 50, 39.99, 4, 4, 'Mancuerna de 20 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_20kg_corength.png'),
('Mancuerna 22.5kg Corength', 50, 44.99, 4, 4, 'Mancuerna de 22.5 kilogramos. Ideal para el entrenamiento serio. Distribuido por la marca Corength.', 'images/productos/mancuernas/mancuerna_22.5kg_corength.png'),

('Mancuerna 5kg Maniak', 50, 24.99, 4, 5, 'Mancuerna de 5 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_5kg_maniak.png'),
('Mancuerna 10kg Maniak', 50, 29.99, 4, 5, 'Mancuerna de 10 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_10kg_maniak.png'),
('Mancuerna 15kg Maniak', 50, 34.99, 4, 5, 'Mancuerna de 15 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_15kg_maniak.png'),
('Mancuerna 20kg Maniak', 50, 39.99, 4, 5, 'Mancuerna de 20 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_20kg_maniak.png'),
('Mancuerna 25kg Maniak', 50, 49.99, 4, 5, 'Mancuerna de 25 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_25kg_maniak.png'),
('Mancuerna 30kg Maniak', 50, 69.99, 4, 5, 'Mancuerna de 30 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_30kg_maniak.png'),
('Mancuerna 35kg Maniak', 50, 109.99, 4, 5, 'Mancuerna de 35 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_35kg_maniak.png'),
('Mancuerna 40kg Maniak', 50, 124.99, 4, 5, 'Mancuerna de 40 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_40kg_maniak.png'),
('Mancuerna 50kg Maniak', 50, 199.99, 4, 5, 'Mancuerna de 50 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_50kg_maniak.png');





-- Accesorios (categoria 5)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Cinturón Lastre', 50, 19.99, 5, 4, 'Cinturón de Lastre. Ideal para entrenar con peso lastrado. Distribuido por la marca Corength.', 'images/productos/accesorios/cinturon_lastre_corength.png'),
('Cinturón Lumbar', 50, 19.99, 5, 4, 'Cinturón Lumbar. Ideal para entrenar seguro y evitar lesiones lumbares y abdominales. Distribuido por la marca Corength.', 'images/productos/accesorios/cinturon_lumbar_corength.png'),
('Coderas Corength', 50, 9.99, 5, 4, 'Coderas. Ideal para entrenar y evitar lesiones en los codos. Distribuido por la marca Corength.', 'images/productos/accesorios/coderas_corength.png'),
('Rodilleras', 50, 9.99, 5, 4, 'Cinturón de Lastre. Ideal para entrenar con peso lastrado. Distribuido por la marca Corength.', 'images/productos/accesorios/rodilleras_corength.png'),
('Straps Tunturi', 50, 4.99, 5, 2, 'Straps. Ideal para que el agarre no limiten el entrenamiento. Distribuido por la marca Tunturi.', 'images/productos/accesorios/straps_tunturi.png'),
('Topes', 50, 0.99, 5, 1, 'Topes. Ideales para evitar que los discos se salgan de la barra al entrenar. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/accesorios/topes_domyos.png');

-- Bandas Elásticas (categoria 6)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Banda 5kg', 50, 4.99, 6, 4, 'Banda elástica de 5 kilogramos. Ideal para el calentamiento. Distribuido por la marca Corength.', 'images/productos/bandas elasticas/banda_5kg.png'),
('Banda 15kg', 50, 9.99, 6, 4, 'Banda elástica de 15 kilogramos. Ideal para entrenamientos dinámicos y calentamiento. Distribuido por la marca Corength.', 'images/productos/bandas elasticas/banda_15kg.png'),
('Banda 25kg', 50, 14.99, 6, 4, 'Banda elástica de 25 kilogramos. Ideal para entrenamientos dinámicos y calentamiento. Distribuido por la marca Corength.', 'images/productos/bandas elasticas/banda_25kg.png'),
('Banda 35kg', 50, 19.99, 6, 4, 'Banda elástica de 35 kilogramos. Ideal para entrenamientos dinámicos y de fuerza. Distribuido por la marca Corength.', 'images/productos/bandas elasticas/banda_35kg.png'),
('Banda 45kg', 50, 24.99, 6, 4, 'Banda elástica de 45 kilogramos. Ideal para entrenamientos dinámicos y de fuerza. Distribuido por la marca Corength.', 'images/productos/bandas elasticas/banda_45kg.png');




-- Kettlebells (categoria 7)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Kettlebell 6kg Domyos', 50, 4.99, 7, 1, 'Kettlebell de 6 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_6kg_domyos.png'),
('Kettlebell 8kg Domyos', 50, 9.99, 7, 1, 'Kettlebell de 8 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_8kg_domyos.png'),
('Kettlebell 12kg Domyos', 50, 14.99, 7, 1, 'Kettlebell de 12 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_12kg_domyos.png'),
('Kettlebell 16kg Domyos', 50, 19.99, 7, 1, 'Kettlebell de 16 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_16kg_domyos.png'),
('Kettlebell 20kg Domyos', 50, 34.99, 7, 1, 'Kettlebell de 20 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_20kg_domyos.png'),
('Kettlebell 24kg Domyos', 50, 44.99, 7, 1, 'Kettlebell de 24 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_24kg_domyos.png'),
('Kettlebell 32kg Domyos', 50, 64.99, 7, 1, 'Kettlebell de 32 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Domyos.', 'images/productos/kettlebells/kettlebell_32kg_domyos.png'),

('Kettlebell 6kg Tunturi', 50, 4.99, 7, 2, 'Kettlebell de 6 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_6kg_tunturi.png'),
('Kettlebell 8kg Tunturi', 50, 6.99, 7, 2, 'Kettlebell de 8 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_8kg_tunturi.png'),
('Kettlebell 10kg Tunturi', 50, 9.99, 7, 2, 'Kettlebell de 10 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_10kg_tunturi.png'),
('Kettlebell 12kg Tunturi', 50, 14.99, 7, 2, 'Kettlebell de 12 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_12kg_tunturi.png'),
('Kettlebell 16kg Tunturi', 50, 19.99, 7, 2, 'Kettlebell de 16 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_16kg_tunturi.png'),
('Kettlebell 20kg Tunturi', 50, 24.99, 7, 2, 'Kettlebell de 20 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_20kg_tunturi.png'),
('Kettlebell 24kg Tunturi', 50, 29.99, 7, 2, 'Kettlebell de 24 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_24kg_tunturi.png'),
('Kettlebell 32kg Tunturi', 50, 39.99, 7, 2, 'Kettlebell de 32 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_32kg_tunturi.png'),

('Kettlebell Gorilla 40kg Kraftboost', 50, 99.99, 7, 3, 'Kettlebell de 40 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Kraft Boost.', 'images/productos/kettlebells/kettlebell_gorilla_40kg_kraftboost.png');

-- Estructuras (categoria 8)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Barra Dominadas Kraftboost', 50, 99.99, 8, 3, 'Barra de dominadas. Ideal para hacer dominadas y muscle ups. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/barra_dominadas_kraftboost.png'),
('Máquina Poleas Kraftboost', 50, 299.99, 8, 3, 'Máquina de poleas. Ideal para hacer ejercicios aislados en polea. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/maquina_poleas_kraftboost.png'),
('Multiestación Kraftboost', 50, 149.99, 8, 3, 'Multiestación. Ideal para realizar todo tipo de ejercicios aislados en polea. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/multiestacion_kraftboost.png'),
('Multipower Kraftboost', 50, 344.99, 8, 3, 'Multipower. Ideal para hacer ejericios asistidos con barra multipower. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/multipower_kraftboost.png'),
('Paralelas Kraftboost', 50, 99.99, 8, 3, 'Paralelas. Ideal para hacer fondos y presses invertidos. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/paralelas_kraftboost.png');




-- Productos nuevos (Apareceran en la sección de productos nuevos del inicio)
INSERT INTO productos (nombre, stock, precio, id_categoria, id_marca, descripcion, imagen)
VALUES
('Banco Multifunción', 50, 174.99, 2, 1, 'Banco con multifunción. Ideal para todo tipo de ejercicios en banco o sentado. Fabricado en la fabrica de
Oxylane, distribuido por la marca Domyos.', 'images/productos/bancos/banco_multifuncion_domyos.png'),
('Torre Paralelas y Dominadas', 50, 149.99, 8, 3, 'Torre de paralelas y dominadas. Ideal para hacer dominadas, muscle ups, fondos y demás ejercicios. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/torre_paralelas_dominadas_kraftboost.png'),
('Kettlebell 28kg Tunturi', 50, 34.99, 7, 2, 'Kettlebell de 28 kilogramos. Ideal para entrenamientos funcionales o CrossFit. Distribuido por la marca Tunturi.', 'images/productos/kettlebells/kettlebell_28kg_tunturi.png'),
('Topes Rojos', 50, 4.99, 5, 3, 'Topes rojos. Ideales para evitar que los discos se salgan de la barra al entrenar. Distribuido por la marca Kraft Boost.', 'images/productos/accesorios/topes_rojos_kraftboost.png'),
('Mancuerna 45kg Maniak', 50, 174.99, 4, 5, 'Mancuerna de 45 kilogramos. Ideal para el entrenamiento profesional. Distribuido por la marca Maniak.', 'images/productos/mancuernas/mancuerna_45kg_maniak.png'),
('Banda 60kg', 50, 29.99, 6, 4, 'Banda elástica de 60 kilogramos. Ideal para entrenamientos dinámicos y de fuerza . Distribuido por la marca Corength.', 'images/productos/bandas elasticas/banda_60kg.png'),
('Megatron Kraftboost', 50, 399.99, 8, 3, 'Megatron. Ideal para realizar todo tipo de ejercicios aislados en polea. Distribuido por la marca Kraft Boost.', 'images/productos/estructuras/megatron_kraftboost.png'),
('Disco 25kg Maniak', 50, 49.99, 3, 5, 'Disco de acero de 25 kilogramos. Ideal para el entreno. Distribuido por la marca Maniak.', 'images/productos/discos/disco_25kg_maniak.png');