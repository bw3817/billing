
CREATE TABLE rates
(
  id integer NOT NULL primary key AUTO_INCREMENT,
  cust_id integer not null,
  rate decimal(10,2) DEFAULT NULL,
  cre_dt timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  mod_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  comments text
) ;


CREATE TABLE projects
(
  id integer NOT NULL primary key AUTO_INCREMENT,
  cust_id integer not null,
  name varchar(40) null,
  billed tinyint(1) default 0,
  paid tinyint(1) default 0,
  cre_dt timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  mod_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  comments text null
) ;


CREATE TABLE hours
(
  id integer NOT NULL primary key AUTO_INCREMENT,
  cust_id integer not null,
  project_id integer not null,
  hrs decimal(10,2) DEFAULT NULL,
  cre_dt timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  mod_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  comments text
) ;



