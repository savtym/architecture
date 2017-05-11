import modelController
import viewController

class AppController():

  def __init__(self):
    self.model = modelController.ModelController()
    self.view = viewController.ViewController()
                

app = AppController()