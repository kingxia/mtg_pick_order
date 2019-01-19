#!/usr/bin/env python
##M:tG pick order lookup
##King Xia

##TODO:
####Add card compare
####Populate KTK draft file, add FRF as well
####Add formatting to files to allow multiple formats
######OR allow multiple files to be accessed at once
####Add a "Did you mean?" section for edit distance matches

from msvcrt import getch
import os
from lib.card import Card

filename_dict = {'DOM':'data/dom.txt',
                 'ORI':"data/ori.txt",
                 'KLD':"data/kld.txt",
                 'KTK':"data/ktk.txt",
                 'DTK':"data/dtk.txt",
		 'WWK':"data/wwk.txt",
		 'ZEN':"data/zenzenzen.txt",
                 'RNA':"data/rna.txt"}
ascending_sets = ['ZEN', 'WWK']
lsv_set_index = 1
tcg_set_index = 3
exit_command = 3 #ctrl-c
clear_command = 4 #ctrl-d
return_command = 13 #enter
edit_distance_ratio_s = 1.0/3 #soft match
edit_distance_ratio_h = 1.0/6 #hard match
soft_match = False
edit_distance_ratio = edit_distance_ratio_s if soft_match else edit_distance_ratio_h
window_height = 23

def get_filename():
    for key in filename_dict:
        print "[%s]" % key
    choice = raw_input("Draft type: ").upper()
    while choice not in filename_dict:
        choice = raw_input("Draft type: ").upper()
    return filename_dict[choice]

def is_asc_set(filename):
    for key in filename_dict:
        if filename_dict[key] == filename:
	    return key in ascending_sets
    return False

def load_pick_order(filename, is_asc=False):
    file_data = open(filename, 'r')
    file_lines = [line.strip().lower() for line in file_data.readlines()]
    file_data.close()

    pick_dict = {}
    card_names = []
    pick_index = tcg_set_index if is_asc else lsv_set_index
    for line in file_lines:
        line_split = line.split("\t")
        card_names.append(line_split[0])
        #print line_split, tcg_set_index, lsv_set_index
        if is_asc:
            pick_dict[line_split[0]] = [float(line_split[tcg_set_index])]
        elif len(line_split) > 2:
            #print line_split
            pick_dict[line_split[0]] = [float(line_split[lsv_set_index]),
                                        float(line_split[lsv_set_index + 1])]
        else:
            pick_dict[line_split[0]] = [float(line_split[lsv_set_index])]

    return card_names, pick_dict

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

def update(strings, names, order, maxlen, asc_order=False):
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
    cardset = sorted(largeset)
    cardset = cardset if asc_order else cardset[::-1]
    for name in cardset:
        print name

def main():
    print "Welcome to the Pick Order Lookup"
    print "Press Ctrl-C at any time to exit."
    filename = get_filename()
    is_asc = is_asc_set(filename)
    names, order = load_pick_order(filename, is_asc)
    current_lookup = [""]
    current_names = [[name for name in names]]
    #os.system('setterm -cursor off')

    while True:
        update(current_lookup, current_names, order, len(names), is_asc)
        
        new_key = getch()

        if ord(new_key) == exit_command:
            os.system('cls')
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
