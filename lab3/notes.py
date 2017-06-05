class Note:

    def __init__(self, name, date, task):
        self.name = name
        self.date = date
        self.task = task

    def __eq__(self, note):
        return self.name == note.name and self.date == note.date \
            and self.task == note.task
