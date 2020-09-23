#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#18/01/2019
#Script to parse the sets of logs coming from Eventgen and using the Bishop format to the format of parsedv3
import sys
import csv
from datetime import datetime
import time

number_fields_output = 13

#output_positions
output_pos_id = 0
output_pos_timestamp = 1
output_pos_origin = 2
output_pos_service = 3
output_pos_source = 4
output_pos_destination = 5
output_pos_type = 6
output_pos_action = 7
output_pos_process_id = 8
output_pos_port_src = 9
output_pos_port_dst = 10
output_pos_log = 11
output_pos_tag = 12

def write_csv_file(filepath,input_list):
    with open(filepath,'wb') as f:
        writer = csv.writer(f)
        writer.writerows(input_list)

def read_file_lines(filepath):
    file = open(filepath,'r')

    list_lines = file.readlines()

    return list_lines

def parse_line(line):
    splitted_line = line.split('#')
    log = ['']*number_fields_output

    log[output_pos_id] = splitted_line[2].split('=')[1]
    log[output_pos_timestamp] = splitted_line[3].split('=')[1]
    log[output_pos_origin] = splitted_line[4].split('=')[1]
    log[output_pos_source] = splitted_line[5].split('=')[1]
    log[output_pos_service] = splitted_line[6].split('=')[1]
    log[output_pos_destination] = splitted_line[7].split('=')[1]
    log[output_pos_type] = splitted_line[8].split('=')[1]
    log[output_pos_action] = splitted_line[9].split('=')[1]
    log[output_pos_tag] = splitted_line[10].split('=')[1]

    return log

def parse_logs(input_filepath):
    list_lines = read_file_lines(input_filepath)
    result = []
    for line in list_lines:
        log = parse_line(line)
        result.append(log)

    return result

def extract_attacks(list_logs):
    dict_attacks = {}
    for log in list_logs:
        tag = int(log[output_pos_tag])
        if tag != 0:
            if tag in dict_attacks:
                dict_attacks[tag].append(log)
            else:
                dict_attacks[tag] = [log]
    return dict_attacks

def extract_all_logs_by_attacker(list_logs):
    dict_attacks = {}
    for log in list_logs:
        tag = int(log[output_pos_tag])
        attacker = log[output_pos_source]
        if tag != 0:
            if attacker in dict_attacks:
                dict_attacks[attacker].append(log)
            else:
                dict_attacks[attacker] = [log]
        elif attacker in dict_attacks:
            dict_attacks[attacker].append(log)
    return dict_attacks

def print_dict_attacks(output_filepaths,dict_attacks):
    file = open(output_filepaths,'wb')
    writer = csv.writer(file)

    for key,value in dict_attacks.iteritems():
        writer.writerows([[key]])
        writer.writerows(value)

        #We write the key elements
        key_elements = []
        for element in value:
            key_elements.append([element[output_pos_origin],element[output_pos_service],element[output_pos_type],element[output_pos_action]])

        writer.writerows(key_elements)

def main(input_filepath):
    list_logs = parse_logs(input_filepath)

    dict_attacks = extract_attacks(list_logs)

    dict_attackers = extract_all_logs_by_attacker(list_logs)

    write_csv_file(input_filepath+".parsed.csv",list_logs)
    print_dict_attacks(input_filepath+".attacks",dict_attacks)
    print_dict_attacks(input_filepath+".attackers",dict_attackers)

if __name__ == "__main__":
    main(sys.argv[1])
