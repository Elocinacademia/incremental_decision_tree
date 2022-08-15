import csv



new_file = []

new_file.append(header_row[0])
for num, row in enumerate(reader):
    new_row = []
    for item in row:
        if item != '':
            new_row.append(item)
    new_file.append(new_row)



header = ['Student Status', 'Highest education level completed', 
'Technology use at work', 'Experience', 'Gender identity', 'Age',
'Datatype','Recipient','Condition','Class']

final_file = []
final_file.append(header)

for index, value in enumerate(new_file[1:]):
    demongraphic = value[:6]
    data_flow = value[6:]
    each_user = []
    
    for key, v in enumerate(data_flow):
        each_flow =[]
        buffer = demongraphic
        v = v[1:-1]
        v_list = v.split(",")
        new_vlist = []
        for attribute in v_list:
            attribute.strip(' ')
            attribute = attribute[1:-1]
            attribute = attribute.lstrip("\'")
            new_vlist.append(attribute)
        del new_vlist[2]
        each_flow = buffer + new_vlist
        each_user.append(each_flow)
    print(each_user)
    for x in each_user:
        final_file.append(x)




save_file = 'saved_file.csv'
with open(save_file,"w") as csv_file:
    writer=csv.writer(csv_file)
    for key,value in enumerate(final_file):
        # import pdb; pdb.set_trace() 
        writer.writerow(value)


import pdb;pdb.set_trace()
        