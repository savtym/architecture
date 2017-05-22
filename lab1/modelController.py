import model.notes


class ModelController:

    """
    return object if find date in list notes
    other - None

    >>> searchByDate("1111")
    None
    """
    # Initialization with data
    def __init__(self):
        self.notes = []
        self.notes.append(model.notes.Note('1', '01.01.2017', 'Desc of 1'))
        self.notes.append(model.notes.Note('2', '01.02.2017', 'Desc of 2'))
        self.notes.append(model.notes.Note('3', '01.03.2017', 'Desc of 3'))
        self.notes.append(model.notes.Note('4', '01.04.2017', 'Desc of 4'))
        self.notes.append(model.notes.Note('5', '01.05.2017', 'Desc of 5'))
        self.notes.append(model.notes.Note('6', '01.06.2017', 'Desc of 6'))
        self.notes.append(model.notes.Note('7', '01.07.2017', 'Desc of 7'))
        self.notes.append(model.notes.Note('8', '01.08.2017', 'Desc of 8'))

    """
    return object if find date in list notes
    other - None

    >>> searchByDate("1111")
    None
    """
    def searchByDate(self, date):
        for note in self.notes:
            if note.date == date:
                return note
        return None

    """
    return object if find title in list notes
    other - None

    >>> searchByTitle("1111")
    None
    """
    def searchByTitle(self, title):
        for note in self.notes:
            if note.title == title:
                return note
        return None
