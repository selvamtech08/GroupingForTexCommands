import re

class AddGrouping:
    '''Adding grouping to the macros which are followed by _ or ^'''
    def __init__(self):
        self.cmd_regex = re.compile(r'[_|^](\\(frac|dfrac|tfrac|sfrac|nicefrac|mbox|hbox|text|mathrm|mathbf))',re.I)            
        self.two_args = ('frac','tfrac','dfrac')

    def get_elements_without_group(self,equString):
        '''finding the arguments for given string and return matchs'''
        self.equ_string = equString
        self.find_pos = re.finditer(self.cmd_regex,self.equ_string)                
        group_elem = []
        elems_args = []
        for str_cmd in self.find_pos:
            prev = ''
            num_of_args = 1
            if str_cmd.group(2) in self.two_args:
                num_of_args = 2
            match_grps = 0
            string_elem = []
            start_delim = 0    
            for s in str_cmd.string[str_cmd.end():]:
                if s == '{' and prev != '\\':
                    string_elem.append(s)
                    match_grps += 1
                    start_delim = 1
                elif s == '}' and prev != '\\':
                    string_elem.append(s)
                    match_grps -= 1
                    if match_grps == 0:
                        group_elem.append("".join(string_elem))
                        string_elem = []
                        start_delim = 0
                    if match_grps == 0 and len(group_elem) == num_of_args:
                        elems_args.append(str_cmd.group(2) + "".join(group_elem))
                        group_elem = []
                        break            
                else:
                    if not re.search(r'\s+',s) and start_delim == 0:
                        string_elem.append(s)
                        match_grps += 1                        
                        group_elem.append("".join(string_elem))                             
                        if (match_grps == 1):
                            match_grps -= 1
                            string_elem = [] 
                        if match_grps == 0 and len(group_elem) == num_of_args:
                            elems_args.append(str_cmd.group(2) + "".join(group_elem))
                            group_elem = []
                            break            
                    else:
                        string_elem.append(s)
                prev = s
        return elems_args
    
    def change_grouping(self,equString):
        'Inserting group around the specified macro commands'
        modify_equation = equString
        for string in self.get_elements_without_group(equString):
            modify_equation = re.sub('(?<=[_|^])('+re.escape('\\' + string)+')',r'{\1}',modify_equation)    
        return modify_equation
    
    def debug_changes(self,equString):
        '''Debug the occurrences'''
        print('\n********************************')
        print("Debuging....\n")
        modify_equation = equString
        for string in self.get_elements_without_group(equString):
            print('\\' + string)
        print('\n********************************\n')            

if __name__ == "__main__":
    equation = r'''\Delta C_{i} = \Bigl(a_\frac {m^{a}/m^{o}}{C_{i}^{a}/C_{i}^{o}}-1\Bigr) C_{i}^{o}.
    ^\frac ab _\frac{a}b ^\frac a b ^\frac {a} b _\text a \text a \text{a}
    '''
    tex_group = AddGrouping()
    print("Before edit:",equation)
    print("After edit:",tex_group.change_grouping(equation))
    tex_group.debug_changes(equation)    
