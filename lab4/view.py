from controllers import Controller


class Menu:
    """
    class to out menu of program and get command to run of program's logic
    _instance -- instance of this class
    _menu -- items of menu with Controller for punct and action name of punct
    """

    _instance = None
    _menu = [

        {
            "id": "1",
            "command": "Get all books",
            "controller": Controller,
            "action": "actionShowAllBooks"
        },
        {
            "id": "2",
            "command": "Add new book",
            "controller": Controller,
            "action": "actionCreateNewBook"
        },
        {
            "id": "3",
            "command": "Remove book",
            "controller": Controller,
            "action": "actionDeleteBookByTitle"
        },
        {
            "id": "4",
            "command": "Remove all books of author",
            "controller": Controller,
            "action": "actionDeleteBookByAuthor"
        },
        {
            "id": "5",
            "command": "Exit",
            "controller": Controller,
            "action": "actionExit"
        }

    ]

    @staticmethod
    def getInstance():
        """
        method for realize pattern singleton for this class
        (one object will be created and saved in _instance)
        """
        if Menu._instance is None:
            Menu._instance = Menu()
        return Menu._instance

    def out(self):
        """
        print Menu of program
        """
        for item in self._menu:
            print(item["id"] + ") " + item["command"])

    def getCommand(self):
        """
        wait for command from Console: command is the nuber of menu punct
        to run it. After entering check entered data and, if command is valid,
        returns dict with command id, command title, controller and action.
        Otherwise run itself again.
        """
        try:
            num = int(input('Enter command number:\n> '))
            if num <= 0 or num > len(self._menu):
                return self.getCommand()
            return self.getItem(num)
        except ValueError:
            return self.getCommand()

    def getItem(self, command):
        """
        returns dict from _menu with command id, command title,
        controller and action by id
        """
        return next(item for item in self._menu if item["id"] == str(command))


class Table:
    """
    class for printing books and authors from table to screen.
    All methods are static, cuz there is not reason to create instances
    """

    @staticmethod
    def showAllBooks(allBooks):
        """
        out all books in database and wait of pressing any key.
        If DataBase is empty,out message about this
        """
        print("")
        if len(allBooks) == 0:
            print("You have not books (or you not added them yet)")
            return
        for book in allBooks:
            Table.showBook(book)
        input("Press any key to continue\n")

    @staticmethod
    def showBook(table):
        """
        wrapper for methods showBookTitle, showBookAuthor,
        out one book and its author(s) call showBookTitle and showBookAuthors
        with necessaries parameters
        """
        Table.showBookTitle(table[0].book)
        Table.showBookAuthors(table)
        print("\n")

    @staticmethod
    def showBookTitle(book):
        """
        out books title as Book:      :bookTitle
        """
        print("Book:      " + book.book)

    @staticmethod
    def showBookAuthors(bookAuthors):
        """
        out book's author(s)'s names as Author(s): :authorName
        """
        print("Author(s): ", end="")
        for author in bookAuthors:
            print(author.author.author, end=" ")


class ConsoleEnter:

    @staticmethod
    def enterNewBook():
        """
        call enterBook and enterAuthor. Collect this data to dict and return it
        Examples of calling -- call of enterBookTitle & enterBookAuthors
        {'book': 'book', 'authors': ['author']}
        """
        return {
            "book": ConsoleEnter.enterBookTitle(),
            "authors": list(ConsoleEnter.enterBookAuthors())
        }

    @staticmethod
    def enterBookTitle():
        """
        enter book\'s title from console if enterring is correct
        return it or run recursively
        """
        bookTitle = input("Enter book\'s title:\n> ")
        if len(bookTitle) == 0:
            return ConsoleEnter.enterBookTitle()
        return bookTitle

    @staticmethod
    def enterBookAuthor():
        """
        enter book\'s author from console if enterring is correct
        return it or run recursively
        """
        author = input("Enter author\'s name:\n> ")
        if len(author) != 0:
            return author
        else:
            return ConsoleEnter.enterBookAuthor()

    @staticmethod
    def enterBookAuthors(authors=set()):
        """
        collect authors of book to set. if pressed 'y', adds another author,
        if 'n', returns collected authors
        """
        authors.add(ConsoleEnter.enterBookAuthor())
        conf = ""
        while conf not in ["y", "n"]:
            conf = input("Add another author (y/n):\n> ")
        if conf == "y":
            ConsoleEnter.enterBookAuthors(authors)
        return authors


class OutMessages:

    """
    class with methods for out messages about errors of finishing operations
    """

    @staticmethod
    def errorDeletingBook(name, flag=False):
        """
        show message if was the error with deleting book or all book(s)
        and their author, wait pressing any key to continue
        """
        if flag:
            print("Book(s) of \"" + name + "\" absent in library")
        else:
            print("Book \"" + name + "\" absent in library")
        input("Press any key to continue\n")

    @staticmethod
    def errorAddingBook(bookTitle):
        """
        show message if book is already in library and adding was not finished,
        and wait pressing any key
        """
        input("Book \"" + bookTitle +
              "\" is already in library.\nPress any key to continue\n")
