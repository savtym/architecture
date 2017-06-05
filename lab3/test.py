from unittest.mock import patch, create_autospec
import unittest as ut

import modelController as mc


class Test(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mc = mc.ModelController()
        cls.mc.loadData()


if __name__ == "__main__":
    ut.main()