#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#29/08/2018
#Script to order the logs and change timestamp to human format
import sys
import csv
from datetime import datetime
import time

number_fields_input = 13
number_fields_output = 13

#input_positions
input_pos_id = 0
input_pos_timestamp = 1
input_pos_source = 2
input_pos_destination = 3
input_pos_type = 4
input_pos_port_src = 5
input_pos_port_dst = 6
input_pos_tag = 7

#output_positions
output_pos_id = 0
output_pos_timestamp = 1
output_pos_source = 2
output_pos_destination = 3
output_pos_type = 4
output_pos_port_src = 5
output_pos_port_dst = 6
output_pos_tag = 7

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

def convert_time_string(timestamp):
    result = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return result

def order_and_convert_file(input_filepath,output_filepath):
    result = []
    list_logs = extract_csv_file(input_filepath)

    sorted_list = sorted(list_logs, key=lambda x: x[output_pos_timestamp])

    for log_tuple in sorted_list:
        log_result = log_tuple
        log_result[output_pos_timestamp] = convert_time_string(float(log_tuple[output_pos_timestamp]))
        result.append(log_result)

    write_csv_file(output_filepath,result)

def main():
    order_and_convert_file("../../datasets/darpa2000/simplified_parsed_v3/llddos1-preinput_notordered.csv","../../datasets/darpa2000/simplified_parsed_v3/llddos1.csv")

if __name__ == "__main__":
    main()
