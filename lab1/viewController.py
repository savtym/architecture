class ViewController():
    def __init__(self, model):
        self.model = model

    def searchByDate(self, date):
        note = self.model.searchByDate(date)
        if note is not None:
            print(
                "Name: %s\nDate: %s\nDesc: %s\n" %
                (note.title, note.date, note.task)
            )
        else:
            print("Not found")
