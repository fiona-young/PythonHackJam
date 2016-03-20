def return_int_list(str_in):
    return [int(x) for x in str_in.split()]

def get_file(file_name):
    input_file = open(file_name + 'in')
    output_file = open(file_name + 'out', 'w')
    dump_file = open(file_name + 'txt', 'w')
    return input_file, output_file, dump_file
