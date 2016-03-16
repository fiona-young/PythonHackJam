import Round1A2008
name = 'B-small-practice'
file = open(name+'.in')
file_write = open(name+'.out','w')

cases = int(file.readline())
my_list = []
for i in range(0,cases):
    if i in {18,29,34,68}:
        a=1
    case=Round1A2008.Milkshakes(file)
    result = case.get_result()
    out_str = 'Case #%s: %s'%(i+1,result)
    file_write.write(out_str+'\n')
    print(out_str)
file.close()
file_write.close()
