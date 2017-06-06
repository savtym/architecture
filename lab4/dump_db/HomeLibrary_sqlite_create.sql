CREATE TABLE library (
	id integer PRIMARY KEY AUTOINCREMENT,
	book integer,
	author integer
);

CREATE TABLE books (
	id integer PRIMARY KEY AUTOINCREMENT,
	book varchar
);

CREATE TABLE authors (
	id integer PRIMARY KEY AUTOINCREMENT,
	author varchar
);

