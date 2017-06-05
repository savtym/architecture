
import modelController
import viewController
import keysController
import configparser


class AppController:

    def __init__(self):
        self.model = modelController.ModelController()
        self.view = viewController.ViewController(self.model)
        self.keys = keysController.KeysController(self.model, self.view)
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.typeUI = ''
        if 'UserInterface' in conf:
            self.typeUI = conf['UserInterface']['Type']


app = AppController()

if app.typeUI == 'keys':
    app.keys.mainMenu()
elif app.typeUI == 'ui':
    app.view.mainMenu()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
