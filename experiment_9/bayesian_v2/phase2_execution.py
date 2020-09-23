#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#31/08/2018

import random
import math
from library import *

def is_eql_match(event,att,r):
    if event[att] != r:
        return False
    return True

def is_neq_match(event,att,r):
    if event[att] == r:
        return False
    return True

def is_txt_match(event,att,r,threshold):
    a = set(event[att].split())
    b = set(r.split())
    c = a.intersection(b)
    jac_index = float(len(c)) / (len(a) + len(b) - len(c))
    if jac_index > threshold:
        return True
    else:
        return False

def from_ip_to_binary_string(ip):
    output = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    return output

def calculate_common_bits(ip1,ip2):
    result = 0
    len1 = len(ip1)
    len2 = len(ip2)
    if len1 == len2:
        for i in range(0,len1):
            if ip1[i] == ip2[i]:
                result += 1
            else:
                break
    return result

def is_pfx_match(event,att,r,threshold):
    bitip1 = from_ip_to_binary_string(event[att])
    bitip2 = from_ip_to_binary_string(r)

    l = calculate_common_bits(bitip1,bitip2)
    sim = float(l)/float(len(bitip1))
    if sim > threshold:
        return True
    else:
        return False

def is_set_match(event,att,R):
    if event[att] not in R:
        return False
    return True

def is_sim_eql_previous(event,attP,attC,previous_event):
    if event[attC] != previous_event[attP]:
        return False
    return True

def is_sim_com_previous(event,attP,attC,previous_event):
    return not set(event[attC]).isdisjoint(previous_event[attP])

def is_sim_pfx_previous(event,attP,attC,previous_event,threshold):
    bitip1 = from_ip_to_binary_string(event[attC])
    bitip2 = from_ip_to_binary_string(previous_event[attP])

    l = calculate_common_bits(bitip1,bitip2)
    sim = float(l)/float(len(bitip1))
    if sim > threshold:
        return True
    else:
        return False

def is_sim_txt_previous(event,attP,attC,previous_event,threshold):
    a = set(event[attC].split())
    b = set(previous_event[attP].split())
    c = a.intersection(b)
    jac_index = float(len(c)) / (len(a) + len(b) - len(c))
    if jac_index > threshold:
        return True
    else:
        return False

def is_sim_neq_previous(event,attP,attC,previous_event):
    if event[attC] == previous_event[attP]:
        return False
    return True

def is_a_match(event,e_star,previous_event):
    #This function determines if there is a match between an event and an abstract event
    for compare_element in e_star:
        function = compare_element["function"]
        if function == "EQL":
            if not is_eql_match(event,compare_element["att"],compare_element["r"]):
                return False
        elif function == "NEQ":
            if not is_neq_match(event,compare_element["att"],compare_element["r"]):
                return False
        elif function == "TXT":
            if not is_txt_match(event,compare_element["att"],compare_element["r"],compare_element["threshold"]):
                return False
        elif function == "PFX":
            if not is_pfx_match(event,compare_element["att"],compare_element["r"],compare_element["threshold"]):
                return False
        elif function == "SET":
            if not is_set_match(event,compare_element["att"],compare_element["r"]):
                return False
        elif function == "SIM_EQL":
            if not is_sim_eql_previous(event,compare_element["attP"],compare_element["attC"],previous_event):
                return False
        elif function == "SIM_COM":
            if not is_sim_com_previous(event,compare_element["attP"],compare_element["attC"],previous_event):
                return False
        elif function == "SIM_PFX":
            if not is_sim_pfx_previous(event,compare_element["attP"],compare_element["attC"],previous_event,compare_element["threshold"]):
                return False
        elif function == "SIM_TXT":
            if not is_sim_txt_previous(event,compare_element["attP"],compare_element["attC"],previous_event,compare_element["threshold"]):
                return False
        elif function == "SIM_NEQ":
            if not is_sim_neq_previous(event,compare_element["attP"],compare_element["attC"],previous_event):
                return False
        else:
            print "The function "+function+" does not exist in our database"
            return False

    return True

#It returns a duple, the first is the identifier of the aasg and the second is the root node
def look_for_aasg(event,aasg_set):
    for i in range(0,len(aasg_set)):
        aasg = aasg_set[i]
        root_node = get_root_node(aasg)
        if is_a_match(event,root_node["e_star"],[]):
            return [i,root_node]

    return [None,None]

def get_root_node(aasg):
    for node in aasg["nodes"]:
        if node["id"] == 0:
            return node
    return None

