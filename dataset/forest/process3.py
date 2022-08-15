import csv


file = open('smarthome.csv')
reader = csv.reader(file)
header_row = next(reader)



header = ['Age','Student Status', 'Highest education level completed', 
'Technology use at work', 'Experience', 'Gender identity',
'Datatype','Recipient','Condition','Class']

final_file = []
final_file.append(header)


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


condition ={'0': 'no condition',
'1': 'if the data is anonymous',
'2': 'if the data is kept confidential',
'3': 'if the data is stored for as long as necessary for the purpose',
'4': 'if you are notified',
'5': 'if you can delete or review the data'
}


student ={'0': 'Not a student',
'1': 'student',
'2': 'unknow'}

education = {'0': 'No formal degree',
'1': 'Secondary degree',
'2': 'High school',
'3': 'Technical or community degree',
'4': 'Undergraduate degree',
'5': 'Graduate degree',
'6': 'Doctoral degree'}

technology = {'0': 'unknow',
'1': 'almost never',
'2': 'less than a month',
'3': 'once a week',
'4': '2 or 3 times a week',
'5': '4 or 6 times a week',
'6': 'once a day',
'7': 'more than once a day'}

experience = {'0': 'never',
'1': 'less than one year',
'2': 'one year',
'3': 'two years',
'4': 'three years',
'5': 'four years'}

gender = {'0': 'Female',
'1': 'Male',
'2': 'Prefer not say'}

label = {'0':'Prohibit',
'1': 'Permit'}

header = ['Age','Student Status', 'Highest education level completed', 
'Technology use at work', 'Experience', 'Gender identity',
'Datatype','Recipient','Condition','Class']




for k, v in enumerate(reader):
    buffer = []
    buffer.append(v[0])
    buffer.append(student[v[1]])
    buffer.append(education[v[2]])
    buffer.append(technology[v[3]])
    buffer.append(experience[v[4]])
    buffer.append(gender[v[5]])
    buffer.append(datatype[v[6]])
    buffer.append(recipient[v[7]])
    buffer.append(condition[v[8]])
    buffer.append(label[v[9]])
    final_file.append(buffer)

save_file = 'smarthome_plaintext.csv'
with open(save_file,"w") as csv_file:
    writer=csv.writer(csv_file)
    for key,value in enumerate(final_file):
        # import pdb; pdb.set_trace() 
        writer.writerow(value)
import pdb;pdb.set_trace()





