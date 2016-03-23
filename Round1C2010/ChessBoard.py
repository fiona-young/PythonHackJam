import utilities

QUAD = 4


class ReloadBoard(Exception):
    pass


class Cell:
    def __init__(self, is_white):
        self.is_white = is_white
        self.down = None
        self.right = None
        self.running_down = None
        self.board_size = None

    def different_colours(self, new_cell):
        return self.is_white + new_cell.is_white == 1

    def right_value(self, new_cell):
        if self.different_colours(new_cell):
            return self.right + 1
        else:
            return 1

    def down_value(self, new_cell):
        if self.different_colours(new_cell):
            return self.down + 1
        else:
            return 1

    @property
    def colour(self):
        return 'X' if self.is_white else '.'


class Board:
    trans = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = {}
        self.board = []
        self.size_list = []
        self.list_results = []
        self.verbose = True if self.height < 100 and self.width < 100 else False

    def load_char(self, height, width_start, hex):
        # print('HEX %s '%hex,end='')
        hex = Board.trans[hex] if hex in Board.trans else int(hex)
        if width_start == 0:
            self.board.append([])
        # print('%2s '%hex,end='')
        for i_width in range(QUAD):
            val = (hex // (2 ** (3 - i_width))) % 2
            self.cells[height, width_start + i_width] = Cell(val)
            self.board[height].append(val)
            # print(val,' ',end='')
            # print()

    def get_down(self, i_height, i_width, my_cell: Cell):
        if i_height == self.height - 1:
            return 1
        else:
            return self.cells[(i_height + 1, i_width)].direction_value(my_cell)

    def get_right(self, i_height, i_width, my_cell: Cell):
        if i_width == self.width - 1:
            return 1
        else:
            return self.cells[(i_height, i_width + 1)].direction_value(my_cell)

    def populate_cell(self, i_height, i_width):
        my_cell = self.cells[(i_height, i_width)]
        if (i_height + 1, i_width) not in self.cells:
            down = 1
        else:
            down = self.cells[(i_height + 1, i_width)].down_value(my_cell)
        if (i_height, i_width + 1) not in self.cells:
            right = 1
            running_down = down
        else:
            right = self.cells[(i_height, i_width + 1)].right_value(my_cell)
            running_down = min(down, self.cells[(i_height, i_width + 1)].running_down)

        my_cell.right = right
        my_cell.down = down
        my_cell.running_down = running_down
        if (my_cell.right > my_cell.running_down) and (my_cell.down > my_cell.running_down):
            my_cell.running_down = self.check_downs(i_height, i_width, my_cell)
        my_cell.board_size = min(my_cell.right, my_cell.running_down)
        self.size_list.append((my_cell.board_size, i_height, i_width))

    def check_downs(self, i_height, i_width, my_cell):
        possible_max = min(my_cell.right, my_cell.down)
        my_list = [possible_max]
        count = 1
        running_max = possible_max
        for i in range(1, possible_max):
            this_down = self.cells[i_height, i_width + i].down
            my_list.append(this_down)
            running_max = min(running_max, this_down)
            if count < running_max:
                count += 1
            else:
                break
        return max(count, my_cell.running_down)

    def load_set(self):
        self.size_list = []
        for i_height in range(self.height - 1, -1, -1):
            for i_width in range(self.width - 1, -1, -1):
                if (i_height, i_width) in self.cells:
                    self.populate_cell(i_height, i_width)

    def sort(self):
        self.size_list = sorted(self.size_list, key=lambda t: (t[0], self.height - t[1], self.width - t[2]),
                                reverse=True)

    def remove_board(self, size, i_height, i_width):
        del_list = []
        for i in range(size):
            for j in range(size):
                if (i_height + i, i_width + j) not in self.cells:
                    return False
                del_list.append((i_height + i, i_width + j))

        for i in del_list:
            del self.cells[i]
            self.board[i[0]][i[1]] = None
        return True

    def try_to_extract(self):
        last_size = None
        for i in range(len(self.size_list)):
            size, i_height, i_width = self.size_list[i]
            if size != last_size and last_size is not None:
                print('new size - so reloading_board')
                raise ReloadBoard
            if (i_height, i_width) in self.cells:
                if self.verbose:
                    print('attempting to extract size %s from (%s,%s) ' % (size, i_height, i_width), end='')
                if (self.remove_board(size, i_height, i_width)):
                    if self.verbose:
                        print('done')
                    if size != last_size:
                        print('starting size %s' % size)
                        last_size = size
                        self.list_results.append([size, 0])
                    self.list_results[len(self.list_results) - 1][1] += 1
                else:
                    print('size %s parts missing - continue'%size)

    def print_colour(self):
        for i_height in range(self.height - 1, -1, -1):
            for i_width in range(self.width - 1, -1, -1):
                if (self.height - 1 - i_height, self.width - 1 - i_width) in self.cells:
                    print('%s ' % (self.cells[self.height - 1 - i_height, self.width - 1 - i_width].colour), end='')
                else:
                    print('N ', end='')
            print()
        print()

    def print_board(self):
        print(' ' * 4, end='')
        for i_width in range(self.width):
            print("%2d " % i_width, end='')
        print(' ' * 5, end='')
        for i_width in range(self.width):
            print("%2d " % i_width, end='')
        print()
        for i_height in range(self.height):
            print('%2d ' % i_height, end='')
            for i_width in range(self.width):
                if (i_height, i_width) in self.cells:
                    print('%2s ' % (self.cells[i_height, i_width].colour), end='')
                else:
                    print('   ', end='')
            print('  %2d ' % i_height, end='')
            for i_width in range(self.width):
                if (i_height, i_width) in self.cells:
                    print('%2s ' % (self.cells[i_height, i_width].board_size), end='')
                else:
                    print('   ', end='')
            print()
        print()

    def print_right(self):
        for i_height in range(self.height - 1, -1, -1):
            for i_width in range(self.width - 1, -1, -1):
                if (self.height - 1 - i_height, self.width - 1 - i_width) in self.cells:
                    print('%2d ' % (self.cells[self.height - 1 - i_height, self.width - 1 - i_width].right), end='')
                else:
                    print('N  ', end='')
            print()
        print()

    def print_down(self):
        for i_height in range(self.height - 1, -1, -1):
            for i_width in range(self.width - 1, -1, -1):
                if (self.height - 1 - i_height, self.width - 1 - i_width) in self.cells:
                    print('%2d ' % (self.cells[self.height - 1 - i_height, self.width - 1 - i_width].down), end='')
                else:
                    print('N  ', end='')
            print()
        print()

    def print_running_down(self):
        for i_height in range(self.height - 1, -1, -1):
            for i_width in range(self.width - 1, -1, -1):
                if (self.height - 1 - i_height, self.width - 1 - i_width) in self.cells:
                    print('%2d ' % (self.cells[self.height - 1 - i_height, self.width - 1 - i_width].running_down),
                          end='')
                else:
                    print('N  ', end='')
            print()
        print()

    def print_board_size(self):
        for i_height in range(self.height - 1, -1, -1):
            for i_width in range(self.width - 1, -1, -1):
                if (self.height - 1 - i_height, self.width - 1 - i_width) in self.cells:
                    print('%2d ' % (self.cells[self.height - 1 - i_height, self.width - 1 - i_width].board_size),
                          end='')
                else:
                    print('N  ', end='')
            print()
        print()

    def extract_boards(self):
        while len(self.cells) > 0:
            self.load_set()
            if self.verbose:
                print('\ncolour\t\tboard size')
                self.print_board()

            self.sort()
            try:
                self.try_to_extract()
            except ReloadBoard:
                print('time to reload...')

        print()
        result = "%s\n" % len(self.list_results) + "\n".join('%s %s' % (i[0], i[1]) for i in self.list_results)
        return result


class ChessBoard:
    def __init__(self, input_file_pointer: open):

        (height, width) = utilities.return_int_list(input_file_pointer.readline())
        self.board = Board(height, width)
        characters = width // QUAD
        for i in range(height):
            line = input_file_pointer.readline()
            for j in range(characters):
                char = line[j]
                self.board.load_char(i, j * QUAD, char)

    def get_result(self, case_str=''):
        print('\n%s ' % case_str)
        print('height %s width %s' % (self.board.height, self.board.width))
        result = case_str + ' ' + self.board.extract_boards()
        print(result)
        return result


def main(large=False):
    text = "large" if large else 'small'
    file_name = 'Data/C-%s-practice.' % text
    file_read, file_write, file_dump = utilities.get_file(file_name)
    number_of_cases = int(file_read.readline())
    # sys.stdout = file_dump
    for i in range(0, number_of_cases):
        case_str = 'Case #%s: ' % (i + 1)
        run_case = ChessBoard(file_read)
        out_str = run_case.get_result(case_str)
        file_write.write(out_str + '\n')
        print(out_str)
    file_read.close()
    file_write.close()
    file_dump.close()


if __name__ == "__main__":
    import cProfile

    cProfile.run("main(True)")
