#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
import sys
import re
from datetime import datetime
import time
import math

example_log = """
323,6,1410,247,67132,,3,2001-11-10 04:07:59,27184,172.016.113.207,27184,25,195.115.218.108,E-mail,00:C0:4F:A3:57:DB,,00:10:5A:9C:B2:8E,,,,,3,?,358,5NPIYAMS4GHTH98I9OS6O46HS8,0,152.014.009.144,101,network_sensor_1,18000,62000000,5,,,172.16.113.207,195.115.218.108,152.14.9.144,Email_Ehlo,,,,,,0,1
"""
#Mar 20 03:34:56
regex_timestamp1a = r'(... \d\d \d\d:\d\d:\d\d)\D'
regex_timestamp1b = r'(... \d \d\d:\d\d:\d\d)\D'
#2016-03-20 03:34:56
regex_timestamp2 = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)'
#20/Mar/2016:03:34:56
regex_timestamp3a = r'\D(\d\d/.../\d\d\d\d:\d\d:\d\d:\d\d)\D'
regex_timestamp3b = r'\D(\d/.../\d\d\d\d:\d\d:\d\d:\d\d)\D'
#20/03/2016 3:34:56 am
regex_timestamp4a = r'\D(\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d ..)\D'
regex_timestamp4b = r'\D(\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d ..)\D'
regex_timestamp4c = r'\D(\d\d/\d\d/\d\d\d\d \d:\d\d:\d\d ..)\D'
regex_timestamp4d = r'\D(\d/\d\d/\d\d\d\d \d:\d\d:\d\d ..)\D'
#20 mar 2016 03:34:56
regex_timestamp5a = r'\D(\d\d ... \d\d\d\d \d\d:\d\d:\d\d)\D'
regex_timestamp5b = r'\D(\d ... \d\d\d\d \d\d:\d\d:\d\d)\D'

def counting_matches_timestamps(raw_log):
    output = {}
    output['t1a'] = len(find_timestamp_regex(raw_log,regex_timestamp1a))
    output['t1b'] = len(find_timestamp_regex(raw_log,regex_timestamp1b))

    output['t2'] = len(find_timestamp_regex(raw_log,regex_timestamp2))

    output['t3a'] = len(find_timestamp_regex(raw_log,regex_timestamp3a))
    output['t3b'] = len(find_timestamp_regex(raw_log,regex_timestamp3b))

    output['t4a'] = len(find_timestamp_regex(raw_log,regex_timestamp4a))
    output['t4b'] = len(find_timestamp_regex(raw_log,regex_timestamp4b))
    output['t4c'] = len(find_timestamp_regex(raw_log,regex_timestamp4c))
    output['t4d'] = len(find_timestamp_regex(raw_log,regex_timestamp4d))

    output['t5a'] = len(find_timestamp_regex(raw_log,regex_timestamp5a))
    output['t5b'] = len(find_timestamp_regex(raw_log,regex_timestamp5b))

    return output

def calculate_single_timestamp(raw_log):
    list_timestamps = find_all_timestamps(raw_log)

    if len(list_timestamps) == 0:
        return 0
    else:
        #return math.floor(sum(list_timestamps)/len(list_timestamps))
        return min(list_timestamps)

def find_all_timestamps(raw_log):

    result_posix = []

    list_timestamp1 = find_timestamp_regex(raw_log,regex_timestamp1a) + find_timestamp_regex(raw_log,regex_timestamp1b)
    for timestamp in list_timestamp1:
        result_posix.append(convert_string_time_1(timestamp,2015))

    list_timestamp2 = find_timestamp_regex(raw_log,regex_timestamp2)
    for timestamp in list_timestamp2:
        result_posix.append(convert_string_time_2(timestamp))

    list_timestamp3 = find_timestamp_regex(raw_log,regex_timestamp3a) + find_timestamp_regex(raw_log,regex_timestamp3b)
    for timestamp in list_timestamp3:
        result_posix.append(convert_string_time_3(timestamp))

    list_timestamp4 = find_timestamp_regex(raw_log,regex_timestamp4a) + find_timestamp_regex(raw_log,regex_timestamp4b) + find_timestamp_regex(raw_log,regex_timestamp4c) + find_timestamp_regex(raw_log,regex_timestamp4d)
    for timestamp in list_timestamp4:
        result_posix.append(convert_string_time_4(timestamp))

    list_timestamp5 = find_timestamp_regex(raw_log,regex_timestamp5a) + find_timestamp_regex(raw_log,regex_timestamp5b)
    for timestamp in list_timestamp5:
        result_posix.append(convert_string_time_5(timestamp))

    return sorted(result_posix)



def find_timestamp_regex(raw_log,regex):
    timestamp = re.findall(regex, raw_log)
    return timestamp

def find_all_IP_addresses(raw_log):
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', raw_log )
    ip = remove_double_elements(ip)
    ip = remove_unwanted_ip_addresses(ip)
    ip = remove_not_ip_addresses(ip)
    ip = sorted(ip)
    return ip


def remove_double_elements(input_list):
    return list(set(input_list))

def remove_unwanted_ip_addresses(input_list):
    ip_addresses_to_remove = ["0.0.0.0"]
    for element in ip_addresses_to_remove:
        if element in input_list:
            input_list.remove(element)
    return input_list

def remove_not_ip_addresses(input_list):
    #There are string with the shape of an IP address but that are not IP addresses.
    for element in input_list:
        splitted_ip = element.split(".")
        for ip in splitted_ip:
            if int(ip) > 256:
                input_list.remove(element)
                break

    return input_list

#---------------------------------

#CONVERSION FUNCTIONS
#For format of style: Mar 20 03:34:56
def convert_string_time_1(string_time, wished_year):
    datetime_object = datetime.strptime(string_time, '%b %d %H:%M:%S')
    datetime_object = datetime_object.replace(year=wished_year)
    result = time.mktime(datetime_object.timetuple())
    return result

#For format of style: 2016-03-20 03:34:56
def convert_string_time_2(string_time):
    datetime_object = datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result

#For format of style: 20/Mar/2016:03:34:56
def convert_string_time_3(string_time):
    datetime_object = datetime.strptime(string_time, '%d/%b/%Y:%H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result

#20/03/2016 3:34:56 am
def convert_string_time_4(string_time):
    datetime_object = datetime.strptime(string_time, '%d/%m/%Y %H:%M:%S %p')
    result = time.mktime(datetime_object.timetuple())
    return result

#20 mar 2016 03:34:56
def convert_string_time_5(string_time):
    datetime_object = datetime.strptime(string_time, '%d %b %Y %H:%M:%S')
    result = time.mktime(datetime_object.timetuple())
    return result


if __name__ == "__main__":
    print find_all_IP_addresses(example_log)
    print find_all_timestamps(example_log)
