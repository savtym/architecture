
import argparse
import viewController
import modelController


class KeysController:

    parser = argparse.ArgumentParser()

    parser.add_argument('-sdate')
    parser.add_argument('-sname')
    parser.add_argument('-add')
    parser.add_argument('-d')
    parser.add_argument('-t')
    parser.add_argument('-remove')
    parser.add_argument('-all', action='store_true')

    def __init__(self, model, view):
        self.model = model
        self.model.loadData()
        self.view = view

    def mainMenu(self):
        self.args = self.parser.parse_args()
        if self.args.sdate:
            note = self.model.searchByDate(self.args.sdate)
            self.view.printSingleNote(note)
        elif self.args.sname:
            note = self.model.searchByName(self.args.sname)
            self.view.printSingleNote(note)
        elif self.args.add and self.args.d and self.args.t:
            self.model.setNewEl(self.args.add, self.args.d, self.args.t)
            self.model.saveData()
        elif self.args.remove:
            self.model.deleteNote(name)
            self.model.saveData()
        elif self.args.all:
            self.view.notesView()
