from models import Book, Library, Author
from database import DataBase
import view
import sys


class Controller:

    """
    Class for calling logic for working with DataBase (models)
    and send data from models to views.
    Controller._instance == Controller.getInstance()
    """

    _instance = None

    @staticmethod
    def getInstance():
        """
        realize pattern singleton for Controller --
        one object of class for all program code
        """
        if Controller._instance is None:
            Controller._instance = Controller()
        return Controller._instance

    def actionShowAllBooks(self):
        """
        print all books in library on screen.
        """
        view.Table.showAllBooks(Library.getBooksAndAuthors())

    def actionCreateNewBook(self):
        """
        save new book in DataBase
        """
        newBook = view.ConsoleEnter.enterNewBook()
        if Book.find("book", newBook["book"]) is not None:
            view.OutMessages.errorAddingBook(newBook["book"])
            return
        book = Book(book=newBook["book"])
        book.save()
        for authorName in newBook["authors"]:
            author = Author(name=authorName)
            author.save()
            Library(Book.find('book', newBook["book"]),
                    Author.find('author', authorName)).save()
        view.Table.showAllBooks(Library.getBooksAndAuthors())

    def actionDeleteBookByTitle(self):
        """
        delete book from library by its title.
        """
        bookTitle = view.ConsoleEnter.enterBookTitle()
        book = Book.find("book", bookTitle)
        if book is None:
            view.OutMessages.errorDeletingBook(bookTitle)
            return
        book.delete()
        view.Table.showAllBooks(Library.getBooksAndAuthors())

    def actionDeleteBookByAuthor(self):
        """
        delete book from library by author\'s name.
        """
        authorName = view.ConsoleEnter.enterBookAuthor()
        author = Author.find("author", authorName)
        if author is None:
            view.OutMessages.errorDeletingBook(authorName, True)
            return
        author.delete()
        view.Table.showAllBooks(Library.getBooksAndAuthors())

    def actionExit(self):
        """
        close program and save current state of DataBase to file
        """
        DataBase.getInstance().saveDataBase()
        sys.exit()
