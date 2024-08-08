Create table nasdaq (
	ticker VARCHAR(50),
    name VARCHAR(500),
    country VARCHAR(100),
    sector VARCHAR(100)
    );

alter table transactions add cumulative double;
alter table transactions add last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

alter table holdings add last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;