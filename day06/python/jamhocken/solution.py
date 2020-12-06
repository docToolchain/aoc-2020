with open("customs.txt",'r') as customs_file: 
    forms = customs_file.readlines()
forms.append('\n')

letters_raw = ''
list_raw = list()
list_common = list()

for file_lines in forms:
    if file_lines == "\n":
        list_raw.append(set(letters_raw))
        list_common.append(set_temp)
            
        letters_raw = ''
    else:
        form_stripped = file_lines.rstrip()
        
        if letters_raw == '':
            set_temp = set(form_stripped)
        letters_raw += form_stripped
        set_temp = set_temp.intersection(set(form_stripped)) 

list_count = list()
[list_count.append(len(n)) for n in list_raw]
print('The sum of yes answers per group:', sum(list_count))

list_count = list()
[list_count.append(len(n)) for n in list_common]
print('The sum of common yes answers per group:', sum(list_count))