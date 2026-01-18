CREATE TABLE IF NOT EXISTS DeviceTypesToUserTypes (
	device_type_id INT NOT NULL,
	user_type_id INT NOT NULL,
	PRIMARY KEY(device_type_id, user_type_id)
);


CREATE TABLE IF NOT EXISTS Users (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL UNIQUE,
	user_type_id INT NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS UserTypes (
	id INT NOT NULL AUTO_INCREMENT,
	type VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS Houses (
	id INT NOT NULL AUTO_INCREMENT,
	adress VARCHAR(255) NOT NULL UNIQUE,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS DeviceTypes (
	id INT NOT NULL AUTO_INCREMENT,
	type VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS Devices (
	id INT NOT NULL AUTO_INCREMENT,
	house_id INT NOT NULL,
	device_type_id INT NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS Scenaries (
	id INT NOT NULL AUTO_INCREMENT,
	time_from TIME NOT NULL,
	time_till TIME NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS CoNEToDevices (
	scenary_id INT NOT NULL,
	device_id INT NOT NULL,
	is_on BOOLEAN NOT NULL,
	PRIMARY KEY(scenary_id, device_id)
) COMMENT='Conjunction of necessary events to devices';


CREATE TABLE IF NOT EXISTS ActivationsToDevices (
	scenary_id INT NOT NULL,
	device_id INT NOT NULL,
	is_on BOOLEAN NOT NULL,
	affect_time TIME,
	PRIMARY KEY(scenary_id, device_id)
);


CREATE TABLE IF NOT EXISTS Events (
	id INT NOT NULL AUTO_INCREMENT UNIQUE,
	user_id INT,
	device_id INT,
	scenary_id INT,
	value BOOLEAN NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS Measures (
	id INT NOT NULL AUTO_INCREMENT UNIQUE,
	device_id INT NOT NULL,
	measure_time DATETIME NOT NULL,
	value REAL,
	PRIMARY KEY(id)
);


ALTER TABLE Users
ADD FOREIGN KEY(user_type_id) REFERENCES UserTypes(id);
ALTER TABLE Devices
ADD FOREIGN KEY(house_id) REFERENCES Houses(id);
ALTER TABLE Devices	
ADD FOREIGN KEY(device_type_id) REFERENCES DeviceTypes(id);
ALTER TABLE CoNEToDevices
ADD FOREIGN KEY(device_id) REFERENCES Devices(id);
ALTER TABLE CoNEToDevices
ADD FOREIGN KEY(scenary_id) REFERENCES Scenaries(id);
ALTER TABLE ActivationsToDevices
ADD FOREIGN KEY(scenary_id) REFERENCES Scenaries(id);
ALTER TABLE ActivationsToDevices
ADD FOREIGN KEY(device_id) REFERENCES Devices(id);
ALTER TABLE DeviceTypesToUserTypes
ADD FOREIGN KEY(user_type_id) REFERENCES UserTypes(id);
ALTER TABLE DeviceTypesToUserTypes
ADD FOREIGN KEY(device_type_id) REFERENCES DeviceTypes(id);
ALTER TABLE Events
ADD FOREIGN KEY(user_id) REFERENCES Users(id);
ALTER TABLE Events
ADD FOREIGN KEY(device_id) REFERENCES Devices(id);
ALTER TABLE Events
ADD FOREIGN KEY(scenary_id) REFERENCES Scenaries(id);
ALTER TABLE Measures
ADD FOREIGN KEY(device_id) REFERENCES Devices(id);