from unittest import TestCase
import io
import Round1A2008
import MilkShake_brute
import Milkshake_refinement1
import Milkshake_refinement2

class TestRound1A2008(TestCase):
    def run_cases(self,test_class, input_file_pointer : open,result_file_pointer : open):
        cases = int(input_file_pointer.readline())
        for i in range(0,cases):
            expected_result = result_file_pointer.readline()
            if i==69:
                a=1
            case = test_class(input_file_pointer)
            actual_result = 'Case #%s: %s\n'%(i+1, case.get_result())

            self.assertEquals(expected_result,actual_result)


    def testScalarProduct(self):
        expected_result = io.StringIO('''Case #1: -25
Case #2: 6
''')
        file = io.StringIO('''2
3
1 3 -5
-2 4 1
5
1 2 3 4 5
1 0 1 0 1
    ''')
        self.run_cases(Round1A2008.MinimumScalarProduct,file,expected_result)


    def testMilkshakesBrue(self):
        expected_result = io.StringIO('''Case #1: 1 0 0 0 0
Case #2: IMPOSSIBLE
''')
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
        self.run_cases(MilkShake_brute.Milkshakes,file_input,expected_result)

    def testMilkshakesRefinement1(self):
        expected_result = io.StringIO('''Case #1: 1 0 0 0 0
Case #2: IMPOSSIBLE
''')
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
        self.run_cases(Milkshake_refinement1.Milkshakes,file_input,expected_result)

    def testMilkshakesRefinement2(self):
        expected_result = io.StringIO('''Case #1: 1 0 0 0 0
Case #2: IMPOSSIBLE
''')
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
        self.run_cases(Milkshake_refinement2.Milkshakes,file_input,expected_result)

    def testMilkshakesSmallBrute(self):
        file_input = open('Milkshake-small.in')
        expected_output = open('Milkshake-small.out')
        self.run_cases(MilkShake_brute.Milkshakes,file_input,expected_output)

    def testMilkshakesSmallRevision1(self):
        file_input = open('Milkshake-small.in')
        expected_output = open('Milkshake-small.out')
        self.run_cases(Milkshake_refinement1.Milkshakes,file_input,expected_output)

    def testMilkshakesSmallRevision2(self):
        file_input = open('Milkshake-small.in')
        expected_output = open('Milkshake-small.out')
        self.run_cases(Milkshake_refinement2.Milkshakes,file_input,expected_output)



