#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#27/12/2018
#Script to analyze iscx
import sys
import csv
from datetime import datetime
import time

number_fields_input = 8
number_fields_output = 8

#positions
pos_id = 0
pos_timestamp = 1
pos_source = 2
pos_destination = 3
pos_type = 4
pos_port_src = 5
pos_port_dst = 6
pos_tag = 7

def extract_csv_file(filepath):
    result = []
    with open(filepath,'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row)

    return result

def write_csv_file(filepath,input_list):
    with open(filepath,'wb') as f:
        writer = csv.writer(f)
        writer.writerows(input_list)

def convert_string_time_2(string_time):
    datetime_object = datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result

def get_involved_logs(input_filepath, list_ip_addresses):
    list_logs = extract_csv_file(input_filepath)
    counter = 0
    for log_tuple in list_logs:
        ipsrc = log_tuple[pos_source]
        ipdst = log_tuple[pos_destination]
        if ipsrc in list_ip_addresses or ipdst in list_ip_addresses:
            string_to_print = ""
            for element in log_tuple:
                string_to_print += str(element)+", "
            print string_to_print
            counter += 1
    print counter

def get_ips(input_filepath, list_ip_addresses):
    list_logs = extract_csv_file(input_filepath)
    dict_ips = {}
    for log_tuple in list_logs:
        ipsrc = log_tuple[pos_source]
        ipdst = log_tuple[pos_destination]
        if ipsrc in list_ip_addresses:
            if ipdst not in dict_ips:
                dict_ips[ipdst] = 1
            else:
                dict_ips[ipdst] += 1
        else:
            if ipdst in list_ip_addresses:
                if ipsrc not in dict_ips:
                    dict_ips[ipsrc] = 1
                else:
                    dict_ips[ipsrc] += 1
    pretty_print_dict(dict_ips)

def pretty_print_dict(input_dict):
    for key in sorted(input_dict.keys()):
        print str(input_dict[key]) + " "+key
    print len(input_dict)

def main(input_filepath):
    #get_involved_logs(input_filepath,["192.168.1.105","192.168.2.112","192.168.5.123"])
    get_involved_logs(input_filepath,["142.167.88.44"])
    #get_ips(input_filepath,["192.168.2.112"])


if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    main("../../datasets/iscx/iscx_ids_simplify_parsed_v3.csv")
