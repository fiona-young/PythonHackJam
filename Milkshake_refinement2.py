import collections
class ImpossibleMilkshake(IndexError):
    pass


def return_int_list(str_in):
    return [int(x) for x in str_in.split()]


MilkshakeType = collections.namedtuple('MilkshakeType', 'flavour, malted')
class TrialFlavour:
    PLAIN, MALTED = 0, 1

    def __init__(self, trial_list):
        self._flavour = trial_list
        self._set_malted = None
        self._set_plain = None

    def __getitem__(self, item):
        return self._flavour[item]

    @property
    def flavour(self):
        return self._flavour

    @property
    def number_of_flavours(self):
        return len(self.flavour)

    def is_full(self):
        return self.unset_count == 0

    @property
    def unset_count(self):
        return self.flavour.count(None)

    @property
    def return_value(self):
        return ' '.join([str(x) for x in self.flavour])

    @property
    def set_malted(self):
        if self._set_malted is None:
            self._set_malted = {key for key, value in enumerate(self.flavour) if value == self.MALTED}
        return self._set_malted

    @property
    def set_plain(self):
        if self._set_plain is None:
            self._set_plain = {key for key, value in enumerate(self.flavour) if value == self.PLAIN}
        return self._set_plain

    def __str__(self):
        return str(self.flavour)



class Customer:
    def __init__(self, str_in, ):
        input_list = return_int_list(str_in)
        self.liked_milkshakes = input_list[0]
        self.milkshake_malted = set()
        self.milkshake_plain = set()
        for i in range(0, self.liked_milkshakes):
            flavour = input_list[(2 * i) + 1] - 1
            is_malted = input_list[2 * i + 2]
            if is_malted:
                self.milkshake_malted.add(flavour)
            else:
                self.milkshake_plain.add(flavour)

    def update_liked_set(self, liked):
        liked['malted'][self.liked_milkshakes - 1].update(self.milkshake_malted)
        liked['plain'][self.liked_milkshakes - 1].update(self.milkshake_plain)

    def update_total_likes(self, total_cutomer_likes):
        for flavour in self.milkshake_malted:
            total_cutomer_likes['malted'][flavour] += 1
        for flavour in self.milkshake_plain:
            total_cutomer_likes['plain'][flavour] += 1

    def is_acceptable(self, trial_flavour: TrialFlavour):
        return (len(self.milkshake_plain.intersection(trial_flavour.set_plain)) > 0) or (
            len(self.milkshake_malted.intersection(trial_flavour.set_malted)) > 0)

    def update_flavours(self,flavours_newly_set: set):
        self.milkshake_malted.difference_update(flavours_newly_set)
        self.milkshake_plain.difference_update(flavours_newly_set)
        self.liked_milkshakes = len(self.milkshake_plain)+ len(self.milkshake_malted)






class LikedSet:
    def __init__(self, number_of_flavours):
        self.number_of_flavours = number_of_flavours
        self.malted = [set() for i in range(self.number_of_flavours + 1)]
        self.plain = [set() for i in range(self.number_of_flavours + 1)]

    def add_customer(self, customer: Customer):
        self.malted[customer.liked_milkshakes - 1].update(customer.milkshake_malted)
        self.plain[customer.liked_milkshakes - 1].update(customer.milkshake_plain)
        self.malted_all.update(self.malted[customer.liked_milkshakes - 1])
        self.plain_all.update(self.plain[customer.liked_milkshakes - 1])

    @property
    def malted_all(self):
        return self.malted[self.number_of_flavours]

    @property
    def plain_all(self):
        return self.plain[self.number_of_flavours]

    @property
    def first_malted(self):
        for i_flavour in range(self.number_of_flavours):
            if len(self.malted):
                return i_flavour

    def not_possible(self):
        return len(self.malted[0].intersection(self.plain[0])) > 0

    def all_can_be_plain(self):
        all_can_be_plain = True
        for i_flavour in range(self.number_of_flavours):
            if (len(self.malted[i_flavour]) > i_flavour) and (len(self.plain[i_flavour]) != self.number_of_flavours):
                all_can_be_plain = False
                break
        return all_can_be_plain


class TotalCustomerLikes:
    def __init__(self, number_of_flavours):
        self.number_of_flavours = number_of_flavours
        self.malted = [0] * self.number_of_flavours
        self.plain = [0] * self.number_of_flavours

    def add_customer(self, customer: Customer):
        for flavour in customer.milkshake_malted:
            self.malted[flavour] += 1
        for flavour in customer.milkshake_plain:
            self.plain[flavour] += 1



