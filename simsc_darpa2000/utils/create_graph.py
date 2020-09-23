#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
import sys
import json
import codecs

from operator import itemgetter

from extraction_from_log import find_all_IP_addresses,calculate_single_timestamp

high_risk_types = ["Admind","Mstream_Zombie","Sadmind_Amslverify_Overflow"]
medium_risk_types = ["FTP_Pass","Rsh","Stream_DoS"]
low_risk_types = ["Email_Ehlo","Sadmind_Ping","TelnetEnvAll","TelnetTerminaltype","TelnetXdisplay"]

def read_log_file(filename):
    with codecs.open(filename,'rb',encoding='utf-8',errors='replace') as f:
        lines = f.readlines()
        return lines

def read_json(filename):
    data = json.load(open(filename))
    return data

def output_to_json_file(content, filename):
    with open(filename, 'w') as outfile:
        json.dump(content, outfile)

def logs_are_in_same_time_window(log_dict_1,log_dict_2,dif_seconds):
    time_1 = log_dict_1["timestamp"]
    time_2 = log_dict_2["timestamp"]

    #sample_time_1 = convert_string_time_2("2016-03-20 03:00:00")
    #sample_time_2 = convert_string_time_2("2016-03-20 04:00:00")
    #print abs(sample_time_1 - sample_time_2)

    if time_1 == 0 or time_2 == 0:
        #If we do not know the timestamp, the condition is False
        return False

    if abs(time_1-time_2)<=dif_seconds:

        return True
    else:
        return False

def calculate_color(log):
    if any(type in log for type in high_risk_types):
        return "#e6194b"
    elif any(type in log for type in medium_risk_types):
        return "#f58231"
    elif any(type in log for type in low_risk_types):
        return "#3cb44b"
    else:
        return "#D3D3D3"


def get_list_common_ip_addresses(log_dict_1,log_dict_2):
    if "ip_addresses" in log_dict_1 and "ip_addresses" in log_dict_2:
        list_ip_1 = log_dict_1["ip_addresses"]
        list_ip_2 = log_dict_2["ip_addresses"]
        list_common_ip = list(set(list_ip_1).intersection(list_ip_2))
        number_common_ip = len(list_common_ip)

        return number_common_ip
    else:
        return 0

def same_ip_address_list(result_common_ip, log_dict_1, log_dict_2):
    if "ip_addresses" in log_dict_1 and "ip_addresses" in log_dict_2:
        list_ip_1 = log_dict_1["ip_addresses"]
        list_ip_2 = log_dict_2["ip_addresses"]
        if len(list_ip_1)==len(list_ip_2) and len(list_ip_1)==result_common_ip:
            return True
        else:
            return False

def create_edge(log_dict_1,log_dict_2, n_commonip, n_timedif):
    number_common_ip = get_list_common_ip_addresses(log_dict_1,log_dict_2)
    same_time_window = logs_are_in_same_time_window(log_dict_1,log_dict_2,n_timedif)
    #We add an extra condition apart from the common number of IPs: if they have exactly the same tuple of IPs, they match
    #This avoid the no match if each log has only one IP and the limit is 2, for example
    if ((number_common_ip > n_commonip-1)or(same_ip_address_list(number_common_ip,log_dict_1,log_dict_2))) and same_time_window:
        output_dict = {}
        output_dict["source"] = log_dict_1["id"]
        output_dict["target"] = log_dict_2["id"]
        output_dict["id"] = "edge_"+str(log_dict_1["id"])+'_'+str(log_dict_2["id"])
        output_dict["weight"] = number_common_ip
        #print log_dict_1["log"]
        #print log_dict_2["log"]
        #print "***************"

        return {"data":output_dict}
    else:
        return None

def build_edges_list(list_logs_dict, n_commonip, n_timedif):
    result = []
    counter = 0
    for i in range(0,len(list_logs_dict)):
        for j in range(i+1,len(list_logs_dict)):
            log_1 = list_logs_dict[i]
            log_2 = list_logs_dict[j]

            print counter
            counter += 1

            edge = create_edge(log_1,log_2, n_commonip, n_timedif)
            if edge:
                result.append(edge)

    return result

def build_nodes_list(list_logs_dict):
    result = []
    for element in list_logs_dict:
        result.append({"data":element})
    return result

def build_json_graph(nodes_list, edges_list):
    return {"nodes":nodes_list,"edges":edges_list}

def log_to_dict_complete(logs):
    result = []

    previous_timestamp = 0

    for i in range(0,len(logs)):
        dict_log = {}

        #order: Au;Av;I;C;A;Ac
        dict_log["log"] = logs[i]
        dict_log["id"] = i+1

        list_ip_addresses = find_all_IP_addresses(dict_log["log"])
        if list_ip_addresses:
            dict_log["ip_addresses"] = list_ip_addresses

        timestamp = calculate_single_timestamp(dict_log["log"])
        #It we do not find timestamp, we take the timestamp of the previous log
        if timestamp == 0:
            dict_log["timestamp"] = previous_timestamp
        else:
            dict_log["timestamp"] = timestamp
            previous_timestamp = timestamp

        dict_log["color"] = calculate_color(logs[i])

        result.append(dict_log)

    result = sorted(result, key=itemgetter('timestamp'))
    return result

def main_extract_logs():

    log_lines = read_log_file("./utils/data/list_logs.csv")
    list_logs_dict = log_to_dict_complete(log_lines)

    return list_logs_dict

def main_create_graph(list_logs_dict,n_commonip,n_timedif):

    node_list = build_nodes_list(list_logs_dict)
    edge_list = build_edges_list(list_logs_dict, int(n_commonip), int(n_timedif))

    json_graph = build_json_graph(node_list, edge_list)

    output_to_json_file(json_graph,'./utils/data/graph_ip.json')

    return len(node_list)

if __name__=="__main__":
    main_create_graph(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
