#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#23/10/2018
#Script to test how to parse snort alerts
import sys
import csv
from datetime import datetime
import time
import re

number_fields_input = 13
number_fields_output = 13

#log_positions
pos_id = 0
pos_timestamp = 1
pos_origin = 2
pos_service = 3
pos_source = 4
pos_destination = 5
pos_type = 6
pos_action = 7
pos_process_id = 8
pos_port_src = 9
pos_port_dst = 10
pos_log = 11
pos_tag = 12

snort_regex_old = r'\[\*\*\] \[\d+:\d+:\d+\] (.+)\[\*\*\]\n\[.+\] \[.+\]\n(\d+)\/(\d+)-(\d+):(\d+):(\d+).(\d+) (.+):(\d+) -> (.+):(\d+)\n.+ID:(\d+)'
snort_regex = r'\[\*\*\] \[.+\] (.+) \[\*\*\]\n.+\n(\d+)\/(\d+)-(\d+):(\d+):(\d+).(\d+) ([0-9]+(?:\.[0-9]+){3}):?([0-9]+)? -> ([0-9]+(?:\.[0-9]+){3}):?([0-9]+)?\n.+ID:(\d+)'

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

def parse_log(log,log_id):
    matchjob = re.match(snort_regex, log)

    output_log = [log_id]

    if not matchjob:
        print "It does not work"
        print log
        return []
    else:

        #EXTRACTION
        type = matchjob.group(1)

        date_month = matchjob.group(2)
        date_day = matchjob.group(3)
        date_hour = matchjob.group(4)
        date_min = matchjob.group(5)
        date_sec = matchjob.group(6)
        string_time = "2017-"+str(date_month)+"-"+str(date_day)+" "+str(date_hour)+":"+str(date_min)+":"+str(date_sec)

        #
        ipsrc = matchjob.group(8)
        psrc = matchjob.group(9)
        ipdst = matchjob.group(10)
        pdst = matchjob.group(11)

        #timestamp
        output_log.append(convert_string_time2(string_time))

        #pos_origin
        output_log.append('')
        #pos_service
        output_log.append('')

        #ipsrc
        output_log.append(ipsrc)
        #ipdst
        output_log.append(ipdst)
        output_log.append(type)

        #action
        output_log.append('')

        #Process_id
        output_log.append('')

        if psrc:
            output_log.append(psrc)
        else:
            output_log.append('')
        if pdst:
            output_log.append(pdst)
        else:
            output_log.append('')

        #log
        output_log.append('')

        #tag
        output_log.append('')

    return output_log

def convert_string_time2(string_time):
    datetime_object = datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result

def parse_file(logfile):
    with open(logfile) as f:
        list_logs = f.read().split('\n\n')

        general_counter = 0
        output_list = []
        for log in list_logs:
            parsed_log = parse_log(log,general_counter)
            if parsed_log:
                output_list.append(parsed_log)
                print parsed_log
            general_counter += 1

        print "TOTAL: "+str(len(list_logs))

        write_csv_file("iscx_ids_simplify_parsed_v3.csv",output_list)

def main():
    parse_file('../../datasets/iscx/iscx_ids')


if __name__ == "__main__":
    main()
