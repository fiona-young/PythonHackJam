import Quaificatin2009.AlienLanguage
name = 'C-small-practice'
#file = open('Data/'+name+'.in')
#file_write = open('Data/'+name+'.out','w')
file_read, file_write = Quaificatin2009.AlienLanguage.get_file(False)

cases = int(file_read.readline())
my_list = []
for i in range(0,cases):
    case=Quaificatin2009.AlienLanguage.AlienLanguage(file_read)
    result = case.get_result()
    out_str = 'Case #%s: %s'%(i+1,result)
    file_write.write(out_str+'\n')
    print(out_str)
file.close()
file_write.close()
