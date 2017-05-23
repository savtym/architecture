import notes


class ModelController:

    def __init__(self):
        self.notes = []
        self.notes.append(notes.Note('1', '01.01.2017', 'Desc of 1'))
        self.notes.append(notes.Note('2', '01.02.2017', 'Desc of 2'))
        self.notes.append(notes.Note('3', '01.03.2017', 'Desc of 3'))
        self.notes.append(notes.Note('4', '01.04.2017', 'Desc of 4'))
        self.notes.append(notes.Note('5', '01.05.2017', 'Desc of 5'))
        self.notes.append(notes.Note('6', '01.06.2017', 'Desc of 6'))
        self.notes.append(notes.Note('7', '01.07.2017', 'Desc of 7'))
        self.notes.append(notes.Note('8', '01.08.2017', 'Desc of 8'))

    
    def searchByDate(self, date):
        """
        return object if find date in list notes
        other - None
        >>> mc = ModelController()
        >>> mc.searchByDate("1111") is None
        True
        >>> mc.searchByDate('01.08.2017') is not None
        True
        """
        for note in self.notes:
            if note.date == date:
                return note
        return None

    def searchByName(self, name):
        """
        return object if find name in list notes
        other - None
        >>> mc = ModelController()
        >>> mc.searchByName("2") is not None
        True
        >>> mc.searchByName("qwerty") is None
        True
        """
        for note in self.notes:
            if note.name == name:
                return note
        return None

    def setNewEl(self, name, date, task):
        """
        add object to db
        >>> mc = ModelController()
        >>> mc.setNewEl('test','01.01.2000', 'test')
        >>> mc.searchByName('test') is not None
        True
        >>> mc.searchByDate('01.01.2000') is not None
        True
        """
        self.notes.append(notes.Note(name, date, task))

    def deleteNote(self, name):
        """
        add object to db
        >>> mc = ModelController()
        >>> mc.setNewEl('test','01.01.2000', 'test')
        >>> mc.searchByName('test') is not None
        True
        >>> mc.searchByDate('01.01.2000') is not None
        True
        >>> mc.deleteNote('test')
        >>> mc.searchByName('test') is None
        True
        >>> mc.searchByDate('01.01.2000') is None
        True
        """
        for i in self.notes:
            if (i.name == name):
                self.notes.remove(i)

    def getList(self):
        """
        add object to db
        >>> mc = ModelController()
        >>> mc.getList() is not None
        True
        """
        return self.notes


if __name__ == "__main__":
    import doctest
    doctest.testmod()