
class ViewController():
	def __init__(self, model):
		self.model = model

	def searchByDate(self, date):
		note = self.model.searchByDate(date)
		if note != None:
			print("Name: %s\nDate: %s\nDescription: %s\n"%(note.name, note.date, note.task))
		else:
			print("Not found")