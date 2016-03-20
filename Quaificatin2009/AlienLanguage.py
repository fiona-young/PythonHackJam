import os
import collections
import utilities

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_file(large=False):
    text = "large" if large else 'small'
    file_name = os.path.join(__location__, 'A-%s-practice.' % text)
    input_file = open(file_name + 'in')
    output_file = open(file_name + 'out', 'w')
    return input_file, output_file


class AlienWord:
    def __init__(self, word):
        self.word = word

    @property
    def first_letter(self):
        return self.word[0]

    def matches_pattern(self, word_pattern_list):
        for i in range(1, len(self.word)):
            if self.word[i] not in word_pattern_list[i]:
                return False
        return True


class AlienLanguage:
    def __init__(self, word_length, words_in_language, file_pointer: open):
        self.word_length = word_length
        self.dictionary_length = words_in_language
        self.dictionary_list = []
        self.first_letter_lookup = collections.defaultdict(list)
        self.load_dictionary(file_pointer)

    def get_result(self, word_pattern):
        word_pattern_list = self.load_word_pattern(word_pattern)
        count = self.get_matching_words(word_pattern_list)
        return str(count)

    def get_matching_words(self, word_pattern_list):
        count = 0
        for first_letter in word_pattern_list[0]:
            for i in self.first_letter_lookup[first_letter]:
                if self.dictionary_list[i].matches_pattern(word_pattern_list):
                    count += 1
        return count

    def load_word_pattern(self, word_pattern):
        word_pattern_list = []
        i_pointer_start = 0
        for i in range(self.word_length):
            char = word_pattern[i_pointer_start]
            if char != '(':
                word_pattern_list.append(set(char))
            else:
                i_pointer_start += 1
                i_pointer_end = i_pointer_start
                while word_pattern[i_pointer_end] != ')':
                    i_pointer_end += 1
                word_pattern_list.append(set(word_pattern[i_pointer_start:i_pointer_end]))
                i_pointer_start = i_pointer_end
            i_pointer_start += 1
        return word_pattern_list

    def load_dictionary(self, file_pointer: open):
        for i in range(self.dictionary_length):
            word = file_pointer.readline()
            self.dictionary_list.append(AlienWord(word[0:self.word_length]))
            first_letter = self.dictionary_list[i].first_letter
            self.first_letter_lookup[first_letter].append(i)


def write_output_file(large=False):
    file_read, file_write = get_file(large)
    word_length, words_in_language, number_of_cases = utilities.return_int_list(file_read.readline())
    alien_language = AlienLanguage(word_length, words_in_language, file_read)
    for i in range(0, number_of_cases):
        word_pattern = file_read.readline()
        out_str = 'Case #%s: %s' % (i + 1, alien_language.get_result(word_pattern))
        file_write.write(out_str+'\n')
        print(out_str)
    file_read.close()
    file_write.close()


write_output_file(True)
