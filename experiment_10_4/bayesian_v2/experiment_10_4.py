#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
from bayesian_main import *
from library import write_csv_file

if __name__=="__main__":

    #file_logs = "../../datasets/eventgen/eventgen_dataset/eventgen.log.parsed.csv"
    #file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_50/prop_attacks_50.log.parsed.csv"
    #file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_500/prop_attacks_500.log.parsed.csv"

    #We try with a bigger dataset:
    file_logs = "../../datasets/eventgen/size_dataset/size_16000/size_16000.log.parsed.csv"
    file_aasg = "../aasg/eventgen_aasg/size_dataset_change_1branch_16000.json"

    #file_aasg = "../aasg/eventgen_aasg/eventgen_aasg_1branch.json"
    #file_aasg = "../aasg/eventgen_aasg/prop_attacks_change_1branch_50.json"
    #file_aasg = "../aasg/eventgen_aasg/prop_attacks_change_1branch_500.json"

    dict_var = {
        "p_t_max":20,
        "p_learning_rate":0.4
    }


    header = ["Tmax","learning_rate","P","N","TP","FP","Alerts","Execution_time"]


    list_t_max = [20,40,80,160,320,640,1280]

    list_results = [header]
    for t_max in list_t_max:
        dict_var["p_t_max"] = t_max

        list_execution_times = []
        result = []
        for i in range(0,10):
            result = main(dict_var,file_logs,file_aasg)
            list_execution_times.append(result[7])

        #We substitute the execution time by the average on 10 executions
        result[7] = sum(list_execution_times)/len(list_execution_times)

        list_results.append(result)

    #write_csv_file("results_experiment_10_4.csv",list_results)
    write_csv_file("results_experiment_10_4_v2.csv",list_results)
