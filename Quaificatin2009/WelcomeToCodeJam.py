import os
import collections
import utilities
import copy
import io
import sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
class NoMoreCodeJams (Exception):
    pass
class MapInfo:
    def __init__(self,match_index,char,index_start,matches):
        self.match_index = match_index
        self.char = char
        self.index_start = index_start
        self.matches = matches

    def __str__(self):
        return 'char %s index %s matches %s'%(self.char,self.index_start,self.matches)

class DictSearch:
    def __init__(self,match,search_str):
        self.dict = {}
        self.match = match
        self.match_set = set(match)
        self.routes={}
        for i in range(len(match)):
            self.routes[i]={}
        for char in self.match_set:
            self.dict[char]=CharSearch(char)
        for i, char in enumerate(search_str):
            if char in self.match_set:
                self.dict[char].append(i)

    def __getitem__(self, item):
        return self.dict[item]

    def match_index(self,index):
        if index<len(self.match):
            return self.match[index]
        return None

    def add_route(self,index_match, start_index, final_count):
        self.routes[index_match][ start_index]=final_count


    def get_count(self,id = 'id0', index_match = 0, start_index = 0, running_count = 1):
        count = 0
        split_id = 0
        first_char = self.match_index(index_match)
        while index_match < len(self.match)-1:
            print('start first_char %s count %s start_index %s running_count %s %s'%(first_char,count,start_index,running_count,id))
            second_char = self.match_index(index_match+1)
            second_next_index = self.dict[second_char].next_index(start_index)
            if second_next_index is None:
                print('return %s %s'%(count,id))
                return count
            first_char_after_split = self.dict[first_char].next_index(second_next_index)
            first_matches_before_split = self.dict[first_char].count_characters(start_index,second_next_index)
            if first_matches_before_split is None:
                print('return %s %s'%(count,id))
                return count
            if first_char_after_split is not None:
                count += self.get_count('%s-%s'%(id,split_id),index_match+1,second_next_index,running_count*first_matches_before_split)
                print('returning first_char %s count %s start_index %s running_count %s %s'%(first_char,count,start_index,running_count,id))
                split_id+=1
                start_index = first_char_after_split
            else:
                print('adding first_char %s count %s start_index %s running_count %s %s'%(first_char,count,start_index,running_count,id))
                index_match += 1
                first_char = second_char
                start_index = second_next_index
                running_count *= first_matches_before_split
        print('return first_char %s count %s start_index %s running_count %s %s'%(first_char,count,start_index,running_count,id))
        running_count *= self.dict[first_char].count_characters(start_index)
        return count+running_count

    def get_count_old(self,id = 'id0', index_match = 0, start_index = 0, running_count = 1):
        count = 0
        split_id = 0
        first_char = self.match_index(index_match)
        while index_match < len(self.match)-1:
            second_char = self.match_index(index_match+1)
            second_next_index = self.dict[second_char].next_index(start_index)
            if second_next_index is None:
                print('return %s %s'%(count,id))
                return count
            first_char_after_split = self.dict[first_char].next_index(second_next_index)
            first_matches_before_split = self.dict[first_char].count_characters(start_index,second_next_index)
            if first_matches_before_split is None:
                print('return %s %s'%(count,id))
                return count
            if first_char_after_split is not None:
                count += self.get_count('%s-%s'%(id,split_id),index_match+1,second_next_index,running_count*first_matches_before_split)
                split_id+=1
                start_index = first_char_after_split
            else:
                index_match += 1
                first_char = second_char
                start_index = second_next_index
                running_count *= first_matches_before_split
        print('first_char %s count %s start_index %s running_count %s %s'%(first_char,count,start_index,running_count,id))
        running_count *= self.dict[first_char].count_characters(start_index)
        return count+running_count

class CharSearch:
    def __init__(self,char):
        self.list = []
        self.dict ={}
        self.char = char

    def append(self,index):
        self.dict[index]=len(self.list)
        self.list.append(index)

    def start_index(self):
        if len(self.list) == 0:
            return None
        return self.list[0]

    def count_characters(self,start_index,end_index=None):
        count = 0
        if start_index not in self.dict:
            return count
        if end_index is None:
            return len(self.list[self.dict[start_index]:])
        for index_val in self.list[self.dict[start_index]:]:
            if index_val > end_index:
                break
            count +=1
        return count


    def next_index(self,current_index):
        if current_index in self.dict:
            list_next = self.dict[current_index]+1
            if list_next < len(self.list):
                return self.list[list_next]
            else:
                return None
        for i in self.list:
            if i >= current_index:
                return i
        else:
            return None




