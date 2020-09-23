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
input_pos_id = 0
input_pos_timestamp = 1
input_pos_origin = 2
input_pos_service = 3
input_pos_source = 4
input_pos_destination = 5
input_pos_type = 6
input_pos_action = 7
input_pos_process_id = 8
input_pos_port_src = 9
input_pos_port_dst = 10
input_pos_log = 11
input_pos_tag = 12

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

def get_stats_from_field(input_filepath, field):
    result = {}
    list_logs = extract_csv_file(input_filepath)
    for log_tuple in list_logs:
        value = log_tuple[field]
        if value in result:
            result[value] += 1
        else:
            result[value] = 1
    #pretty_print_dict(result)
    #print_dict_differently(result)
    print_dict_for_table(result)
    print "Size: "+str(len(result))

def pretty_print_dict(input_dict):
    for key, value in sorted(input_dict.iteritems(), key=lambda (k,v): (v,k)):
        print str(input_dict[key]) + " "+key

def print_dict_differently(input_dict):
    for key, value in sorted(input_dict.iteritems(), key=lambda (k,v): (v,k)):
        print "'"+key+"',"

def print_dict_for_table(input_dict):
    for key, value in sorted(input_dict.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        print key+" & "+str(value)+" \\ "
        print "\hline"

def main(input_filepath):
    get_stats_from_field(input_filepath,input_pos_type)

if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    main("../../datasets/iscx/iscx_ids_simplify_parsed_v3.csv")
