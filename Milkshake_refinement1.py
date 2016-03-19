import collections


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
                truth_table['malted'].add(flavour)
            else:
                self.milkshake_plain.add(flavour)
            self.milkshake_both[flavour] = is_malted

            truth_table['plain'].update(self.milkshake_plain)


    def acceptable_result(self, attempted_flavour):
        for flavour, type in self.milkshake_both.items():
            if attempted_flavour[flavour] == type:
                return True
        return False

    def update_liked_set(self, liked):
        liked_milkshakes = self.liked_milkshakes
        if self.milkshake_malted is not None:
            liked['malted'][self.liked_milkshakes - 1].add(self.milkshake_malted)
            liked_milkshakes -= 1
        if liked_milkshakes > 0:
            liked['plain'][self.liked_milkshakes - 1].update(self.milkshake_plain)

    def update_total_likes(self,total_cutomer_likes):
        if self.milkshake_malted is not None:
            total_cutomer_likes['malted'][self.milkshake_malted]+=1
        for flavour in self.milkshake_plain:
            total_cutomer_likes['plain'][flavour]+=1

class Milkshakes:
    IMPOSSIBLE = "IMPOSSIBLE"

    def __init__(self, file_pointer: open):
        self.number_of_flavours = int(file_pointer.readline())
        self.number_of_customers = int(file_pointer.readline())
        self.truth_table = [{'malted':set(),'plain':set()} for j in
                            range(0, self.number_of_customers)]

        self.customer = []
        for i in range(0, self.number_of_customers):
            self.customer.append(Customer(file_pointer.readline()[:-1], self.truth_table[i]))

    def get_likes(self):
        total_customer_likes = {'malted': [0] * self.number_of_flavours ,
                               'plain':  [0] * self.number_of_flavours }
        liked_set = {'malted': [set() for i in range(0,self.number_of_flavours + 1)],
                          'plain': [set() for i in range(0,self.number_of_flavours + 1)]}
        for i_customer in range(0, self.number_of_customers):
            self.customer[i_customer].update_liked_set(liked_set)
            self.customer[i_customer].update_total_likes(total_customer_likes)
        for i_flavour in range(0, self.number_of_flavours):
            liked_set['malted'][self.number_of_flavours].update(liked_set['malted'][i_flavour])
            liked_set['plain'][self.number_of_flavours].update(liked_set['plain'][i_flavour])
        return (total_customer_likes,liked_set)

    def get_required_flavours(self, liked_set):
        required_flavours = [None] * self.number_of_flavours
        for i_flavour in range(0, self.number_of_flavours):
            if i_flavour in liked_set['malted'][0]:
                required_flavours[i_flavour] = 1
            elif i_flavour in liked_set['plain'][0]:
                required_flavours[i_flavour] = 0
        return required_flavours

    def is_selected_flavours_full(self,selected_flavours):
         return len([1 for i in selected_flavours if i is None]) == 0

    def get_flavour_as_string(self, selected_flavours):
        return ' '.join([str(x) for x in selected_flavours])

    def fill_flavour(self,selected_flavours, value = 0):
        for i_flavour in range(0, self.number_of_flavours):
            if selected_flavours[i_flavour] is None:
                selected_flavours[i_flavour] = value

    def get_result(self):
        total_customer_likes,liked_set = self.get_likes()
        if max(total_customer_likes['plain']) == self.number_of_customers:
            return self.get_flavour_as_string([0]*self.number_of_flavours)
        if len(liked_set['malted'][0].intersection(liked_set['plain'][0])) > 0:
            return self.IMPOSSIBLE

        selected_flavours = self.get_required_flavours(liked_set)
        if self.is_selected_flavours_full(selected_flavours):
            return self.get_flavour_as_string(selected_flavours)
        if len(liked_set['malted'][self.number_of_flavours].intersection(liked_set['plain'][self.number_of_flavours])) == 0:
            for i_flavour in range(0, self.number_of_flavours):
                if selected_flavours[i_flavour] is None:
                    if total_customer_likes['malted'][i_flavour] == 0:
                        selected_flavours[i_flavour] = 0
                    else:
                        raise UnboundLocalError
        if self.is_selected_flavours_full(selected_flavours):
            return self.get_flavour_as_string(selected_flavours)
        if len([1 for x in liked_set['malted'][0:self.number_of_flavours-1] if x!=set()]) == 0:
            for i_flavour in range(0, self.number_of_flavours):
                 if selected_flavours[i_flavour] is None:
                    selected_flavours[i_flavour] =0
            return self.get_flavour_as_string(selected_flavours)
        undefined_flavours = {key for key,value in enumerate(selected_flavours) if value == None}
        unhappy_customers = set()
        for i_customer in range(0, self.number_of_customers):
            if not self.customer[i_customer].acceptable_result(selected_flavours):
                unhappy_customers.add(i_customer)
        if len(unhappy_customers) == 0:
            for i_flavour in undefined_flavours.copy():
                selected_flavours[i_flavour] = 0
                undefined_flavours.discard(i_flavour)
        if self.is_selected_flavours_full(selected_flavours):
            return self.get_flavour_as_string(selected_flavours)
        if len(unhappy_customers) == 1:
            for i_customer in unhappy_customers:
                if len(undefined_flavours.intersection(self.customer[i_customer].milkshake_plain)) > 0:
                    for i_flavour in undefined_flavours:
                        selected_flavours[i_flavour] = 0
                if self.customer[i_customer].milkshake_malted in undefined_flavours:
                    selected_flavours[self.customer[i_customer].milkshake_malted] = 1
                    for i_flavour in undefined_flavours.difference({self.customer[i_customer].milkshake_malted}):
                         selected_flavours[i_flavour] = 0
        if self.is_selected_flavours_full(selected_flavours):
            return self.get_flavour_as_string(selected_flavours)

        if len(undefined_flavours) == 1:
            for i_flavour in undefined_flavours:
                for trial in [0,1]:
                    attempt = selected_flavours.copy()
                    attempt[i_flavour]=trial
                    happy = True
                    for i_customer in unhappy_customers:
                         happy = happy and self.customer[i_customer].acceptable_result(attempt)
                    if happy:
                        return self.get_flavour_as_string(attempt)



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
