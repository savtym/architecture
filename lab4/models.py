from database import Table


class Book (Table):
    """
    class Book to describe Book table in database
    id -- id in table in database
    book -- name of field with book title
    """

    id = None
    book = None

    def __init__(self, book):
        """
        Creates new table Book for book with name `book`
        """
        super().__init__()
        self.id = super().getLastId("books")
        self.book = book
        super().isPossibleType(book, str)

    def save(self):
        """
        save book in table in database. Returns last ID
        """
        return super().save(self.__dict__, "books")

    def delete(self):
        """
        delete book from table in DataBase
        """
        # for book in Library.find("book", self):
        #     book.delete()
        # Book.listAll().remove(self)
        self.remove("book", self.book, "books")
        del self

    @staticmethod
    def listAll():
        """
        returns all books as list
        """
        # [Book(b["book"]) for b in Table.listAll("books")]
        # return Table.listAll("books")
        lst = []
        for b in Table.listAll("books"):
            book = Book(b['book'])
            book.id = b['id']
            lst.append(book)
        return lst

    @staticmethod
    def find(key, value):
        """
        find book by key (f.e. book), where key == value
        """
        data = Table.find("books", key, value)
        if data is None:
            return None
        b = data[0]
        book = Book(b['book'])
        book.id = b['id']
        return book


class Author (Table):
    """
    class Author to describe Author table in database
    id -- id in table in database
    name -- field with authors name
    """

    id = None
    author = None

    def __init__(self, name):
        self.id = super().getLastId("authors")
        self.author = name
        super().isPossibleType(name, str)

    def save(self):
        """
        save author in table in database. Returns last ID
        """
        return super().save(self.__dict__, "authors")

    def delete(self):
        """
        delete author from table in DataBase
        >>> from database import DataBase
        >>> DataBase.getInstance().clear()
        >>> author = Author(name='name')
        >>> author.save()
        2
        >>> [author] == Author.listAll()
        True
        >>> author.delete()
        >>> Author.listAll()
        []
        >>> author = Author(name='name1')
        >>> author.save()
        2
        >>> book = Book("book")
        >>> book.save()
        2
        >>> Library(book=book, author=author).save()
        2
        >>> author.delete()
        >>> Author.listAll()
        []
        >>> Book.listAll()
        []
        """
        # for book in Library.find("author", self):
        #     book.book.delete()
        # Author.listAll().remove(self)
        self.remove("author", self.author, "authors")
        del self

    @staticmethod
    def listAll():
        """
        returns all authors as list
        """
        # return Table.listAll("authors")
        # return [Author(a["author"]) for a in Table.listAll("authors")]
        lst = []
        for a in Table.listAll("authors"):
            author = Author(a['author'])
            author.id = a['id']
            lst.append(author)
        return lst

    @staticmethod
    def find(key, value):
        """
        find author by key (f.e. name), where key == value
        """
        data = Table.find("authors", key, value)
        if data is None:
            return None
        a = data[0]
        author = Author(a['author'])
        author.id = a['id']
        return author


class Library (Table):
    """
    class Library to make relate between Author and Book
    id -- id in table in database
    author -- foreign key to Author
    book   -- foreign key to Book
    """

    id = None
    book = None
    author = None

    def __init__(self, book, author):
        self.id = super().getLastId("library")
        self.book = book
        self.author = author
        super().isPossibleType(book, Book)
        super().isPossibleType(author, Author)

    def save(self):
        """
        save Library in table in database. Returns last ID
        """
        return super().save({'book': str(self.book.id),
                             'author': str(self.author.id)}, "library")

    def delete(self):
        """
        delete book from table in DataBase
        >>> from database import DataBase
        >>> DataBase.getInstance().clear()
        >>> book = Book(book = 'book')
        >>> book.save()
        2
        >>> author = Author(name = 'author')
        >>> author.save()
        2
        >>> lib = Library(book = book, author = author)
        >>> lib.save()
        2
        >>> Library.listAll() == [lib]
        True
        >>> lib.delete()
        >>> Library.listAll()
        []
        """
        # Library.listAll().remove(self)
        # del self
        pass

    @staticmethod
    def listAll():
        """
        returns all books and authors as list
        >>> from database import DataBase
        >>> DataBase.getInstance().clear()

        >>> book1 = Book(book = 'book1')
        >>> book1.save()
        2
        >>> author1 = Author(name = 'author1')
        >>> author1.save()
        2
        >>> lib1 = Library(book = book1, author = author1)
        >>> lib1.save()
        2
        >>> lst = [[lib1]]

        >>> book2 = Book(book = 'book2')
        >>> book2.save()
        3
        >>> author2 = Author(name = 'author2')
        >>> author2.save()
        3
        >>> lib2 = Library(book = book2, author = author2)
        >>> lib2.save()
        3
        >>> lst.append([lib2])
        >>> [lib1, lib2] == Library.listAll()
        True
        """
        lst = []
        for lib in Table.listAll("library"):
            l = Library(
                Book.find("id", str(lib["book"])),
                Author.find("id", str(lib["author"])))
            l.id = lib['id']
            lst.append(l)
        return lst

    @staticmethod
    def find(key, value):
        """
        find Book and its Author by key (f.e. name), where key == value
        >>> from database import DataBase
        >>> DataBase.getInstance().clear()
        >>> book = Book(book = 'namebook')
        >>> book.save()
        2
        >>> author = Author(name = 'author')
        >>> author.save()
        2
        >>> lib = Library(book = book, author = author)
        >>> lib.save()
        2
        >>> founded = Library.find('book', book)[0]
        >>> founded == lib
        True
        """
        return Table.find("library", key, value)

    @staticmethod
    def getBooksAndAuthors():
        """
        convert list of books and authors. Group
        authors in list and returns it with Book.
        Make the same for other books and returns
        list of lists of Book and list of authors.
        >>> from database import DataBase
        >>> DataBase.getInstance().clear()
        >>> book = Book(book = 'book')
        >>> book.save()
        2
        >>> author = Author(name = 'author')
        >>> author.save()
        2
        >>> author1 = Author(name = 'author1')
        >>> author1.save()
        3
        >>> lib1 = Library(book = book, author = author)
        >>> lib1.save()
        2
        >>> lib2 = Library(book = book, author = author1)
        >>> lib2.save()
        3
        >>> lst = [lib1, lib2]
        >>> lst == Library.listAll()
        True
        >>> ls = [lst]
        >>> ls == Library.getBooksAndAuthors()
        True
        >>> Library.listAll() == Library.getBooksAndAuthors()
        False
        """
        tmp = []
        bookName = ""
        i = 0
        length = len(Library.listAll())
        for row in Library.listAll():
            if bookName != row.book.book:
                bookName = row.book.book
                tmp = Library._collect(tmp, bookName, i, length)
            i += 1
        return tmp

    @staticmethod
    def _collect(tmp, book, i, length):
        """
        collect authors, if they write the same book, to list and returns it
        """
        lst = Library.listAll()
        if i < length:
            tmp.append([item for item in lst[i:] if item.book.book == book])
        return tmp
