#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#28/12/2018
#Script to change the fields action and type in the firewall logs
import sys
import csv
from datetime import datetime
import time

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

def convert_string_time_2(string_time):
    datetime_object = datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result

def extract_file(input_filepath,output_filepath):
    result = []
    list_logs = extract_csv_file(input_filepath)
    counter = 0
    for log_tuple in list_logs:
        #print counter
        counter += 1
        if log_tuple[input_pos_source]=="192.168.142.11" and log_tuple[input_pos_destination]=="192.168.128.40":

            result.append(log_tuple)
            print log_tuple

    result = sorted(result, key=lambda x: x[output_pos_timestamp])

    #write_csv_file(output_filepath,result)

def get_stats_from_field(input_filepath, field):
    result = {}
    list_logs = extract_csv_file(input_filepath)
    for log_tuple in list_logs:
        value = log_tuple[field]
        if value in result:
            result[value] += 1
        else:
            result[value] = 1
    print result
    print "Size: "+str(len(result))

def main(input_filepath,output_filepath):
    extract_file(input_filepath,output_filepath)
    #get_stats_from_field(input_filepath,input_pos_process_id)

if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    #main("../../datasets/huma/reduced_attacks.csv","../../datasets/huma/reduced_attacks_v2.csv")
    main("../../datasets/huma/log_airbus_simplify_v2.csv","")