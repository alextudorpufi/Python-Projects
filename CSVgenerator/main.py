import csv
import random
from collections import Counter

def generate_username(i):
    return f'user_random_{i}@pypl.com'

def generate_PNC():
    random_number1 = random.randint(100000, 999999) # 6
    random_number2 = random.randint(1000000, 9999999) # 7
    return f'{random_number1}{random_number2}' # 13

def generate_State():
    gen=random.randint(1, 2)
    if(gen==1):
        return f'Active'
    else:
        return f'Inactive'

def generate_Type():
    types=['rights1','rights2','rights2.1','rights2.2','rights3','rights4']
    return types[random.randint(0, 5)]

header = ['Username', 'PNC', 'STATE', 'TYPE']

data = [
    [generate_username(i),
     generate_PNC(),
     generate_State(),
     generate_Type()]
    for i in range(1, 65536)
]

with open('tabel.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)

###############

reader = csv.reader(open('tabel.csv', 'r'))

def Username_parity(username):
    #user_random_ ---> 1 <--- @pypl.com
    num = int(username.split('_')[2].split('@')[0])
    return 'even' if num % 2 == 0 else 'odd'

def PNC_number(pnc):
    return pnc[0]

def STATE_status(state):
    return state

def Type_version(type):
    return type

username_parity_counter = Counter()
pnc_start_digit_counter = Counter()
state_status_counter = Counter()
type_right_counter = Counter()

with open('tabel.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        username_parity_counter[Username_parity(row['Username'])] += 1
        pnc_start_digit_counter[PNC_number(row['PNC'])] += 1
        state_status_counter[STATE_status(row['STATE'])] += 1
        type_right_counter[Type_version(row['TYPE'])] += 1

# second_header = ['Username_parity', 'PNC_number', 'STATE_status', 'TYPE_version']

with open('statistici.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(second_header)

    for key, value in username_parity_counter.items():
        writer.writerow(['Username_parity', key, value])

    for key, value in pnc_start_digit_counter.items():
        writer.writerow(['PNC_number', key, value])

    for key, value in state_status_counter.items():
        writer.writerow(['STATE_status', key, value])

    for key, value in type_right_counter.items():
        writer.writerow(['TYPE_version', key, value])