class FinalFlavour(TrialFlavour):
    def __init__(self, number_of_flavours):
        self.previous_flavour = TrialFlavour([None]*number_of_flavours)
        super().__init__([None] * number_of_flavours)

    def update_previous_flavour(self):
        super().__init__(self._flavour.copy())
        self.previous_flavour = TrialFlavour(self._flavour.copy())

    def set_all_plain(self):
        for i_flavour, flavour in enumerate(self.flavour):
            if flavour is None:
                self.flavour[i_flavour] = self.PLAIN

    def update_from_total_customer_likes(self, total_customer_likes: TotalCustomerLikes, number_of_customers):
        if max(total_customer_likes.plain) == number_of_customers:
            self.set_all_plain()

    def update_from_liked_set(self, liked_set: LikedSet):
        if liked_set.all_can_be_plain():
            self.set_all_plain()
            return

        self.set_required_flavours(liked_set)

        self.all_remaining_plain(liked_set)

    def set_required_flavours(self, liked_set: LikedSet):
        for flavour in liked_set.malted[0]:
            self.flavour[flavour] = self.MALTED
        for flavour in liked_set.plain[0]:
            self.flavour[flavour] = self.PLAIN

    def all_remaining_plain(self, liked_set):
        remaining_plain = True

        for i_liked in range(len(liked_set.malted_all)):
            if len(liked_set.malted_all.intersection(liked_set.plain[i_liked])):
                remaining_plain = False
        if remaining_plain:
            for i_flavour in range(self.number_of_flavours):
                if self.flavour[i_flavour] is None:
                    self.flavour[i_flavour] = self.PLAIN

    @property
    def newly_set(self):
        new_flavours = set()
        for i_flavour in range(self.number_of_flavours):
            if self.flavour[i_flavour] != self.previous_flavour[i_flavour]:
                new_flavours.add(i_flavour)
        return new_flavours



    def get_trial(self):
        trial = self.flavour.copy()
        unset_flavours = [key for key, value in enumerate(self.flavour) if value is None]
        combinations = [self.PLAIN, self.MALTED]
        base = len(combinations)
        num_combinations = base ** len(unset_flavours)
        print('combinations', num_combinations, 'unset ', unset_flavours)
        for i in range(num_combinations):
            for key_change, change_value in enumerate(unset_flavours):
                set_val = (i // (base ** key_change)) % base
                trial[change_value] = combinations[set_val]
            if(num_combinations < 10) or i%100 ==0:
                print('trial %s: %s'%(i,trial))
            yield TrialFlavour(trial)

class Milkshakes:
    IMPOSSIBLE = "IMPOSSIBLE"

    def __init__(self, file_pointer: open):
        self.number_of_flavours = int(file_pointer.readline())
        self.number_of_customers = int(file_pointer.readline())
        self.customer = {}
        self.liked_set = LikedSet(self.number_of_flavours)
        self.total_customer_likes = TotalCustomerLikes(self.number_of_flavours)
        for i in range(0, self.number_of_customers):
            self.customer[i]=Customer(file_pointer.readline()[:-1])
            self.liked_set.add_customer(self.customer[i])
            self.total_customer_likes.add_customer(self.customer[i])

    def get_result(self):
        try:
            final_flavour = FinalFlavour(self.number_of_flavours)
            while True:
                result = self.iterate_result(final_flavour)
                if result is not None:
                    return result
                flavours_newly_set = final_flavour.newly_set
                if len(flavours_newly_set)==0:
                    raise ImpossibleMilkshake

                self.update_flavours(flavours_newly_set,final_flavour)
                if self.number_of_customers==0:
                    final_flavour.set_all_plain()
                    return final_flavour.return_value
        except ImpossibleMilkshake as err:
            return self.IMPOSSIBLE

    def update_flavours(self,flavours_newly_set: set,final_flavour : FinalFlavour):
        final_flavour.update_previous_flavour()
        self.liked_set = LikedSet(self.number_of_flavours)
        self.total_customer_likes = TotalCustomerLikes(self.number_of_flavours)
        for i in list(self.customer):
            if self.customer[i].is_acceptable(final_flavour):
                del self.customer[i]
                continue
            self.customer[i].update_flavours(flavours_newly_set)
            if self.customer[i].liked_milkshakes ==0:
                raise ImpossibleMilkshake
            self.liked_set.add_customer(self.customer[i])
            self.total_customer_likes.add_customer(self.customer[i])
        self.number_of_customers = len(self.customer)

    def iterate_result(self, final_flavour: FinalFlavour):
        if self.liked_set.not_possible():
            raise ImpossibleMilkshake
        final_flavour.update_from_total_customer_likes(self.total_customer_likes,self.number_of_customers)
        if final_flavour.is_full():
            return final_flavour.return_value
        final_flavour.update_from_liked_set(self.liked_set)
        if final_flavour.is_full():
            return final_flavour.return_value
        if final_flavour.unset_count < 0:
            for trial_flavour in final_flavour.get_trial():
                for i in range(0, self.number_of_customers):
                    if not self.customer[i].is_acceptable(trial_flavour):
                        break
                else:
                    return trial_flavour.return_value
            else:
                raise ImpossibleMilkshake
