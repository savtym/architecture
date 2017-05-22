import modelController
import viewController


class AppController():

    def __init__(self):
        self.model = modelController.ModelController()
        self.view = viewController.ViewController(self.model)


app = AppController()
print(app.view.searchByDate('1111'))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
