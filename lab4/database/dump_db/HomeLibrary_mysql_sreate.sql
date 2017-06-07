CREATE DATABASE IF NOT EXISTS library DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE library;

-- --------------------------------------------------------

--
-- Структура таблицы authors
--

CREATE TABLE IF NOT EXISTS authors (
  id int(10) NOT NULL AUTO_INCREMENT,
  author varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY authors_author_uindex (`author`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы authors
--

INSERT INTO authors (`id`, `author`) VALUES
(1, 'author1'),
(3, 'author111'),
(2, 'author2');

-- --------------------------------------------------------

--
-- Структура таблицы books
--

CREATE TABLE IF NOT EXISTS books (
  id int(10) NOT NULL AUTO_INCREMENT,
  book varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY books_book_uindex (`book`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы books
--

INSERT INTO books (`id`, `book`) VALUES
(9, 'book11'),
(10, 'book123');

-- --------------------------------------------------------

--
-- Структура таблицы library
--

CREATE TABLE IF NOT EXISTS library (
  id int(10) NOT NULL AUTO_INCREMENT,
  book int(10) NOT NULL,
  author int(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY book (`book`,`author`),
  KEY author_fk0 (`author`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы library
--
ALTER TABLE library
  ADD CONSTRAINT author_fk0 FOREIGN KEY (`author`) REFERENCES authors (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT book_fk0 FOREIGN KEY (`book`) REFERENCES books (`id`) ON DELETE CASCADE ON UPDATE CASCADE;