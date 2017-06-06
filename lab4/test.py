
if __name__ == "__main__":
    import unittest
    import doctest
    import database
    import models

    import test_serialize

    doctest.testmod()
    doctest.testmod(m=database)
    doctest.testmod(m=models)

    unittest.TestProgram(test_serialize)
