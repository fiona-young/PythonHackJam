import Milkshake_refinement2
name = 'B-large-practice'
file = open('Data/'+name+'.in')
file_write = open('Data/'+name+'.out','w')

cases = int(file.readline())
my_list = []
for i in range(0,cases):
    case=Milkshake_refinement2.Milkshakes(file)
    result = case.get_result()
    out_str = 'Case #%s: %s'%(i+1,result)
    file_write.write(out_str+'\n')
    print(out_str)
file.close()
file_write.close()
