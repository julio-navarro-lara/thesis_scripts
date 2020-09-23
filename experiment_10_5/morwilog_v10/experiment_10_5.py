#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
from morwilog_main import *
from library import write_csv_file

if __name__=="__main__":

    beginning_file_logs = "../../datasets/eventgen/max_step_distance/max_step_distance_"
    beginning_file_aasg = "../aasg/eventgen_aasg/max_step_distance/max_step_distance_1branch_"
    dict_var = {"p_t_max" : 120,
                "p_evap_rate" : 0.02,
                "p_omega" : 1000.0,
                "p_delta_ph_0" : 500.0,
                "p_minimum_ph" : 100.0,
                "p_minimum_ph_attack" : 200.0,
                "p_initial_ph": 1000.0
                }

    list_max_step_distance = [3,10,25,50,75,100]

    dict_equivalence_time = {
            3: 10,
            10: 16,
            25: 39,
            50: 65,
            75: 89,
            100: 115
    }

    header = ["max_step_distance","equivalence_in_seconds","initial_ph","minimum_ph","delta_ph_0","Tmax","rho","omega","P","N","TP","FP","Alerts","B[0,1,3]","B[0,1,4]","B[0,2,5]","B[0,2,6]"]

    list_results = [header]
    for max_step_distance in list_max_step_distance:
        file_logs = beginning_file_logs + str(max_step_distance) +"/max_step_distance_"+str(max_step_distance)+".log.parsed.csv"
        file_aasg = beginning_file_aasg +str(max_step_distance)+".json"

        result = main(dict_var,file_logs,file_aasg)
        list_results.append([max_step_distance, dict_equivalence_time[max_step_distance]]+result)

    write_csv_file("results_experiment_10_5.csv",list_results)
