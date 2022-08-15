import csv


file = open('scaled_data.csv')
reader = csv.reader(file)
header_row = next(reader)

new_file = []








header = ['Age','Student Status', 'Highest education level completed', 
'Technology use at work', 'Experience', 'Gender identity',
'Datatype','Recipient','Condition','Class']

final_file = []
final_file.append(header)

new_file = []
for num, row in enumerate(reader):
    new_row = []
    # print(row[-3:])
    if len(row) > 10:
        if row[-2] == '' and row[-1]=='':
            new_file.append(row[:10])
        elif row[-3] == 'i.e':
            for x in row[:9]:
                new_row.append(x)
            new_row.append(row[-1])
            new_file.append(new_row)
        elif row[-2] != '':
            for x in row[:9]:
                new_row.append(x)
            new_row.append(row[-2])
            new_file.append(new_row)


        # else:
        #     # print(row)
        #     if 'confidentia' in row[-4]:
        #         for x in row[:9]:
        #             new_row.append(x)
        #         new_row.append(row[-2])
        #         new_file.append(new_row)
        else:
            print(row)


for k, value in enumerate(new_file):
    if value[-1] == 'not shared with others':
        print(k)
        print(value)
        

# import pdb;pdb.set_trace()



datatype = {'1':'email', 
'2':'banking','3':'healthcare',
'4':'door locker','5':'camera','6':'call assistant',
'7':'video call',
'8':'location',
'9':'voice recording',
'10':'todo',
'11':'sleep hours',
'12':'playlists',
'13':'thermostat',
'14':'shopping',
'15':'weather'}



recipient = {'1':'your parents',
'2':'your partner',
'3':'your siblings',
'4':'your housemates',
'5':'your children',
'6': 'neighbours',
'7':'your friends',
'8':'close family',
'9':'house keeper/helper',
'10':'visitors in general',
'11':'assistant provider',
'12':'skills',
'13':'other skills',
'14':'advertising agencies',
'15':'law enforcement agencies'}

condition = {'no condition': '0',
'no conditions': '0',
'if the data is anonymous': '1',
'if the data is confidentia': '2',
'if the data is kept confidentia': '2',
'if the data is kept confidential': '2',
'if the data is confidential i.e. not shared with others': '2',
'if the data is kept confidential i.e. not shared with others.': '2',
'if the data is kept confidential i.e. not shared with others': '2',
'if the data is stored for as long as necessary for the purpose above':'3',
'if the data is stored for as long as reasonably for the purpose above': '3',
'if the data stored for as long as necessary for the purpose above': '3',
'if the data stored for as long as necessary for the purpose above.' : '3',
'if you are notified': '4',
'if you can review or delete the data': '5',
'if you review or delete the data': '5',
'if you can delete or review the data': '5'
}


def get_key (dict, value):
    for k, v in dict.items():
        if v == value:
            return k

    
label = {'Somewhat Acceptable' : '1',
'Somewhat acceptable' : '1',
'Completely Acceptable' : '1',
'Completely Acceptable ': '1',
'Neutral' : '1',
'Completely acceptable': '1',
'Somewhat unacceptable': '0',
'Completely unacceptable': '0',
'Completely Unacceptable': '0',
'Somewhat Unacceptable': '0'
}





outlier_key = []
for k,v in enumerate(new_file):
    buffer =[]
    buffer.append(v[0])
    #deal with student status
    if v[1] == 'Yes':
        buffer.append('1')
    elif v[1] == 'No':
        buffer.append('0')
    elif 'not applicable' in v[1] or 'REVOKED' in v[1] or 'EXPIRED' in v[1]:
        buffer.append('2')
    elif 'Undergraduate' in v[1]:
        outlier_key.append(k)
        buffer.append('100')
    else:
        print('student status' , v[1])


    #deal with Highest education
    if 'know' in v[2] or 'formal' in v[2] or 'REVOKED' in v[2] :
        buffer.append('0')
    elif 'Secondary' in v[2]:
        buffer.append('1')
    elif 'school' in v[2]:
        buffer.append('2')
    elif 'Technical' in v[2]:
        buffer.append('3')
    elif 'BA' in v[2]:
        buffer.append('4')
    elif 'MA' in v[2]:
        buffer.append('5')
    elif 'Doctor' in v[2]:
        buffer.append('6')
    else:
        outlier_key.append(k)
        buffer.append('100')

    #deal with tech usage
    if 'REVOKED' in v[3]:
        buffer.append('0')
    elif 'all' in v[3]:
        buffer.append('1')
    elif 'less than' in v[3]:
        buffer.append('2')
    elif 'nce a week' in v[3]:
        buffer.append('3')
    elif '2 or 3' in v[3]:
        buffer.append('4')
    elif '4 or 6' in v[3]:
        buffer.append('5')
    elif 'ce a day' in v[3]:
        buffer.append('6')
    elif 'ore than once a day' in v[3]:
        buffer.append('7')
    else:
        outlier_key.append(k)
        buffer.append('100')


    #deal with experience
    if v[4] == 'none':
        buffer.append('0')
    elif v[4] == 'lessayear':
        buffer.append('1')
    elif 'one' in v[4]:
        buffer.append('2')
    elif 'two' in v[4]:
        buffer.append('3')
    elif 'three' in v[4]:
        buffer.append('4')
    elif 'four' in v[4]:
        buffer.append('5')
    else:
        outlier_key.append(k)
        buffer.append('100')
     
        

    #deal with gender
    if v[5] == 'Female':
        buffer.append('0')
    elif v[5] == 'Male':
        buffer.append('1')
    elif 'Rather' in v[5] or 'REVOKED' in v[5]:
        buffer.append('2')
    else:
        outlier_key.append(k)
        buffer.append('100')
        
    
    #deal with datatype
    # print(v[6])
    # if v[6] == 'todo':
    #     import pdb;pdb.set_trace()
    num_data = get_key(datatype,v[6])
    buffer.append(num_data)

    
    #deal with recipient
    # print(v[7])
    num_recipient = get_key(recipient,v[7])
    buffer.append(num_recipient)

    #deal with condition
    # print(v[8])
    if v[8] in condition.keys():
        buffer.append(condition[v[8]])
    else:
        print(v[8])

    #deal with acceptance
    if v[9] in label.keys():
        buffer.append(label[v[9]])
    elif v[9] == 'Click to write Scale Point 6':
        outlier_key.append(k)
        buffer.append('100')
    else:
        print(v[9])


   
    final_file.append(buffer)

keylist = []
for key, value in enumerate(final_file):
    if '100' in value:
        keylist.append(key)
print(len(final_file))


for i in reversed(keylist):
    del final_file[i]
print(len(final_file))



save_file = 'smarthome.csv'
with open(save_file,"w") as csv_file:
    writer=csv.writer(csv_file)
    for key,value in enumerate(final_file):
        # import pdb; pdb.set_trace() 
        writer.writerow(value)
import pdb;pdb.set_trace()








    

        


    








        











            