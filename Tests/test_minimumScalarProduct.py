from unittest import TestCase
import io
import Round1A2008

class TestRouund1A2008(TestCase):

    def testScalarProduct(self):
        expected_result = '''Case #1: -25
Case #2: 6
'''
        file = io.StringIO('''2
3
1 3 -5
-2 4 1
5
1 2 3 4 5
1 0 1 0 1
    ''')
        cases = int(file.readline())
        out_str= ''
        for i in range(0,cases):
            case = Round1A2008.MinimumScalarProduct(file)
            result = case.get_result()
            out_str += 'Case #%s: %s\n'%(i+1,result)
        self.assertEquals(expected_result,out_str)


    def testMilkshakes(self):
        expected_result = '''Case #1: 1 0 0 0 0
Case #2: IMPOSSIBLE
'''
        file_input = io.StringIO('''2
5
3
1 1 1
2 1 0 2 0
1 5 0
1
2
1 1 0
1 1 1
    ''')
        cases = int(file_input.readline())
        out_str= ''
        for i in range(0,cases):
            case = Round1A2008.Milkshakes(file_input)
            result = case.get_result()
            out_str += 'Case #%s: %s\n'%(i+1,result)
        self.assertEquals(expected_result,out_str)
