import io
from unittest import TestCase
from Quaificatin2009.AlienLanguage import AlienLanguage
import utilities
class TestAlienLanguage(TestCase):

    def run_cases(self, input_file_pointer : open,result_file_pointer : open):
        word_length,words_in_language,number_of_cases = utilities.return_int_list(input_file_pointer.readline())
        alien_language = AlienLanguage(word_length,words_in_language,input_file_pointer)
        for i in range(0,number_of_cases):
            expected_result = result_file_pointer.readline()
            word_pattern = input_file_pointer.readline()
            if i==69:
                a=1
            actual_result = 'Case #%s: %s\n'%(i+1, alien_language.get_result(word_pattern))

            self.assertEquals(expected_result,actual_result)
    def testBasicInput(self):
        expected_result = io.StringIO('''Case #1: 2
Case #2: 1
Case #3: 3
Case #4: 0

''')
        file = io.StringIO('''3 5 4
abc
bca
dac
dbc
cba
(ab)(bc)(ca)
abc
(abc)(abc)(abc)
(zyx)bc
    ''')
        self.run_cases(file,expected_result)


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

    def testLargeNumbers(self):
        expected_result = io.StringIO('''Case #1: 935
Case #2: 027
''')
        file_input = io.StringIO('''2
5
2
    ''')
        self.run_cases(LargeNumbers.LargeNumbers,file_input,expected_result)


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



