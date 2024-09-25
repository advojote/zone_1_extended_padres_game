CREATE TABLE areas (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255),
  runs INT DEFAULT 0,
  adds INT DEFAULT 0,
  PRIMARY KEY (id)
);

CREATE TABLE districts (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE missionaries (
  name VARCHAR(255),
  area INT NOT NULL,
  district INT NOT NULL,
  zone INT NOT NULL,
  PRIMARY KEY (name)
);

