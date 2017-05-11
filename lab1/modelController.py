import model.notes

class ModelController:

  # Initialization with data
  def __init__(self):
    self.notes = []
    self.notes.append(model.notes.Note('Task 1', '01.01.2017', 'Description of task 1'))
    self.notes.append(model.notes.Note('Task 2', '01.02.2017', 'Description of task 2'))
    self.notes.append(model.notes.Note('Task 3', '01.03.2017', 'Description of task 3'))
    self.notes.append(model.notes.Note('Task 4', '01.04.2017', 'Description of task 4'))
    self.notes.append(model.notes.Note('Task 5', '01.05.2017', 'Description of task 5'))
    self.notes.append(model.notes.Note('Task 6', '01.06.2017', 'Description of task 6'))
    self.notes.append(model.notes.Note('Task 7', '01.07.2017', 'Description of task 7'))
    self.notes.append(model.notes.Note('Task 8', '01.08.2017', 'Description of task 8'))

  def searchByDate(self, date):
    for note in self.notes:
      if note.date == date:
        return note
    return None