def build_adjacency_matrix(aasg):
    #This is a dict with the structure: {source:[t1,t2],source:[t1,t2]}.
    #Each source with its targets
    dict_source_targets = {}
    set_arcs = aasg["arcs"]

    for arc in set_arcs:
        source = arc["start"]
        list_children = []
        for child in arc["children"]:
            list_children.append(child["id"])

        if source not in dict_source_targets:
            dict_source_targets[source] = list_children
        else:
            dict_source_targets[source] += list_children

    return dict_source_targets

def parse(node, aasg, depth=1):
    result = []
    if node not in aasg:
        return [[node] * depth]
    else:
        res = []
        for next_node in aasg[node]:
            res.extend(parse(next_node, aasg, depth+1))
        print res
        for r in res:
            r[depth-1] = node
            result.append(r)
        return result

def get_all_paths_aasg(node_id,adj_matrix):
    if node_id not in adj_matrix:
        return [[node_id]]
    else:
        result = []
        for child in adj_matrix[node_id]:
            partial_result = get_all_paths_aasg(child,adj_matrix)
            for element in partial_result:
                result.append([node_id]+element)
        return result

def decomposition_aasg_in_paths(aasg):
    #As in bayesian there is no choice as it happens in Morwilog, we decompose
    #The aasg in all the possible paths and branches doing a deep breath search
    adj_matrix = build_adjacency_matrix(aasg)
    result = get_all_paths_aasg(0,adj_matrix)
    return result

def get_node(aasg,node_id):
    for node in aasg["nodes"]:
        if node["id"] == node_id:
            return node
    return None

def get_position_from_id(dict_list,element_id,id_name):
    for i in range(0,len(dict_list)):
        if dict_list[i][id_name] == element_id:
            return i

    return -1

def find_node(e_clas,n_event,node,previous_events,p_t_max):
    result = {"event_found":None,"is_found":False,"pos_found":None}
    event = e_clas.iloc[n_event]
    initial_time = float(event["time"])

    e_star = node["e_star"]

    #If there are counters or not
    if "counter" in node and node["counter"] > 1:
        counter = node["counter"]
        for i in range(n_event+1,len(e_clas)):
            event = e_clas.iloc[i]
            #During time Tmax find the matches
            if float(event["time"])-initial_time >= p_t_max:
                break
            if is_a_match(event,e_star,previous_events[0]):
                #We only stored the first event
                if counter == node["counter"]:
                    result["event_found"] = event
                    result["pos_found"] = i
                counter -= 1
                if counter == 0:
                    result["is_found"] = True
                    break
    else:
        for i in range(n_event+1,len(e_clas)):
            event = e_clas.iloc[i]

            #if n_event==401 and event["type"]=="Rsh":
            #    print "Compare A:"
            #    print previous_events[0]["ipsrc"]
            #    print event["ipdst"]
            #    print "Compare B"
            #    print previous_events[0]["ipdst"]
            #    print event["ipsrc"]

            #During time Tmax find the matches
            if float(event["time"])-initial_time >= p_t_max:
                break
            if is_a_match(event,e_star,previous_events[0]):
                result["event_found"] = event
                result["pos_found"] = i
                result["is_found"] = True
                break

    return result


def look_for_sequence_in_logs(event,path,aasg_pos,aasg,e_clas,n_event,p_t_max):
    result = {"sequence":[event],"aasg_pos":aasg_pos,"branch":path,"pos_list":[n_event],"isresult":False}

    #We have to remove the first element, the node 0, because it has been already found
    for node_id in path[1:]:
        previous_events = list(reversed(result["sequence"])) #We reverse the list of previous events to make it easier to search

        result_search = find_node(e_clas,n_event,get_node(aasg,node_id),previous_events,p_t_max)

        if result_search["is_found"]:
            event_found = result_search["event_found"]
            result["sequence"].append(event_found)
            n_event = result_search["pos_found"]
            result["pos_list"].append(n_event)
        else:
            return result



    result["isresult"] = True
    return result


def bayes_iteration(e_clas,n_event,aasg_set,p_t_max):
    event = e_clas.loc[n_event]

    [aasg_pos,node] = look_for_aasg(event,aasg_set)

    result = []

    id_event = event["id"]
    #if id_event == 67286 or id_event == 67341 or id_event == 67343:
    #    print "------"

    if aasg_pos is not None:

        aasg = aasg_set[aasg_pos]

        list_paths = decomposition_aasg_in_paths(aasg_set[aasg_pos])

        for path in list_paths:

            result_path = look_for_sequence_in_logs(event,path,aasg_pos,aasg,e_clas,n_event,p_t_max)
            if result_path["isresult"]:
                result.append(result_path)

    return result

