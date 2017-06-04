import modelController
import viewController


class AppController():

    def __init__(self):
        self.model = modelController.ModelController()
        self.view = viewController.ViewController(self.model)


app = AppController()
# app.view.mainMenu()
# app.model.saveData()
app.model.loadData()
app.view.notesView()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
