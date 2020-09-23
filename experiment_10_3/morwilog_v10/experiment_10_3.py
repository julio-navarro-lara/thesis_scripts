#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
from morwilog_main import *
from library import write_csv_file

if __name__=="__main__":

    beginning_file_logs = "../../datasets/eventgen/size_dataset/size_"
    beginning_file_aasg = "../aasg/eventgen_aasg/size_dataset_change/size_dataset_change_1branch_"
    dict_var = {"p_t_max" : 20,
                "p_evap_rate" : 0.02,
                "p_omega" : 1000.0,
                "p_delta_ph_0" : 500.0,
                "p_minimum_ph" : 100.0,
                "p_minimum_ph_attack" : 200.0,
                "p_initial_ph": 1000.0
                }

    list_size_dataset = [1000,2000,4000,8000,16000,32000]

    dict_number_attacks = {
            1000:1,
            2000:3,
            4000:6,
            8000:13,
            16000:26,
            32000:53
    }

    header = ["size_dataset","num_attacks","initial_ph","minimum_ph","delta_ph_0","Tmax","rho","omega","P","N","TP","FP","Alerts","Execution_time"]

    list_results = [header]
    for size_dataset in list_size_dataset:
        file_logs = beginning_file_logs + str(size_dataset) +"/size_"+str(size_dataset)+".log.parsed.csv"
        file_aasg = beginning_file_aasg +str(size_dataset)+".json"

        list_execution_times = []
        result = []
        for i in range(0,10):
            result = main(dict_var,file_logs,file_aasg)
            list_execution_times.append(result[11])

        #We substitute the execution time by the average on 10 executions
        result[11] = sum(list_execution_times)/len(list_execution_times)

        list_results.append([size_dataset, dict_number_attacks[size_dataset]]+result)

    write_csv_file("results_experiment_10_3.csv",list_results)
