import io
import random
from unittest import TestCase
from Round1C2010.RopeIntranet import RopeIntranet
class TestRopeIntranet(TestCase):

    def run_cases(self, input_file_pointer : open,result_file_pointer : open):
        number_of_cases = int(input_file_pointer.readline())
        for i in range(0,number_of_cases):
            welcome_to_code_jam = RopeIntranet(input_file_pointer)
            case = 'Case #%s:'%(i+1)
            expected_result = result_file_pointer.readline()
            actual_result = '%s\n'%( welcome_to_code_jam.get_result(case))

            self.assertEquals(expected_result,actual_result)
    def testBasicInput(self):
        expected_result = io.StringIO('''Case #1: 2
Case #2: 0
''')
        file = io.StringIO('''2
3
1 10
5 5
7 7
2
1 1
2 2''')
        self.run_cases(file,expected_result)

    def testBasicLongerInput(self):
        expected_result = io.StringIO('''Case #1: 14
Case #2: 0
''')
        file = io.StringIO('''1
7
1 6
2 7
3 1
4 3
5 5
6 4
7 2''')
        self.run_cases(file,expected_result)

    def testBasicLongerInput2(self):
        num = 993
        a = list(range(num))
        b = list(range(num))
        random.shuffle(a)
        random.shuffle(b)
        string = '1\n%s\n'%num
        for i in range(num):
            string += '%s %s\n'%(a[i],b[i])
        print(string)
        expected_result = io.StringIO('Case #1: 14')
        file = io.StringIO(string)
        self.run_cases(file,expected_result)

