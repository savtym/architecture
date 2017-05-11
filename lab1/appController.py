import modelController
import viewController

class AppController():

  def __init__(self):
    self.model = modelController.ModelController()
    self.view = viewController.ViewController(self.model)
                

app = AppController()
app.view.searchByDate('01.01.2017')
