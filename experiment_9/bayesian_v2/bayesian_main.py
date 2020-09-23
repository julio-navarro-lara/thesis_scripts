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

if __name__=="__main__":
    print "Reading logs..."

    #DARPA 2000
    #file_logs = "../../datasets/darpa2000/simplified_parsed_v3/inside1_events_simplified_parsed_v3.csv"
    #file_logs = "../../datasets/darpa2000/experiment_1/darpa2000_inside1.csv"
    #file_logs = "/Users/Julio/programming/python/thesis_scripts/datasets/darpa2000/test/test_darpa2000_inside1.csv"
    #file_logs = "../../datasets/darpa2000/simplified_parsed_v3/No_attack1_inside1_events_simplified_parsed_v3.csv" ##This rules
    file_logs = "../../datasets/darpa2000/simplified_parsed_v3/inside2_events_simplified_parsed_v3.csv" ##This rules
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



    #file_logs = "../../datasets/darpa2000/experiment_1/darpa2000_inside1.csv"
    #file_logs = "/Users/Julio/programming/python/thesis_scripts/datasets/darpa2000/test/test_darpa2000_inside1.csv"

    e_clas = read_logs(file_logs)

    print "Read "+str(len(e_clas))+ " logs"
    print file_logs
    print "Reading AASGs..."

    #DARPA 2000
    #file_aasg = "../aasg/DARPA2000_example_aasg_v1.json"
    file_aasg = "../aasg/mill2_test_darpa2000_aasg.json"

    #ISCX
    #file_aasg = "../aasg/iscx_aasg.json"

    #Huma
    #file_aasg = "../aasg/huma_aasg.json"

    aasg_set = read_aasg_set(file_aasg)

    print "Read "+str(len(aasg_set))+ " AASGs"
    print file_aasg

    aasg_set = adding_arcs_optional_nodes(aasg_set)
    #print "Optional nodes processed"

    aasg_set = initialization_probabilities(aasg_set)
    print "Probabilities initialized"

    #DARPA 2000 inside1 1200 seconds (20 minutes)
    #DARPA 2000 inside2 1200 seconds (20 minutes)
    #ISCX 28,800 seconds (8 hours)
    #HuMa 172,800 seconds (48 hours)
    dict_var = {
        "p_t_max":172800,
        "p_learning_rate":0.4
    }

    print dict_var

    start = time.time()
    bayesian_method(e_clas,aasg_set,dict_var)
    end = time.time()

    print "Execution time (seconds):"
    print end-start
