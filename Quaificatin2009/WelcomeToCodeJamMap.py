import os
import collections
import utilities
import copy
import io
import sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MatchMap:
    def __init__(self,char,match_index,search_list):
        self.char = char
        self.match_index = match_index
        self.search_list = search_list
        self.weight_list = collections.defaultdict(int)
        self._cached_weight = {}

    def get_weight_from_index(self, index):
        if index not in self._cached_weight:
            weight = 0
            for search_index in self.search_list:
                if index < search_index:
                    weight += self.weight_list[search_index]
            self._cached_weight[index]=weight
            #print('set: char %s match index %s cached index %s weight %s'%(self.char,self.match_index,index,self._cached_weight))
       # else:
            #print('cached: char %s match index %s cached index %s weight %s'%(self.char,self.match_index,index,self._cached_weight))
        return self._cached_weight[index]


    def build_map(self, last_map = None):
        for search_index in self.search_list:
            if last_map is None:
                self.weight_list[search_index]=1
            else:
                self.weight_list[search_index]=last_map.get_weight_from_index(search_index)

    def sum_weight(self):
        weight = 0
        for weight_values in self.weight_list.values():
            weight += weight_values
        return weight



class WelcomeToCodeJamMap:
    def __init__(self, text_line, match = 'welcome to code jam'):
        self.text_line = text_line.strip()
        self.match = match
        self.discard_unwanted()

        self.search_dict = collections.defaultdict(list)
        for search_index,char in enumerate(self.text_line):
            self.search_dict[char].append(search_index)
        self.match_list = []
        for match_index in range(len(self.match)-1,-1,-1):
            char = self.match[match_index]
            self.match_list.append(MatchMap(char,match_index,self.search_dict[char]))

    def build_map(self):
        last_build_map = None
        for match_map in self.match_list:
            match_map.build_map(last_build_map)
            last_build_map = match_map
        return self.match_list[len(self.match_list)-1].sum_weight()

    def get_result(self,case_str=''):
        print('\n%s ext line: '%case_str,self.text_line)
        print('%s search: '%case_str,self.match)
        count = self.build_map()
        str_count = '0'*4+str(count)
        last_4_letters = str_count[-4:]
        print(count,'\n',last_4_letters)
        return last_4_letters


    def discard_unwanted(self):
        i_start = self.text_line.find(self.match[0])
        i_end = self.text_line.rfind(self.match[-1])
        search_string = self.text_line[i_start:i_end+1]
        i_start=0
        self.text_line = ''
        match_set = set(self.match)
        for i in search_string:
            if i in match_set:
                self.text_line += i
                i_start +=1



def write_output_file(large=False):
    text = "large" if large else 'small'
    file_name = os.path.join(__location__, 'Data/C-%s-practice.' % text)
    file_read, file_write, file_dump = utilities.get_file(file_name)
    number_of_cases = int(file_read.readline())
    #sys.stdout = file_dump
    for i in range(0, number_of_cases):
        file_line = file_read.readline()
        case_str = 'Case #%s: ' % (i + 1)
        welcome_to_code_jam = WelcomeToCodeJamMap(file_line)
        out_str = '%s%s\n' % (case_str, welcome_to_code_jam.get_result(case_str))
        file_write.write(out_str)
        print(out_str)
    file_read.close()
    file_write.close()
    file_dump.close()

if __file__ == sys.argv[0]:
    write_output_file(True)
