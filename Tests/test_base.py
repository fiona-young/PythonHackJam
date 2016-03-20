from unittest import TestCase

class TestBase(TestCase):
    def run_cases(self,test_class, input_file_pointer : open,result_file_pointer : open):
        cases = int(input_file_pointer.readline())
        for i in range(0,cases):
            expected_result = result_file_pointer.readline()
            if i==69:
                a=1
            case = test_class(input_file_pointer)
            actual_result = 'Case #%s: %s\n'%(i+1, case.get_result())

            self.assertEquals(expected_result,actual_result)




