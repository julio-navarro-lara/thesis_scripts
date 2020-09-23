#Copyright 2019 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#17/01/2019
#Script to change the timestamps in the dataset for a sequence
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

def convert_string_time_2(string_time):
    datetime_object = datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result

def dec2sex(deci):
    #Script from the internet: https://github.com/esheldon/sdsspy/blob/master/sdsspy/sandbox/convert.py
    (hfrac, hd) = math.modf(deci)
    (min_frac, m) = math.modf(hfrac * 60)
    s = min_frac * 60.
    return (int(hd), int(m), s)


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

def get_number_of_lines(input_filepath):
    list_logs = extract_csv_file(input_filepath)

    print "Size: "+str(len(list_logs))

def get_difference_time(input_filepath):
    list_logs = extract_csv_file(input_filepath)

    time1 = list_logs[0][input_pos_timestamp]
    time2 = list_logs[-1][input_pos_timestamp]

    diff_time = float(time2)-float(time1)

    print "Diff in time:"
    print "Seconds: "+str(diff_time)
    print "Minutes: "+str(diff_time/60)
    print "Hours: "+str(diff_time/3600)
    print "Hours: "+str(dec2sex(diff_time/3600))

def change_timestamps(input_filepath,output_filepath):
    list_logs = extract_csv_file(input_filepath)
    result = []
    for i in range(0,len(list_logs)):
        new_log = list_logs[i]
        new_log[input_pos_timestamp] = i
        result.append(new_log)

    write_csv_file(output_filepath,result)


def main(input_filepath,output_filepath):
    #extract_file(input_filepath,output_filepath)
    #get_stats_from_field(input_filepath,input_pos_type)
    #get_number_of_lines(input_filepath)
    #get_difference_time(input_filepath)
    change_timestamps(input_filepath,output_filepath)


if __name__ == "__main__":
    #main(sys.argv[1],sys.argv[2])
    main("../../datasets/huma/agg_attacks.csv","../../datasets/huma/tests/sequential_time_agg_attacks.csv")