def update_aasg_set_aasg(aasg,branch,verdict,p_learning_rate):

    list_arcs = aasg["arcs"]

    if verdict:
        for set_arc_pos in range(0,len(list_arcs)):
            arc_set = list_arcs[set_arc_pos]
            start = arc_set["start"]
            for children_pos in range(0,len(arc_set["children"])):
                child = arc_set["children"][children_pos]
                end = child["id"]
                prob = child["prob"]
                if (start in branch) and (end in branch):
                    aasg["arcs"][set_arc_pos]["children"][children_pos]["prob"] = p_learning_rate + (1-p_learning_rate)*prob
                else:
                    aasg["arcs"][set_arc_pos]["children"][children_pos]["prob"] = (1-p_learning_rate)*prob

    return aasg


def expert_evaluation(sequence):
    #So far if just one of the step belongs to the attack, the whole is considered as an attack
    for event in sequence:
        if event["tag"] != 0:
            return True
    return False


def bayesian_method(e_clas,aasg_set,dict_var):
    total_strength = 1

    #We create a dictionary where the id of the last log of found sequence is the key
    #The value is the list of corresponding result with this id as last log
    #Doing so, we can retard the update of probabilities to the arrival of the last log in the sequence
    dict_changes_to_made = {}
    alerts_sent = 0

    results_alerts = []

    for i in range(0,len(e_clas)):
        #list_result_bayesian is a list of objects of three elements:
        #   1: the output sequence
        #   2: the aasg used
        #   3: a boolean that says if it is a valid result or not
        #   And also the path followed (branch)
        #It is a list of objects because this time we can find two or more sequences in each execution
        #It is a class
        list_result_bayesian = bayes_iteration(e_clas,i,aasg_set,dict_var["p_t_max"])

        #If there is a sequence found, we also take it into the list of json_results.
        #The attacks in DARPA 2000 starts in events 67286, 67341, 67343
        #Experiment 5
        id_event = e_clas.iloc[i]["id"]
        #if id_event == 67286 or id_event == 67341 or id_event == 67343:
        #    print " "
        #    print "Results"
        #    for result_bayesian in list_result_bayesian:
        #        print result_bayesian["branch"]

        if list_result_bayesian:
            for result_bayesian in list_result_bayesian:

                last_id = result_bayesian["sequence"][-1]["id"]
                if last_id in dict_changes_to_made:
                    dict_changes_to_made[last_id].append(result_bayesian)
                else:
                    dict_changes_to_made[last_id] = [result_bayesian]


        if id_event in dict_changes_to_made:
            for result in dict_changes_to_made[id_event]:
                #selection of path matching the sequence
                branch = result["branch"]
                aasg_pos = result["aasg_pos"]
                sequence = result["sequence"]
                pos_list = result["pos_list"]

                aasg_set[aasg_pos] = update_aasg_set_aasg(aasg_set[aasg_pos],branch,expert_evaluation(sequence),dict_var["p_learning_rate"])

                alerts_sent += 1

                results_alerts.append([id_event,e_clas.iloc[i]["time"],alerts_sent])

                sequence_ids = []
                for element in sequence:
                    sequence_ids.append(element["id"])
                print sequence_ids
                print branch
                print pos_list
                print "----"


            del dict_changes_to_made[id_event]

                #print ""
                #print "Sequence:"
                #print ""

                #for log in sequence:
                #    print str(log["id"]) + ", " + str(log["ipsrc"]) + ", "+str(log["ipdst"])+", "+log["type"]

                #print ""
                #print "aasg: "
                #print ""

                #for node in aasg_set[aasg_pos]["nodes"]:
                #    print "Node "+str(node["id"])+", "+str(node["e_star"])

                #print "************"

                # total_strength = 1
                # for node in aasg_set[aasg_pos]["nodes"][1:4]:
                #     print node["e_star"][0]["fields_values"]["type"]
                #     total_strength = total_strength * node["strength"]
                # print "Total strength big arm: "+str(total_strength)

    print "Alerts"
    print alerts_sent
    print results_alerts
    return total_strength

def bayesian_method_tests(e_clas,aasg_set):
    print decomposition_aasg_in_paths(aasg_set[0])
