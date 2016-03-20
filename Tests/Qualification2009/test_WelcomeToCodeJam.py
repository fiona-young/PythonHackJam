import io
from unittest import TestCase
from Quaificatin2009.WelcomeToCodeJam import WelcomeToCodeJam
import utilities
class TestWaterSheds(TestCase):

    def run_cases(self, input_file_pointer : open,result_file_pointer : open):
        number_of_cases = int(input_file_pointer.readline())
        for i in range(0,number_of_cases):
            file_line =input_file_pointer.readline()
            welcome_to_code_jam = WelcomeToCodeJam(file_line)
            expected_result = result_file_pointer.readline()
            actual_result = 'Case #%s: %s\n'%(i+1, welcome_to_code_jam.get_result())

            self.assertEquals(expected_result,actual_result)
    def testBasicInput(self):
        expected_result = io.StringIO('''Case #1: 0001
Case #2: 0256
Case #3: 0000
''')
        file = io.StringIO('''3
elcomew elcome to code jam
wweellccoommee to code qps jam
welcome to codejam''')
        self.run_cases(file,expected_result)

    def testShortInput(self):
        expected_result = '0256'
        input = 'wweellccoommee to code qps jam'
        match_string = 'welcome to code jam'
        welcome_to_code_jam = WelcomeToCodeJam(input,match_string)
        actual_result = welcome_to_code_jam.get_result()
        self.assertEquals(expected_result,actual_result)

    def testDoubleInput(self):
        expected_result = '0010'
        input = 'abcabcabc'
        match_string = 'abc'
        welcome_to_code_jam = WelcomeToCodeJam(input,match_string)
        actual_result = welcome_to_code_jam.get_result()
        self.assertEquals(expected_result,actual_result)

    def testDoubleRepeatingInput(self):
        expected_result = '0016'
        input = 'aabbaccabcaab'
        match_string = 'abc'
        welcome_to_code_jam = WelcomeToCodeJam(input,match_string)
        actual_result = welcome_to_code_jam.get_result()
        self.assertEquals(expected_result,actual_result)


    def testDoubleRepeatingInput2(self):
        expected_result = '0016'
        input = 'aabcabcbabc'
        match_string = 'abc'
        welcome_to_code_jam = WelcomeToCodeJam(input,match_string)
        actual_result = welcome_to_code_jam.get_result()
        self.assertEquals(expected_result,actual_result)

    def testDoubleRepeatingInput3(self):
        expected_result = '0016'
        input = 'aabcabcbabc'
        match_string = 'abbc'
        welcome_to_code_jam = WelcomeToCodeJam(input,match_string)
        actual_result = welcome_to_code_jam.get_result()
        self.assertEquals(expected_result,actual_result)