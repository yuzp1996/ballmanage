import unittest, ballmange
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

class BallOrderTest(unittest.TestCase):
    
    def testInputStr(self):
        p = ballmange.BadmintonVenueOrder.main("U123 2017-10-10 12:00~17:00 A")
        self.failUnless(p.startswith("Success"),u'Error')

if __name__ == "__main__":unittest.main()
    