class WelcomeToCodeJam:
    def __init__(self, text_line, match = 'welcome to code jam'):
        self.text_line = text_line.strip()
        self.match = match
        self.discard_unwanted()
        #self.match_dict = DictSearch(set(match),match)
        self.search_dict = DictSearch(match,self.text_line)
        #self.list_help = []
        #for i in match:
        #    self.list_help.append([i,-1])

    def discard_unwanted(self):
        i_start = self.text_line.find(self.match[0])
        i_end = self.text_line.rfind(self.match[-1])
        self.text_line = self.text_line[i_start:i_end+1]
       # i_start=0
    #    self.text_line = ''
       # for i in search_string:
        #    if i in self.match_dict:
         #       self.text_line += i
          #      self.search_dict[i][i_start]=i_start
           #     i_start +=1


    def get_next_char(self,current_index):
        next_index = current_index+1
        return None if next_index == len(self.match) else self.match[next_index]

    def get_iterate(self,match_count,match_index = 0, info_str = '' ,string_index=0):
        char_now_search=self.match[match_index]
        char_next_search=self.get_next_char(match_index)
        now_found = False
        count_sum = 0
        info_str +='%s:'%char_now_search
        while string_index < len(self.text_line):
            string_char = self.text_line[string_index]
            if string_char == char_now_search:
                info_str += '%s,'%string_index
                now_found = True
                match_count[match_index]+=1
            elif now_found and (char_next_search is not None) and (string_char==char_next_search):
                count_sum += self.get_iterate(match_count.copy(),match_index+1,'%s # '%info_str,string_index)
                match_count[match_index]=0
                info_str = info_str[0:info_str.rfind(':')+1]
                now_found = False
            string_index +=1
        if min(match_count)==0:
            count = 0
        else:
            count =1
            for num in match_count:
                count*=num
        count_sum +=count
        if match_index == (len(match_count)-1):
            info_str +='\t\t{%s}'%count
            print(info_str)
        return count_sum

    def get_iterate_list(self,running_count=1,match_index = 0, info_str = '' ,string_index=0):
        char_now_search=self.match[match_index]
        char_next_search=self.get_next_char(match_index)
        now_found = False
        count_sum = 0
        this_count = 0
        info_str +='%s:'%char_now_search
        #while match_index < len(self.match):
        for now_index in self.search_dict[char_now_search].list:
            this_count +=1
            branch_index = self.search_dict.next_branch_index(now_index,char_now_search,char_next_search)
            if branch_index is not None:
                count_sum += self.get_iterate_list(running_count*this_count,match_index+1,'%s # '%info_str,string_index)
                this_count=0
                info_str = info_str[0:info_str.rfind(':')+1]

        string_char = self.text_line[string_index]
        if string_char == char_now_search:
            info_str += '%s,'%string_index
            now_found = True
            this_count+=1
        elif now_found and (char_next_search is not None) and (string_char==char_next_search):
            count_sum += self.get_iterate(running_count*this_count,match_index+1,'%s # '%info_str,string_index)
            this_count=0
            info_str = info_str[0:info_str.rfind(':')+1]
            now_found = False
        string_index +=1

        if match_index == (len(self.match)-1):
            count = running_count*this_count
            info_str +='\t\t{%s}'%count
            print(info_str)
            count_sum +=count
        return count_sum


    def get_result(self,case_str=''):
        print('\n%s ext line: '%case_str,self.text_line)
        print('%s search: '%case_str,self.match)
        #count = self.search_dict.get_count(case_str)
        match_count = [0]*len(self.match)
        count = self.get_iterate(match_count,0,case_str)
        str_count = '0'*4+str(count)
        return str_count[-4:]


def write_output_file(large=False):
    text = "large" if large else 'small'
    file_name = os.path.join(__location__, 'Data/C-%s-practice.' % text)
    file_read, file_write, file_dump = utilities.get_file(file_name)
    number_of_cases = int(file_read.readline())
    #sys.stdout = file_dump
    for i in range(0, number_of_cases):
        file_line = file_read.readline()
        case_str = 'Case #%s: ' % (i + 1)
        welcome_to_code_jam = WelcomeToCodeJam(file_line)
        out_str = '%s%s\n' % (case_str, welcome_to_code_jam.get_result(case_str))
        file_write.write(out_str)
        print(out_str)
    file_read.close()
    file_write.close()
    file_dump.close()

if __file__ == sys.argv[0]:
    write_output_file(False)
