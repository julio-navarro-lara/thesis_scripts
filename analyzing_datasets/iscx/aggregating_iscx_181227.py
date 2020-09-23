#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#26/12/2018
#Script to aggregate ISCX following the method by 14_Zargar
import sys
import csv
from datetime import datetime
import time

number_fields_input = 8
number_fields_output = 13

#positions
pos_id = 0
pos_timestamp = 1
pos_source = 2
pos_destination = 3
pos_type = 4
pos_port_src = 5
pos_port_dst = 6
pos_tag = 7

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

def check_log(previous_log,current_log):

    if previous_log[pos_source] != current_log[pos_source]:
        return False

    if previous_log[pos_destination] != current_log[pos_destination]:
        return False

    if previous_log[pos_type] != current_log[pos_type]:
        return False

    if (float(current_log[pos_timestamp])-float(previous_log[pos_timestamp]))>5:
        return False

    return True

def aggregate_file(input_filepath,output_filepath):
    result = []
    list_logs = extract_csv_file(input_filepath)
    print len(list_logs)
    logs_seen = []
    for log_tuple in list_logs:
        found = False
        if logs_seen:
            for previous_log in logs_seen:
                if check_log(previous_log,log_tuple):
                    found = True
                    break
        if not found:
            logs_seen.append(log_tuple)


    result = sorted(logs_seen, key=lambda x: x[pos_timestamp])

    print len(result)
    result_in_parsed_v3 = to_version_parsed_v3(result)
    write_csv_file(output_filepath,result_in_parsed_v3)
    print len(result_in_parsed_v3)

def to_version_parsed_v3(input_log_list):
    output_log_list = []
    for log in input_log_list:
        new_log = []
        # output_pos_id = 0
        new_log.append(log[pos_id])
        # output_pos_timestamp = 1
        new_log.append(log[pos_timestamp])
        # output_pos_origin = 2
        new_log.append('')
        # output_pos_service = 3
        new_log.append('')
        # output_pos_source = 4
        new_log.append(log[pos_source])
        # output_pos_destination = 5
        new_log.append(log[pos_destination])
        # output_pos_type = 6
        new_log.append(log[pos_type])
        # output_pos_action = 7
        new_log.append('')
        # output_pos_process_id = 8
        new_log.append('')
        # output_pos_port_src = 9
        if pos_port_src in log:
            new_log.append(log[pos_port_src])
        else:
            new_log.append('')
        # output_pos_port_dst = 10
        if pos_port_dst in log:
            new_log.append(log[pos_port_dst])
        else:
            new_log.append('')
        # output_pos_log = 11
        new_log.append('')
        # output_pos_tag = 12
        if pos_tag in log:
            new_log.append(log[pos_tag])
        else:
            new_log.append('')

        output_log_list.append(new_log)
    return output_log_list

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
    aggregate_file(input_filepath,output_filepath)
    #get_stats_from_field(input_filepath,input_pos_process_id)

def conversion_without_aggregation(input_filepath,output_filepath):
    result = []
    list_logs = extract_csv_file(input_filepath)
    print len(list_logs)

    result_in_parsed_v3 = to_version_parsed_v3(list_logs)
    write_csv_file(output_filepath,result_in_parsed_v3)
    print len(result_in_parsed_v3)

if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    #main("../../datasets/iscx/iscx_ids_simplify.csv","../../datasets/iscx/aggr_iscx_ids_simplify_parsed_v3.csv")
    conversion_without_aggregation("../../datasets/iscx/iscx_ids_simplify.csv","../../datasets/iscx/iscx_ids_simplify_parsed_v3.csv")
