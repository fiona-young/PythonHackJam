import random
import collections


def swap_list_items(my_list, i_one, i_two):
    temp = my_list[i_one]
    my_list[i_one] = my_list[i_two]
    my_list[i_two] = temp


def quick_sort(my_list, i_min, i_max, reverse=False):
    if (i_max - i_min) == 0:
        return
    swap_list_items(my_list, i_min, random.randint(i_min, i_max))
    partition = i_min
    for i in range(i_min + 1, i_max + 1):
        if reverse:
            partition = quick_sort_reverse(my_list, i, i_min, partition)
        else:
            partition = quick_sort_normal(my_list, i, i_min, partition)
    swap_list_items(my_list, partition, i_min)
    if partition > i_min:
        quick_sort(my_list, i_min, max(i_min, partition - 1), reverse)
    if partition < i_max:
        quick_sort(my_list, min(i_max, partition + 1), i_max, reverse)


def quick_sort_normal(my_list, i, i_min, partition):
    if my_list[i] < my_list[i_min]:
        partition += 1
        swap_list_items(my_list, partition, i)
    return partition


def quick_sort_reverse(my_list, i, i_min, partition):
    if my_list[i] > my_list[i_min]:
        partition += 1
        swap_list_items(my_list, partition, i)
    return partition


class MinimumScalarProduct:
    dict_list_possibilities = {}

    def __init__(self, file_pointer: open):
        self.count = int(file_pointer.readline())
        self.index1 = return_int_list(file_pointer.readline())
        self.index2 = return_int_list(file_pointer.readline())

    def get_result(self):
        quick_sort(self.index1, 0, self.count - 1)
        quick_sort(self.index2, 0, self.count - 1, True)
        current_sum = self.scalar_product(self.index1, self.index2)
        return current_sum

    def get_result_brute(self):
        current_sum = self.scalar_product(self.index1, self.index2)
        if self.count not in self.dict_list_possibilities:
            list_out = []
            list_section = []
            self.get_list_possibilities(list(range(0, self.count)), list_out, list_section)
            self.dict_list_possibilities[self.count] = list_out
        for vector in self.dict_list_possibilities[self.count]:
            current_sum = min(current_sum, self.scalar_product([self.index1[x] for x in vector], self.index2))
        return current_sum

    def get_list_possibilities(self, list_in, list_out, list_section):
        for i in range(0, len(list_in)):
            if len(list_in) == 1:
                list_out.append(list_section + list_in.copy())
                return
            self.get_list_possibilities(list_in[0:i] + list_in[i + 1:], list_out, list_section.copy() + [list_in[i]])

    def scalar_product(self, vector1, vector2):
        my_sum = 0
        for i in range(0, len(vector1)):
            my_sum += vector1[i] * vector2[i]
        return my_sum


def return_int_list(str_in):
    return [int(x) for x in str_in.split()]


MilkshakeType = collections.namedtuple('MilkshakeType', 'flavour, malted')


class Customer:
    def __init__(self, str_in, truth_table):
        input_list = return_int_list(str_in)
        self.liked_milkshakes = input_list[0]
        self.milkshake_both = {}
        self.milkshake_malted = None
        self.milkshake_plain = set()
        for i in range(0, self.liked_milkshakes):
            flavour = input_list[(2 * i) + 1] - 1
            is_malted = input_list[2 * i + 2]
            if is_malted:
                self.milkshake_malted = flavour
            else:
                self.milkshake_plain.add(flavour)
            self.milkshake_both[flavour] = is_malted

            truth_table[flavour] = is_malted

    def acceptable_result(self, attempted_flavour):
        for flavour, type in self.milkshake_both.items():
            if attempted_flavour[flavour] == type:
                return True
        return False

    def update_liked(self,liked):
        liked_milkshakes = self.liked_milkshakes
        if self.milkshake_malted is not None:
            liked['malted'][self.liked_milkshakes-1].add(self.milkshake_malted)
            liked_milkshakes -= 1
        if liked_milkshakes > 0:
            liked['plain'][self.liked_milkshakes-1].update(self.milkshake_plain)


