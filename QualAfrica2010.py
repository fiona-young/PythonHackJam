import collections

Price = collections.namedtuple('Price', 'value, index')


class ReverseWords:
    def __init__(self, file_pointer: open):
        self.line = file_pointer.readline()[:-1]
        self.word_list = []
        self.word_count =0

    def add_word(self,word):
        self.word_list.append(word)
        self.word_count+=1


    def reverse(self):

        self.create_word_list()
        result = ''
        for i in range(0,self.word_count):
            result +=self.word_list[self.word_count-1-i]+' '
        return result[:-1]


    def create_word_list(self):
        word = ''
        for my_char in self.line:
            if my_char is not ' ':
                word+=my_char
            else:
                self.add_word(word)
                word = ''
        if word is not '':
            self.add_word(word)



class StoreCredit:
    def __init__(self, file_pointer: open):
        self.credit = int(file_pointer.readline())
        self.items = int(file_pointer.readline())
        self.prices = sorted([Price(int(x), i) for i, x in enumerate(file_pointer.readline().split(), 1)])

    def find_pair(self):
        for i, price in enumerate(self.prices):
            pair = self.search(self.credit - price[0], self.prices, i + 1, len(self.prices) - 1)
            if pair is not None:
                return (price.index, pair.index)

    def search(self, value, my_list, i_min, i_max):
        i_mid = (i_min + i_max) // 2
        if my_list[i_mid].value == value:
            return my_list[i_mid]
        if i_min == i_max:
            return None
        if value > my_list[i_mid].value:
            return self.search(value, my_list, min(i_mid + 1, i_max), i_max)
        else:
            return self.search(value, my_list, i_min, max(i_mid - 1, i_min))

CharInfo = collections.namedtuple('CharInfo', 'count, number, repeat')

class T9Spelling:
    def __init__(self, file_pointer: open):
        self.line = file_pointer.readline()[:-1]
        trans_dict=dict(zip("abcdefghijklmnopqrstuvwxyz",range(0,26)))
        self.trans_dict={}
        for char,index in trans_dict.items():
            if index < trans_dict['p']:
                self.trans_dict[char]=CharInfo(index,2+index//3,1+index%3)
            elif char in 'pqrs':
                self.trans_dict[char]=CharInfo(index,7,index +1 - trans_dict['p'])
            elif char in 'tuv':
                self.trans_dict[char]=CharInfo(index,8,index +1 - trans_dict['t'])
            else:
                self.trans_dict[char]=CharInfo(index,9,index +1 - trans_dict['w'])
        self.trans_dict[' ']=CharInfo(0,0,1)


    def get_result(self):
        result_out=''
        last_number = 'z'
        for char in self.line:
            if last_number is self.trans_dict[char].number:
                result_out+=' '
            result_out+=str(self.trans_dict[char].number)*self.trans_dict[char].repeat
            last_number = self.trans_dict[char].number
        return result_out
