class ViewController():
	def __init__(self, model):
		self.model = model

	def mainMenu (self):
		while(1):
			print ("1. View all notes\n2. Add new note\n3. Delete note\n4. Search by name\n5. Search by date\n6. Exit\n")
			print ("Input a number to choose an apropriate option")
			option = input()
			try:
				option = int(option)
			except ValueError:
				print("Please input a number")
			if (option < 1 or option > 6):
				print("Please input a number from 1 to 6")
			if (option == 6):
				return
			self.chooseMainOption(option)



	def chooseMainOption(self, option):
		if (option == 1):
			self.notesView()
		elif (option == 2):
			self.addNewEl()
		elif (option == 3):
			self.deleteEl()
		elif (option == 4):
			self.searchByName()
		elif (option == 5):
			self.searchByDate()

	def notesView(self):
		notes = self.model.getList()
		if notes == None:
			print("Not found")
		else:
			for i in notes:
				print("Name: %s\nDate: %s\nDescription: %s\n" % (i.name, i.date, i.task))

	def addNewEl(self):
		name = input("Input name of new note\n")
		date = input("Input date of new note\n")
		task = input("Input task of new note\n")
		self.model.setNewEl(name,date,task)

	def deleteEl(self):
		print ("Input name of note you want to delete")
		name = input()
		self.model.deleteNote(name)

	def searchByDate(self):
		date = input("Input date to search\n")
		note = self.model.searchByDate(date)
		if note != None:
			print("Name: %s\nDate: %s\nDescription: %s\n"%(note.name, note.date, note.task))
		else:
			print("Not found")

	def searchByName(self):
		name = input("Input name to search\n")
		note = self.model.searchByDate(name)
		if note != None:
			print("Name: %s\nDate: %s\nDescription: %s\n"%(note.name, note.date, note.task))
		else:
			print("Not found")