class Milkshakes:
    IMPOSSIBLE = "IMPOSSIBLE"

    def __init__(self, file_pointer: open):
        self.number_of_flavours = int(file_pointer.readline())
        self.number_of_customers = int(file_pointer.readline())
        self.truth_table = [[None for i in range(0, self.number_of_flavours)].copy() for j in
                            range(0, self.number_of_customers)]
        self.customer = []
        for i in range(0, self.number_of_customers):
            self.customer.append(Customer(file_pointer.readline()[:-1], self.truth_table[i]))

    def get_result_brute(self):
        my_array = [{0} for i in range(0, self.number_of_flavours)]
        for i_flavour in range(0, self.number_of_flavours):
            for i_customer in range(0, self.number_of_customers):
                type = self.truth_table[i_customer][i_flavour]
                if type == 1:
                    my_array[i_flavour].add(type)

        option_arrays = [[] for i in range(0, self.number_of_flavours + 1)]
        get_list_options(my_array, option_arrays)
        sorted_option_array = []
        for options_by_malted in option_arrays:
            for each_option_array in options_by_malted:
                sorted_option_array.append(each_option_array)
        acceptable_result = self.get_acceptable_results(sorted_option_array)
        if acceptable_result is None:
            return self.IMPOSSIBLE
        else:
            return ' '.join([str(x) for x in acceptable_result])

    def get_result_revision1(self):
        liked = {'malted': None, 'plain': None}
        liked['malted'] = [set() for i in [0] * (self.number_of_flavours+1)]
        liked['plain'] = [set() for i in [0] * (self.number_of_flavours+1)]
        for i_customer in range(0, self.number_of_customers):
            self.customer[i_customer].update_liked(liked)

        if len(liked['malted'][0].intersection(liked['plain'][0])) > 0:
            return self.IMPOSSIBLE
        first_try = [None]* self.number_of_flavours
        for i_flavour in range(0, self.number_of_flavours):
            liked['malted'][self.number_of_flavours].update(liked['malted'][i_flavour])
            liked['plain'][self.number_of_flavours].update(liked['plain'][i_flavour])
            if i_flavour in liked['malted'][0]:
                first_try[i_flavour]=1
            elif i_flavour in liked['plain'][0]:
                first_try[i_flavour]=0
        if len([1 for i in first_try if i is not None])==self.number_of_flavours:
            return ' '.join([str(x) for x in first_try])
        if len(liked['malted'][self.number_of_flavours].intersection(liked['plain'][self.number_of_flavours])) == 0:
            for i_flavour in range(0, self.number_of_flavours):
                first_try[i_flavour]=0
                if i_flavour in liked['malted'][ self.number_of_flavours]:
                    first_try[i_flavour]=1
            return ' '.join([str(x) for x in first_try])

        my_array = [{0} for i in range(0, self.number_of_flavours)]
        for i_flavour in range(0, self.number_of_flavours):
            for i_customer in range(0, self.number_of_customers):
                type = self.truth_table[i_customer][i_flavour]
                if type == 1:
                    my_array[i_flavour].add(type)

        option_arrays = [[] for i in range(0, self.number_of_flavours + 1)]
        get_list_options(my_array, option_arrays)
        sorted_option_array = []
        for options_by_malted in option_arrays:
            for each_option_array in options_by_malted:
                sorted_option_array.append(each_option_array)
        acceptable_result = self.get_acceptable_results(sorted_option_array)
        if acceptable_result is None:
            return self.IMPOSSIBLE
        else:
            return ' '.join([str(x) for x in acceptable_result])

    def get_acceptable_results(self, option_arrays):
        acceptable_result = None
        malt_count = self.number_of_flavours + 1
        for attempt in option_arrays:

            current_malt_count = len([x for x in attempt if x == 1])
            if current_malt_count >= malt_count:
                continue
            for o_customer in self.customer:
                if not o_customer.acceptable_result(attempt):
                    break
            else:
                malt_count = current_malt_count
                acceptable_result = attempt
        return acceptable_result


def get_list_options(my_array, result, i_min=0, progress=None):
    if progress is None:
        progress = []
    if my_array[i_min] is None:
        my_array[i_min] = {0}
    for options in my_array[i_min]:
        if i_min == len(my_array) - 1:
            final_array = progress + [options]
            current_malt_count = len([x for x in final_array if x == 1])
            result[current_malt_count].append(final_array)
        else:
            get_list_options(my_array, result, i_min + 1, progress[:] + [options])
    a = 1
