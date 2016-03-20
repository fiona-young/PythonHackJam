import io
from unittest import TestCase
from Quaificatin2009.Watersheds import WaterSheds
import utilities
class TestWaterSheds(TestCase):

    def run_cases(self, input_file_pointer : open,result_file_pointer : open):
        number_of_cases = int(input_file_pointer.readline())
        for i in range(0,number_of_cases):
            height,width = utilities.return_int_list(input_file_pointer.readline())
            water_sheds = WaterSheds(height,width,input_file_pointer)
            expected_result = result_file_pointer.readline()
            for j in range(height):
                 expected_result += result_file_pointer.readline()
            if i==69:
                a=1
            actual_result = 'Case #%s:%s'%(i+1, water_sheds.get_result())

            self.assertEquals(expected_result,actual_result)
    def testBasicInput(self):
        expected_result = io.StringIO('''Case #1:
a b b
a a b
a a a
Case #2:
a a a a a a a a a b
Case #3:
a a a
b b b
Case #4:
a a a a a
a a b b a
a b b b a
a b b b a
a a a a a
Case #5:
a b c d e f g h i j k l m
n o p q r s t u v w x y z
''')
        file = io.StringIO('''5
3 3
9 6 3
5 9 6
3 5 9
1 10
0 1 2 3 4 5 6 7 8 7
2 3
7 6 7
7 6 7
5 5
1 2 3 4 5
2 9 3 9 6
3 3 0 8 7
4 9 8 9 8
5 6 7 8 9
2 13
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
    ''')
        self.run_cases(file,expected_result)
