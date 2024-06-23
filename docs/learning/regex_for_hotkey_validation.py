''' Regular Expressions - used in the Settings window / hotkeys validation '''

import re

# this list used to learn / compile regex
# it is not part of the media player
list = ['bubuka@gmail.com','bubu.pa@gmail.com','bubu-ta@gmail.com','Hey snake! What is your email address? Yesss, bubuka@gmail.comssss.''4',
        'bubuka_long@gmaillll.com', 'bubuka@gma00il.com', 'bubuka616@gmail.com', 'bubuka@gmail@.com@'
        '077 566 5654','077_566_5654', '0775665654','077-566-123', '077-566-5654', '077K566K5654'
        'random words', '554654654', 'M', 'tt', '0', 'Del', 'space+enter', 'm+space+enter', 't+del+alt', 't+delTT']


# ^Shift - the string starts with Shift
# Shift$ - the string ends with Shift

''' WITHOUT KEY LIST '''
# exp_1 = '^Shift$|^Alt$|^Enter$|^Space$|^Ctrl$|^Del$|^Left$|^Right$|^[a-zA-Z0-9]$'
# exp_2 = '(^Shift|^Alt|^Enter|^Space|^Ctrl|^Del|^Left|^Right|^[a-zA-Z0-9])\+(Shift$|Alt$|Enter$|Space$|Ctrl$|Del$|Left$|Right$|[a-zA-Z0-9]$)'
# exp_3 = '(^Shift|^Alt|^Enter|^Space|^Ctrl|^Del|^Left|^Right|^[a-zA-Z0-9])\+(Shift|Alt|Enter|Space|Ctrl|Del|Left|Right|[a-zA-Z0-9])\+(Shift$|Alt$|Enter$|Space$|Ctrl$|Del$|Left$|Right$|[a-zA-Z0-9]$)'

# search_regex = re.compile(f'{exp_1}|{exp_2}|{exp_3}')

# for i in list:
#     search_result = search_regex.search(i.title())
#     if search_result:
#         print(search_result.group())
# print('\n')

''' WITH KEY LIST '''
keys_list = ['Shift', 'Alt', 'Enter', 'Space', 'Ctrl', 'Del', 'Left', 'Right', 'Backspace', '[a-zA-Z0-9]']

exp_1 = ''
for item in keys_list[0:-1]:
    exp_1 = exp_1 + f'^{item}$|'
exp_1 = exp_1 + f'^{keys_list[-1]}$'


exp_2 = '('
for item in keys_list[0:-1]:
    exp_2 = exp_2 + f'^{item}|'
exp_2 = exp_2 + f'^{keys_list[-1]})\+('

for item in keys_list[0:-1]:
    exp_2 = exp_2 + f'{item}$|'
exp_2 = exp_2 + f'{keys_list[-1]}$)'


exp_3 = '('
for item in keys_list[0:-1]:
    exp_3 = exp_3 + f'^{item}|'
exp_3 = exp_3+ f'^{keys_list[-1]})\+('

for item in keys_list[0:-1]:
    exp_3 = exp_3 + f'{item}|'
exp_3 = exp_3+ f'{keys_list[-1]})\+('

for item in keys_list[0:-1]:
    exp_3 = exp_3 + f'{item}$|'
exp_3 = exp_3+ f'{keys_list[-1]}$)'

# print(exp_1)
# print(exp_2)
# print(exp_3)

search_regex = re.compile(f'{exp_1}|{exp_2}|{exp_3}')
for i in list:
    search_result = search_regex.search(i.title())
    if search_result:
        print(search_result.group())
print('\n')      