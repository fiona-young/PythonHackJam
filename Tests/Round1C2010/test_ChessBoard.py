import io
import random
from unittest import TestCase
from Round1C2010.ChessBoard import ChessBoard
class TestChessBoard(TestCase):

    def run_cases(self, input_file_pointer : open,result_file_pointer : open):
        number_of_cases = int(input_file_pointer.readline())
        for i in range(0,number_of_cases):
            welcome_to_code_jam = ChessBoard(input_file_pointer)
            case = 'Case #%s:'%(i+1)
            expected_result = result_file_pointer.readline()
            boards=int(expected_result.strip().rsplit(':',1)[1])
            for i in range(boards):
                expected_result += result_file_pointer.readline()
            actual_result = '%s\n'%( welcome_to_code_jam.get_result(case))

            self.assertEquals(expected_result,actual_result)
    def testHexInput(self):
        expected_result = io.StringIO('''Case #1: 2
2 7
1 36
''')
        file = io.StringIO('''1
16 4
0
1
2
3
4
5
6
7
8
9
A
B
C
D
E
F
''')
        self.run_cases(file,expected_result)

    def testBasicInput(self):
        expected_result = io.StringIO('''Case #1: 2
2 1
1 12
''')
        file = io.StringIO('''1
4 4
3
3
C
C''')
        self.run_cases(file,expected_result)

    def testBasicLongerInput(self):
        expected_result = io.StringIO('''Case #1: 5
6 2
4 3
3 7
2 15
1 57
Case #2: 1
1 16
Case #3: 2
2 1
1 12
Case #4: 1
2 4
''')
        file = io.StringIO('''4
15 20
55555
FFAAA
2AAD5
D552A
2AAD5
D542A
4AD4D
B52B2
52AAD
AD552
AA52D
AAAAA
5AA55
A55AA
5AA55
4 4
0
0
0
0
4 4
3
3
C
C
4 4
6
9
9
6
''')
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

