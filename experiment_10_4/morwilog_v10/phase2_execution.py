#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#12/06/2018

import random
import math
from library import *


def roulette_choice(choices):
    max = sum(choices.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key

def choose_pheromones_based(list_selected_nodes):
    choices = {i: list_selected_nodes[i]["ph"] for i in range(0,len(list_selected_nodes))}
    chosen_pos = roulette_choice(choices)
    return chosen_pos

def iterate_find_node(e_clas,n_event,e_star,previous_events,initial_time,p_t_max,pos_list):
    #Result: event
    previous_time = e_clas.iloc[n_event]["time"]
    for i in range(n_event+1,len(e_clas)):
        event = e_clas.iloc[i]

        #During time Tmax find the matches
        if float(event["time"])-initial_time >= p_t_max:
            return [None,None,i]
        if is_a_match(event,e_star,previous_events[0]) and (i not in pos_list):
            return [event,i,i]
            #We need to return the position in the list together with the event
    return [None,None,len(e_clas)-1]

def iterate_find_node_counters(e_clas,n_event,e_star,previous_events,initial_time,p_t_max,counter,pos_list):
    #Result: [events]
    result = []
    found = False
    max_pos = 0
    while counter > 0:
        position = 0
        for i in range(n_event+1,len(e_clas)):

            position = i
            event = e_clas.iloc[i]
            #During time Tmax find the matches
            if float(event["time"])-initial_time >= p_t_max:
                if n_event == 2:
                    print "pasao de tiempo"
                if i > max_pos:
                    max_pos = i
                return [None,i]
            if is_a_match(event,e_star,previous_events[0]) and (i not in pos_list):
                result.append([event,i])
                initial_time = event["time"]
                n_event = i
                found = True
                break

        if not found:
            if position > max_pos:
                max_pos = position
            return [None,position]

        counter -= 1
        found = False

    return result


def find_nodes(e_clas,n_event,children_list,previous_events,p_t_max,aasg):
    children_found = []
    event_list = []
    pos_list = []
    initial_time = float(e_clas.iloc[n_event]["time"])
    final_pos = 0 #This variable serves to return the further position in logs that we have explored

    for child in children_list:
        child_id = child["id"]

        node = get_node(aasg,child_id)
        e_star = node["e_star"]

        if "counter" in node and node["counter"] > 1:
            #print "There are counters!! "+str(node["counter"])
            counter = node["counter"]
            eventsandpos = iterate_find_node_counters(e_clas,n_event,e_star,previous_events,initial_time,p_t_max,counter,pos_list)

            #We do not return all the matched events, just the first one
            if eventsandpos[0] is not None:
                event_list.append(eventsandpos[0][0])
                pos_list.append(eventsandpos[0][1])
                children_found.append(child)
                if eventsandpos[-1][1] > final_pos:
                    final_pos = eventsandpos[-1][1]
            else:
                if eventsandpos[1] > final_pos:
                    final_pos = eventsandpos[1]
        else:
            [event,pos,max_pos] = iterate_find_node(e_clas,n_event,e_star,previous_events,initial_time,p_t_max,pos_list)
            if max_pos > final_pos:
                final_pos = max_pos
            if event is not None:
                event_list.append(event)
                pos_list.append(pos)
                children_found.append(child)

    return {"children_found":children_found,"event_list":event_list,"pos_list":pos_list,"final_pos":final_pos}

def is_eql_match(event,att,r):
    if event[att] != r:
        return False
    return True

def is_neq_match(event,att,r):
    if event[att] == r:
        return False
    return True

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

def is_txt_match(event,att,r,threshold):
    a = set(event[att].split())
    b = set(r.split())
    c = a.intersection(b)
    jac_index = float(len(c)) / (len(a) + len(b) - len(c))
    if jac_index > threshold:
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

def get_node(aasg,node_id):
    for node in aasg["nodes"]:
        if node["id"] == node_id:
            return node
    return None

def get_output_arcs(aasg,node_id):
    for arc in aasg["arcs"]:
        if arc["start"] == node_id:
            return arc.copy()

    #If no children are found, we return an empty dict
    return {}

def get_position_from_id(dict_list,element_id,id_name):
    for i in range(0,len(dict_list)):
        if dict_list[i][id_name] == element_id:
            return i

    return -1

def equal_last_generated_morwi(last_generated_morwi,event,aasg_pos,p_t_max):
    if aasg_pos == last_generated_morwi["aasg_pos"]:
        if event["time"]-last_generated_morwi["time"]<p_t_max:
            if (event["type"]==last_generated_morwi["type"]):
                if event["ipsrc"]==last_generated_morwi["ipsrc"]:
                    if (event["psrc"]==last_generated_morwi["psrc"]) or (math.isnan(event["psrc"]) and math.isnan(last_generated_morwi["psrc"])):
                        return True
    return False

def morwi(e_clas,n_event,aasg_set,p_t_max,last_generated_morwi):
    event = e_clas.loc[n_event]

    [aasg_pos,node] = look_for_aasg(event,aasg_set)

    result_morwi = {"sequence":[event],"aasg_pos":aasg_pos,"branch":[],"isresult":False,"pos_seq":[n_event],"matched_nodes":[],"time_matched":[],"pos_matched":[],"pos_choosing":[]}

    #We interrupt the execution of the morwi if there has been already a close match
    if last_generated_morwi and equal_last_generated_morwi(last_generated_morwi,event,aasg_pos,p_t_max):
        return result_morwi

    last_pheromone_value = 0



    if aasg_pos is not None:

        aasg = aasg_set[aasg_pos]

        output_arcs = get_output_arcs(aasg,node["id"])

        result_morwi["branch"].append(0)
        result_morwi["matched_nodes"].append([0])
        result_morwi["time_matched"].append([event["time"]])
        result_morwi["pos_matched"].append([n_event])

        print_log_line(event)

        print ""
        print ""

        print "There is match"
        print_log_line(event)

        while (output_arcs) and (output_arcs["children"]):



            previous_events = list(reversed(result_morwi["sequence"])) #We reverse the list of previous events to make it easier to search
            #Children found are nodes as they are defined for the aasg
            result_from_search = find_nodes(e_clas,n_event,output_arcs["children"],previous_events,p_t_max,aasg)

            pos_list = result_from_search["pos_list"]
            children_found = result_from_search["children_found"]

            #print children_found
            if result_morwi["pos_choosing"] and result_morwi["pos_choosing"][-1] > result_from_search["final_pos"]:
                result_morwi["pos_choosing"].append(result_morwi["pos_choosing"][-1])
            else:
                result_morwi["pos_choosing"].append(result_from_search["final_pos"])

            if children_found:
                #Random search pheromone-based
                event_list = result_from_search["event_list"]

                #Other measures for the graphs
                found_ids = []
                for child in children_found:
                    found_ids.append(child["id"])
                result_morwi["matched_nodes"].append(found_ids)
                time_matched = []
                for event_a in event_list:
                    time_matched.append(event_a["time"])
                result_morwi["time_matched"].append(time_matched)
                result_morwi["pos_matched"].append(pos_list)
                ######

                chosen_pos = choose_pheromones_based(children_found)
                last_pheromone_value = children_found[chosen_pos]["ph"]

                node_id = children_found[chosen_pos]["id"]
                output_arcs = get_output_arcs(aasg,node_id)

                n_event = pos_list[chosen_pos]

                result_morwi["branch"].append(node_id)
                result_morwi["sequence"].append(event_list[chosen_pos])
                result_morwi["pos_seq"].append(pos_list[chosen_pos])

                print_log_line(event_list[chosen_pos])

                print result_morwi["pos_seq"]
            else:
                return result_morwi


        result_morwi["isresult"] = True

    #We have to test minimum value of pheromone attacks
    return result_morwi

def pheromone_evaporation_all(aasg_set,aasg_pos,p_evap_rate,p_minimum_ph):
    #In this method we evaporate all the pheromones
    output_aasg_set = list(aasg_set)

    list_arcs = aasg_set[aasg_pos]["arcs"]

    for arc_pos in range(0,len(list_arcs)):
        if "children" in list_arcs[arc_pos]:
            list_children = list_arcs[arc_pos]["children"]
            for child_pos in range(0,len(list_children)):
                resulting_ph = (1.0-p_evap_rate)*list_children[child_pos]["ph"]

                if resulting_ph < p_minimum_ph:
                    output_aasg_set[aasg_pos]["arcs"][arc_pos]["children"][child_pos]["ph"] = p_minimum_ph
                else:
                    output_aasg_set[aasg_pos]["arcs"][arc_pos]["children"][child_pos]["ph"] = resulting_ph

    return output_aasg_set

def expert_evaluation(sequence):
    #We check not only that the events correspond to an attack, but that they correspond to the good one
    tag = None
    for event in sequence:
        event_tag = event["tag"]
        if (not tag) and (event_tag != 0):
            tag = event_tag
        elif event_tag != tag:
            return False
    return True

def increment_decrement_ph(aasg_set,branch,aasg_pos,verdict,p_delta_ph_0,p_omega,p_initial_ph):

    output_aasg_set = list(aasg_set)

    list_arcs = output_aasg_set[aasg_pos]["arcs"]

    #The elements in the branch are node ids, but we need to find the arcs. We need to select them by pairs
    for i in range(0,len(branch)-1):
        start = branch[i]
        end = branch[i+1]

        set_arc_pos = get_position_from_id(list_arcs,start,"start")
        children_pos = get_position_from_id(list_arcs[set_arc_pos]["children"],end,"id")

        child = list_arcs[set_arc_pos]["children"][children_pos]
        ph = child["ph"]

        delta_ph = p_delta_ph_0*math.exp(-math.pow(ph-p_initial_ph,2)/(2*math.pow(p_omega,2)))

        if verdict:
            output_aasg_set[aasg_pos]["arcs"][set_arc_pos]["children"][children_pos]["ph"] += delta_ph
        else:
            pheromones = output_aasg_set[aasg_pos]["arcs"][set_arc_pos]["children"][children_pos]["ph"] - delta_ph
            if pheromones < p_minimum_ph:
                output_aasg_set[aasg_pos]["arcs"][set_arc_pos]["children"][children_pos]["ph"] = p_minimum_ph
            else:
                output_aasg_set[aasg_pos]["arcs"][set_arc_pos]["children"][children_pos]["ph"] = pheromones

    return output_aasg_set

def update_json_results(input_json_results,aasg_set,id_event,time_event,alerts_sent,string_sequence_dict):

    json_results = input_json_results.copy()

    json_results["list_event_ids"].append(id_event)
    json_results["list_times"].append(time_event)
    json_results["list_alerts_sent"].append(alerts_sent)

    for aasg in aasg_set:
        #Every arc will have its results

        for arc_set in aasg["arcs"]:
            start = arc_set["start"]

            total_ph = 0
            for child in arc_set["children"]:
                total_ph += child["ph"]

            for child in arc_set["children"]:
                end = child["id"]
                combined_name = str(start)+'_'+str(end)

                ph = child["ph"]
                strength = float(ph)/float(total_ph)

                json_results["results"][aasg["id"]]["arcs"][combined_name]["ph"].append(ph)
                json_results["results"][aasg["id"]]["arcs"][combined_name]["strength"].append(strength)


    #So far we add the new sequences if there is any to the AASG with ID 1
    if string_sequence_dict["branch"] != "":
        json_results["results"][1]["branches_found"].append(string_sequence_dict["branch"])
        json_results["results"][1]["sequences_found"].append(string_sequence_dict["sequence"])
        json_results["results"][1]["pos_seq_found"].append(string_sequence_dict["pos_seq"])

    return json_results

def get_last_generated_morwi(result_morwi):
    last_generated_morwi = {}
    last_generated_morwi["aasg_pos"] = result_morwi["aasg_pos"]
    first_event = result_morwi["sequence"][0]
    last_generated_morwi["type"] = first_event["type"]
    last_generated_morwi["time"] = first_event["time"]
    last_generated_morwi["ipsrc"] = first_event["ipsrc"]
    last_generated_morwi["ipdst"] = first_event["ipdst"]
    last_generated_morwi["psrc"] = first_event["psrc"]
    last_generated_morwi["action"] = first_event["action"]
    return last_generated_morwi

def morwihill(e_clas,aasg_set,dict_var):
    #total_strength = 1

    #We create a dictionary where the id of the last log of found sequence is the key
    #The value is the list of corresponding result_morwis with this id as last log
    #Doing so, we can retard the update of pheromones to the arrival of the last log in the sequence
    dict_changes_to_made = {}

    #json_results, to store the results that will be later be processed by another script
    #json_results = create_json_results(aasg_set)
    #We do not use so far the json results and we create a dictionary with results. The key is the first pos of sequence
    dict_results = {}

    alerts_sent = 0
    number_logs_alerts = 0

    last_generated_morwi = {}

    number_events = len(e_clas)

    false_positives = 0
    true_positives = 0


    for i in range(0,number_events):
        #print i
        #result_morwi is an object of three elements:
        #   1: the output sequence
        #   2: the aasg used
        #   3: a boolean that says if it is a valid result or not
        #It is a class
        result_morwi = morwi(e_clas,i,aasg_set,dict_var["p_t_max"],last_generated_morwi)

        if result_morwi["aasg_pos"] is not None:
            last_generated_morwi = get_last_generated_morwi(result_morwi)

        #We append the result to the list, to make the pheromone changes in the future
        if result_morwi["isresult"]:
            last_id = result_morwi["pos_choosing"][-1]
            #if last_id < result_morwi["pos_seq"][-1]:
            #    w = raw_input("joder")
            if last_id in dict_changes_to_made:
                dict_changes_to_made[last_id].append(result_morwi)
            else:
                dict_changes_to_made[last_id] = [result_morwi]

        # #Pheromone update phase
        id_event = e_clas.iloc[i]["id"]
        time_event = e_clas.iloc[i]["time"]

        #If there is a sequence found, we also take it into the list of json_results.
        string_sequence_dict = {"branch":"","sequence":"","pos_seq":""}

        if result_morwi["isresult"]:
            branch = result_morwi["branch"]
            sequence = result_morwi["sequence"]
            pos_seq = result_morwi["pos_seq"]

            len_sequence = len(sequence)

            if expert_evaluation(sequence):
                string_sequence_dict["branch"] = ';'.join(str(e) for e in branch)
                string_sequence_dict["sequence"] = ';'.join(str(e["id"]) for e in sequence)
                string_sequence_dict["pos_seq"] = ';'.join(str(e+1) for e in pos_seq)
                true_positives += len_sequence
            else:
                string_sequence_dict["branch"] = "NONE "+';'.join(str(e) for e in branch)
                string_sequence_dict["sequence"] = "NONE "+';'.join(str(e["id"]) for e in sequence)
                string_sequence_dict["pos_seq"] = "NONE "+';'.join(str(e+1) for e in pos_seq)
                false_positives += len_sequence
        #else:
            #We extract also if the sequence is not a result
            #But for some statistics we just do not need to extract them
            # sequence = result_morwi["sequence"]
            # if len(sequence) > 1:
            #     sequence_ids = []
            #     for element in sequence:
            #         sequence_ids.append(element["id"])
            #     dict_results[i] = {"branch":result_morwi["branch"], "pos_seq":result_morwi["pos_seq"], "sequence_ids":sequence_ids,"moment_alert":None}

        if i in dict_changes_to_made:
            for result in dict_changes_to_made[i]:
                #selection of path matching the sequence
                branch = result["branch"]
                aasg_pos = result["aasg_pos"]
                sequence = result["sequence"]

                #The evaporation of the ph is done in all the nodes
                aasg_set = pheromone_evaporation_all(aasg_set,aasg_pos,dict_var["p_evap_rate"],dict_var["p_minimum_ph"])

                #The increment or decrement of pheromones is done in every node of the sequence
                #of the sequence, depending on the reinforcement learning.
                sequence = result["sequence"]
                aasg_set = increment_decrement_ph(aasg_set,branch,aasg_pos,expert_evaluation(sequence),dict_var["p_delta_ph_0"],dict_var["p_omega"],dict_var["p_initial_ph"])

                alerts_sent += 1
                number_logs_alerts += len(sequence)

                #####################
                #TO SEE HOW THE EXECUTION EVOLVES
                pos_seq = result["pos_seq"]
                sequence_ids = []
                for element in sequence:
                    sequence_ids.append(element["id"])
                print "*********"
                print "Alert"
                print time_event
                print "Position "+str(i)
                print sequence_ids
                print branch
                print result["pos_seq"]
                ####################

                dict_results[pos_seq[0]] = {"branch":branch, "pos_seq":pos_seq, "sequence_ids":sequence_ids,"moment_alert":i}


            del dict_changes_to_made[i]


        #json_results = update_json_results(json_results,aasg_set,id_event,time_event,alerts_sent,string_sequence_dict)

        # if result_morwi["time_matched"]:
        #     print "----------"
        #     print "Sequence"
        #     print result_morwi["matched_nodes"]
        #     print result_morwi["time_matched"]
        #     print result_morwi["pos_matched"]
        #     print result_morwi["pos_choosing"] #We need to add +1 if we want it correspond to the list of logs


    print "Number of alerts:"
    print alerts_sent

    print ""
    print "RESULTS to evaluate:"
    print "P: "+str(number_logs_alerts)
    print "N: "+str(number_events-number_logs_alerts)
    print "TP: "+str(true_positives)
    print "FP: "+str(false_positives)

    #aasg_set, P, N, TP, FP, alerts
    return [aasg_set,number_logs_alerts,number_events-number_logs_alerts,true_positives,false_positives,alerts_sent]
