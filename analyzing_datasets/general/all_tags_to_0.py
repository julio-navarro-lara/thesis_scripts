#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#22/01/2019
#Script to convert all the tags in a dataset to 0
import sys
import csv
from datetime import datetime
import time
import math

number_fields_input = 13
number_fields_output = 13

#input_positions
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

def convert_all_tags_to_0(input_filepath, output_filepath):
    result = []
    list_logs = extract_csv_file(input_filepath)
    for log_tuple in list_logs:
        log_tuple[input_pos_tag] = 0
        result.append(log_tuple)

    write_csv_file(output_filepath, result)
    print "Size: "+str(len(result))

def main(input_filepath,output_filepath):
    convert_all_tags_to_0(input_filepath,output_filepath)

if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    #main("../../datasets/huma/reduced_attacks.csv","../../datasets/huma/reduced_attacks_v2.csv")
    main(sys.argv[1],sys.argv[2])
