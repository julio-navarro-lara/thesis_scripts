#Copyright 2019 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#17/01/2019
#Script to insert the logs missing from the attack
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

def simplify_log(log_tuple):
    result = ['']*number_fields_output

    result[output_pos_id] = log_tuple[input_pos_id]
    result[output_pos_timestamp] = log_tuple[input_pos_timestamp]
    result[output_pos_origin] = log_tuple[input_pos_origin]
    result[output_pos_service] = log_tuple[input_pos_service]
    result[output_pos_port_src] = log_tuple[input_pos_port_src]
    result[output_pos_source] = log_tuple[input_pos_source]
    result[output_pos_port_dst] = log_tuple[input_pos_port_dst]
    result[output_pos_destination] = log_tuple[input_pos_destination]
    result[output_pos_type] = log_tuple[input_pos_action]
    result[output_pos_action] = log_tuple[input_pos_type]
    result[output_pos_process_id] = log_tuple[input_pos_process_id]

    return result

def modify_file(input_filepath,alert_filepath,output_filepath):
    result = []
    list_logs = extract_csv_file(input_filepath)
    list_attack = extract_csv_file(alert_filepath)
    counter = 0
    for attack_log in list_attack:
        print counter
        counter+=1
        id_attack = attack_log[input_pos_id]
        not_found = True
        for dataset_log in list_logs:
            if id_attack == dataset_log[input_pos_id]:
                not_found = False
                break
        if not_found:
            list_logs.append(attack_log)

    result = sorted(list_logs, key=lambda x: x[output_pos_timestamp])

    write_csv_file(output_filepath,result)

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

def main(input_filepath,alert_filepath,output_filepath):
    modify_file(input_filepath,alert_filepath,output_filepath)
    #get_stats_from_field(input_filepath,input_pos_process_id)

if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    #main("../../datasets/huma/reduced_attacks.csv","../../datasets/huma/reduced_attacks_v2.csv")
    main("../../datasets/huma/aggr_log_airbus_simplify_v3.csv","../../datasets/huma/agg_attacks_v3.csv","../../datasets/huma/aggr_log_airbus_simplify_v4.csv")
