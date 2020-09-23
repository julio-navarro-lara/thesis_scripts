#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
import sys
import json
import codecs
import os
import datetime

def from_int_to_string_date(int_timestamp):
    return datetime.datetime.fromtimestamp(
        int_timestamp
    ).strftime('%d/%m/%Y %H:%M:%S')

def output_to_website(filename,content):
    first_string = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
    </head>
    <body>
      """

    second_string = """
</body>
</html>
    """

    with open(filename,'w') as f:
        f.write(first_string+'\n'+content+'\n'+second_string)

def get_number_of_logs(list_logs_dict):
    return '<p>Number of logs: '+str(len(list_logs_dict))+'</p>\n'

def get_separation_by_timestamp(list_logs_dict,n_timedif):
    first_timestamp = list_logs_dict[0]["timestamp"]
    list_intervals = []
    list_zeros = []


    name_interval = from_int_to_string_date(int(first_timestamp))

    current_list_logs = []

    current_timestamp = first_timestamp
    time_dif = int(n_timedif)
    for element in list_logs_dict:
        time_log = element["timestamp"]
        if time_log == 0:
            list_zeros.append(element)
        else:
            if abs(time_log-current_timestamp) <= time_dif:
                current_timestamp = time_log
                current_list_logs.append(element)
            else:
                name_interval += ' -> '+from_int_to_string_date(int(current_timestamp))
                list_intervals.append([name_interval,current_list_logs])

                name_interval = from_int_to_string_date(int(time_log))
                current_list_logs = [element]

                current_timestamp = time_log

    list_intervals.append([name_interval+' -> '+from_int_to_string_date(int(current_timestamp)),current_list_logs])
    list_intervals.append(["zeros",list_zeros])

    return list_intervals

def split_by_ip_addresses(list_log_dict,n_commonip):

    result = {}

    for element in list_log_dict:

        if "ip_addresses" in element:
            list_ip_addresses = element["ip_addresses"]

            joined_ip_addr = ",".join(list_ip_addresses)
            if joined_ip_addr in result:
                result[joined_ip_addr].append(element)
            else:
                result[joined_ip_addr] = [element]
        else:
            if "NONE" in result:
                result["NONE"].append(element)
            else:
                result["NONE"] = [element]

    return result

def output_stats_by_ipaddress(dict_ip_addresses):
    result=''
    for key,value in dict_ip_addresses.iteritems():
        result += '<p>'+key+': <b>'+str(len(value))+'</b></p>\n'

    return result

def output_stats_by_timestamp(list_logs_dict,n_timedif,n_commonip):
    stats_separated = get_separation_by_timestamp(list_logs_dict,n_timedif)
    result = ''
    for element in stats_separated:
        number_of_logs = len(element[1])
        if number_of_logs > 0:
            result += '<p>'+element[0]+': <b>'+str(number_of_logs)+'</b></p>\n'

            separated_result = split_by_ip_addresses(element[1],n_commonip)
            result += output_stats_by_ipaddress(separated_result)

    return result

def output_stats(list_logs_dict):
    dict_list_ip_addresses = {}

    for element in list_logs_dict:

        if "ip_addresses" in element:

            tag_ip_addresses = ""

            for ip_address in element["ip_addresses"]:
                tag_ip_addresses += ip_address+"\t//\t"
        else:
            tag_ip_addresses = "None"

        if tag_ip_addresses in dict_list_ip_addresses:
            dict_list_ip_addresses[tag_ip_addresses] += 1
        else:
            dict_list_ip_addresses[tag_ip_addresses] = 1

    result = '<hr>'

    result += '<p><b>STATS IP ADDRESSES:</b></p>\n'

    for key, value in dict_list_ip_addresses.iteritems():
        result += '<p>'+key+' <b>'+str(value)+'</b></p>\n'

    return result

def compose_output_string(list_logs_dict,n_timedif,n_commonip):
    result = ''
    result += get_number_of_logs(list_logs_dict)+'<hr>'
    result += output_stats(list_logs_dict)+'<hr>'


    return result

def main_calculate_previous_stats(list_logs_dict,n_timedif,n_commonip):
    output_to_website('./simsc_app/templates/stats_graph.html',compose_output_string(list_logs_dict,n_timedif,n_commonip))
