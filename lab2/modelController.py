import notes
import configparser
import jsonSerialization as jsSer
import yamlSerialization as yaSer
import pickleSerialization as piSer


class ModelController:

    def __init__(self, file='notes', conf='conf.ini'):
        self.notes = []
        self.fileOfData = file
        self.fileOfConf = conf

        # self.notes.append(notes.Note('1', '01.01.2017', 'Desc of 1'))
        # self.notes.append(notes.Note('2', '01.02.2017', 'Desc of 2'))
        # self.notes.append(notes.Note('3', '01.03.2017', 'Desc of 3'))
        # self.notes.append(notes.Note('4', '01.04.2017', 'Desc of 4'))
        # self.notes.append(notes.Note('5', '01.05.2017', 'Desc of 5'))
        # self.notes.append(notes.Note('6', '01.06.2017', 'Desc of 6'))
        # self.notes.append(notes.Note('7', '01.07.2017', 'Desc of 7'))
        # self.notes.append(notes.Note('8', '01.08.2017', 'Desc of 8'))

        self.jsSer = jsSer.JSONSerializer()
        self.yaSer = yaSer.YAMLSerializer()
        self.piSer = piSer.PickleSerializer()

    def __iter__(self):
        return NotesIterator(self)

    def __eq__(self, otherNotes):
        return self.notes == otherNotes

    def __str__(self):
        if len(self.notes) == 0:
            return 'List of notes is empty'
        return str(self.notes)

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
            if i.name == name:
                self.notes.remove(i)

    def getList(self):
        """
        add object to db
        >>> mc = ModelController()
        >>> mc.getList() is not None
        True
        """

        return self.notes

    def saveData(self):
        """
        Serialize data into file using method specified in configuration file.
        """

        method = self.getMethodWithConf()
        if method == 'pickle':
            with open(self.fileOfData + '.pickle', 'wb') as f:
                self.piSer.serialize(self, f)
        elif method == 'yaml':
            with open(self.fileOfData + '.yaml', 'w') as f:
                self.yaSer.serialize(self, f)
        elif method == 'json':
            with open(self.fileOfData + '.json', mode='w') as f:
                self.jsSer.serialize(self, f)

    def loadData(self):
        """
        Desialize data from file.
        """

        method = self.getMethodWithConf()
        if method == 'json':
            with open(self.fileOfData + '.json', mode='r') as f:
                self.notes = self.jsSer.deserialize(f)
        elif method == 'pickle':
            with open(self.fileOfData + '.pickle', mode='rb') as f:
                self.notes = self.piSer.deserialize(f)
        elif method == 'yaml':
            with open(self.fileOfData + '.yaml', mode='r') as f:
                self.notes = self.yaSer.deserialize(f)

    def getMethodWithConf(self):
        """
        Get method for serialization data
        """

        config = configparser.ConfigParser()
        config.read(self.fileOfConf)
        if 'Serialization' in config:
            return config['Serialization']['Method']


class NotesIterator:
    """
    Class Iterator for ModelController => Notes
    """
    def __init__(self, model):
        self.model = model
        self.start = 0
        self.stop = len(model.notes)
        self.index = self.start - 1

    def __next__(self):
        self.index += 1
        if self.index == self.stop:
            raise StopIteration
        return self.model.notes[self.index]


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
