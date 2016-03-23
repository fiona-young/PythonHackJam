import utilities

class Rope:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def crosses(self, other_rope):
        if self.x > other_rope.x and self.y < other_rope.y:
            return True
        if self.x < other_rope.x and self.y > other_rope.y:
            return True
        return False



class RopeIntranet:
    def __init__(self, input_file_pointer : open):
        self.rope_list = []
        self.rope_count = int(input_file_pointer.readline())
        for i in range(self.rope_count):
            rope_coords =utilities.return_int_list(input_file_pointer.readline())
            self.rope_list.append(Rope(*rope_coords))

    def get_result(self,case_str=''):
        print('\n%s '%case_str)
        count = 0
        line = 0
        for i in range(self.rope_count):
            for j in range(i+1,self.rope_count):
                line +=1
                crosses = self.rope_list[i].crosses(self.rope_list[j])
                if crosses:
                    count += 1
               # print('%s i against j %s %s %s'%(line,i,j,crosses))
        result = '%s %s'%(case_str,count)
        print(result)
        return result



def main(large=False):
    text = "large" if large else 'small'
    file_name =  'Data/A-%s-practice.' % text
    file_read, file_write, file_dump = utilities.get_file(file_name)
    number_of_cases = int(file_read.readline())
    #sys.stdout = file_dump
    for i in range(0, number_of_cases):
        case_str = 'Case #%s: ' % (i + 1)
        run_case = RopeIntranet(file_read)
        out_str = run_case.get_result(case_str)
        file_write.write(out_str+'\n')
        print(out_str)
    file_read.close()
    file_write.close()
    file_dump.close()

if __name__ == "__main__":
    import cProfile
    cProfile.run("main(True)")
