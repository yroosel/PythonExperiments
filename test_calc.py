import unittest
import calc

class TestCalc(unittest.TestCase):

   def test_add(self):
       self.assertEqual(calc.add(100, 10), 110)
       self.assertEqual(calc.add(-1, 1), 0)
       self.assertEqual(calc.add(-1, -1), -2)

   def test_multiply(self):
       self.assertEqual(calc.multiply(100, 10), 1000)
       self.assertEqual(calc.multiply(-1, 1), -1)
       self.assertEqual(calc.multiply(-1, -1), 1)

if __name__ == "__main__":
   unittest.main()
