CREATE DATABASE IF NOT EXISTS songs_app
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE songs_app;

CREATE TABLE usuarios (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(60)  NOT NULL,
  email         VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE artistas (
  id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE canciones (
  id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id   INT UNSIGNED      NOT NULL,
  artista_id   INT UNSIGNED      NOT NULL,
  titulo       VARCHAR(80)       NOT NULL,
  tonalidad    VARCHAR(4)        NOT NULL,
  bpm          SMALLINT UNSIGNED NOT NULL,
  duracion_min DECIMAL(4,1)      NOT NULL,
  fecha_ensayo DATE              NOT NULL,
  estado       ENUM('no_dominada','a_medias','dominada')
               NOT NULL DEFAULT 'no_dominada',
  letra        TEXT              NULL,
  CONSTRAINT fk_canciones_usuario FOREIGN KEY (usuario_id)
    REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_canciones_artista FOREIGN KEY (artista_id)
    REFERENCES artistas (id),
  CONSTRAINT chk_canciones_bpm CHECK (bpm BETWEEN 40 AND 240),
  CONSTRAINT chk_canciones_duracion
    CHECK (duracion_min > 0 AND duracion_min <= 20)
);

CREATE TABLE cancion_acordes (
  cancion_id INT UNSIGNED     NOT NULL,
  posicion   TINYINT UNSIGNED NOT NULL,
  acorde     VARCHAR(8)       NOT NULL,
  PRIMARY KEY (cancion_id, posicion),
  CONSTRAINT fk_acordes_cancion FOREIGN KEY (cancion_id)
    REFERENCES canciones (id) ON DELETE CASCADE,
  CONSTRAINT chk_acordes_posicion CHECK (posicion BETWEEN 1 AND 12)
);
