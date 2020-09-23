#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#25/10/2018

from phase1_read_data import *
from phase2_execution import *

import time

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

def get_choosing_prob_two_nodes(aasg,node1,node2):
    #In Bayesian it should be the same as the probability parameters anyways

    for arc_set in aasg["arcs"]:
        if arc_set["start"] == node1:
            for child in arc_set["children"]:
                if child["id"] == node2:
                    return float(child["prob"])

    return 0.0

def get_choosing_prob_branch(aasg,branch):
    previous_node = branch[0]
    result = 1.0
    for node in branch[1:]:
        result = result * get_choosing_prob_two_nodes(aasg,previous_node,node)
        previous_node = node
    return result

def print_results_aasgs(aasg_set_result):
    print ""
    print "Results AASGs"
    result = []
    for aasg in aasg_set_result:
        list_branches = decomposition_aasg_in_paths(aasg)
        print "-----------"
        print "AASG "+str(aasg["id"])

        for branch in list_branches:
            choosing_prob = get_choosing_prob_branch(aasg,branch)
            print branch
            print "Choosing prob: "+str(choosing_prob)
            result.append(choosing_prob)
    return result



def main(dict_var,file_logs,file_aasg):
    print "Reading logs..."

    if not file_logs:
        #DARPA 2000
        #file_logs = "../../datasets/darpa2000/simplified_parsed_v3/inside1_events_simplified_parsed_v3.csv"
        #file_logs = "../../datasets/darpa2000/experiment_1/darpa2000_inside1.csv"
        #file_logs = "/Users/Julio/programming/python/thesis_scripts/datasets/darpa2000/test/test_darpa2000_inside1.csv"
        #file_logs = "../../datasets/darpa2000/simplified_parsed_v3/No_attack1_inside1_events_simplified_parsed_v3.csv" ##This rules
        #file_logs = "../../datasets/darpa2000/simplified_parsed_v3/inside2_events_simplified_parsed_v3.csv" ##This rules
        #file_logs = "../../datasets/darpa2000/aggregated_parsed_v3/aggregated_No_attack1_inside1_events_simplified_parsed_v3.csv"

        #ISCX
        #file_logs = "../../datasets/iscx/aggr_iscx_ids_simplify_parsed_v3.csv"##This rules
        #file_logs = "../../datasets/iscx/REDUCED_aggr_iscx_ids_simplify_parsed_v3.csv"

        #Huma
        #file_logs = "../../datasets/huma/attacks.csv"
        #file_logs = "../../datasets/huma/reduced_attacks_v2.csv"
        #file_logs = "../../datasets/huma/log_airbus_simplify_v2.csv"
        #file_logs = "../../datasets/huma/aggr_log_airbus_simplify_v2.csv"
        #file_logs = "../../datasets/huma/aggr_log_airbus_simplify_v3.csv"
        #file_logs = "../../datasets/huma/aggr_log_airbus_simplify_v4.csv" ##This rules
        #file_logs = "../../datasets/huma/agg_attacks_v2.csv"
        #file_logs = "../../datasets/huma/agg_attacks_v3.csv"
        #file_logs = "../../datasets/huma/tests/sequential_time_agg_attacks.csv"
        #file_logs = "../../datasets/huma/tests/sequential_time_agg_attacks_v2.csv"

        #Eventgen
        file_logs = "../../datasets/eventgen/eventgen_dataset/eventgen.log.parsed.csv"


    e_clas = read_logs(file_logs)

    print "Read "+str(len(e_clas))+ " logs"
    print file_logs
    print "Reading AASGs..."

    if not file_aasg:

        #DARPA 2000
        #file_aasg = "../aasg/DARPA2000_example_aasg_v1.json"
        #file_aasg = "../aasg/mill2_test_darpa2000_aasg.json"

        #ISCX
        #file_aasg = "../aasg/iscx_aasg.json"

        #Huma
        #file_aasg = "../aasg/huma_aasg.json"

        #Eventgen
        file_aasg = "../aasg/eventgen_aasg/eventgen_aasg_1branch.json"

    aasg_set = read_aasg_set(file_aasg)

    print "Read "+str(len(aasg_set))+ " AASGs"
    print file_aasg

    #--------------------
    #PARTICULAR FOR BIDIMAC
    if not dict_var:
        #DARPA 2000 inside1 1200 seconds (20 minutes)
        #DARPA 2000 inside2 1200 seconds (20 minutes)
        #ISCX 28,800 seconds (8 hours)
        #HuMa 172,800 seconds (48 hours)
        dict_var = {
            "p_t_max":20,
            "p_learning_rate":0.4
        }

    print dict_var

    aasg_set = adding_arcs_optional_nodes(aasg_set)
    #print "Optional nodes processed"

    aasg_set = initialization_probabilities(aasg_set)
    print "Probabilities initialized"

    start = time.time()
    result = bayesian_method(e_clas,aasg_set,dict_var)
    end = time.time()
    #--------------------

    print "Execution time (seconds):"
    print end-start

    aasg_set_result = result[0]
    choosing_prob_branches = print_results_aasgs(aasg_set_result)

    #["Tmax","learning_rate","P","N","TP","FP","Alerts","B[0,1,3]","B[0,1,4]","B[0,2,5]","B[0,2,6]"]
    return [dict_var["p_t_max"],
            dict_var["p_learning_rate"],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5]
            ]+choosing_prob_branches

if __name__=="__main__":
    main({},"","")
