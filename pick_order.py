##M:tG pick order lookup

##TODO:
####Add card compare
####Add formatting to files to allow multiple formats
######OR allow multiple files to be accessed at once
####Add a "Did you mean?" section for edit distance matches

from msvcrt import getch
from msvcrt import kbhit
import os

filename_dict = {'ORI':"data/origins.txt",
                 'KTK':"data/khans.txt"}
exit_command = 3 #ctrl-c
clear_command = 4 #ctrl-d
return_command = 13 #enter
edit_distance_ratio_s = 1.0/3 #soft match
edit_distance_ratio_h = 1.0/6 #hard match
soft_match = False
edit_distance_ratio = edit_distance_ratio_s if soft_match else edit_distance_ratio_h
window_height = 23

def get_filename():
    print "[ORI]\t3x Origins"
    print "[KTK]\tFate Khans Khans"
    choice = raw_input("Draft type: ").upper()
    while choice not in filename_dict:
        choice = raw_input("Draft type: ").upper()
    return filename_dict[choice]

def load_pick_order(filename):
    file_data = open(filename, 'r')
    file_lines = [line.strip().lower() for line in file_data.readlines()]
    file_data.close()

    pick_dict = {}
    counter = 0
    for line in file_lines:
        counter += 1
        pick_dict[line] = counter

    return file_lines, pick_dict

def levenshtein_distance(string, target):
    if string == target:
        return 0
    elif len(string) == 0:
        return len(target)
    elif len(target) == 0:
        return len(string)

    s_vec = [0 for i in range(len(target) + 1)]
    t_vec = [0 for i in range(len(target) + 1)]

    for i in range(len(s_vec)):
        s_vec[i] = i
    for i in range(len(string)):
        t_vec[0] = i + 1
        for j in range(len(target)):
            cost = 0 if string[i] == target[j] else 1
            t_vec[j + 1] = min(t_vec[j] + 1, s_vec[j+1]+1, s_vec[j]+cost)

        for j in range(len(s_vec)):
            s_vec[j] = t_vec[j]

    return t_vec[len(target)]

def string_match(target, compare):
    edit_distance = levenshtein_distance(compare, target)
    return (edit_distance * 1.0) / max(len(target), 1) <= edit_distance_ratio
    #return target != compare

def prune_names(names, string):
    new_names = []
    for name in names:
        if not string_match(name[:len(string)], string):
            continue
        new_names.append(name)
    return new_names

class Card():
    def __init__(self, name, order):
        self.name = name
        self.order = order

    def __lt__(self, other):
        return self.order < other.order

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        h = 0
        c = 1
        for i in self.name.lower():
            h += ord(i) ** c
            h %= 104729
        return h

    def __str__(self):
        return "#%d  - %s" % (self.order, self.name.title())

def update(strings, names, order, maxlen):
    os.system('cls')
    for string in strings:
        print "> %s" % string
    print ""
    largeset = set()
    for nameset in names:
        if len(nameset) == maxlen:
            continue
        for name in nameset:
            largeset.add(Card(name, order[name]))
    for name in sorted(largeset):
        print name

def main():
    print "Welcome to the Pick Order Lookup"
    print "Press Ctrl-C at any time to exit."
    filename = get_filename()
    names, order = load_pick_order(filename)
    current_lookup = [""]
    current_names = [[name for name in names]]
    #os.system('setterm -cursor off')

    while True:
        update(current_lookup, current_names, order, len(names))
        
        new_key = getch()

        if ord(new_key) == exit_command:
            exit()

        if new_key == '\b' and current_lookup[-1] != "":
            current_lookup[-1] = current_lookup[-1][:len(current_lookup[-1])-1]
            current_names[-1] = prune_names(names, current_lookup[-1])
        elif ord(new_key) == clear_command or new_key == '\b' and current_lookup[-1] == "":
            current_lookup.pop()
            current_names.pop()
            if len(current_lookup) == 0:
                current_lookup.append("")
            if len(current_names) == 0:
                current_names.append([name for name in names])
        elif ord(new_key) == return_command:
            current_lookup.append("")
            current_names.append([name for name in names])
        else:
            current_lookup[-1] += new_key
            current_names[-1] = prune_names(names, current_lookup[-1].lower())
        

if __name__ == "__main__":
    main()
