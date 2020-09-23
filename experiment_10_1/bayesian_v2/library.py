#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#10/04/2018
#Library with methods for reading the logs, etc.

import sys
import csv
import json
import os, shutil
import pandas as pd

def erase_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def print_log_line(log_tuple):
    result = ""
    result += str(log_tuple["id"])+","
    result += str(log_tuple["time"])+","
    result += str(log_tuple["origin"])+","
    result += str(log_tuple["service"])+","
    result += str(log_tuple["ipsrc"])+","
    result += str(log_tuple["ipdst"])+","
    result += str(log_tuple["type"])+","
    result += str(log_tuple["action"])+","
    result += str(log_tuple["process_id"])+","
    result += str(log_tuple["psrc"])+","
    result += str(log_tuple["pdst"])+","
    result += str(log_tuple["log"])+","
    result += str(log_tuple["tag"])

    print result

def extract_csv_file(filepath):
    result = []
    with open(filepath,'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row)

    return result

def extract_csv_pandas(filepath):
    #df = pd.read_csv(filepath,dtype={"id":int,"timestamp":float,"origin":string,"service":string,"source":string,"destination":string,"type":string,"action":string,"process_id":int,"port_src":int,"port_dst":int,"log":string,"tag":int},names=["id","timestamp","origin","service","source","destination","type","action","process_id","port_src","port_dst","log","tag"])

    df = pd.read_csv(filepath,names=["id","time","origin","service","ipsrc","ipdst","type","action","process_id","psrc","pdst","log","tag"])

    df = df.infer_objects()

    return df

def write_csv_file(filepath,input_list):
    with open(filepath,'wb') as f:
        writer = csv.writer(f)
        writer.writerows(input_list)

def read_json(filename):
    data = json.load(open(filename))
    return data

def output_to_json_file(content, filename):
    with open(filename, 'w') as outfile:
        json.dump(content, outfile)

def print_clusters_logs_reduced(clustered_logs):
    for list_logs in clustered_logs:
        print_logs_reduced(list_logs)

def calculate_strength_aasg_set(list_aasgs):

    result_list_aasgs = []

    for aasg in list_aasgs:
        aasg["nodes"][0]["strength"] = 1
        for node in aasg["nodes"]:
            if node["children"]:

                list_siblings = node["children"]
                total = 0
                for child in list_siblings:
                    total += float(aasg["nodes"][child]["prob"])

                for child in list_siblings:
                    aasg["nodes"][child]["strength"] = float(aasg["nodes"][child]["prob"])/total
        result_list_aasgs.append(aasg)

    return result_list_aasgs

def print_logs_reduced(list_logs):
    print "********"
    print len(list_logs)
    for element in list_logs:
        string = ""
        for position in selected_positions:
            string += element[position]+','
        print string

def print_aasg_set(aasg_set):
    for aasg in aasg_set:
        print_aasg(aasg)

def print_aasg(aasg):
    print "aasg "+str(aasg["id"])
    for node in aasg["nodes"]:
        print "["
        print "Node "+str(node["id"])
        print "E_star:"
        print node["e_star"]
        print "children:"
        print node["children"]
        print "ph: "+str(node["ph"])
        print "]"
